#!/usr/bin/env node
/**
 * 跨设备通知脚本 - 通知 Surface 上的 AI
 * 用法：node notify-surface.js "任务内容" [优先级]
 */

const fs = require('fs');
const crypto = require('crypto');
const { execSync } = require('child_process');

const [,, task, priority = 'normal'] = process.argv;

if (!task) {
  console.error('用法：node notify-surface.js "任务内容" [优先级]');
  process.exit(1);
}

// 读取环境变量
function getEnv() {
  const envPath = '/root/air/mycc/.env';
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf8');
    return content.split('\n').reduce((acc, line) => {
      const parts = line.split('=');
      if (parts.length >= 2) {
        const key = parts[0].trim();
        const value = parts.slice(1).join('=').trim().replace(/^"(.*)"$/, '$1');
        if (key) acc[key] = value;
      }
      return acc;
    }, {});
  }
  return process.env;
}

const env = getEnv();

// 钉钉加签
function signDingTalk(secret) {
  const timestamp = Date.now();
  const stringToSign = `${timestamp}\n${secret}`;
  const sign = crypto.createHmac('sha256', secret).update(stringToSign).digest('base64');
  return { timestamp, sign: encodeURIComponent(sign) };
}

// 发送钉钉消息
async function sendDingTalk(webhook, secret, title, content, label) {
  if (!webhook) {
    console.log(`⚠️  钉钉 (${label}) Webhook 未配置`);
    return false;
  }

  let url = webhook;
  if (secret) {
    const { timestamp, sign } = signDingTalk(secret);
    url += `&timestamp=${timestamp}&sign=${sign}`;
  }

  const data = {
    msgtype: 'markdown',
    markdown: {
      title: title,
      text: `## ${title}\n\n${content}\n\n> 🕐 ${new Date().toLocaleString('zh-CN')}`
    }
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'application/json' }
    });
    const result = await res.json();
    
    if (result.errcode === 0) {
      console.log(`✅ 钉钉 (${label}) 发送成功`);
      return true;
    } else {
      console.error(`❌ 钉钉 (${label}) 失败：[${result.errcode}] ${result.errmsg}`);
      return false;
    }
  } catch (err) {
    console.error(`❌ 钉钉 (${label}) 网络错误：${err.message}`);
    return false;
  }
}

// 发送 Telegram 消息
async function sendTelegram(token, chatId, text) {
  if (!token || !chatId) {
    console.log('⚠️  Telegram 未配置');
    return false;
  }

  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  
  try {
    const res = await fetch(url, {
      method: 'POST',
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'HTML'
      }),
      headers: { 'Content-Type': 'application/json' }
    });
    const result = await res.json();
    
    if (result.ok) {
      console.log('✅ Telegram 发送成功');
      return true;
    } else {
      console.error(`❌ Telegram 失败：${result.description}`);
      return false;
    }
  } catch (err) {
    console.error(`❌ Telegram 网络错误：${err.message}`);
    return false;
  }
}

// 写入共享任务文件（Surface 会读取）
function writeSharedTask(taskData) {
  const sharedDir = '/root/air/mycc/0-System/agents/shared-tasks/inbox';
  const date = new Date().toISOString().split('T')[0];
  const taskId = `surface-${date}-morning-report`;
  const filePath = `${sharedDir}/${taskId}.md`;
  
  try {
    fs.mkdirSync(sharedDir, { recursive: true });
    fs.writeFileSync(filePath, taskData);
    console.log(`✅ 共享任务已写入：${filePath}`);
    return true;
  } catch (err) {
    console.error(`❌ 写入共享任务失败：${err.message}`);
    return false;
  }
}

// 主逻辑
(async () => {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║   通知 Surface AI                          ║');
  console.log('╚════════════════════════════════════════════╝');
  console.log();
  
  const morningTask = `## 🌅 明早汇报任务

**优先级**: ${priority}
**执行时间**: 明早 08:00
**任务内容**: ${task}

### 要求:
1. ✅ 发送早安消息到钉钉群
2. ✅ 配上语音播报（TTS）
3. ✅ 包含夜间运行统计
4. ✅ 今日计划建议

### 语音内容建议:
"早上好！我是 Surface AI 助手。现在是北京时间早上 8 点。
系统昨夜运行正常，累计运行 X 小时。
今天建议您关注以下事项...
祝您今天工作顺利！"

---
*此任务由 Qwen 监控系统自动创建*
`;

  // 1. 写入共享任务文件
  writeSharedTask(morningTask);
  
  // 2. 发送到钉钉群（Surface 会看到）
  const dingtalkContent = `📢 **任务分配给 千问 (Surface)**

${task}

**执行时间**: 明早 08:00
**要求**: 
• 发送早安消息
• 配上语音播报

请确认收到任务。`;

  let sent = false;
  if (env.DINGTALK_WEBHOOK_PRIMARY) {
    sent = await sendDingTalk(
      env.DINGTALK_WEBHOOK_PRIMARY,
      env.DINGTALK_SECRET_PRIMARY,
      '📋 任务分配',
      dingtalkContent,
      '主'
    );
  }
  
  if (!sent && env.DINGTALK_WEBHOOK_SECONDARY) {
    await sendDingTalk(
      env.DINGTALK_WEBHOOK_SECONDARY,
      env.DINGTALK_SECRET_SECONDARY,
      '📋 任务分配',
      dingtalkContent,
      '备'
    );
  }
  
  // 3. 发送 Telegram 提醒（如果 Surface 也监听 Telegram）
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
    await sendTelegram(
      env.TELEGRAM_BOT_TOKEN,
      env.TELEGRAM_CHAT_ID,
      `🔔 <b>Surface AI 任务提醒</b>\n\n${task}\n\n明早 08:00 执行，请准备语音播报。`
    );
  }
  
  console.log();
  console.log('✅ 通知已发送');
})();
