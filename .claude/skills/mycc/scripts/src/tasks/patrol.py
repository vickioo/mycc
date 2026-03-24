#!/usr/bin/env python3
"""
统一巡检脚本
  无参数  → 异常巡检（7-21点，每15分钟）
  --daily    → 晨报（8:27）
  --evening  → 晚报（21:03）
"""
import subprocess, json, sys, re
from datetime import datetime
from os.path import exists

SEND = 'node /home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js --text'
PM2 = '/home/vicki/.npm-global/bin/pm2'

def cmd(c, timeout=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()

def send(msg):
    if not msg.strip(): return
    subprocess.run(f'{SEND} "{msg.replace(chr(34), chr(92)+chr(34))}"',
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

mode = sys.argv[1] if len(sys.argv) > 1 else None
now = datetime.now()
t = f"{now.hour:02d}:{now.minute:02d}"

# ── 晨报 ──────────────────────────────────────────────────
if mode == '--daily':
    pm2 = json.loads(cmd(f'{PM2} jlist'))
    procs = '\n'.join(f"  {p['name'].ljust(22)} {'✅在线' if p['pm2_env']['status']=='online' else '❌'+p['pm2_env']['status']}" for p in pm2)
    disk = cmd("df -h / | tail -1 | awk '{print $5}'")
    mem = cmd("free -h | awk '/Mem:/ {print $3\" / \"$2}'")
    try:
        nv = cmd('curl -s -o /dev/null -w "%{http_code}" https://integrate.api.nvidia.com/v1/models --max-time 5')
        prov = '✅ nvidia_nim' if nv == '200' else f'⚠️ nvidia_nim({nv})'
    except: prov = '❌ nvidia_nim'
    send(f"🌅 晨报 · {t}\n\n📊 系统状态\n{procs}\n\n💾 磁盘: {disk}\n🧠 内存: {mem}\n🌐 Provider: {prov}\n\n祝今天顺利！")
    print(f'[{t}] 晨报已发送')
    sys.exit(0)

# ── 晚报 ──────────────────────────────────────────────────
if mode == '--evening':
    CHANGES = '/home/vicki/air/mycc/3-Thinking/2026-03-23-mycc-changes.md'
    summary = '今日无归档记录'
    if exists(CHANGES):
        content = open(CHANGES).read()
        sections = re.findall(r'^## .+$', content, re.M)
        if sections:
            summary = '\n'.join(s.replace('## ', '• ') for s in sections[:5])
    pm2 = json.loads(cmd(f'{PM2} jlist'))
    restarts = sum(p['pm2_env'].get('restart_time', 0) for p in pm2)
    online = sum(1 for p in pm2 if p['pm2_env']['status'] == 'online')
    send(f"🌙 晚报 · {now.month}月{now.day}日\n\n📋 今日进展\n{summary}\n\n📊 进程: {online}/{len(pm2)}在线 · 总重启{restarts}次\n\n好好休息，明天继续 💪")
    print(f'[{t}] 晚报已发送')
    sys.exit(0)

# ── 异常巡检 ──────────────────────────────────────────────
errors = []
info_lines = []

try:
    pm2 = json.loads(cmd(f'{PM2} jlist'))
    for p in pm2:
        s = p['pm2_env']['status']
        r = p['pm2_env'].get('restart_time', 0)
        if s != 'online': errors.append(f'❌ {p["name"]} 离线: {s}')
        elif r > 2: errors.append(f'⚠️ {p["name"]} 重启{r}次')
except Exception as e:
    errors.append(f'❌ pm2 查询失败')

for name, url in [
    ('nvidia_nim', 'https://integrate.api.nvidia.com/v1/models'),
    ('openrouter', 'https://openrouter.ai/api/v1/models'),
    # silicon_flow 已停用（2026-03-23），不再巡检
]:
    try:
        r = cmd(f'curl -s -o /dev/null -w "%{{http_code}}" {url} --max-time 6')
        if r != '200': errors.append(f'⚠️ {name} HTTP {r}')
    except: errors.append(f'❌ {name} 连接失败')

try:
    mem = cmd("free -h | awk '/Mem:/ {print $3\" / \"$2}'")
    disk = cmd("df -h / | tail -1 | awk '{print $5}'")
    load = cmd("uptime | awk -F'load average:' '{print $2}'")
    info_lines.append(f'💾 {disk} · 🧠 {mem} · 📊 {load.strip()}')
except: pass

if not errors:
    print(f'[{t}] 巡检正常 ✓')
else:
    msg = f'🚨 巡检异常 · {t}\n\n━━━ 进程 ━━━'
    proc_errs = [e for e in errors if any(x in e for x in ['离线', '重启', 'pm2'])]
    msg += '\n' + ('\n'.join(proc_errs) if proc_errs else '  正常')
    msg += '\n\n━━━ 链路 ━━━'
    net_errs = [e for e in errors if any(x in e for x in ['HTTP', 'nvidia', 'openrouter', 'silicon'])]
    msg += '\n' + ('\n'.join(net_errs) if net_errs else '  正常')
    if info_lines:
        msg += '\n\n━━━ 资源 ━━━\n' + '\n'.join(info_lines)
    send(msg)
    print(f'[{t}] 巡检异常 · {len(errors)}项')
