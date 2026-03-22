#!/bin/bash
#
# 系统服务一键启动脚本
# 用途：启动所有核心服务
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
echo "║     系统服务一键启动                            ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 1. 启动 V3 移动端
log "启动 V3 移动端..."
if curl -s http://localhost:8769/api/health | grep -q ok; then
    echo "  ✅ V3 已在运行"
else
    cd /root/air/qwq/mobile-web
    nohup python3 app.py > /tmp/mobile-web-v2.log 2>&1 &
    sleep 3
    if curl -s http://localhost:8769/api/health | grep -q ok; then
        echo "  ✅ V3 已启动 (:8769)"
    else
        warn "V3 启动失败"
    fi
fi

# 2. 启动 free-claude-code
log "启动 free-claude-code..."
if curl -s http://localhost:8083/ | grep -q ok; then
    echo "  ✅ free-claude-code 已在运行"
else
    cd /root/free-claude-code
    nohup .venv_fix/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8083 > /tmp/free-cc.log 2>&1 &
    sleep 3
    if curl -s http://localhost:8083/ | grep -q ok; then
        echo "  ✅ free-claude-code 已启动 (:8083)"
    else
        warn "free-claude-code 启动失败"
    fi
fi

# 3. 检查 CC Clash Watchdog
log "检查 CC Clash Watchdog..."
if pm2 status | grep -q "cc-clash-watchdog.*online"; then
    echo "  ✅ CC Clash Watchdog 运行中"
else
    warn "CC Clash Watchdog 未运行"
fi

# 4. 检查 cc-clash-tunnel
log "检查 cc-clash-tunnel..."
if pm2 status | grep -q "cc-clash-tunnel.*online"; then
    echo "  ✅ cc-clash-tunnel 运行中"
else
    warn "cc-clash-tunnel 未运行 (需手动修复)"
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     服务状态                                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "V3 移动端：         http://localhost:8769"
echo "free-claude-code:   http://localhost:8083"
echo ""
echo "测试命令:"
echo "  curl http://localhost:8769/api/health"
echo "  curl http://localhost:8083/"
echo ""
