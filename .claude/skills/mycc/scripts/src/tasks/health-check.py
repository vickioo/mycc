#!/usr/bin/env python3
import subprocess, json
from datetime import datetime

REPLY = '/home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js'

def cmd(c):
    return subprocess.check_output(c, shell=True, encoding='utf8').strip()

def send(msg):
    subprocess.run(['node', REPLY, '--text', msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

alerts = []
now = datetime.now()
is_hour = now.minute == 0

pm2 = json.loads(cmd('pm2 jlist'))
for p in pm2:
    if p['pm2_env']['status'] != 'online':
        alerts.append(f"❌ {p['name']} 离线 ({p['pm2_env']['status']})")
    elif p['pm2_env'].get('restart_time', 0) > 0:
        alerts.append(f"⚠️ {p['name']} 重启{p['pm2_env']['restart_time']}次")

for name, url in [('nvidia_nim', 'https://integrate.api.nvidia.com/v1/models'),
                  ('openrouter',  'https://openrouter.ai/api/v1/models')]:
    try:
        r = cmd(f'curl -s -o /dev/null -w "%{{http_code}}" "{url}" --max-time 5')
        if r != '200':
            alerts.append(f"⚠️ {name} HTTP {r}")
    except:
        alerts.append(f"❌ {name} 连接失败")

if alerts:
    t = f"{now.hour:02d}:{now.minute:02d}"
    proc_lines = '\n'.join(f"  {p['name'].ljust(20)} {'✅' if p['pm2_env']['status']=='online' else '❌'+p['pm2_env']['status']}" for p in pm2)
    footer = """
━━━ 指标说明 ━━━
• 重启次数：进程自上次 pm2 reset 后的累积重启，正常应保持为 0
• HTTP 状态：Provider /v1/models 接口，200 = 正常，其他 = 异常
• ⚠️ = 警告（不稳定），❌ = 失败（需立即处理）""" if is_hour else ''

    send(f"🚨 系统报警 · {t}{'（详细版）' if is_hour else ''}\n\n📊 进程\n{proc_lines}\n\n⚠️ 异常\n" + '\n'.join(alerts) + footer)
