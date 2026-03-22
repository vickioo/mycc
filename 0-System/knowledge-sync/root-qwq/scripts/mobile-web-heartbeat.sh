#!/bin/bash
# Mobile-Web 三方协作心跳机制 - 带反思学习
# 每 5 分钟检查一次进度，每 5 次心跳触发反思

HEARTBEAT_LOG="/tmp/mobile-web-heartbeat.log"
TASKS_FILE="/root/air/qwq/shared-tasks/mobile-web-todo.md"
COLLAB_FILE="/root/air/qwq/mobile-web/COLLABORATION.md"
EVOLVE_MEMORY="/root/air/qwq/QWEN-EVOLVING-MEMORY.md"
COUNTER_FILE="/tmp/heartbeat-counter.txt"
REFLECTION_INTERVAL=5  # 每 N 次心跳触发反思

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$HEARTBEAT_LOG"
}

# 读取/初始化心跳计数
get_heartbeat_count() {
    if [ -f "$COUNTER_FILE" ]; then
        cat "$COUNTER_FILE"
    else
        echo "0"
    fi
}

# 增加心跳计数
increment_heartbeat() {
    local count=$(get_heartbeat_count)
    count=$((count + 1))
    echo "$count" > "$COUNTER_FILE"
    echo "$count"
}

# 触发反思
trigger_reflection() {
    log "🤔 触发反思学习..."
    
    local reflection_file="/root/air/qwq/3-Thinking/evolution/reflection-$(date +%Y%m%d-%H%M).md"
    
    cat > "$reflection_file" << REFLECTION
# 心跳反思 - $(date '+%Y-%m-%d %H:%M')

## 心跳计数：$1

## 状态检查
- mycc: $(check_mycc_status && echo "在线" || echo "离线")
- CC-Server: $(check_cc_server_status && echo "在线" || echo "离线")
- mobile-web: $(check_mobile_web_service && echo "运行中" || echo "未运行")

## 反思问题
1. 过去 25 分钟有什么进展？
2. 遇到了什么阻碍？
3. 下一步应该如何调整？

## 行动项
- [ ] 
- [ ] 
- [ ]

---
*自动触发 - 等待 AI 填写*
REFLECTION

    log "  反思文件已创建：$reflection_file"
    
    # 更新进化记忆
    cat >> "$EVOLVE_MEMORY" << MEMORY

---
## $(date '+%Y-%m-%d %H:%M') - 心跳反思 #$1

**状态**:
- mycc: $(check_mycc_status && echo "在线" || echo "离线")
- CC-Server: $(check_cc_server_status && echo "在线" || echo "离线")

**进展**: 待 AI 分析

**待办**: 待 AI 更新
MEMORY

    log "  进化记忆已更新"
}

check_mycc_status() {
    if [ -d "/root/air/mycc/.claude" ]; then
        return 0
    else
        return 1
    fi
}

check_cc_server_status() {
    if ssh -o ConnectTimeout=3 -o BatchMode=yes CC "echo OK" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

check_mobile_web_service() {
    if curl -s http://localhost:8766/api/health 2>/dev/null | grep -q "ok"; then
        return 0
    else
        return 1
    fi
}

sync_tasks() {
    if [ -d "/root/air/mycc/shared-tasks" ]; then
        cp "$TASKS_FILE" /root/air/mycc/shared-tasks/mobile-web-todo.md 2>/dev/null
        log "📋 任务同步到 mycc"
    fi
}

# 主循环
log "╔════════════════════════════════════════════╗"
log "║   Mobile-Web 心跳监控启动                  ║"
log "╚════════════════════════════════════════════╝"

check_mycc_status && log "✅ mycc: 在线" || log "❌ mycc: 离线"
check_cc_server_status && log "✅ CC-Server: 在线" || log "⚠️  CC-Server: 暂时离线"
check_mobile_web_service && log "✅ mobile-web 服务：运行中" || log "⚠️  mobile-web 服务：未运行"
sync_tasks

# 心跳计数和反思触发
COUNT=$(increment_heartbeat)
log "💓 心跳次数：$COUNT"

if [ $((COUNT % REFLECTION_INTERVAL)) -eq 0 ]; then
    trigger_reflection $COUNT
fi

log "💓 心跳正常 - 持续监控中..."
