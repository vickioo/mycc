#!/bin/bash
# AI Agent 整体进度状态检查
# 检查本地 + CC + SJLL 所有 AI 智能体

echo "╔════════════════════════════════════════════════════╗"
echo "║         AI Agent 整体进度状态                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# 颜色定义
GREEN="✅"
RED="❌"
YELLOW="⚠️"

# ========== 本地代理 ==========
echo "📍 本地 (qwq)"
echo "─────────────────────────────────────────────────────"

# Qwen Code (本地)
if [ -d "/root/air/qwq" ]; then
    echo "  $GREEN Qwen Code      /root/air/qwq"
else
    echo "  $RED Qwen Code"
fi

# mycc (Claude Code 本地)
if [ -d "/root/air/mycc" ]; then
    echo "  $GREEN mycc (Claude)  /root/air/mycc"
else
    echo "  $RED mycc (Claude)"
fi

# free-claude-code 代理
if curl -s http://localhost:8083/health >/dev/null 2>&1; then
    PROXY_INFO=$(curl -s http://localhost:8083/)
    echo "  $GREEN free-claude    http://localhost:8083"
    echo "     └─ Provider: $(echo $PROXY_INFO | grep -o '"provider":"[^"]*"' | cut -d'"' -f4)"
else
    echo "  $RED free-claude    (未运行)"
fi

# Codex CLI
if command -v codex &> /dev/null; then
    echo "  $GREEN Codex CLI      $(codex --help 2>&1 | head -1 | grep -o 'v[0-9.]*')"
else
    echo "  $RED Codex CLI"
fi

echo ""

# ========== CC 服务器 ==========
echo "📍 CC 服务器 (CC)"
echo "─────────────────────────────────────────────────────"

CC_STATUS=$(ssh -o BatchMode=yes -o ConnectTimeout=3 CC "echo OK" 2>/dev/null)
if [ "$CC_STATUS" = "OK" ]; then
    echo "  $GREEN SSH 连接       已连接"
    
    # Gemini CLI
    GEMINI=$(ssh CC "ps aux | grep -v grep | grep -i 'gemini' | head -1" 2>/dev/null)
    if [ -n "$GEMINI" ]; then
        echo "  $GREEN Gemini CLI   运行中"
    else
        echo "  $YELLOW Gemini CLI   未运行"
    fi
    
    # Claude
    CLAUDE=$(ssh CC "ps aux | grep -v grep | grep -i 'claude' | head -1" 2>/dev/null)
    if [ -n "$CLAUDE" ]; then
        echo "  $GREEN Claude         运行中"
    else
        echo "  $YELLOW Claude         未运行"
    fi
    
    # One-API
    ONEAPI=$(ssh CC "curl -s http://localhost:3000/api/status" 2>/dev/null)
    if echo "$ONEAPI" | grep -q "success"; then
        echo "  $GREEN One-API        http://localhost:3000"
    else
        echo "  $YELLOW One-API        未响应"
    fi
else
    echo "  $RED SSH 连接       无法连接"
fi

echo ""

# ========== SJLL 主机 ==========
echo "📍 SJLL 主机 (龙虾)"
echo "─────────────────────────────────────────────────────"

SJLL_STATUS=$(ssh -o BatchMode=yes -o ConnectTimeout=3 sjll-agent "echo OK" 2>/dev/null)
if [ "$SJLL_STATUS" = "OK" ]; then
    echo "  $GREEN SSH 连接       已连接"
    
    # OpenClaw Gateway
    OPENCLAW=$(ssh sjll-agent "curl -s http://localhost:18789/api/health" 2>/dev/null)
    if [ -n "$OPENCLAW" ]; then
        echo "  $GREEN OpenClaw       端口 18789"
    else
        echo "  $YELLOW OpenClaw       未响应"
    fi
    
    # Qwen CLI
    QWEN_CLI=$(ssh sjll-agent "netstat -tlnp 2>/dev/null | grep 18790" 2>/dev/null)
    if [ -n "$QWEN_CLI" ]; then
        echo "  $GREEN Qwen CLI       端口 18790"
    else
        echo "  $YELLOW Qwen CLI       未运行"
    fi
else
    echo "  $RED SSH 连接       无法连接 (需刷新隧道)"
fi

echo ""

# ========== 任务系统 ==========
echo "📋 任务系统状态"
echo "─────────────────────────────────────────────────────"

# 本地任务
LOCAL_INBOX=$(ls /root/air/qwq/shared-tasks/inbox/*.json 2>/dev/null | wc -l)
LOCAL_DONE=$(ls /root/air/qwq/shared-tasks/completed/*.json 2>/dev/null | wc -l)
echo "  本地任务：待处理 $LOCAL_INBOX | 已完成 $LOCAL_DONE"

# CC 任务
CC_INBOX=$(ssh -o BatchMode=yes CC "ls /data/mycc/shared-tasks/inbox/*.json 2>/dev/null | wc -l" 2>/dev/null || echo "0")
CC_DONE=$(ssh -o BatchMode=yes CC "ls /data/mycc/shared-tasks/completed/*.json 2>/dev/null | wc -l" 2>/dev/null || echo "0")
echo "  CC 任务：待处理 $CC_INBOX | 已完成 $CC_DONE"

echo ""

# ========== 网络隧道 ==========
echo "🔗 网络隧道"
echo "─────────────────────────────────────────────────────"

# Clash 隧道
CLASH=$(pgrep -f "cc-clash" 2>/dev/null)
if [ -n "$CLASH" ]; then
    echo "  $GREEN CC Clash 隧道  运行中 (SOCKS5 :7890)"
else
    echo "  $YELLOW CC Clash 隧道  未运行"
fi

echo ""
echo "════════════════════════════════════════════════════"
echo "检查完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
