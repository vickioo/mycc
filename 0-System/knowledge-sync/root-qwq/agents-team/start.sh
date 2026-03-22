#!/bin/bash
# Agents Team 启动脚本

LOG_DIR="/root/air/qwq/agents-team/logs"
cd /root/air/qwq/agents-team

echo "╔════════════════════════════════════════════════╗"
echo "║     Agents Team 启动                           ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 启动本地 Worker
echo "🚀 启动本地 Worker..."
nohup python3 workers/worker.py worker-local local > $LOG_DIR/worker-local.log 2>&1 &
echo "   ✅ worker-local (PID: $!)"

# 启动 CC Worker
echo "🚀 启动 CC Worker..."
nohup python3 workers/worker.py worker-cc cc > $LOG_DIR/worker-cc.log 2>&1 &
echo "   ✅ worker-cc (PID: $!)"

# 启动 Termux Worker
echo "🚀 启动 Termux Worker..."
nohup python3 workers/worker.py worker-termux termux > $LOG_DIR/worker-termux.log 2>&1 &
echo "   ✅ worker-termux (PID: $!)"

# 启动调度器 (每分钟)
echo "⏰ 启动调度器..."
(crontab -l 2>/dev/null | grep -v "scheduler.py"; echo "*/1 * * * * cd /root/air/qwq/agents-team && python3 scheduler/scheduler.py >> $LOG_DIR/scheduler.log 2>&1") | crontab -
echo "   ✅ 调度器已添加到 crontab"

# 启动监控器 (每 5 分钟)
echo "📊 启动监控器..."
(crontab -l 2>/dev/null | grep -v "monitor.py"; echo "*/5 * * * * cd /root/air/qwq/agents-team && python3 monitor/monitor.py >> $LOG_DIR/monitor.log 2>&1") | crontab -
echo "   ✅ 监控器已添加到 crontab"

echo ""
echo "✅ Agents Team 启动完成"
echo ""
echo "查看状态：python3 monitor/monitor.py"
echo "查看日志：tail -f $LOG_DIR/*.log"
