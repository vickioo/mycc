#!/bin/bash
# cc-switch 自动轮替守护脚本

SCRIPT_PATH="/data/mycc/.claude/skills/cc-switch/scripts/auto_switcher.py"
LOG_FILE="/var/log/cc-switch-auto.log"
PID_FILE="/var/run/cc-switch-auto.pid"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "cc-switch 自动轮替已在运行 (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "启动 cc-switch 自动轮替..."
    nohup python3 "$SCRIPT_PATH" --monitor >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "cc-switch 自动轮替已启动 (PID: $(cat $PID_FILE))"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "停止 cc-switch 自动轮替 (PID: $PID)..."
            kill "$PID"
            rm -f "$PID_FILE"
            echo "cc-switch 自动轮替已停止"
        else
            echo "cc-switch 自动轮替未运行"
            rm -f "$PID_FILE"
        fi
    else
        echo "cc-switch 自动轮替未运行"
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "cc-switch 自动轮替正在运行 (PID: $PID)"
            echo "日志文件: $LOG_FILE"
            echo "最近日志:"
            tail -10 "$LOG_FILE"
        else
            echo "cc-switch 自动轮替进程文件存在但进程未运行"
            rm -f "$PID_FILE"
        fi
    else
        echo "cc-switch 自动轮替未运行"
    fi
}

restart() {
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0