#!/usr/bin/env node
/**
 * 钉钉通知脚本 - 用于 5 分钟汇报
 * 用法：node dingtalk-notify.js "标题" "内容" [级别]
 * 级别：info, success, warning, error
 */

const crypto = require('crypto');
const fs = require('fs');

const [,, title, content, level = 'info'] = process.argv;

if (!title || !content) {
  console.error('用法：node dingtalk-notify.js "标题" "内容" [级别]');
  process.exit(1);
}

// 读取环境变量
function getEnv() {
  const envPath = '/root/air/mycc/.env';
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    return envContent.split('\n').reduce((acc, line) => {
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

// 钉钉加签算法
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

// 主逻辑
(async () => {
  let sent = false;

  // 优先使用主通道
  if (env.DINGTALK_WEBHOOK_PRIMARY) {
    sent = await sendDingTalk(
      env.DINGTALK_WEBHOOK_PRIMARY,
      env.DINGTALK_SECRET_PRIMARY,
      title,
      content,
      '主'
    );
  }

  // 主通道失败时使用备用通道
  if (!sent && env.DINGTALK_WEBHOOK_SECONDARY) {
    await sendDingTalk(
      env.DINGTALK_WEBHOOK_SECONDARY,
      env.DINGTALK_SECRET_SECONDARY,
      title,
      content,
      '备'
    );
  }

  if (!sent) {
    console.error('⚠️  未配置任何钉钉通道');
    process.exit(1);
  }
})();
