# SJLL 龙虾连接状态

> 与 SJLL 服务器 (Cherry Studio / 龙虾) 的连接信息

---

## SSH 配置

**别名**: `sjll-agent`
**连接**: `databasei` 跳板 → `sj-liuliang.local:22`
**用户**: `work`

---

## 环境信息

**系统**: Windows (WSL)
**用户**: `vicki`

**已安装**:
- Cherry Studio: `~/.cherrystudio/`
- OpenClaw: `~/.openclaw/`
- Claude Code: `~/.claude/`

---

## OpenClaw 配置

**模型**: `cc-oneapi/qwen/qwen3-235b-a22b`
**One-API 地址**: `http://192.168.100.228:3000/v1`

**Fallback**:
1. `cc-oneapi/meta-llama/llama-3.3-70b-instruct:free`
2. `cc-oneapi/anthropic/claude-sonnet-4-20250514`

---

## 连接状态

| 检查项 | 状态 |
|--------|------|
| SSH 隧道 | ✅ |
| sjll-agent 别名 | ✅ |
| Cherry Studio | ✅ |
| OpenClaw | ✅ |
| Claude Code | ✅ |

---

*Last updated: 2026-03-05 20:35*
