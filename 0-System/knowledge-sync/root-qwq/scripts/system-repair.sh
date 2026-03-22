#!/bin/bash
#
# 系统一键修复脚本
# 用途：修复检查中发现的关键问题
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
info() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] 警告:${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] 错误:${NC} $1"; }

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     🔧 系统一键修复                             ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 1. 启动 U22 sv 服务
log "启动 U22 sv 服务..."
/root/bin/sv/sv start ssh-gate 2>&1 || warn "ssh-gate 启动失败"
/root/bin/sv/sv start watchdog 2>&1 || warn "watchdog 启动失败"
sleep 2
/root/bin/sv/sv status

# 2. 清理磁盘空间
log "清理磁盘空间..."
pm2 flush 2>/dev/null || true
rm -rf /tmp/*.log /tmp/*-pm2*.log /tmp/uvicorn*.log 2>/dev/null || true
info "  PM2 日志已清理"
info "  临时日志已清理"

# 3. 重启 CC Clash Tunnel
log "重启 CC Clash Tunnel..."
pm2 restart cc-clash-tunnel 2>&1 || warn "PM2 重启失败"
sleep 3

# 4. 检查服务状态
echo ""
log "检查服务状态..."
echo ""

echo "=== PM2 服务 ==="
pm2 status 2>&1 | head -15

echo ""
echo "=== U22 sv 服务 ==="
/root/bin/sv/sv status 2>&1

echo ""
echo "=== 知识库服务 ==="
curl -s http://localhost:8772/api/health 2>&1 | head -1 || echo "❌"

echo ""
echo "=== free-claude-code ==="
curl -s http://localhost:8083/ 2>&1 | head -1 || echo "❌"

echo ""
echo "=== 磁盘空间 ==="
df -h / 2>/dev/null | tail -1

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     ✅ 修复完成！                               ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
