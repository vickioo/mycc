#!/bin/bash
#
# 为 Gemini CLI 设置 Clash 代理
# 用法：source /root/air/qwq/0-System/setup-gemini-proxy.sh
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
echo "║     Gemini CLI Clash 代理设置                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 方案 1: 使用 CC 服务器的 Clash (需要 Termux 中转)
log "方案 1: 通过 Termux + CC 服务器建立代理隧道..."

# 在 Termux 中启动 SSH 隧道
ssh -p 8022 localhost "
  pkill -f 'ssh.*-D 7891' 2>/dev/null || true
  sleep 1
  nohup ssh -N \
    -D 7891 \
    -o ServerAliveInterval=15 \
    -o ServerAliveCountMax=2 \
    -o ExitOnForwardFailure=yes \
    -o TCPKeepAlive=yes \
    -o ClearAllForwardings=yes \
    gate >> /tmp/clash-tunnel.log 2>&1 &
  echo \$! > /tmp/clash-tunnel.pid
  sleep 2
  if kill -0 \$(cat /tmp/clash-tunnel.pid) 2>/dev/null; then
    echo '✅ Clash tunnel started in Termux'
  else
    echo '❌ Failed to start tunnel'
  fi
" 2>&1

sleep 3

# 检查代理是否可用
log "检查代理端口..."
if timeout 2 bash -c "echo > /dev/tcp/localhost/7891" 2>/dev/null; then
    log "✅ 代理端口 7891 已开放"
    
    # 设置环境变量
    export ALL_PROXY=socks5h://localhost:7891
    export HTTPS_PROXY=socks5h://localhost:7891
    export HTTP_PROXY=socks5h://localhost:7891
    
    log "✅ 代理环境变量已设置"
    echo ""
    echo "当前代理配置:"
    echo "  ALL_PROXY=$ALL_PROXY"
    echo "  HTTPS_PROXY=$HTTPS_PROXY"
    echo ""
    
    # 测试代理
    log "测试代理连通性..."
    if timeout 5 curl -s --socks5-hostname localhost:7891 https://www.google.com >/dev/null 2>&1; then
        log "✅ 代理工作正常！可以访问 Google"
    else
        warn "代理可能不可用，继续测试..."
    fi
    
    # 测试 Gemini
    log "测试 Gemini CLI..."
    timeout 10 gemini "Hello, are you connected?" 2>&1 | head -10
    
else
    error "代理端口 7891 不可用"
    echo ""
    warn "备用方案：直接在 Termux 中使用 Gemini"
    echo ""
    echo "在 Termux 中执行:"
    echo "  export ALL_PROXY=socks5h://localhost:7891"
    echo "  gemini 'Hello'"
fi
