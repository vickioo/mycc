---
name: dingtalk
description: 钉钉机器人（Stream 模式）。支持双向对话和群通知。触发词："/dingtalk"、"钉钉通知"、"钉钉机器人"、"启动钉钉"
---

# DingTalk - 钉钉 Stream 机器人

通过钉钉 Stream 协议实现双向交互机器人，支持群通知和对话。无需公网 IP。

## 触发词

- "/dingtalk"
- "钉钉通知"
- "钉钉机器人"
- "启动钉钉"

## 功能

### 1. 群通知（类似 tell-me）

总结当前对话要点并发送到钉钉群。

```bash
node .claude/skills/dingtalk/scripts/notify.js "标题" "内容"
```

### 2. Stream 机器人（双向对话）

启动后台 Stream 机器人，在钉钉群里 @机器人 发消息，机器人会调用 Claude Code 处理并回复。

```bash
node .claude/skills/dingtalk/scripts/bot.js
```

## 执行步骤

### 发通知时
1. 总结对话要点（3-5 句话）
2. 运行 `node .claude/skills/dingtalk/scripts/notify.js "标题" "内容"`

### 启动机器人时
1. 运行 `node .claude/skills/dingtalk/scripts/bot.js`（后台运行）
2. 在钉钉群 @机器人 即可对话

## 配置

凭证存放在 `.claude/skills/dingtalk/scripts/config.json`，包含：
- `clientId`: 钉钉应用 AppKey
- `clientSecret`: 钉钉应用 AppSecret
