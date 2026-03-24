#!/usr/bin/env tsx
import { execSync } from 'child_process'

const REPLY = '/home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js'

function cmd(c: string): string {
  return execSync(c, { encoding: 'utf8' }).trim()
}

function send(msg: string): void {
  execSync(`${REPLY} "${msg.replace(/"/g, '\\"')}"`, { stdio: 'ignore' })
}

const alerts: string[] = []
const now = new Date()
const isOnTheHour = now.getMinutes() === 0  // 整点 = 详细版，其余 = 精简版

// ── PM2 进程检查 ──
const pm2 = JSON.parse(cmd('pm2 jlist'))
for (const p of pm2 as any[]) {
  if (p.pm2_env.status !== 'online') {
    alerts.push(`❌ ${p.name} 离线 (${p.pm2_env.status})`)
  } else if ((p.pm2_env.restart_time || 0) > 0) {
    alerts.push(`⚠️ ${p.name} 重启 ${p.pm2_env.restart_time} 次`)
  }
}

// ── Provider 检查（主链路 nvidia_nim + open_router）──
for (const [name, url] of [
  ['nvidia_nim', 'https://integrate.api.nvidia.com/v1/models'],
  ['openrouter',  'https://openrouter.ai/api/v1/models'],
] as [string, string][]) {
  try {
    const r = cmd(`curl -s -o /dev/null -w "%{http_code}" "${url}" --max-time 5`)
    if (r !== '200') alerts.push(`⚠️ ${name} HTTP ${r}`)
  } catch {
    alerts.push(`❌ ${name} 连接失败`)
  }
}

// ── 只在异常时发送 ──
if (alerts.length > 0) {
  const t = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  const procLines = pm2.map((p: any) =>
    `  ${p.name.padEnd(20)} ${p.pm2_env.status === 'online' ? '✅' : '❌' + p.pm2_env.status}`
  ).join('\n')

  const footer = isOnTheHour ? `
━━━ 指标说明 ━━━
• 重启次数：进程自上次"pm2 reset"后的累积重启次数，正常应保持为 0
• HTTP 状态：Provider 的 /v1/models 接口响应码，200 = 正常，其他 = 异常
• ⚠️ = 警告（可继续尝试但不稳定），❌ = 失败（立即处理）` : ''

  send(`🚨 系统报警 · ${t}${isOnTheHour ? '（详细版）' : ''}\n\n📊 进程\n${procLines}\n\n⚠️ 异常\n${alerts.join('\n')}${footer}`)
}
