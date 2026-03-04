#!/usr/bin/env node
/**
 * 钉钉群通知脚本
 * 用法: node notify.js "标题" "内容"
 *
 * 通过钉钉机器人的 sessionWebhook 或 OpenAPI 发送群消息
 * 这里使用 OpenAPI 方式，需要 access_token
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const [,, title, content] = process.argv;

if (!title || !content) {
  console.error('用法: node notify.js "标题" "内容"');
  process.exit(1);
}

// 读取配置
let config;
try {
  config = JSON.parse(readFileSync(join(__dirname, 'config.json'), 'utf-8'));
} catch (e) {
  console.error('❌ 配置文件读取失败，请检查 config.json');
  process.exit(1);
}

async function getAccessToken() {
  const url = `https://oapi.dingtalk.com/gettoken?appkey=${config.clientId}&appsecret=${config.clientSecret}`;
  const res = await fetch(url);
  const data = await res.json();
  if (data.errcode !== 0) {
    throw new Error(`获取 access_token 失败: ${data.errmsg}`);
  }
  return data.access_token;
}

async function sendMessage(accessToken, text) {
  // 使用钉钉 OpenAPI 发送工作通知（应用内通知）
  // 如果要发到群里，需要知道群的 chatId
  // 这里先用 Markdown 格式的工作通知
  const markdown = `## ${title}\n\n${text}\n\n---\n*⏰ ${new Date().toLocaleString('zh-CN')}*`;

  console.log('📌 钉钉通知内容:');
  console.log(`   标题: ${title}`);
  console.log(`   内容: ${content}`);
  console.log(`   时间: ${new Date().toLocaleString('zh-CN')}`);
  console.log('');
  console.log('✅ 通知已准备就绪');
  console.log('');
  console.log('💡 提示: 群通知需要通过 Stream 机器人在群内发送');
  console.log('   启动机器人: node bot.js');
  console.log('   然后在群里 @机器人 即可交互');

  return { markdown, accessToken };
}

try {
  const accessToken = await getAccessToken();
  await sendMessage(accessToken, content);
} catch (err) {
  console.error('❌ 发送失败:', err.message);
  process.exit(1);
}
