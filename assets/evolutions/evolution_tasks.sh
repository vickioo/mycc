#!/bin/bash
# ============================================================================
# Victory 自进化任务系统
# ============================================================================

TASK_DIR="/home/vicki/air/mycc/assets/evolutions"
LOG_DIR="/home/vicki/air/mycc/assets/logs"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
LOG_FILE="$LOG_DIR/evolution_$DATE.log"

mkdir -p "$TASK_DIR" "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ============================================================================
# 任务 1: 整理记忆
# ============================================================================
evolve_memory() {
    log "=== 开始记忆整理 ==="

    MEMORY_FILE="/home/vicki/air/mycc/memory/MEMORY.md"

    # 更新短期记忆
    cat > /tmp/short_term.md << EOF

## 今日快照

**日期**: $DATE

**今天做了什么**:
- 1052Bot 后端 + 前端部署完成
- 飞书发送通道测试成功
- Victory 架构文档创建
- 自进化任务系统搭建

**待办**:
- 测试 Feishu WebSocket 接收
- 配置 ACP 协议
- 启用 Agent 间通信

EOF

    # 合并到记忆文件
    if [ -f "$MEMORY_FILE" ]; then
        # 保留文件的前半部分（模板）和新内容
        head -20 "$MEMORY_FILE" > /tmp/memory_head.md
        cat /tmp/memory_head.md /tmp/short_term.md > "$MEMORY_FILE"
    fi

    log "记忆整理完成"
}

# ============================================================================
# 任务 2: 检查服务状态
# ============================================================================
check_services() {
    log "=== 检查服务状态 ==="

    SERVICES=(
        "1052Bot:10053"
        "AIHub:9000"
        "CLIProxyAPI:8317"
    )

    for svc in "${SERVICES[@]}"; do
        IFS=':' read -r name port <<< "$svc"
        if powershell.exe -c "netstat -ano | Select-String ':$port'" 2>/dev/null | grep -q LISTEN; then
            log "✓ $name 运行中 (端口 $port)"
        else
            log "✗ $name 未运行 (端口 $port)"
        fi
    done
}

# ============================================================================
# 任务 3: 记录今日进展
# ============================================================================
log_progress() {
    log "=== 记录今日进展 ==="

    PROGRESS_FILE="$TASK_DIR/progress_$DATE.md"

    cat > "$PROGRESS_FILE" << EOF
# $DATE 进展记录

## 时间
$TIME

## 完成事项
1. 1052Bot 部署完成
2. 飞书通道测试成功
3. Victory 架构文档创建

## 下一步
1. 测试 Feishu WebSocket
2. 配置 ACP
3. 启用 Agent 通信

## 踩坑记录
- WSL2 网络隔离问题: Windows 端口无法从 WSL 直接访问
- 解决方案: 使用 PowerShell 或 Windows 本地命令

EOF

    log "进展已记录到 $PROGRESS_FILE"
}

# ============================================================================
# 任务 4: Git 提交（如果有变化）
# ============================================================================
auto_commit() {
    log "=== 检查 Git 变更 ==="

    cd /home/vicki/air/mycc

    # 检查是否有变更
    if git diff --quiet && git diff --cached --quiet; then
        log "没有变更，跳过提交"
        return
    fi

    # 添加变更
    git add -A

    # 创建提交
    git commit -m "[EVOLVE] $(date +%Y-%m-%d) 自进化 - $DATE $TIME

- 记忆同步更新
- 架构文档维护
- 服务状态检查

Co-Authored-By: Vicki-Linux Claude <noreply@victory.local>" 2>/dev/null

    if [ $? -eq 0 ]; then
        log "Git 提交成功"
    else
        log "Git 提交失败或没有变更"
    fi
}

# ============================================================================
# 主流程
# ============================================================================
main() {
    log "=========================================="
    log "Victory 自进化任务开始 - $DATE $TIME"
    log "=========================================="

    evolve_memory
    check_services
    log_progress
    auto_commit

    log "=========================================="
    log "Victory 自进化任务完成"
    log "=========================================="
}

main "$@"
