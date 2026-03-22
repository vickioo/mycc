# Gemini API 配置说明

**更新日期**: 2026-03-07 20:40
**来源**: 用户确认

---

## 📌 关键信息

### API Key 说明

```
GEMINI_API_KEY=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
```

**重要**: 虽然以 `nvapi-` 开头，但这是 **Antigravity Tools 网关的 API Key**，不是 NVIDIA 官方 API Key。

- ✅ 可用于连接 Antigravity Proxy
- ✅ 可通过 Antigravity 访问 NVIDIA 服务
- ⚠️ 不是 NVIDIA 官方 Key

---

## CC 服务器配置

### 环境变量 (`~/.gemini/.env`)

```bash
GOOGLE_GEMINI_BASE_URL=http://127.0.0.1:8045
GEMINI_API_KEY=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
GOOGLE_GEMINI_MODEL=gemini-3-flash
```

### Antigravity Proxy

- **端口**: 8045
- **进程**: `antigravity_too` (PID 2504626)
- **状态**: 运行中
- **健康检查**: `curl http://127.0.0.1:8045/api/health`

---

## 当前问题

### 503 Token Error

```
Token acquisition timeout (5s) - system too busy or deadlock detected
```

**可能原因**:
1. Antigravity 网关服务繁忙
2. API Key 限流/配额问题
3. 后端服务连接问题

---

## 使用方式

### 在 CC 服务器上使用 Gemini

```bash
# 方式 1: 自动加载 ~/.gemini/.env
gemini 'Hello'

# 方式 2: 手动指定
export GEMINI_API_KEY=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
export GOOGLE_GEMINI_BASE_URL=http://127.0.0.1:8045
gemini -m gemini-3-flash 'Hello'
```

### 通过 API 调用

```bash
curl http://127.0.0.1:8045/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 相关服务

| 服务 | 端口 | 说明 |
|------|------|------|
| Antigravity Proxy | 8045 | Gemini 代理网关 |
| One-API | 3000 | 统一 API 网关 |
| Clash | 7890 | SOCKS5 代理 |

---

## 记忆同步目标

- [x] qwq (本地 Qwen Code)
- [ ] mycc (CC 服务器 Claude)
- [ ] free-claude-code (本地 Claude 代理)
- [ ] CC 服务器 Gemini CLI
- [ ] sjll-agent (龙虾)

---

*最后更新：2026-03-07 20:40*
