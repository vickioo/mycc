# AI 工具技能与通知系统调用手册

**日期**: 2026-03-16
**状态**: ✅ 已归档

---

## 一、本地 AI 工具技能总览

### 1. Claude Code (mycc)

**配置文件**: `/root/air/mycc/`
**后端服务**: free-claude-code (PM2, 端口 8082)

**技能列表**:

| 技能 | 功能 | 触发词 |
|------|------|--------|
| cc-audit | token 审计 + 超过阈值报警 | `/cc-audit`、`安全审计`、`token 报警` |
| cc-usage | token 用量统计（按日期×模型） | `/cc-usage`、`看看用量`、`token 消耗` |
| collect | 多源每日情报采集 → 飞书简报 | `/collect`、`每日采集`、`早报` |
| dashboard | 能力看板可视化 | `/dashboard`、`看看能力看板` |
| desktop | macOS 桌面操控（OCR + 鼠标控制） | `/desktop`、`帮我操作桌面` |
| mycc | 网页版后端服务 | `/mycc`、`启动 mycc` |
| read-gzh | 微信公众号文章读取总结 | `/read-gzh`、`读一下这篇公众号` |
| tell-me | 飞书通知全平台 | `/tell-me`、`通知我`、`飞书通知` |
| termux-notify | 手机端弹窗 + 语音提醒 | `/notify`、`弹窗提醒`、`手机通知` |
| skill-creator | 创建新 Skill 工具 | `帮我创建一个 skill` |
| scheduler | 定时任务系统 | `/scheduler`、`定时任务` |

### 2. Qwen (通义千问)

**配置文件**: `/root/.qwen/`、`/root/air/qwq/`
**PM2 服务**: 5min-report (已停止)

**技能列表**:

| 技能 | 功能 | 触发词 |
|------|------|--------|
| qwq-usage | token 用量统计 | `/qwq-usage`、`看看用量` |
| inject-context | 会话上下文注入 | `/inject-context`、`load context` |

**脚本工具**:

| 脚本 | 功能 |
|------|------|
| `/root/air/qwq/scripts/5min-report.sh` | 5分钟定时进度汇报 → 钉钉 |
| `/root/air/qwq/scripts/morning-report.sh` | 每日早报 |
| `/root/air/qwq/scripts/notify-surface.js` | Surface 手机钉钉推送 |

### 3. Gemini CLI (茜茜)

**配置文件**: `/root/.gemini/`
**特殊**: 与 Claude 共享长期记忆

**技能**: (无额外 skill)

### 4. Codex (OpenAI)

**配置文件**: `/root/.codex/`
**PM2 服务**: cc-clash-tunnel、cc-clash-watchdog (已停止)
**功能**: 提供 Claude → OpenAI API 代理

---

## 二、通知系统调用方式

### 1. 钉钉通知

```bash
# 基本调用
node /root/air/qwq/scripts/dingtalk-notify.js "标题" "内容" "info|warning|error"

# 示例
node /root/air/qwq/scripts/dingtalk-notify.js "测试通知" "来自 Claude 的消息" "info"
```

**配置位置**: `/root/air/mycc/.env`
- 主机器人: DINGTALK_WEBHOOK_PRIMARY + DINGTALK_SECRET_PRIMARY
- 备用机器人: DINGTALK_WEBHOOK_SECONDARY + DINGTALK_SECRET_SECONDARY

### 2. Termux 手机通知 (弹窗 + 语音)

**连接方式**: SSH 127.0.0.1:8022

```bash
# 弹窗通知
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-notification --title '标题' --content '内容'"

# 语音播报
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-tts-speak '语音内容'"

# 调音量 + 播报 (最大音量)
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-volume music 100; termux-tts-speak '语音内容'"

# 组合: 弹窗 + 语音
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-notification --title '标题' --content '内容' && termux-tts-speak '语音内容'"
```

### 3. 飞书通知

**触发方式**: 使用 tell-me skill
- 触发词: `/tell-me`、`通知我`、`飞书通知`

---

## 三、PM2 服务状态

| 服务 | 状态 | 端口 | 说明 |
|------|------|------|------|
| free-claude-code | ✅ online | 8082 | Claude Code 后端 |
| mobile-hub | ✅ online | 8080 | 手机网页服务 |
| team-gateway | ✅ online | - | 团队网关 |
| cc-clash-tunnel | ⏸ stopped | - | Codex 代理 (手动停止) |
| cc-clash-watchdog | ⏸ stopped | - | Codex 看门狗 (手动停止) |
| 5min-report | ⏹ stopped | - | Qwen 定时汇报 |

---

## 四、快速调用模板

### 发送钉钉通知
```bash
node /root/air/qwq/scripts/dingtalk-notify.js "【CC通知】" "内容" "info"
```

### 发送 Termux 手机弹窗
```bash
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-notification -t 'CC通知' -c '内容'"
```

### 发送 Termux 语音播报 (最大音量)
```bash
ssh -o StrictHostKeyChecking=no -p 8022 root@127.0.0.1 "termux-volume music 100; termux-tts-speak '来自 CC 的语音播报：内容'"
```

---

## 五、相关文档

- [全局 AI 拓扑](./global-ai-topology.md)
- [API 拓扑](./api-topology.md)
- [Termux 架构](./termux-architecture.md)
- [系统健康报告](./system-health-report.md)