#!/bin/bash
# Crash-Resistant Wrapper - 防止异常退出的包装器
# 用于保护关键进程，捕获异常并自动重启

set -u

LOG_FILE="${LOG_FILE:-/tmp/crash-wrapper.log}"
RESTART_DELAY="${RESTART_DELAY:-3}"
MAX_RESTARTS="${MAX_RESTARTS:-5}"
RESTART_WINDOW="${RESTART_WINDOW:-60}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 重启计数
declare -a restart_times=()

check_restart_limit() {
    local now=$(date +%s)
    local window_start=$((now - RESTART_WINDOW))
    
    # 清理旧的 restart 记录
    restart_times=($(printf '%s\n' "${restart_times[@]}" 2>/dev/null | while read t; do
        [ "$t" -ge "$window_start" ] && echo "$t"
    done))
    
    if [ ${#restart_times[@]} -ge $MAX_RESTARTS ]; then
        return 1  # 超过限制
    fi
    
    restart_times+=("$now")
    return 0
}

# 捕获退出信号
exit_handler() {
    local exit_code=$?
    log "⚠️  进程异常退出 (code: $exit_code)"
    
    if check_restart_limit; then
        log "🔄 ${RESTART_DELAY}秒后重启... (重启次数：${#restart_times[@]}/$MAX_RESTARTS)"
        sleep $RESTART_DELAY
        exec "$@"  # 重新执行
    else
        log "❌ 重启次数过多，停止重启"
        exit $exit_code
    fi
}

trap 'exit_handler "$@"' EXIT

# 执行命令
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [args...]"
    exit 1
fi

log "🚀 启动受保护进程：$*"
exec "$@"
