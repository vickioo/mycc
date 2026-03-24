#!/usr/bin/env python3
import subprocess, json

REPLY = '/home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js'

def cmd(c):
    r = subprocess.run(c, shell=True, capture_output=True)
    return r.stdout.decode('utf8').strip()

def send(msg):
    subprocess.run(['node', REPLY, '--text', msg], capture_output=True)

try:
    nv = cmd('curl -s -o /dev/null -w "%{http_code}" https://integrate.api.nvidia.com/v1/models --max-time 5')
    prov = '✅ nvidia_nim' if nv == '200' else f'⚠️ nvidia_nim({nv})'
except:
    prov = '❌ nvidia_nim离线'

try:
    or_ = cmd('curl -s -o /dev/null -w "%{http_code}" https://openrouter.ai/api/v1/models --max-time 5')
    or_status = '✅ openrouter' if or_ == '200' else f'⚠️ openrouter({or_})'
except:
    or_status = '❌ openrouter'

disk = cmd("df -h / | tail -1 | awk '{print $5}'")
mem = cmd("free -h | awk '/Mem:/ {print $3\" / \"$2}'")
pm2 = json.loads(cmd('pm2 jlist'))
lines = []
for p in pm2:
    name = p['name']
    status = '✅在线' if p['pm2_env']['status']=='online' else '❌'+p['pm2_env']['status']
    lines.append(f"  {name:20s} {status}")
procs = '\n'.join(lines)

from datetime import datetime
now = datetime.now()
t = f"{now.hour:02d}:{now.minute:02d}"
msg = f"🌅 晨报 · {t}\n\n📊 系统状态\n{procs}\n\n💾 磁盘: {disk}\n🧠 内存: {mem}\n🌐 nvidia: {prov}\n🌐 openrouter: {or_status}\n\n祝今天顺利！"
send(msg)
