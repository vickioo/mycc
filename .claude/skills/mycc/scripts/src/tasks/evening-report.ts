#!/usr/bin/env tsx
import { execSync } from 'child_process'
import { existsSync, readFileSync } from 'fs'
const REPLY = 'node /home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js --text'
const CHANGES = '/home/vicki/air/mycc/3-Thinking/2026-03-23-mycc-changes.md'
function cmd(c: string) { return execSync(c, {encoding:'utf8'}).trim() }
function send(m: string) { execSync(`${REPLY} "${m.replace(/"/g,'\\"')}"`, {stdio:'ignore'}) }
let summary = '今日无归档记录'
if (existsSync(CHANGES)) {
  const content = readFileSync(CHANGES, 'utf8')
  const sections = content.match(/^## .+$/gm) || []
  if (sections.length > 0) summary = sections.slice(0,5).map((s:string) => s.replace('## ','• ')).join('\n')
}
const pm2 = JSON.parse(cmd('pm2 jlist'))
const restarts = pm2.reduce((s: number, p: any) => s + (p.pm2_env.restart_time||0), 0)
const online = pm2.filter((p: any) => p.pm2_env.status === 'online').length
const now = new Date()
send(`🌙 晚报 · ${now.getMonth()+1}月${now.getDate()}日\n\n📋 今日进展\n${summary}\n\n📊 进程: ${online}/${pm2.length}在线 · 总重启${restarts}次\n\n好好休息，明天继续 💪`)
