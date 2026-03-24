#!/usr/bin/env python3
import subprocess, json
from datetime import datetime

REPLY = '/home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js'
CHANGES = '/home/vicki/air/mycc/3-Thinking/2026-03-23-mycc-changes.md'

def cmd(c):
    return subprocess.check_output(c, shell=True, encoding='utf8').strip()

def send(msg):
    subprocess.run(['node', REPLY, '--text', msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

summary = '今日无归档记录'
try:
    with open(CHANGES) as f:
        content = f.read()
    sections = __import__('re').findall(r'^## .+$', content, __import__('re').M)
    if sections:
        summary = '\n'.join(s.replace('## ', '• ') for s in sections[:5])
except:
    pass

pm2 = json.loads(cmd('pm2 jlist'))
restarts = sum(p['pm2_env'].get('restart_time', 0) for p in pm2)
online = sum(1 for p in pm2 if p['pm2_env']['status'] == 'online')

now = datetime.now()
send(f"🌙 晚报 · {now.month}月{now.day}日\n\n📋 今日进展\n{summary}\n\n📊 进程: {online}/{len(pm2)}在线 · 总重启{restarts}次\n\n好好休息，明天继续 💪")
