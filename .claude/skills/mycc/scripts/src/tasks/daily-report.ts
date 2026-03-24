#!/usr/bin/env tsx
import { execSync } from 'child_process'
const REPLY = 'node /home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js --text'
function cmd(c: string) { return execSync(c, { encoding: 'utf8' }).trim() }
function send(msg: string) { execSync(`${REPLY} "${msg.replace(/"/g, '\\"')}"`, { stdio: 'ignore' }) }
const pm2 = JSON.parse(cmd('pm2 jlist'))
const procs = pm2.map((p: any) => `  ${p.name.padEnd(20)} ${p.pm2_env.status==='online'?'✅在线':'❌'+p.pm2_env.status}`).join('\n')
const disk = cmd("df -h / | tail -1 | awk '{print $5}'")
const mem = cmd("free -h | awk '/Mem:/ {print $3\" / \"$2}'")
let prov='未知'
try{ const r=execSync('curl -s -o /dev/null -w "%{http_code}" https://integrate.api.nvidia.com/v1/models --max-time 5',{encoding:'utf8'}); prov=r==='200'?'✅ nvidia_nim':'⚠️ nvidia_nim('+r+')' }catch(){prov='❌ nvidia_nim离线'}
const now=new Date(); const t=`${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`
send(`🌅 晨报 · ${t}\n\n📊 系统状态\n${procs}\n\n💾 磁盘: ${disk}\n🧠 内存: ${mem}\n🌐 Provider: ${prov}\n\n祝今天顺利！`)
