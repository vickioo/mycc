#!/bin/bash
#
# migrate-to-termux.sh - 将 sv 服务迁移到 Termux
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] 警告:${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] 错误:${NC} $1"; }

TERMUX_HOME="/data/data/com.termux/files/home"
TERMUX_SSH="$TERMUX_HOME/.ssh"
TERMUX_SV="$TERMUX_HOME/.local/sv"
TERMUX_BIN="$TERMUX_HOME/bin"

echo "╔════════════════════════════════════════════════╗"
echo "║     Termux 服务迁移脚本                        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查是否在 U22 运行
if [ "$(whoami)" != "root" ]; then
    error "此脚本必须在 U22 中以 root 身份运行"
    exit 1
fi

# 检查 Termux 数据目录
if [ ! -d "$TERMUX_HOME" ]; then
    error "Termux 数据目录不存在：$TERMUX_HOME"
    exit 1
fi

log "步骤 1/5: 检查 Termux 是否安装 openssh..."
if [ ! -f "$TERMUX_HOME/../usr/bin/ssh" ]; then
    warn "Termux 可能未安装 openssh"
    echo "请在 Termux 中执行：pkg install openssh"
fi

log "步骤 2/5: 创建 Termux SSH 目录..."
mkdir -p "$TERMUX_SSH"
chmod 700 "$TERMUX_SSH"

log "步骤 3/5: 复制 SSH 配置和密钥..."
cp /root/.ssh/config "$TERMUX_SSH/" 2>/dev/null && log "  ✓ SSH config"
cp /root/.ssh/id_ed25519_vi "$TERMUX_SSH/id_ed25519" 2>/dev/null && log "  ✓ SSH key"
cp /root/.ssh/id_ed25519_vi.pub "$TERMUX_SSH/id_ed25519.pub" 2>/dev/null
chmod 600 "$TERMUX_SSH/config" "$TERMUX_SSH/id_ed25519" 2>/dev/null
chmod 644 "$TERMUX_SSH/id_ed25519.pub" 2>/dev/null

log "步骤 4/5: 创建 Termux sv 目录..."
mkdir -p "$TERMUX_SV/ssh-gate/log" "$TERMUX_SV/watchdog/log" "$TERMUX_BIN"

log "步骤 5/5: 创建 Termux ssh-gate 服务..."
cat > "$TERMUX_SV/ssh-gate/run" << 'EOFGATE'
#!/data/data/com.termux/files/usr/bin/bash
SVC_NAME="ssh-gate"
PIDFILE="/data/data/com.termux/files/usr/tmp/$SVC_NAME.pid"
LOGFILE="$HOME/.local/sv/$SVC_NAME/log/current"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }

check_running() {
    [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null
}

start() {
    if check_running; then
        log "⚠️ 服务已在运行"
        return 0
    fi
    
    log "▶️ 启动 ssh-gate..."
    pkill -f "ssh -N.*gate" 2>/dev/null || true
    
    ssh -N \
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
    
    if kill -0 $! 2>/dev/null; then
        log "✅ 服务已启动 (PID: $!)"
        return 0
    else
        log "❌ 服务启动失败"
        rm -f "$PIDFILE"
        return 1
    fi
}

stop() {
    if ! check_running; then
        log "⚠️ 服务未运行"
        return 0
    fi
    PID=$(cat "$PIDFILE")
    log "⏹️ 停止服务 (PID: $PID)..."
    kill "$PID" 2>/dev/null
    rm -f "$PIDFILE"
    log "✅ 服务已停止"
}

restart() { stop; sleep 1; start; }
status() { check_running && echo "✅ 运行中" || echo "❌ 未运行"; }
health() { check_running && echo "healthy" || echo "unhealthy"; }

case "${1:-start}" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    health) health ;;
    *) echo "用法：$0 {start|stop|restart|status|health}"; exit 1 ;;
esac
EOFGATE
chmod +x "$TERMUX_SV/ssh-gate/run"
log "  ✓ ssh-gate/run"

log "创建 Termux sv 命令..."
cat > "$TERMUX_BIN/sv" << 'EOFCSV'
#!/data/data/com.termux/files/usr/bin/bash
SV_BASE="$HOME/.local/sv"

cmd_status() {
    echo "╔════════════════════════════════════════╗"
    echo "║         服务状态 (Termux)              ║"
    echo "╚════════════════════════════════════════╝"
    for dir in "$SV_BASE"/*/; do
        [ -x "$dir/run" ] && echo -n "  $(basename "$dir"): " && "$dir/run" status
    done
}

cmd_start() {
    [ -x "$SV_BASE/$1/run" ] && "$SV_BASE/$1/run" start || echo "❌ 服务不存在：$1"
}

cmd_stop() {
    [ -x "$SV_BASE/$1/run" ] && "$SV_BASE/$1/run" stop || echo "❌ 服务不存在：$1"
}

cmd_restart() {
    [ -x "$SV_BASE/$1/run" ] && "$SV_BASE/$1/run" restart || echo "❌ 服务不存在：$1"
}

case "${1:-status}" in
    start|stop|restart|status) "cmd_$1" "${2:-}" ;;
    *) echo "用法：sv {start|stop|restart|status} [service]"; exit 1 ;;
esac
EOFCSV
chmod +x "$TERMUX_BIN/sv"
log "  ✓ sv command"

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     迁移完成！                                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "下一步操作:"
echo "1. 在 Termux 中执行：sv start ssh-gate"
echo "2. 验证连接：ssh CC \"echo OK\""
echo "3. 配置 Termux 保活机制 (Tasker 或 Termux:Boot)"
echo ""
echo "U22 配置调整:"
echo "编辑 ~/.ssh/config，将 gate 改为 localhost:2222"
echo ""
