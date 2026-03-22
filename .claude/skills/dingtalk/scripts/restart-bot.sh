#!/bin/bash
# 钉钉机器人守护重启脚本
export LANG=zh_CN.UTF-8

# 停止旧进程
pkill -f "bot-v2.js" 2>/dev/null
pkill -f "bot.js" 2>/dev/null
sleep 2

# 确保 tmux 会话存在
tmux has-session -t cc-daemon 2>/dev/null || tmux new-session -d -s cc-daemon -n main

# 启动新版机器人
tmux send-keys -t cc-daemon "C-c"
sleep 1
tmux send-keys -t cc-daemon "node bot-v2.js" ENTER

echo "机器人已重启"
