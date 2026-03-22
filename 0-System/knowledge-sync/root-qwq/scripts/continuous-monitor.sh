#!/bin/bash
# Continuous Monitor with Watchdog - 持续监控和看门狗
# 防止进程异常退出，自动恢复

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/tmp/qwq-monitor"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/monitor.log"
PID_FILE="$LOG_DIR/monitor.pid"
HEARTBEAT_FILE="/tmp/heartbeat-counter.txt"
LAST_REPORT_FILE="$LOG_DIR/last-report.txt"

# 初始化
init() {
    > "$LOG_FILE"
    echo $$ > "$PID_FILE"
    [ ! -f "$HEARTBEAT_FILE" ] && echo "0" > "$HEARTBEAT_FILE"
    log "🚀 监控系统启动 (PID: $$)"
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 捕获信号，优雅退出
cleanup() {
    log "⚠️  收到退出信号，清理中..."
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup SIGTERM SIGINT SIGHUP

# 检查关键进程
check_critical_processes() {
    local issues=()
    
    # 检查 mobile-web
    if ! curl -s --connect-timeout 2 http://localhost:8766/api/health 2>/dev/null | grep -q "ok"; then
        issues+=("mobile-web 服务异常")
    fi
    
    # 检查 CC Clash Tunnel
    if ! curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
        issues+=("CC Clash Tunnel 异常")
    fi
    
    # 检查 PM2 服务
    if ! pm2 list >/dev/null 2>&1; then
        issues+=("PM2 服务异常")
    fi
    
    # 返回问题列表
    printf '%s\n' "${issues[@]}"
}

# 恢复服务
recover_service() {
    local service="$1"
    log "🔄 尝试恢复服务：$service"
    
    case "$service" in
        "mobile-web")
            # 检查是否在 mycc 目录
            if [ -d "/root/air/mycc" ]; then
                cd /root/air/mycc && pm2 restart mobile-web 2>/dev/null || \
                pm2 start npm --name mobile-web -- start 2>/dev/null
            fi
            ;;
        "CC Clash Tunnel")
            /root/cc-clash-tunnel.sh restart
            ;;
        "PM2")
            pm2 resurrect 2>/dev/null || pm2 save
            ;;
    esac
    
    sleep 2
    
    # 验证恢复
    if check_critical_processes | grep -q "$service"; then
        log "❌ 恢复失败：$service"
        return 1
    else
        log "✅ 恢复成功：$service"
        return 0
    fi
}

# 生成 5 分钟汇报
generate_report() {
    local count=$(cat "$HEARTBEAT_FILE" 2>/dev/null || echo "0")
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local next_reflection=$((10 - (count % 10)))
    
    # 获取问题列表
    local issues=$(check_critical_processes)
    local status="✅"
    [ -n "$issues" ] && status="⚠️"
    
    cat << REPORT

╔═══════════════════════════════════════════════════════════╗
║  📋 5 分钟进度汇报 #${count}                                   ║
╠═══════════════════════════════════════════════════════════╣
║  时间：${timestamp}
║  状态：${status}
║  下次反思：心跳 #${count} + ${next_reflection} (约${next_reflection} 分钟后)
╚═══════════════════════════════════════════════════════════╝

🔍 服务检查
$(if [ -n "$issues" ]; then
    echo "$issues" | while read -r issue; do
        echo "  ❌ $issue"
    done
else
    echo "  ✅ 所有服务正常"
fi)

📊 运行统计
  累计运行：$((count * 5)) 分钟
  反思触发：$((count / 5)) 次
  最后报告：$timestamp

REPORT

    echo "$timestamp" > "$LAST_REPORT_FILE"
}

# 主循环
main_loop() {
    local interval=600  # 5 分钟
    local check_interval=30  # 30 秒检查一次
    local last_report=$(date +%s)
    
    while true; do
        # 增加心跳计数
        local count=$(($(cat "$HEARTBEAT_FILE" 2>/dev/null || echo "0") + 1))
        echo "$count" > "$HEARTBEAT_FILE"
        
        # 每 5 分钟生成报告
        local now=$(date +%s)
        if [ $((now - last_report)) -ge $interval ]; then
            generate_report
            last_report=$now
        fi
        
        # 检查并恢复服务
        local issues=$(check_critical_processes)
        if [ -n "$issues" ]; then
            log "⚠️  检测到问题:"
            echo "$issues" | while read -r issue; do
                log "  - $issue"
                # 尝试恢复
                recover_service "$issue" &
            done
        fi
        
        # 等待下次检查
        sleep $check_interval
    done
}

# 启动
init
main_loop
