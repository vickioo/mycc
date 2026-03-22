# 钉钉机器人配置状态总结

## 📊 当前配置状态

### ✅ 已配置：Webhook 单向通知

**用途**: 接收 5 分钟汇报、告警通知

**配置**:
```bash
# /root/air/mycc/.env
DINGTALK_WEBHOOK_PRIMARY="https://oapi.dingtalk.com/robot/send?access_token=71bcdde..."
DINGTALK_SECRET_PRIMARY="SECcc86e370f..."

DINGTALK_WEBHOOK_SECONDARY="https://oapi.dingtalk.com/robot/send?access_token=ae8d3ab..."
DINGTALK_SECRET_SECONDARY="SEC5a0e24964..."
```

**状态**:
- 备用通道 ✅ 正常工作
- 主通道 ⚠️ 签名不匹配（需重新生成密钥）

**测试命令**:
```bash
node /root/air/qwq/scripts/dingtalk-notify.js "测试" "内容" info
```

---

### ❌ 未配置：WebSocket 双向机器人

**用途**: 接收用户消息、双向对话、命令交互

**所需配置** (未实现):
```bash
DINGTALK_APP_KEY="your_app_key"
DINGTALK_APP_SECRET="your_app_secret"
DINGTALK_ROBOT_CODE="your_robot_code"
```

**历史讨论**:
- 与 Gemini 讨论过使用 **钉钉 Stream 模式**（免内网穿透）
- 计划在 `free-claude-code` 项目中添加 `messaging/platforms/dingtalk.py`
- 需要安装 `dingtalk-stream` Python SDK

---

## 🔧 两种模式对比

| 特性 | Webhook (已配置) | WebSocket/Stream (未配置) |
|------|-----------------|--------------------------|
| **方向** | 单向（服务器→钉钉） | 双向（可收发消息） |
| **配置难度** | 简单 | 中等 |
| **内网穿透** | 不需要 | Stream 模式不需要 |
| **实时对话** | ❌ | ✅ |
| **命令交互** | ❌ | ✅ |
| **适用场景** | 通知、告警 | 聊天机器人、任务控制 |

---

## 📋 如需配置 WebSocket 双向机器人

### 方案 A：钉钉 Stream 模式（推荐）

**优点**: 无需公网 IP，无需内网穿透

**步骤**:
1. 访问 https://open.dingtalk.com/document/
2. 创建企业内部机器人
3. 获取 `AppKey`, `AppSecret`, `RobotCode`
4. 安装 SDK: `pip install dingtalk-stream`
5. 在 `free-claude-code` 项目中添加钉钉通道

### 方案 B：Webhook 接收模式

**优点**: 简单直接

**缺点**: 需要公网 IP 或内网穿透

**步骤**:
1. 配置内网穿透（ngrok/cpolar）
2. 在钉钉后台设置回调 URL
3. 在 `api/routes.py` 添加接收接口

---

## 🎯 当前能力

✅ **可以做的**:
- 每 5 分钟发送进度汇报到钉钉群
- 服务异常时发送告警通知
- 发送 Markdown 格式消息

❌ **暂时不能做的**:
- 在钉钉群里发消息给 AI
- 通过钉钉控制任务
- 双向对话

---

## 📝 下一步建议

如果只需要**接收通知**，当前配置已足够使用。

如果需要**双向对话**，可以：
1. 使用已有的 **Telegram 机器人**（已配置）
2. 或配置钉钉 WebSocket 机器人（需要额外开发）

**Telegram 配置** (已可用):
```bash
TELEGRAM_BOT_TOKEN="8592183023:AAHyzlp6OKYb432b9tBDouJYbOuq7qYJuEU"
TELEGRAM_CHAT_ID="7669193471"
```

---

## 🔍 相关位置

| 文件 | 用途 |
|------|------|
| `/root/air/mycc/.env` | 钉钉 Webhook 配置 |
| `/root/air/qwq/scripts/dingtalk-notify.js` | 钉钉通知脚本 |
| `/root/air/qwq/scripts/5min-report.sh` | 5 分钟汇报（已集成钉钉） |
| `/root/air/mycc/.claude/skills/tell-me/send.js` | 原有多通道通知脚本 |
