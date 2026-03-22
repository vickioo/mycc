# 联通云 HA 配置归档

> 归档时间：2026-03-05 21:47

---

## 📁 归档内容

### 配置文件

| 文件 | 来源 | 用途 |
|------|------|------|
| `free-claude-code.env` | `/root/free-claude-code/.env` | 本地 free-claude-code 联通云优先配置 |
| `mycc.env` | `/root/air/mycc/.env` | mycc (Claude Code) 联通云优先配置 |

### 脚本文件

| 文件 | 用途 |
|------|------|
| `auto_rotate.sh` | 自动灾备轮换脚本（联通云优先） |
| `switch_to_unicom.sh` | 一键切换到联通云 Claude |
| `SKILL.md` | cc-switch 技能文档 |

### 文档

| 文件 | 内容 |
|------|------|
| `unicom-ha-plan.md` | 联通云 HA 完整方案 |
| `unicom-config-done.md` | 配置完成报告 |

---

## 🔄 优先级架构

```
用户请求
    │
    ▼
联通云 (antigravity) ← Priority 1
    │ 失败 ↓
    ▼
NVIDIA NIM ← Priority 2
    │ 失败 ↓
    ▼
SiliconFlow ← Priority 3
    │ 失败 ↓
    ▼
OpenRouter ← Priority 4
    │ 失败 ↓
    ▼
智谱 GLM ← Priority 5 (兜底)
```

---

## 🔧 使用方式

### free-claude-code
```bash
cd /root/free-claude-code
# 已自动使用联通云优先配置
./claude-pick
```

### mycc (Claude Code)
```bash
# 在 mycc 会话中
/unicom    # 切换到联通云 Claude
/rotate    # 自动灾备轮换
```

### CC 服务器 One-API
```bash
curl http://192.168.100.228:3000/v1/chat/completions \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  -d '{"model":"claude-3-5-sonnet-20241022",...}'
```

---

## 📊 渠道状态

### CC 服务器 One-API
| ID | 名称 | Priority | 状态 |
|----|------|----------|------|
| 7 | CC-Antigravity-SVIP | 1 | ✅ 联通云 |
| 2 | SiliconFlow-VIP | 2 | ✅ |
| 8 | VIP-Channel | 2 | ✅ |
| 9 | 智谱 GLM z-ai | 3 | ⚠️ |
| 6 | OpenRouter-Free | 4 | ✅ |

### 模型映射
- `claude-3-5-sonnet-20241022` → 渠道 7 (联通云)
- `claude-3-5-sonnet-20240620` → 渠道 7 (联通云)
- `claude-3-haiku` → 渠道 7 (联通云)
- `gemini-2.5-flash` → 渠道 7 (联通云)

---

## 📝 恢复步骤

如需恢复配置：

```bash
# 恢复 free-claude-code
cp /root/air/qwq/4-Assets/unicom-config/free-claude-code.env /root/free-claude-code/.env

# 恢复 mycc
cp /root/air/qwq/4-Assets/unicom-config/mycc.env /root/air/mycc/.env

# 恢复脚本
cp /root/air/qwq/4-Assets/unicom-config/auto_rotate.sh \
   /root/air/mycc/.claude/skills/cc-switch/scripts/
cp /root/air/qwq/4-Assets/unicom-config/switch_to_unicom.sh \
   /root/air/mycc/.claude/skills/cc-switch/scripts/
```

---

## 🔑 API Key 管理

**联通云 Antigravity**:
- API Key: `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`
- Base URL: `http://192.168.100.228:8045/v1`

**One-API (CC 服务器)**:
- API Key: `sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f`
- Base URL: `http://192.168.100.228:3000/v1`

---

*归档位置：`/root/air/qwq/4-Assets/unicom-config/`*
*创建者：qwq (Qwen Code)*
