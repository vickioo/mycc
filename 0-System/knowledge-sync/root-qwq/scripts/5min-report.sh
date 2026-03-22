#!/bin/bash
# 每 5 分钟进度汇报 - 增强版
# 支持前台/后台/静默模式

set -u

REPORT_LOG="/tmp/5min-report.log"
NOTIFICATION_MODE="${NOTIFICATION_MODE:-auto}"  # auto, foreground, background, silent

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$REPORT_LOG"
}

# 发送钉钉通知
send_dingtalk() {
    local title="$1"
    local message="$2"
    local level="${3:-info}"
    
    # 使用 Node.js 钉钉通知脚本
    if [ -f "/root/air/qwq/scripts/dingtalk-notify.js" ]; then
        node /root/air/qwq/scripts/dingtalk-notify.js "$title" "$message" "$level" 2>/dev/null
    fi
}

# 发送通知
send_notification() {
    local title="$1"
    local message="$2"
    
    case "$NOTIFICATION_MODE" in
        "silent")
            # 静默模式，只写日志
            log "[NOTIFY] $title: $message"
            ;;
        "dingtalk"|"dingtalk-only")
            # 仅钉钉通知
            send_dingtalk "$title" "$message"
            log "[NOTIFY] $title: $message"
            ;;
        "foreground"|"background")
            # Termux 通知 + 钉钉
            if command -v termux-notification >/dev/null 2>&1; then
                termux-notification \
                    --title "$title" \
                    --content "$message" \
                    --id "5min-report" \
                    2>/dev/null || true
            fi
            send_dingtalk "$title" "$message"
            log "[NOTIFY] $title: $message"
            ;;
        "auto")
            # 自动检测：默认使用钉钉
            send_dingtalk "$title" "$message"
            log "[NOTIFY] $title: $message"
            ;;
    esac
}

# 获取心跳计数
get_heartbeat_count() {
    cat /tmp/heartbeat-counter.txt 2>/dev/null || echo "0"
}

# 检查服务状态
check_services() {
    local status="✅"
    local issues=""

    # mobile-web
    if ! curl -s --connect-timeout 2 http://localhost:8766/api/health 2>/dev/null | grep -q "ok"; then
        status="❌"
        issues="${issues}mobile-web 异常; "
    fi

    # mycc
    if [ ! -d "/root/air/mycc/.claude" ]; then
        status="⚠️"
        issues="${issues}mycc 未配置; "
    fi

    # CC-Server
    if ! ssh -o ConnectTimeout=3 -o BatchMode=yes CC "echo OK" 2>/dev/null; then
        status="⚠️"
        issues="${issues}CC-Server 离线; "
    fi

    # CC Clash Tunnel
    if ! curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
        status="⚠️"
        issues="${issues}Clash Tunnel 异常; "
    fi

    echo "$status|$issues"
}

# 生成汇报
generate_report() {
    local count=$(get_heartbeat_count)
    local services_result=$(check_services)
    local status="${services_result%%|*}"
    local issues="${services_result#*|}"
    local next_reflection=$((10 - (count % 10)))
    local timestamp=$(date '+%Y-%m-%d %H:%M')

    local report=$(cat << REPORT

╔═══════════════════════════════════════════════════════════╗
║  📋 5 分钟进度汇报 #${count}                                   ║
╠═══════════════════════════════════════════════════════════╣
║  时间：${timestamp}
║  状态：${status}
║  下次反思：心跳 #${count} + ${next_reflection} (约${next_reflection} 分钟后)
╚═══════════════════════════════════════════════════════════╝

📊 运行统计
  累计运行：$((count * 5)) 分钟
  反思触发：$((count / 5)) 次

$(if [ -n "$issues" ] && [ "$issues" != "" ]; then
    echo "⚠️  问题检测:"
    echo "$issues" | tr ';' '\n' | while read -r issue; do
        [ -n "$issue" ] && echo "  - $issue"
    done
else
    echo "✅ 所有服务运行正常"
fi)
REPORT
)

    echo "$report"
    echo "$report" >> "$REPORT_LOG"
    
    # 发送通知
    if [ "$status" = "❌" ]; then
        send_notification "⚠️ 服务异常" "$issues"
    elif [ $((count % 10)) -eq 0 ]; then
        send_notification "📋 5 分钟汇报 #${count}" "运行正常，累计$((count * 5))分钟"
    fi
}

# 主流程
main() {
    log "╔════════════════════════════════════════════╗"
    log "║   5 分钟汇报生成                            ║"
    log "╚════════════════════════════════════════════╝"
    
    generate_report
}

# 支持多种运行模式
case "${1:-report}" in
    "report")
        main
        ;;
    "daemon")
        # 守护模式，每 5 分钟运行一次
        while true; do
            main
            sleep 300
        done
        ;;
    "check")
        # 仅检查服务状态
        check_services
        ;;
    *)
        echo "Usage: $0 {report|daemon|check}"
        exit 1
        ;;
esac
