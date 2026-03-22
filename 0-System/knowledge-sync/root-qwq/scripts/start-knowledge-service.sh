#!/bin/bash
#
# 知识库网页版一键启动脚本
# 用途：启动知识库服务，支持本地访问
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PORT=8772
PROJECT_DIR="/root/air/qwq/mobile-web"

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
info() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] 警告:${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] 错误:${NC} $1"; }

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     📚 知识库网页版服务                         ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 1. 检查是否已有服务运行
log "检查服务状态..."
if curl -s http://localhost:$PORT/kb > /dev/null 2>&1; then
    info "✅ 知识库服务已在端口 $PORT 运行"
    echo ""
    echo "访问地址:"
    echo "  📚 知识库索引：http://localhost:$PORT/kb"
    echo "  📱 移动端主页：http://localhost:$PORT/"
    echo ""
    exit 0
fi

# 2. 生成最新索引
log "生成知识库索引..."
python3 /root/air/qwq/scripts/generate-knowledge-index.py

# 3. 启动服务
log "启动知识库服务 (端口 $PORT)..."
cd "$PROJECT_DIR"

# 先停止旧服务
pkill -9 -f "uvicorn.*$PORT" 2>/dev/null || true
sleep 2

# 使用 nohup 后台运行
nohup uvicorn app:app --host 0.0.0.0 --port $PORT > /tmp/knowledge-service.log 2>&1 &
PID=$!

# 4. 等待启动
sleep 3

# 5. 验证
if curl -s http://localhost:$PORT/kb > /dev/null 2>&1; then
    echo ""
    echo "╔════════════════════════════════════════════════╗"
    echo "║     ✅ 服务启动成功！                          ║"
    echo "╚════════════════════════════════════════════════╝"
    echo ""
    echo "📍 服务信息:"
    echo "  PID: $PID"
    echo "  端口：$PORT"
    echo ""
    echo "🌐 访问地址:"
    echo "  📚 知识库索引：http://localhost:$PORT/kb"
    echo "  📱 移动端主页：http://localhost:$PORT/"
    echo "  💻 局域网访问：http://$(hostname -I | awk '{print $1}'):$PORT/kb"
    echo ""
    echo "📋 管理命令:"
    echo "  查看日志：tail -f /tmp/knowledge-service.log"
    echo "  停止服务：pkill -f 'uvicorn.*$PORT'"
    echo "  重启服务：$0"
    echo ""
else
    error "服务启动失败，查看日志："
    cat /tmp/knowledge-service.log
    exit 1
fi
