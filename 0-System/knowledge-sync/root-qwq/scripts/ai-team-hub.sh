#!/bin/bash
#
# AI Team Hub 服务守护脚本
# 用途：自动检测并重启服务，防止意外退出
#

SERVICE_NAME="ai-team-hub"
PORT=8772
PROJECT_DIR="/root/air/qwq/mobile-web"
LOG_FILE="/tmp/ai-team-hub.log"
PID_FILE="/tmp/ai-team-hub.pid"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_service() {
    if curl -s http://localhost:$PORT/api/health > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

start_service() {
    log "${GREEN}启动 AI Team Hub 服务...${NC}"
    cd "$PROJECT_DIR"
    nohup uvicorn app:app --host 0.0.0.0 --port $PORT > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 3
    
    if check_service; then
        log "${GREEN}✅ 服务启动成功 (PID: $(cat $PID_FILE))${NC}"
        return 0
    else
        log "${RED}❌ 服务启动失败${NC}"
        return 1
    fi
}

stop_service() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        log "${YELLOW}停止服务 (PID: $PID)...${NC}"
        kill "$PID" 2>/dev/null
        rm -f "$PID_FILE"
        sleep 2
        log "${GREEN}服务已停止${NC}"
    fi
}

restart_service() {
    stop_service
    sleep 2
    start_service
}

# 主循环
log "╔════════════════════════════════════════════════╗"
log "║     AI Team Hub 服务守护进程启动                ║"
log "╚════════════════════════════════════════════════╝"

# 初始检查
if check_service; then
    log "${GREEN}✅ 服务已在运行${NC}"
else
    log "${YELLOW}⚠️ 服务未运行，启动中...${NC}"
    start_service
fi

# 持续监控 (每 30 秒检查一次)
while true; do
    sleep 30
    
    if ! check_service; then
        log "${RED}❌ 服务异常，尝试重启...${NC}"
        
        # 清理旧进程
        pkill -f "uvicorn.*$PORT" 2>/dev/null
        sleep 2
        
        # 重启服务
        start_service
        
        if [ $? -ne 0 ]; then
            log "${RED}❌ 重启失败，5 秒后重试...${NC}"
            sleep 5
        fi
    fi
done
