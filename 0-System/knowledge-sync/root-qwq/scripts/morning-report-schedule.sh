#!/bin/bash
# 明早汇报 - Morning Report Scheduler
# 用法：bash morning-report.sh [时间]
# 默认：08:00 发送明早汇报

REPORT_TIME="${1:-08:00}"

echo "╔════════════════════════════════════════════╗"
echo "║   明早汇报已设置                            ║"
echo "╚════════════════════════════════════════════╝"
echo
echo "📅 汇报时间：明天 ${REPORT_TIME}"
echo "📍 通知渠道：钉钉群"
echo

# 创建定时任务
CRON_MINUTE=$(echo "$REPORT_TIME" | cut -d: -f2)
CRON_HOUR=$(echo "$REPORT_TIME" | cut -d: -f1)

# 添加到 crontab (如果不存在)
EXISTING_CRON=$(crontab -l 2>/dev/null | grep "morning-report" || true)
if [ -z "$EXISTING_CRON" ]; then
    (crontab -l 2>/dev/null | grep -v "morning-report"; echo "$CRON_MINUTE $CRON_HOUR * * * bash /root/air/qwq/scripts/morning-report.sh") | crontab -
    echo "✅ 定时任务已添加"
else
    echo "ℹ️  定时任务已存在"
fi

echo
echo "💡 取消命令：crontab -e  # 删除 morning-report 行"
