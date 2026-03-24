#!/bin/bash
# ============================================================================
# Victory Agent 通信系统
# ============================================================================

LOG_FILE="/home/vicki/air/mycc/assets/logs/agent_comm_$(date +%Y-%m-%d).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ============================================================================
# 发送消息到 1052Bot
# ============================================================================
send_to_1052bot() {
    local message="$1"
    log "发送消息到 1052Bot: ${message:0:50}..."

    result=$(powershell.exe -c "
        \$body = @{
            message = '$message'
            receive_id = 'oc_bfec000013f21b6e810166f00533f18f'
        } | ConvertTo-Json

        try {
            \$resp = Invoke-RestMethod -Uri 'http://localhost:10053/api/feishu/send' -Method POST -Body \$body -ContentType 'application/json' -UseBasicParsing
            \$resp | ConvertTo-Json
        } catch {
            Write-Output '{\"success\": false}'
        }
    " 2>/dev/null)

    echo "$result" | grep -q '"success":true' && log "✓ 消息发送成功" || log "✗ 消息发送失败"
}

# ============================================================================
# 获取 1052Bot 状态
# ============================================================================
get_1052bot_status() {
    log "检查 1052Bot 状态..."

    result=$(powershell.exe -c "
        try {
            \$resp = Invoke-RestMethod -Uri 'http://localhost:10053/api/agent/info' -Method GET -UseBasicParsing
            \$resp | ConvertTo-Json
        } catch {
            Write-Output '{\"error\": \"failed\"}'
        }
    " 2>/dev/null)

    if echo "$result" | grep -q "agent_name"; then
        log "✓ 1052Bot 在线"
    else
        log "✗ 1052Bot 离线"
    fi
}

# ============================================================================
# 获取 AIHub 状态
# ============================================================================
get_aihub_status() {
    if lsof -i :9000 2>/dev/null | grep -q LISTEN; then
        log "✓ AIHub 运行中"
    else
        log "✗ AIHub 未运行"
    fi
}

# ============================================================================
# 定期报告
# ============================================================================
periodic_report() {
    log "=========================================="
    log "Victory Agent 状态报告 - $(date '+%Y-%m-%d %H:%M')"
    log "=========================================="
    get_1052bot_status
    get_aihub_status
    log "=========================================="
}

main() {
    local command="${1:-report}"
    case "$command" in
        "report") periodic_report ;;
        "status") get_1052bot_status; get_aihub_status ;;
        "send") send_to_1052bot "${2:-测试消息}" ;;
        *) echo "用法: $0 {report|status|send <msg>}" ;;
    esac
}

main "$@"
