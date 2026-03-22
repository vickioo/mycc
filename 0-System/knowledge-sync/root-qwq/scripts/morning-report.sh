#!/bin/bash
# 明早汇报脚本 - Morning Report
# 发送夜间总结和当日展望到钉钉群

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_LOG="/tmp/morning-report.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$REPORT_LOG"
}

# 获取夜间运行统计
get_night_stats() {
    local heartbeat=$(cat /tmp/heartbeat-counter.txt 2>/dev/null || echo "0")
    local running_minutes=$((heartbeat * 5))
    local hours=$((running_minutes / 60))
    local mins=$((running_minutes % 60))
    
    echo "运行时长：${hours}小时${mins}分钟"
}

# 检查服务状态
check_services() {
    local issues=""
    
    # mobile-web
    if ! curl -s --connect-timeout 2 http://localhost:8766/api/health 2>/dev/null | grep -q "ok"; then
        issues="${issues}• mobile-web: 未运行\n"
    else
        issues="${issues}• mobile-web: ✅ 正常\n"
    fi
    
    # CC Clash Tunnel
    if ! curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
        issues="${issues}• CC Clash Tunnel: 未运行\n"
    else
        issues="${issues}• CC Clash Tunnel: ✅ 正常\n"
    fi
    
    # PM2
    local pm2_status=$(pm2 status 2>/dev/null | grep -c "online" || echo "0")
    issues="${issues}• PM2 进程：${pm2_status} 个在线\n"
    
    echo -e "$issues"
}

# 生成明早汇报
generate_morning_report() {
    local date=$(date '+%Y年%m月%d日 %A')
    local time=$(date '+%H:%M')
    local stats=$(get_night_stats)
    local services=$(check_services)
    
    cat << REPORT
## 🌅 早安 · ${date}

**当前时间**: ${time}

---

### 📊 夜间运行统计
${stats}

### 🔍 服务状态
${services}
### 📋 今日计划建议

1. 检查监控系统运行状态
2. 查看夜间日志有无异常
3. 根据需要启动/停止服务

---
*自动汇报 · Qwen 监控系统*
REPORT
}

# 发送钉钉通知
send_to_dingtalk() {
    local content="$1"
    
    if [ -f "/root/air/qwq/scripts/dingtalk-notify.js" ]; then
        node /root/air/qwq/scripts/dingtalk-notify.js "🌅 早安汇报" "$content" success
    fi
}

# 主流程
log "╔════════════════════════════════════════════╗"
log "║   明早汇报生成                              ║"
log "╚════════════════════════════════════════════╝"

REPORT=$(generate_morning_report)
echo "$REPORT"
echo ""

# 发送钉钉
send_to_dingtalk "$REPORT"

log "✅ 明早汇报已发送"
