#!/system/bin/sh
#
# termux-setup.sh - 在 Termux 中执行此脚本
# 用法：在 Termux 中运行 bash ~/air/qwq/0-System/termux-setup.sh
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
echo "║     Termux SSH 服务设置脚本                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查是否在 Termux 中运行
if [ -z "$PREFIX" ]; then
    error "此脚本必须在 Termux 中运行"
    echo "请在 Termux 应用中执行此脚本"
    exit 1
fi

log "步骤 1/4: 安装 openssh..."
pkg install openssh -y 2>/dev/null || warn "openssh 可能已安装"

log "步骤 2/4: 配置 SSH..."
mkdir -p $HOME/.ssh
chmod 700 $HOME/.ssh

# 复制配置 (如果 U22 共享目录可访问)
if [ -f "/root/.ssh/config" ]; then
    cp /root/.ssh/config $HOME/.ssh/ 2>/dev/null || true
fi
if [ -f "/root/.ssh/id_ed25519_vi" ]; then
    cp /root/.ssh/id_ed25519_vi $HOME/.ssh/id_ed25519 2>/dev/null || true
    cp /root/.ssh/id_ed25519_vi.pub $HOME/.ssh/id_ed25519.pub 2>/dev/null || true
    chmod 600 $HOME/.ssh/id_ed25519 2>/dev/null || true
fi

log "步骤 3/4: 创建 sv 服务目录..."
mkdir -p $HOME/.local/sv/ssh-gate/log $HOME/.local/sv/watchdog/log $HOME/bin

log "步骤 4/4: 创建服务脚本..."

# ssh-gate 服务
cat > $HOME/.local/sv/ssh-gate/run << 'EOFGATE'
#!/data/data/com.termux/files/usr/bin/bash
SVC_NAME="ssh-gate"
PIDFILE="$PREFIX/tmp/$SVC_NAME.pid"
LOGFILE="$HOME/.local/sv/$SVC_NAME/log/current"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }
check_running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
check_health() { check_running || return 1; timeout 2 bash -c "echo > /dev/tcp/localhost/8045" 2>/dev/null || return 1; return 0; }

start() {
    check_running && { log "⚠️ 已在运行"; return 0; }
    log "▶️ 启动 ssh-gate..."
    # 先停止旧的 SSH 隧道 (如果有)
    pkill -f "ssh -N.*gate" 2>/dev/null || true
    sleep 1
    # 使用 setsid 启动，避免被父进程杀死
    setsid ssh -N \
        -L 3390:database.local:13193 \
        -L 3391:sj-liuliang.local:3389 \
        -L 3394:ECS-C6-2XLARGE-.local:23389 \
        -L 3395:dbx.local:3389 \
        -L 3396:AmPosERP.local:3389 \
        -L 8006:192.168.100.222:8006 \
        -L 8045:127.0.0.1:8045 \
        -L 8821:sj-liuliang.local:22 \
        -o ServerAliveInterval=15 \
        -o ServerAliveCountMax=2 \
        -o ExitOnForwardFailure=yes \
        -o TCPKeepAlive=yes \
        -o ClearAllForwardings=yes \
        gate >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 2
    kill -0 $! 2>/dev/null && { log "✅ 已启动 (PID: $!)"; return 0; }
    log "❌ 启动失败"
    rm -f "$PIDFILE"
    return 1
}
stop() {
    check_running || { log "⚠️ 未运行"; return 0; }
    PID=$(cat "$PIDFILE")
    log "⏹️ 停止 (PID: $PID)..."
    kill "$PID" 2>/dev/null; rm -f "$PIDFILE"
    log "✅ 已停止"
}
restart() { stop; sleep 1; start; }
status() { check_running && echo "✅ 运行中" || echo "❌ 未运行"; }
health() { check_health && echo "healthy" || echo "unhealthy"; }

case "${1:-start}" in
    start) start ;; stop) stop ;; restart) restart ;; status) status ;; health) health ;;
    *) echo "用法：$0 {start|stop|restart|status|health}"; exit 1 ;;
esac
EOFGATE
chmod +x $HOME/.local/sv/ssh-gate/run

# watchdog 服务
cat > $HOME/.local/sv/watchdog/run << 'EOFWD'
#!/data/data/com.termux/files/usr/bin/bash
SVC_NAME="watchdog"
PIDFILE="$PREFIX/tmp/$SVC_NAME.pid"
LOGFILE="$HOME/.local/sv/$SVC_NAME/log/current"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }
check_running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
start() {
    check_running && { log "⚠️ 已在运行"; return 0; }
    log "▶️ 启动 watchdog..."
    nohup bash -c 'while true; do $HOME/.local/sv/ssh-gate/run health | grep -q healthy || $HOME/.local/sv/ssh-gate/run restart; sleep 30; done' >> "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 1; kill -0 $! 2>/dev/null && { log "✅ 已启动"; return 0; }
    log "❌ 启动失败"
    rm -f "$PIDFILE"
    return 1
}
stop() { check_running || return 0; kill "$(cat "$PIDFILE")" 2>/dev/null; rm -f "$PIDFILE"; log "✅ 已停止"; }
restart() { stop; sleep 1; start; }
status() { check_running && echo "✅ 运行中" || echo "❌ 未运行"; }

case "${1:-start}" in
    start) start ;; stop) stop ;; restart) restart ;; status) status ;;
    *) echo "用法：$0 {start|stop|restart|status}"; exit 1 ;;
esac
EOFWD
chmod +x $HOME/.local/sv/watchdog/run

# sv 命令
cat > $HOME/bin/sv << 'EOFSV'
#!/data/data/com.termux/files/usr/bin/bash
SV_BASE="$HOME/.local/sv"
[ -z "$1" ] && { echo "用法：sv {start|stop|restart|status|log} [service]"; exit 1; }
[ -x "$SV_BASE/$2/run" ] && "$SV_BASE/$2/run" "$1" || { [ -z "$2" ] && { for d in $SV_BASE/*/; do [ -x "$d/run" ] && "$(basename "$d")/run" "$1"; done; } || echo "❌ 服务不存在：$2"; exit 1; }
EOFSV
chmod +x $HOME/bin/sv

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     设置完成！                                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "启动服务:"
echo "  sv start ssh-gate    # 启动端口转发"
echo "  sv start watchdog    # 启动健康检查"
echo "  sv status            # 查看状态"
echo ""
echo "验证连接:"
echo "  ssh CC \"echo OK\""
echo ""
