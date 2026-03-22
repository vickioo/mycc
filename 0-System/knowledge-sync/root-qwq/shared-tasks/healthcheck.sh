#!/bin/bash
# Agent 网络健康检查脚本

echo "╔════════════════════════════════════════╗"
echo "║     Agent Network Health Check         ║"
echo "╚════════════════════════════════════════╝"
echo ""

# qwq (local)
echo -n "qwq (Qwen Code)....... "
if [ -d "/root/air/qwq" ]; then echo "✅"; else echo "❌"; fi

# mycc (local)
echo -n "mycc (Claude Code).... "
if [ -d "/root/air/mycc" ]; then echo "✅"; else echo "❌"; fi

# CC Server
echo -n "CC Server............. "
if ssh -o BatchMode=yes -o ConnectTimeout=3 CC "echo OK" 2>/dev/null; then
    echo "✅"
else
    echo "❌"
fi

# SJLL Agent
echo -n "SJLL (龙虾)............ "
if ssh -o BatchMode=yes -o ConnectTimeout=3 sjll-agent "echo OK" 2>/dev/null; then
    echo "✅"
else
    echo "❌"
fi

# One-API
echo -n "One-API (CC).......... "
if ssh -o BatchMode=yes CC "curl -s http://localhost:3000/api/status" 2>/dev/null | grep -q "success"; then
    echo "✅"
else
    echo "❌"
fi

# Task Scheduler
echo -n "Scheduler (CC)........ "
if ssh -o BatchMode=yes CC "pgrep -f scheduler.sh" >/dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "════════════════════════════════════════"
