#!/bin/bash
# Agent 任务路由器

TASK_FILE="$1"
TARGET="${2:-cc}"  # cc, sjll, local

case $TARGET in
  cc)
    echo "路由到 CC 服务器..."
    scp "$TASK_FILE" CC:/data/mycc/shared-tasks/inbox/
    ;;
  sjll)
    echo "路由到 SJLL 龙虾..."
    scp "$TASK_FILE" sjll-agent:~/.openclaw/tasks/inbox/
    ;;
  local)
    echo "路由到本地 mycc..."
    cp "$TASK_FILE" /root/air/mycc/shared-tasks-qwq/inbox/
    ;;
esac
