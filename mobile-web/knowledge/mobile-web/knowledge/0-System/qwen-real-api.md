# Qwen Code (千问) 真实 API 配置

**日期**: 2026-03-06  
**状态**: ✅ 已验证 - OAuth 授权模式

---

## 🔐 授权方式

**OAuth 2.0 邮箱账号授权**

```json
// /root/.qwen/oauth_creds.json
{
  "access_token": "f_uvz1sFlaRKKd-Ac8WTfYMA6IrnQWYG_XL07AsIuYsL-IVRiJndRmRQQpeaFXJz38F_gIMgxy3o65aqmwIlGw",
  "token_type": "Bearer",
  "refresh_token": "2TIToG2t7CZz0mZ27yHd_7Cg_7Oe_aayJ7tbOUhpIImUJQiWzY-BWY0BRLYlFFnK4BU2yefjLWDQ2eqhP7VomA",
  "resource_url": "portal.qwen.ai",
  "expiry_date": 1772773937105  // 2026-03-05 + 1 年
}
```

**授权服务器**: `https://portal.qwen.ai`

---

## 🗺️ API 调用拓扑图

```
┌─────────────────────────────────────────────────────────────┐
│                    用户 (vicki)                              │
│                                                              │
│  授权方式：邮箱注册 → OAuth 2.0 授权                          │
│  凭证位置：~/.qwen/oauth_creds.json                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ 授权完成
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Qwen Code CLI (千问代码助手)                     │
│                                                              │
│  安装位置：/usr/lib/node_modules/@qwen-code/qwen-code/      │
│  版本：0.11.1                                               │
│  工作目录：/root/air/qwq                                    │
│  日志：~/.qwen/projects/*/chats/*.jsonl                     │
│  配置：~/.qwen/settings.json                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API 调用
                            │ Access Token: f_uvz1sFlaRKKd...
                            │ Resource URL: portal.qwen.ai
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              阿里云 Qwen API (通义千问)                        │
│                                                              │
│  端点：https://portal.qwen.ai/api                           │
│  模型：coder-model (Qwen Code 专用)                          │
│  认证：OAuth 2.0 Bearer Token                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              通义千问大模型                                   │
│                                                              │
│  模型：Qwen 3.5 / Qwen Code                                 │
│  提供商：阿里云                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 关键文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| **OAuth 凭证** | `/root/.qwen/oauth_creds.json` | Access Token, Refresh Token |
| **安装 ID** | `/root/.qwen/installation_id` | `a48204e0-745a-481b-8ee9-167c915cc481` |
| **全局配置** | `/root/.qwen/settings.json` | 模型选择、安全设置 |
| **项目配置** | `/root/air/qwq/.qwen/settings.local.json` | 权限、Hooks |
| **会话日志** | `/root/.qwen/projects/*/chats/*.jsonl` | 完整对话记录 |
| **临时日志** | `/root/.qwen/tmp/*/logs.json` | 简化日志 |
| **TODO 记录** | `/root/.qwen/todos/*.json` | 任务追踪 |

---

## 🔑 认证流程

1. **首次授权**
   ```bash
   qwen-code --login
   # 打开浏览器 → 邮箱登录 → 授权 → 回调
   ```

2. **Token 使用**
   ```javascript
   // CLI 内部调用
   fetch('https://portal.qwen.ai/api/...', {
     headers: {
       'Authorization': `Bearer ${access_token}`,
       'Content-Type': 'application/json'
     }
   })
   ```

3. **Token 刷新**
   - Access Token 过期前自动刷新
   - 使用 Refresh Token 获取新 Access Token
   - 刷新失败需要重新登录

---

## 💬 模型信息

**当前使用模型**: `coder-model` (Qwen Code 专用)

| 属性 | 值 |
|------|-----|
| 模型 ID | `coder-model` |
| 实际模型 | Qwen 3.5 Code |
| 提供商 | 阿里云通义千问 |
| 上下文窗口 | 256K tokens |
| 训练数据 | 代码 + 技术文档 |

---

## 📊 真实用量统计

**截至 2026-03-06**:

```
TOTAL: 45.1M tokens (44.9M input + 235K output)
Cost: $0.00 (OAuth 免费额度)
Messages: 552
```

**查看用量**:
```bash
python3 /root/air/qwq/.qwen/skills/qwq-usage/scripts/analyzer.py --days 7
```

### 日志格式

```jsonl
// ~/.qwen/projects/*/chats/*.jsonl
{
  "uuid": "...",
  "sessionId": "24391b6d-510c-433c-a498-e48c39cf3521",
  "timestamp": "2026-03-05T23:12:42.905Z",
  "type": "assistant",
  "model": "coder-model",
  "message": {...},
  "usageMetadata": {
    "promptTokenCount": 181684,
    "candidatesTokenCount": 298,
    "thoughtsTokenCount": 44,
    "totalTokenCount": 181982,
    "cachedContentTokenCount": 0
  }
}
```

### 查看用量

```bash
# 查看当前会话用量
cat /root/.qwen/projects/-root-air-qwq/chats/*.jsonl | \
  grep -o '"totalTokenCount":[0-9]*' | \
  awk -F: '{sum+=$2} END {print "Total tokens:", sum}'

# 查看用量统计脚本
python3 /root/air/qwq/.qwen/skills/qwq-usage/scripts/analyzer.py --days 7
```

---

## 🔧 与 Claude Code (mycc) 的区别

| 特性 | Qwen Code (qwq) | Claude Code (mycc) |
|------|-----------------|-------------------|
| **授权方式** | OAuth 2.0 (邮箱) | API Key |
| **API 端点** | portal.qwen.ai | api.anthropic.com |
| **凭证文件** | `~/.qwen/oauth_creds.json` | `~/.claude/` 或环境变量 |
| **模型** | Qwen 3.5 Code | Claude 3.5 Sonnet |
| **提供商** | 阿里云 | Anthropic |
| **日志格式** | JSONL (含 usageMetadata) | JSONL (含 usage) |
| **Token 统计** | ✅ 日志包含实际数据 | ✅ 日志包含实际数据 |

---

## ⚠️ 重要说明

### 之前搞错的原因

1. **环境变量误导**: `ANTHROPIC_API_KEY` 是给 free-claude-code proxy 用的
2. **Base URL 混淆**: `CLAUDE_BASE_URL` 是 mycc 的代理配置
3. **Qwen Code 使用 OAuth**: 不需要配置 API Key，使用 OAuth 凭证

### 正确的 API 调用

```
Qwen Code → portal.qwen.ai (OAuth) → Qwen 模型
```

**不是**:
```
❌ Qwen Code → free-claude-code → Claude API
```

---

## 🛠️ 管理命令

```bash
# 查看授权状态
cat ~/.qwen/oauth_creds.json

# 重新授权
qwen-code --logout
qwen-code --login

# 查看安装 ID
cat ~/.qwen/installation_id

# 查看日志
cat ~/.qwen/projects/-root-air-qwq/chats/*.jsonl | tail -50

# 清理旧日志
rm -rf ~/.qwen/tmp/*/logs.json
```

---

## 📋 用量统计修正

之前的 `qwq-usage` 脚本需要修正：
1. ✅ 从 `usageMetadata` 读取实际 token 数
2. ✅ 使用 Qwen 模型价格计算
3. ✅ 移除 Claude 价格配置

---

## 📄 相关文档

- `0-System/api-topology.md` - 完整 API 拓扑（已更新）
- `0-System/qwq-api-usage.md` - API 配置与用量（需更新）
- `.qwen/skills/qwq-usage/SKILL.md` - 用量统计技能
