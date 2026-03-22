#!/data/data/com.termux/files/usr/bin/bash
#
# Termux 优化一键执行脚本
# 用途：修复 SSH、安装 services、配置自启动
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] 警告:${NC} $1"; }
info() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] 错误:${NC} $1"; }

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     Termux 优化脚本                              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Step 1: 修复 SSH
log "Step 1/5: 修复 SSH 连接..."
pkill sshd 2>/dev/null || true
sleep 1
sshd
sleep 2

if ss -tlnp 2>/dev/null | grep -q 8022; then
    log "✅ SSH 已启动 (端口 8022)"
else
    warn "❌ SSH 启动失败，继续执行..."
fi

# Step 2: 安装 termux-services
log "Step 2/5: 安装 termux-services..."
if pkg list-installed termux-services > /dev/null 2>&1; then
    info "termux-services 已安装"
else
    pkg install termux-services -y
    log "✅ termux-services 已安装"
fi

# Step 3: 配置服务目录
log "Step 3/5: 配置服务目录..."
mkdir -p ~/.termux/services

if [ ! -f "$PREFIX/etc/services/sshd.sh" ]; then
    cat > $PREFIX/etc/services/sshd.sh << 'EOFSSH'
#!/data/data/com.termux/files/usr/bin/bash
exec sshd -D -e -R
EOFSSH
    chmod +x $PREFIX/etc/services/sshd.sh
fi

cp $PREFIX/etc/services/sshd.sh ~/.termux/services/
log "✅ 服务目录已配置"

# Step 4: 启用服务
log "Step 4/5: 启用 sshd 服务..."
termux-services enable sshd.sh 2>/dev/null || {
    warn "termux-services 启用失败，手动启动..."
    sshd -D -e -R &
}
log "✅ 服务已启用"

# Step 5: 安装 Termux:API
log "Step 5/5: 安装 Termux:API..."
if pkg list-installed termux-api > /dev/null 2>&1; then
    info "Termux:API 已安装"
else
    pkg install termux-api -y
    log "✅ Termux:API 已安装"
fi

# 测试 API
info "测试 API 命令..."
termux-battery-status 2>/dev/null | head -3 || warn "API 测试失败 (可能需要安装 App)"

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     ✅ Termux 优化完成！                         ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "📋 下一步:"
echo "  1. 安装 Termux:Boot App (开机自启)"
echo "  2. 安装 Termux:API App (API 功能)"
echo "  3. 授予所有权限"
echo "  4. 重启手机测试"
echo ""
echo "🔗 下载链接:"
echo "  F-Droid: https://f-droid.org/"
echo "  Play Store: 搜索 Termux"
echo ""
