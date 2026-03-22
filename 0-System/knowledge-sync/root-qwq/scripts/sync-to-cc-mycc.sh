#!/bin/bash
# qwq (local) → CC 服务器 mycc 同步脚本
# 用于将本地任务同步到 CC 服务器的中台项目

set -e

QWQ="/root/air/qwq"
CC_HOST="CC"
CC_MYCC="/data/mycc"
REMOTE_SYNC_DIR="$CC_MYCC/shared-tasks-qwq"

echo "=== qwq → CC 服务器 mycc 同步 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"

# 测试 SSH 连接
echo -n "测试 SSH 连接... "
if ssh -o ConnectTimeout=5 -o BatchMode=yes $CC_HOST "echo OK" >/dev/null 2>&1; then
    echo "✅ 成功"
else
    echo "❌ 失败 - 请检查 SSH 连接和 fail2ban"
    exit 1
fi

# 创建远程目录
echo "创建远程目录..."
ssh $CC_HOST "mkdir -p $REMOTE_SYNC_DIR/inbox $REMOTE_SYNC_DIR/processing $REMOTE_SYNC_DIR/completed"

# 同步 inbox 任务
echo "同步 inbox 任务..."
rsync -avz --delete "$QWQ/shared-tasks/inbox/" "$CC_HOST:$REMOTE_SYNC_DIR/inbox/"

# 同步 processing 任务
echo "同步 processing 任务..."
rsync -avz --delete "$QWQ/shared-tasks/processing/" "$CC_HOST:$REMOTE_SYNC_DIR/processing/"

# 同步 completed 任务 (仅元数据)
echo "同步 completed 任务..."
rsync -avz --delete "$QWQ/shared-tasks/completed/" "$CC_HOST:$REMOTE_SYNC_DIR/completed/"

# 同步 V9 开发文档
echo "同步 V9 开发文档..."
rsync -avz "$QWQ/tasks/v9-*.md" "$CC_HOST:$REMOTE_SYNC_DIR/" 2>/dev/null || true

echo ""
echo "=== 同步完成 ==="
echo "远程目录：$CC_HOST:$REMOTE_SYNC_DIR"
ssh $CC_HOST "ls -la $REMOTE_SYNC_DIR/"
