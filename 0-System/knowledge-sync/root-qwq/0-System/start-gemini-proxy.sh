#!/bin/bash
#
# start-gemini-proxy.sh - 启动 Gemini CLI 代理
# 用途：在 Termux 中启动 Clash 隧道，为 Gemini 提供代理
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] 警告:${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] 错误:${NC} $1"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     Gemini CLI 代理启动脚本                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 步骤 1: 测试 U22 SSH 连接
log "步骤 1/4: 测试 U22 SSH 连接..."
if ssh -o BatchMode=yes -o ConnectTimeout=5 gate "echo OK" 2>&1 | grep -q OK; then
    log "✅ U22 SSH 连接正常"
else
    error "❌ U22 SSH 连接失败，请检查网络或服务器状态"
    exit 1
fi

# 步骤 2: 测试 Termux SSH 连接
log "步骤 2/4: 测试 Termux SSH 连接..."
if ssh -p 8022 localhost "ssh -o BatchMode=yes -o ConnectTimeout=5 gate 'echo OK'" 2>&1 | grep -q OK; then
    log "✅ Termux SSH 连接正常"
else
    error "❌ Termux SSH 连接失败"
    exit 1
fi

# 步骤 3: 启动 Clash 隧道
log "步骤 3/4: 启动 Clash 隧道..."
TUNNEL_OUTPUT=$(ssh -p 8022 localhost "bash ~/start-clash-tunnel.sh" 2>&1)
if echo "$TUNNEL_OUTPUT" | grep -q "✅"; then
    log "✅ Clash 隧道已启动"
    echo "$TUNNEL_OUTPUT" | grep "代理地址"
else
    error "❌ Clash 隧道启动失败"
    echo "$TUNNEL_OUTPUT"
    exit 1
fi

# 步骤 4: 测试代理
log "步骤 4/4: 测试代理..."
PROXY_TEST=$(ssh -p 8022 localhost "timeout 5 curl -s --socks5-hostname localhost:7891 https://api.ip.sb/ip 2>&1 | head -1" 2>&1)
if [ -n "$PROXY_TEST" ] && ! echo "$PROXY_TEST" | grep -q "timeout\|failed"; then
    log "✅ 代理工作正常！出口 IP: $PROXY_TEST"
else
    warn "⚠️ 代理测试超时或失败，但隧道可能仍在运行"
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     启动完成！                                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "使用方法:"
echo ""
echo "1. 在 Termux 中使用 Gemini:"
echo "   ssh -p 8022 localhost"
echo "   export ALL_PROXY=socks5h://localhost:7891"
echo "   gemini 'Hello'"
echo ""
echo "2. 在 U22 中通过反向隧道使用:"
echo "   export ALL_PROXY=socks5h://localhost:7892"
echo "   gemini 'Hello'"
echo ""
echo "查看状态:"
echo "   ssh -p 8022 localhost 'cat ~/clash-tunnel.log | tail -5'"
echo ""
echo "停止隧道:"
echo "   ssh -p 8022 localhost 'pkill -f \"ssh.*-D 7891\"'"
echo ""
