# 🤖 Agent Network Dashboard

> 多 Agent 协同系统统一看板

---

## 实时状态

| Agent | 状态 | 位置 | 用途 |
|-------|------|------|------|
| **qwq** | 🟢 | `/root/air/qwq` | Qwen Code - 主协调器 |
| **mycc** | 🟢 | `/root/air/mycc` | Claude Code - 本地协同 |
| **CC Server** | 🟢 | `192.168.100.228` | Claude - 重型任务 |
| **sjll** | 🟢 | `sj-liuliang.local` | 龙虾/Cherry - Windows 任务 |

---

## 服务状态

| 服务 | 状态 | 端口 | 备注 |
|------|------|------|------|
| One-API | 🟢 | 3000 | GLM5 可用 |
| Task Scheduler | 🟢 | - | 30s 轮询 |
| SSH Tunnel (SJLL) | 🟢 | 8821 | 经 databasei 跳板 |

---

## 任务统计

| 目录 | Inbox | Processing | Completed |
|------|-------|------------|-----------|
| qwq | `shared-tasks/inbox/` | `processing/` | `completed/` |
| mycc | `shared-tasks-qwq/inbox/` | `processing/` | `completed/` |
| CC | `/data/mycc/shared-tasks/inbox/` | `processing/` | `completed/` |
| sjll | `~/.openclaw/tasks/inbox/` | `processing/` | `completed/` |

---

## 快速命令

```bash
# 健康检查
./shared-tasks/healthcheck.sh

# 任务路由
./shared-tasks/router.sh task.json [cc|sjll|local]

# 同步状态
./shared-tasks/sync-to-mycc.sh
```

---

## 模型可用性

| 模型 | 渠道 | 状态 |
|------|------|------|
| z-ai/glm5 | 智谱 GLM | 🟢 |
| qwen/qwen3-235b-a22b | NVIDIA | 🟢 |
| meta-llama/llama-3.3-70b | OpenRouter | 🟢 |

---

*Last updated: 2026-03-05 21:00*
