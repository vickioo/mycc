#!/data/data/com.termux/files/usr/bin/bash
#
# Termux SSHD 自启动一键配置脚本
# 用法：在 Termux 中运行 bash ~/setup-sshd-autostart.sh
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     Termux SSHD 自启动配置脚本                 ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查是否在 Termux 中运行
if [ -z "$PREFIX" ]; then
    error "此脚本必须在 Termux 中运行"
    exit 1
fi

# 步骤 1: 检查 Termux:Boot
log "步骤 1/5: 检查 Termux:Boot..."
if [ -d "/data/data/com.termux.boot" ]; then
    success "Termux:Boot 已安装"
else
    warn "Termux:Boot 未安装"
    echo ""
    echo "请安装 Termux:Boot:"
    echo "  1. 打开 F-Droid 或 GitHub"
    echo "  2. 搜索 'Termux:Boot'"
    echo "  3. 安装应用"
    echo ""
    echo "F-Droid: https://f-droid.org/packages/com.termux.boot/"
    echo "GitHub:  https://github.com/termux/termux-boot/releases"
    echo ""
    read -p "安装完成后按回车继续..."
fi

# 步骤 2: 创建 boot 目录
log "步骤 2/5: 创建 boot 目录..."
mkdir -p ~/.termux/boot
success "目录已创建"

# 步骤 3: 生成主机密钥
log "步骤 3/5: 生成 SSH 主机密钥..."
if [ ! -d ~/.ssh/hostkeys ]; then
    mkdir -p ~/.ssh/hostkeys
    ssh-keygen -t rsa -f ~/.ssh/hostkeys/ssh_host_rsa_key -N '' -q
    ssh-keygen -t ed25519 -f ~/.ssh/hostkeys/ssh_host_ed25519_key -N '' -q
    success "主机密钥已生成"
else
    success "主机密钥已存在"
fi

# 步骤 4: 创建 boot 脚本
log "步骤 4/5: 创建启动脚本..."

cat > ~/.termux/boot/00-start-sshd.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Termux Boot: SSH 守护进程

sleep 10

# 停止旧的
pkill sshd 2>/dev/null || true

# 生成主机密钥
if [ ! -d ~/.ssh/hostkeys ]; then
    mkdir -p ~/.ssh/hostkeys
    ssh-keygen -t rsa -f ~/.ssh/hostkeys/ssh_host_rsa_key -N '' -q 2>/dev/null
    ssh-keygen -t ed25519 -f ~/.ssh/hostkeys/ssh_host_ed25519_key -N '' -q 2>/dev/null
fi

# 启动
sshd -p 8022 -h ~/.ssh/hostkeys

# 验证
sleep 2
if pgrep -f 'sshd.*8022' >/dev/null 2>&1; then
    echo '[sshd] ✅ 已启动'
else
    echo '[sshd] ❌ 失败'
fi
EOF
chmod +x ~/.termux/boot/00-start-sshd.sh
success "SSHD 启动脚本已创建"

# 创建 sv 服务启动脚本
if [ -d ~/.local/sv/ssh-gate ]; then
    cat > ~/.termux/boot/10-start-services.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Termux Boot: sv 服务

sleep 15

if [ -x ~/.local/sv/ssh-gate/run ]; then
    bash ~/.local/sv/ssh-gate/run start
fi
if [ -x ~/.local/sv/watchdog/run ]; then
    bash ~/.local/sv/watchdog/run start
fi

echo '[sv] 服务已启动'
EOF
    chmod +x ~/.termux/boot/10-start-services.sh
    success "SV 服务启动脚本已创建"
fi

# 步骤 5: 配置电池优化
log "步骤 5/5: 电池优化配置..."
echo ""
echo "请在 Android 设置中:"
echo "  1. 设置 → 应用 → Termux → 电池"
echo "  2. 选择 '无限制'"
echo ""
echo "这可以防止系统杀死后台进程"
echo ""

# 完成
echo "╔════════════════════════════════════════════════╗"
echo "║     配置完成！                                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "下一步操作:"
echo ""
echo "1. 安装 Termux:Boot (如未安装)"
echo "   https://f-droid.org/packages/com.termux.boot/"
echo ""
echo "2. 授予自启动权限"
echo "   设置 → 应用 → Termux:Boot → 权限"
echo ""
echo "3. 配置电池优化白名单"
echo "   设置 → 应用 → Termux → 电池 → 无限制"
echo ""
echo "4. 测试启动脚本"
echo "   ~/.termux/boot/00-start-sshd.sh"
echo ""
echo "5. 重启手机验证"
echo ""
echo "查看状态:"
echo "  ssh -p 8022 localhost 'pgrep -f sshd'"
echo ""
