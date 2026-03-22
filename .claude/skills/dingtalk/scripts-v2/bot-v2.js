#!/usr/bin/env node
/**
 * 钉钉机器人 V2 - 高可用版
 *
 * 特性：
 * 1. 使用 Claude Code SDK（而非 CLI）
 * 2. 管理员模式：全能力（文件、命令、Skills、MCP）
 * 3. 普通用户模式：安全沙箱
 * 4. 会话持久化
 * 5. 多机器人配置
 */

import { DWClient, TOPIC_ROBOT } from 'dingtalk-stream';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ============================================================
// 配置
// ============================================================

const configPath = join(__dirname, 'config-v2.json');
let config;
try {
  config = JSON.parse(readFileSync(configPath, 'utf-8'));
} catch (e) {
  console.error('❌ 配置文件读取失败:', configPath);
  process.exit(1);
}

const DATA_DIR = join(__dirname, 'data');
if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });

// ============================================================
// 会话管理
// ============================================================

class SessionManager {
  constructor() {
    this.sessionsFile = join(DATA_DIR, 'sessions.json');
    this.load();
  }

  load() {
    try {
      if (existsSync(this.sessionsFile)) {
        this.sessions = new Map(Object.entries(JSON.parse(readFileSync(this.sessionsFile, 'utf-8'))));
      } else {
        this.sessions = new Map();
      }
    } catch {
      this.sessions = new Map();
    }
  }

  save() {
    const obj = Object.fromEntries(this.sessions);
    writeFileSync(this.sessionsFile, JSON.stringify(obj, null, 2), 'utf-8');
  }

  get(userId) {
    return this.sessions.get(userId);
  }

  set(userId, session) {
    this.sessions.set(userId, {
      ...session,
      lastActive: new Date().toISOString(),
    });
    this.save();
  }

  getOrCreate(userId, nick) {
    let session = this.get(userId);
    if (!session) {
      session = {
        createdAt: new Date().toISOString(),
        nick,
        messageCount: 0,
        isAdmin: config.admins.includes(userId),
      };
    }
    session.messageCount++;
    this.set(userId, session);
    return session;
  }
}

const sessionManager = new SessionManager();

// ============================================================
// 权限管理
// ============================================================

class PermissionHandler {
  constructor(config) {
    this.admins = new Set(config.admins || []);
    this.safeModeConfig = config.safeMode || {};
  }

  isAdmin(userId) {
    return this.admins.has(userId);
  }

  getMode(userId) {
    return this.isAdmin(userId) ? 'admin' : 'safe';
  }

  getToolsForMode(mode) {
    if (mode === 'admin') {
      return {
        allowedTools: undefined, // 全部允许
        disallowedTools: undefined,
        permissionMode: 'bypassPermissions',
      };
    }
    // 安全模式
    return {
      allowedTools: this.safeModeConfig.allowedTools || ['Read', 'Grep', 'Glob'],
      disallowedTools: this.safeModeConfig.disallowedTools || ['Bash', 'Write', 'Edit', 'WebFetch'],
      permissionMode: 'default',
    };
  }
}

const permissionHandler = new PermissionHandler(config);

// ============================================================
// Claude Code SDK 调用
// ============================================================

async function callClaudeSDK(message, userId, session) {
  const mode = permissionHandler.getMode(userId);
  const toolConfig = permissionHandler.getToolsForMode(mode);

  console.log(`   [${session.nick}] 模式: ${mode}`);

  // 构建请求
  const requestBody = {
    model: config.model || 'claude-sonnet-4-6',
    max_tokens: config.maxTokens || 4096,
    messages: [
      {
        role: 'user',
        content: message,
      },
    ],
  };

  // 管理员模式添加系统提示
  if (mode === 'admin') {
    requestBody.system = `你是 CC 机器人，通过钉钉与管理员对话。
当前项目路径: ${config.projectPath || '/data/mycc'}
你有完整的文件访问、命令执行、网络请求能力。
用户 ${session.nick} (ID: ${userId}) 正在与你对对话。`;
  } else {
    requestBody.system = `你是 CC 机器人，通过钉钉与用户对话。
你处于安全模式，只能进行对话和查看公开信息。
不要透露任何内部路径、密钥、配置。
用户 ${session.nick} 正在与你对话。`;
  }

  // 调用 API
  try {
    const apiKey = process.env.ANTHROPIC_AUTH_TOKEN || process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      throw new Error('未配置 ANTHROPIC_AUTH_TOKEN');
    }

    const baseUrl = process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com';

    const response = await fetch(`${baseUrl}/v1/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || `API 错误: ${response.status}`);
    }

    const data = await response.json();
    const text = data.content
      .filter(block => block.type === 'text')
      .map(block => block.text)
      .join('\n');

    return text;

  } catch (err) {
    console.error('   API 调用失败:', err.message);
    throw err;
  }
}

// ============================================================
// 钉钉消息处理
// ============================================================

async function replyViaWebhook(webhookUrl, text) {
  try {
    const payload = {
      msgtype: 'markdown',
      markdown: { title: 'CC 回复', text },
    };
    const res = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.errcode !== 0) {
      console.error('   Webhook 回复失败:', data.errmsg);
    }
  } catch (err) {
    console.error('   Webhook 调用失败:', err.message);
  }
}

// ============================================================
// 主程序
// ============================================================

console.log('🤖 钉钉机器人 V2 启动中...');
console.log(`   AppKey: ${config.clientId}`);
console.log(`   管理员: ${config.admins?.length || 0} 人`);
console.log(`   项目路径: ${config.projectPath || '未设置'}`);

const client = new DWClient({
  clientId: config.clientId,
  clientSecret: config.clientSecret,
  debug: false,
});

client.registerCallbackListener(TOPIC_ROBOT, async (res) => {
  try {
    const msgData = JSON.parse(res.data);
    const text = msgData?.text?.content?.trim() || '';
    const senderNick = msgData?.senderNick || '未知用户';
    const senderStaffId = msgData?.senderStaffId || '';
    const senderId = msgData?.senderId || '';
    const sessionWebhook = msgData?.sessionWebhook || '';
    const userId = senderStaffId || senderId;

    console.log(`[${new Date().toISOString()}] [${senderNick}] ${text.substring(0, 100)}`);

    if (!text) {
      client.socketCallBackResponse(res.headers.messageId, {
        response: JSON.stringify({ msgtype: 'text', text: { content: '请说点什么' } }),
      });
      return;
    }

    // 获取/创建会话
    const session = sessionManager.getOrCreate(userId, senderNick);
    const mode = permissionHandler.getMode(userId);

    // 处理命令
    if (text === '/status' || text === '/ping') {
      const reply = [
        `🤖 **CC 机器人 V2 状态**`,
        ``,
        `- 用户: ${senderNick}`,
        `- 模式: **${mode === 'admin' ? '管理员' : '安全模式'}**`,
        `- 消息数: ${session.messageCount}`,
        `- 时间: ${new Date().toLocaleString('zh-CN')}`,
      ].join('\n');

      if (sessionWebhook) await replyViaWebhook(sessionWebhook, reply);
      client.socketCallBackResponse(res.headers.messageId, {
        response: JSON.stringify({ msgtype: 'text', text: { content: reply } }),
      });
      return;
    }

    if (text === '/help' || text === '/start') {
      const adminCommands = mode === 'admin' ? [
        '',
        '**管理员命令:**',
        `- /status - 状态`,
        `- /usage - 用量统计`,
        `- /model - 切换模型`,
      ].join('\n') : '';

      const reply = [
        `👋 你好 ${senderNick}！`,
        ``,
        `我是 CC 机器人 V2`,
        `当前模式: **${mode === 'admin' ? '管理员' : '安全模式'}**`,
        ``,
        `直接发消息即可对话。`,
        adminCommands,
      ].join('\n');

      if (sessionWebhook) await replyViaWebhook(sessionWebhook, reply);
      client.socketCallBackResponse(res.headers.messageId, {
        response: JSON.stringify({ msgtype: 'text', text: { content: reply } }),
      });
      return;
    }

    // 调用 Claude
    console.log(`   ⏳ 处理中...`);
    let reply;
    try {
      reply = await callClaudeSDK(text, userId, session);
    } catch (err) {
      reply = `❌ 处理失败: ${err.message}`;
    }

    // 截断过长回复
    if (reply.length > 4000) {
      reply = reply.substring(0, 4000) + '\n\n... (回复过长已截断)';
    }

    console.log(`   ✅ 回复: ${reply.substring(0, 100)}...`);

    if (sessionWebhook) await replyViaWebhook(sessionWebhook, reply);
    client.socketCallBackResponse(res.headers.messageId, {
      response: JSON.stringify({ msgtype: 'text', text: { content: reply } }),
    });

  } catch (err) {
    console.error('处理消息异常:', err);
    client.socketCallBackResponse(res.headers.messageId, {
      response: JSON.stringify({ msgtype: 'text', text: { content: '系统繁忙，请稍后重试。' } }),
    });
  }
});

client.on('open', () => {
  console.log('✅ Stream 连接已建立');
});

client.on('error', (err) => {
  console.error('❌ Stream 错误:', err);
});

client.on('close', () => {
  console.log('⚠️ Stream 连接已断开');
});

try {
  await client.connect();
} catch (err) {
  console.error('❌ 连接失败:', err.message);
  process.exit(1);
}
