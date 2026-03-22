import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function sendWebhook(title, text, type = 'primary') {
  try {
    const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf-8'));
    const hook = config.webhooks[type];
    if (!hook) throw new Error(`Webhook ${type} not found`);

    const timestamp = Date.now();
    const stringToSign = `${timestamp}\n${hook.secret}`;
    const sign = crypto.createHmac('sha256', hook.secret).update(stringToSign).digest('base64');
    const encodedSign = encodeURIComponent(sign);

    const url = `${hook.url}&timestamp=${timestamp}&sign=${encodedSign}`;

    const payload = {
      msgtype: 'markdown',
      markdown: {
        title: title,
        text: `**${title}**\n\n${text}`
      }
    };

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await res.json();
    console.log(`[Webhook ${type}] status:`, result);
  } catch (err) {
    console.error(`[Webhook error]`, err.message);
  }
}

const args = process.argv.slice(2);
if (args.length >= 2) {
  sendWebhook(args[0], args[1], args[2] || 'primary');
} else {
  console.log("Usage: node notify-webhook.js <title> <text> [primary|backup]");
}
