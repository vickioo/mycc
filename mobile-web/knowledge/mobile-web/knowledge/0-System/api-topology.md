# Qwen Code API 调用拓扑与配置

**日期**: 2026-03-05  
**状态**: ✅ 已验证 (free-claude-code 运行在 8082 端口)

---

## 🗺️ API 调用拓扑图

```
┌──────────────────────────────────────────────────────────────┐
│                   Qwen Code (我)                              │
│                                                               │
│  工作目录：/root/air/qwq                                     │
│  日志：~/.qwen/tmp/*/logs.json                               │
│  配置：~/.qwen/settings.local.json                           │
│  环境变量：~/.bashrc                                         │
└──────────────────────────────────────────────────────────────┘
                            │
                            │ Anthropic API Protocol
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│              环境变量配置                                     │
│                                                               │
│  ANTHROPIC_API_KEY=sk-ant-api03-localproxy-*                 │
│  CLAUDE_BASE_URL=http://localhost:8082                       │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│           free-claude-code Proxy (端口 8082/8083)            │
│                                                               │
│  位置：/root/free-claude-code/                               │
│  配置：/root/free-claude-code/.env                           │
│  功能：Anthropic API → 多模型路由                            │
│  状态：✅ 运行中 (端口 8082)                         │
└──────────────────────────────────────────────────────────────┘
                            │
                            │ Provider Priority
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                  模型路由优先级                               │
│                                                               │
│  1️⃣ 联通云 Antigravity API                                   │
│     URL: http://192.168.100.228:8045/v1                      │
│     Key: nvapi-AbUHOllo...                                   │
│     Model: claude-3-5-sonnet-20241022                        │
│                                                               │
│  2️⃣ NVIDIA NIM                                               │
│     Key: nvapi-hEi5o_2h3k8n...                               │
│                                                               │
│  3️⃣ OpenRouter                                               │
│     Key: sk-or-v1-ce74519b...                                │
│                                                               │
│  4️⃣ SiliconFlow                                              │
│     Key: sk-xataxbjlof...                                    │
│                                                               │
│  5️⃣ Zhipu (Fallback)                                         │
│     Key: 868d2bef5ff44911...                                 │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    实际 AI 模型                                │
│                                                               │
│  ✅ Claude 3.5 Sonnet (联通云)                               │
│  ✅ Claude 3 Opus                                             │
│  ✅ Claude 3 Haiku                                            │
│  ✅ 其他 Provider 模型                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| **Qwen Code 项目配置** | `/root/air/qwq/.qwen/settings.local.json` | 权限、Hooks、自动批准 |
| **Qwen Code 全局配置** | `/root/.qwen/settings.json` | 模型选择、安全设置 |
| **环境变量** | `/root/.bashrc` | ANTHROPIC_API_KEY, CLAUDE_BASE_URL |
| **Proxy 配置** | `/root/free-claude-code/.env` | 多 Provider 配置 |
| **用量日志** | `/root/.qwen/tmp/*/logs.json` | 会话日志 |

---

## 🔑 关键配置详解

### 1. Qwen Code 项目配置

```json
// /root/air/qwq/.qwen/settings.local.json
{
  "permissions": {
    "allow": ["WebSearch", "WebFetch", "Read", "Edit", "Write", ...],
    "deny": ["Bash(rm -rf /*)", ...]
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "echo '<current-time>' && date '+%Y-%m-%d %H:%M %A' ..."
      }
    ]
  },
  "autoApprove": {
    "fileEdits": true,
    "toolUse": true,
    "bashCommands": true
  }
}
```

### 2. 环境变量

```bash
# ~/.bashrc
export CLAUDE_BASE_URL="http://localhost:8082"
export ANTHROPIC_API_KEY="sk-ant-api03-localproxy-0000000000000000000000000000000000000000000000"
```

### 3. free-claude-code Proxy

```bash
# /root/free-claude-code/.env

# 联通云 Antigravity API (Priority 1)
UNICLOUD_API_KEY="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"
UNICLOUD_BASE_URL="http://192.168.100.228:8045/v1"

# NVIDIA NIM (Priority 2)
NVIDIA_NIM_API_KEY="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"

# OpenRouter (Priority 3)
OPENROUTER_API_KEY="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"

# 默认模型
MODEL="unicloud/claude-3-5-sonnet-20241022"
```

---

## 📊 用量统计说明

### 当前限制

| 问题 | 说明 |
|------|------|
| **日志无 token 数据** | Qwen Code 日志只记录消息内容，不记录 API 响应的 usage |
| **模型标识不准确** | 日志显示 `qwen-code`，实际调用 Claude |
| **费用估算偏差** | 使用字符数估算，非实际 token |

### 解决方案

**方案 1: 从 free-claude-code 获取数据** (推荐)

```bash
# 查看 free-claude-code 日志
pm2 logs free-claude-code --lines 100

# 或添加用量记录 hook
```

**方案 2: 从联通云 One-API 获取**

```bash
# CC 服务器 One-API 统计
ssh CC "curl -s http://localhost:3000/api/billing"
```

**方案 3: 增强 Qwen Code 日志**

修改配置记录 API 响应：
```json
{
  "hooks": {
    "AssistantResponse": [
      {
        "command": "echo '{\"usage\": $USAGE}' >> ~/.qwen/usage.jsonl"
      }
    ]
  }
}
```

---

## 🔧 服务状态检查

```bash
# 检查 PM2 服务
pm2 list

# 检查 free-claude-code
pm2 logs free-claude-code --lines 20

# 测试 API 连通性
curl -X POST http://localhost:8082/v1/messages \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-5-sonnet","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'

# 重启 Proxy
pm2 restart free-claude-code
```

---

## 💰 API 价格参考

### Claude (Anthropic)

| 模型 | Input | Output |
|------|-------|--------|
| Claude 3.5 Sonnet | $3/M | $15/M |
| Claude 3 Opus | $15/M | $75/M |
| Claude 3 Haiku | $0.8/M | $4/M |

### Qwen (阿里云)

| 模型 | Input | Output |
|------|-------|--------|
| Qwen-Max | $0.04/M | $0.12/M |
| Qwen-Plus | $0.01/M | $0.03/M |
| Qwen-Turbo | $0.002/M | $0.006/M |

---

## 📋 快速命令

```bash
# 查看 Qwen Code 用量 (估算)
python3 /root/air/qwq/.qwen/skills/qwq-usage/scripts/analyzer.py --days 7

# 查看 free-claude-code 日志
pm2 logs free-claude-code --lines 50

# 重启 Proxy
pm2 restart free-claude-code

# 检查 CC 服务器 One-API
ssh CC "docker logs oneapi --tail 20"
```

---

## ⚠️ 注意事项

1. **free-claude-code 状态**: PM2 显示 `waiting...` 可能需要重启
2. **联通云优先级**: 默认使用联通云 Claude，失败后降级
3. **日志准确性**: Qwen Code 日志不包含实际 token 使用量
4. **费用估算**: 当前 qwq-usage 使用估算值，仅供参考
