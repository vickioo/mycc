#!/bin/bash
# 本地 CC ↔ CC 服务器 任务同步脚本

REMOTE="CC:/data/mycc/shared-tasks/"
LOCAL="/root/air/qwq/shared-tasks"

echo "=== 任务同步 ==="
echo "本地：$LOCAL"
echo "远程：$REMOTE"

# 本地 → 远程 (inbox)
echo "上传 inbox..."
scp $LOCAL/inbox/*.json CC:/data/mycc/shared-tasks/inbox/ 2>/dev/null

# 远程 → 本地 (completed)
echo "下载 completed..."
scp CC:/data/mycc/shared-tasks/completed/*.json $LOCAL/completed/ 2>/dev/null

echo "同步完成"
