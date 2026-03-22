#\!/bin/bash
# 简易任务调度器 - 检查 inbox 并处理
INBOX="/data/mycc/shared-tasks/inbox"
PROCESSING="/data/mycc/shared-tasks/processing"
COMPLETED="/data/mycc/shared-tasks/completed"
LOG="/data/mycc/shared-tasks/scheduler.log"

while true; do
    for task in $INBOX/*.json; do
        [ -f "$task" ] || continue
        filename=$(basename "$task")
        id=${filename%.json}
        
        # 移动到 processing
        mv "$task" "$PROCESSING/"
        echo "$(date): 开始处理任务 $id" | tee -a $LOG
        
        # 这里可以添加任务处理逻辑
        # 目前只是记录日志
        
        # 移动到 completed
        mv "$PROCESSING/$filename" "$COMPLETED/"
        echo "$(date): 完成任务 $id" | tee -a $LOG
    done
    sleep 30  # 每30秒检查一次
done
