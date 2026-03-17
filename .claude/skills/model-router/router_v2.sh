#!/bin/bash
# 智能模型路由系统 V2 - 指数退避 + 多供应商轮替

CONFIG_FILE="/root/air/mycc/.claude/skills/model-router/config.json"
LOG_FILE="/root/air/mycc/.claude/skills/model-router/router.log"

# 指数退避配置
MAX_RETRIES=5
BASE_DELAY=1  # 基础延迟 (秒)
MAX_DELAY=60  # 最大延迟 (秒)

# 模型配置 (多供应商)
declare -A MODELS=(
    # 高档
    ["claude-3-5-sonnet"]="unicloud/claude-3-5-sonnet-20241022|high|unicloud"
    ["claude-3-opus"]="unicloud/claude-3-opus|high|unicloud"
    ["qwen-max"]="unicloud/qwen-max|high|unicloud"
    
    # 中档
    ["claude-3-haiku"]="unicloud/claude-3-haiku|mid|unicloud"
    ["qwen-plus"]="unicloud/qwen-plus|mid|unicloud"
    ["glm-4-air"]="zhipu/glm-4-air|mid|zhipu"
    ["deepseek-v3"]="silicon_flow/deepseek-ai/DeepSeek-V3|mid|siliconflow"
    
    # 低档
    ["qwen-turbo"]="unicloud/qwen-turbo|low|unicloud"
    ["glm-flash"]="zhipu/glm-flash|low|zhipu"
    ["qwen2.5-7b"]="silicon_flow/Qwen/Qwen2.5-7B-Instruct|low|siliconflow"
)

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

# 指数退避函数
exponential_backoff() {
    local attempt=$1
    local delay=$((BASE_DELAY * (2 ** attempt)))
    
    # 限制最大延迟
    [ $delay -gt $MAX_DELAY ] && delay=$MAX_DELAY
    
    log "⏳ 等待 ${delay}s (第 $attempt 次重试)"
    sleep $delay
}

# 健康检查 (带重试)
health_check() {
    local model_path=$1
    local retry=0
    
    while [ $retry -lt $MAX_RETRIES ]; do
        log "💓 健康检查：$model_path (尝试 $((retry+1))/$MAX_RETRIES)"
        
        # 测试模型连通性
        local response=$(curl -s -w "%{http_code}" -o /dev/null \
            -X POST http://localhost:8082/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d "{\"model\":\"$model_path\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}" \
            --connect-timeout 5 --max-time 10)
        
        if [ "$response" = "200" ]; then
            log "✅ 健康检查通过：$model_path"
            return 0
        fi
        
        log "❌ 健康检查失败：$model_path (HTTP $response)"
        exponential_backoff $retry
        retry=$((retry + 1))
    done
    
    log "❌ 健康检查失败 (已达最大重试): $model_path"
    return 1
}

# 智能切换 (带指数退避)
switch_model() {
    local key=$1
    local info="${MODELS[$key]}"
    [ -z "$info" ] && { log "❌ 未知模型：$key"; return 1; }
    
    local path=$(echo $info | cut -d'|' -f1)
    local tier=$(echo $info | cut -d'|' -f2)
    
    log "🔄 切换：$key -> $path ($tier 档)"
    
    # 健康检查
    if ! health_check "$path"; then
        log "⚠️ 模型不可用，尝试下一个..."
        return 1
    fi
    
    # 执行切换
    if bash /root/air/mycc/.claude/skills/cc-switch/scripts/switch.sh "$path" 2>&1 | grep -q "SUCCESS"; then
        save_config "$key" "$tier"
        log "✅ 成功：$key"
        return 0
    fi
    
    log "❌ 失败：$key"
    return 1
}

# 供应商轮替 (带退避)
rotate_provider() {
    local tier=$1
    local providers=("unicloud" "zhipu" "siliconflow")
    
    for provider in "${providers[@]}"; do
        log "🔄 尝试供应商：$provider"
        
        for key in "${!MODELS[@]}"; do
            local info="${MODELS[$key]}"
            local model_tier=$(echo $info | cut -d'|' -f2)
            local model_provider=$(echo $info | cut -d'|' -f3)
            
            if [ "$model_tier" = "$tier" ] && [ "$model_provider" = "$provider" ]; then
                if switch_model "$key"; then
                    return 0
                fi
            fi
        done
    done
    
    return 1
}

get_current() {
    [ -f "$CONFIG_FILE" ] && python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('model', 'claude-3-haiku'))" || echo "claude-3-haiku"
}

save_config() {
    echo "{\"model\":\"$1\",\"tier\":\"$2\",\"updated\":\"$(date -Iseconds)\"}" > "$CONFIG_FILE"
}

switch_tier() {
    local tier=$1
    rotate_provider "$tier"
}

smart_route() {
    log "🧠 智能路由启动..."
    for tier in high mid low; do
        log "📊 尝试 $tier 档..."
        switch_tier "$tier" && { log "✅ 路由成功：$tier"; return 0; }
    done
    log "❌ 路由失败"
    return 1
}

auto_rotate() {
    log "🔄 自动轮替启动..."
    local current=$(get_current)
    for key in "${!MODELS[@]}"; do
        [ "$key" = "$current" ] && continue
        local info="${MODELS[$key]}"
        local tier=$(echo $info | cut -d'|' -f2)
        local curr_tier=$(echo "${MODELS[$current]}" | cut -d'|' -f2)
        [ "$tier" = "$curr_tier" ] && switch_model "$key" && { log "✅ 轮替成功：$key"; return 0; }
    done
    switch_model "$current"
    log "⚠️ 轮替失败，回退：$current"
    return 1
}

show_status() {
    echo "╔════════════════════════════════════════════════╗"
    echo "║     智能模型路由系统 V2                        ║"
    echo "╚════════════════════════════════════════════════╝"
    echo ""
    echo "当前：$(get_current)"
    echo "最大重试：$MAX_RETRIES"
    echo "退避策略：${BASE_DELAY}s -> ${MAX_DELAY}s"
    echo ""
    echo "高档：claude-3-5-sonnet, claude-3-opus, qwen-max"
    echo "中档：claude-3-haiku, qwen-plus, glm-4-air, deepseek-v3"
    echo "低档：qwen-turbo, glm-flash, qwen2.5-7b"
}

case "${1:-status}" in
    switch) switch_model "$2" ;;
    tier) switch_tier "$2" ;;
    route) smart_route ;;
    rotate) auto_rotate ;;
    status) show_status ;;
    *) echo "用法：$0 {switch|tier|route|rotate|status} [参数]" ;;
esac
