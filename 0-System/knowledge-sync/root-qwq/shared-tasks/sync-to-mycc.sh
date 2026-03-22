#!/bin/bash
# qwq → mycc 同步脚本

QWQ="/root/air/qwq"
MYCC="/root/air/mycc"

echo "=== qwq → mycc 同步 ==="

# 同步状态文件
cp $QWQ/0-System/status.md $MYCC/0-System/agents/qwq/status.md

# 同步完成任务
cp $QWQ/shared-tasks/completed/*.json $MYCC/shared-tasks-qwq/completed/ 2>/dev/null

# 同步 inbox 任务
cp $QWQ/shared-tasks/inbox/*.json $MYCC/shared-tasks-qwq/inbox/ 2>/dev/null

echo "同步完成"
