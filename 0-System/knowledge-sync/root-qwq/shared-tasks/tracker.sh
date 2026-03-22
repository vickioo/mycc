#!/bin/bash
# 任务状态追踪器

echo "╔════════════════════════════════════════╗"
echo "║       Task Status Tracker              ║"
echo "╚════════════════════════════════════════╝"
echo ""

# qwq tasks
echo "📁 qwq tasks:"
echo -n "  Inbox: "; ls /root/air/qwq/shared-tasks/inbox/*.json 2>/dev/null | wc -l
echo -n "  Completed: "; ls /root/air/qwq/shared-tasks/completed/*.json 2>/dev/null | wc -l

# CC server tasks
echo ""
echo "📁 CC Server tasks:"
INBOX=$(ssh -o BatchMode=yes CC "ls /data/mycc/shared-tasks/inbox/*.json 2>/dev/null | wc -l" 2>/dev/null || echo "0")
COMPLETED=$(ssh -o BatchMode=yes CC "ls /data/mycc/shared-tasks/completed/*.json 2>/dev/null | wc -l" 2>/dev/null || echo "0")
echo "  Inbox: $INBOX"
echo "  Completed: $COMPLETED"

# sjll tasks
echo ""
echo "📁 SJLL tasks:"
echo "  (requires tunnel refresh)"

echo ""
echo "════════════════════════════════════════"
