#!/bin/bash
# 明早通知 Surface AI - 发送任务并配语音
# 执行时间：明早 08:00

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/surface-notify.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "╔════════════════════════════════════════════╗"
log "║   通知 Surface AI - 明早汇报任务            ║"
log "╚════════════════════════════════════════════╝"

# 创建共享任务文件
SHARED_DIR="/root/air/mycc/0-System/agents/shared-tasks/inbox"
DATE=$(date +%Y%m%d)
TASK_FILE="${SHARED_DIR}/${DATE}-surface-morning-report.md"

mkdir -p "$SHARED_DIR"

cat > "$TASK_FILE" << 'TASK'
# 🌅 明早汇报任务

**优先级**: P1
**执行时间**: 08:00
**创建者**: Qwen 监控系统

## 任务内容

1. ✅ 发送早安消息到钉钉群
2. ✅ 配上语音播报（TTS）
3. ✅ 包含夜间运行统计
4. ✅ 今日计划建议

## 语音播报内容建议

```
早上好！我是 Surface AI 助手。现在是北京时间早上 8 点。

系统昨夜运行正常，累计运行 X 小时。

今天建议您关注以下事项：
- 检查监控系统运行状态
- 查看夜间日志有无异常
- 根据需要启动/停止服务

祝您今天工作顺利！
```

## 钉钉消息格式

```markdown
## 🌅 早安 · [日期]

**当前时间**: [时间]

### 📊 夜间运行统计
- 运行时长：X 小时 Y 分钟
- 心跳次数：N 次

### 🔍 服务状态
- mobile-web: [状态]
- CC Clash Tunnel: [状态]
- PM2 进程：N 个在线

### 📋 今日计划建议
1. 检查监控系统运行状态
2. 查看夜间日志有无异常
3. 根据需要启动/停止服务

---
*自动汇报 · Surface AI*
```

---
*此任务由 Qwen 监控系统自动创建*
TASK

log "✅ 共享任务已创建：$TASK_FILE"

# 发送到钉钉群（通知 Surface AI）
DINGTALK_CONTENT="## 📢 任务分配给 千问 (Surface)

**执行时间**: 立即
**任务**: 明早 08:00 汇报

请查看共享任务文件：
\`/root/air/mycc/0-System/agents/shared-tasks/inbox/${DATE}-surface-morning-report.md\`

**要求**:
• 发送早安消息到钉钉群
• 配上语音播报 (TTS)
• 包含夜间运行统计
• 今日计划建议

收到请回复。✅"

# 使用备用通道发送（主通道签名有问题）
WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=ae8d3ab29108edf4f52747f604400a24b7b20a0a32d21e4291f5d8e1d24a3e2e"
SECRET="SEC5a0e24964ca88a4f57d543c6885864f6d337c4eade89dea9724196a76585cdae"

# 生成签名
TIMESTAMP=$(date +%s)
STRING_TO_SIGN="${TIMESTAMP}\n${SECRET}"
SIGN=$(echo -en "$STRING_TO_SIGN" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64 | urlencode)

URL="${WEBHOOK}&timestamp=${TIMESTAMP}&sign=${SIGN}"

# 发送钉钉消息
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"msgtype\": \"markdown\",
    \"markdown\": {
      \"title\": \"📋 任务分配\",
      \"text\": \"${DINGTALK_CONTENT//\"/\\\"}\"\n\n> 🕐 $(date '+%Y-%m-%d %H:%M:%S')\"
    }
  }" > /dev/null

log "✅ 钉钉通知已发送"

# 同时发送到 Telegram（如果 Surface 也监听）
TELEGRAM_TOKEN="8592183023:AAHyzlp6OKYb432b9tBDouJYbOuq7qYJuEU"
TELEGRAM_CHAT_ID="7669193471"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{
    \"chat_id\": \"${TELEGRAM_CHAT_ID}\",
    \"text\": \"🔔 <b>Surface AI 任务提醒</b>\n\n明早 08:00 发送汇报消息，请准备语音播报。\n\n任务文件：${TASK_FILE}\",
    \"parse_mode\": \"HTML\"
  }" > /dev/null

log "✅ Telegram 通知已发送"
log ""
log "✅ Surface AI 通知完成 - 明早 08:00 执行汇报"
