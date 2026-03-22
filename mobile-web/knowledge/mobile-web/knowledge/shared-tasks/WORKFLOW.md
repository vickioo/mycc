# Agent 协同工作流

> 多 Agent 协同开发的标准工作流程

---

## 架构概览

```
                    ┌─────────────────┐
                    │   qwq (Qwen)    │
                    │  /root/air/qwq  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │ mycc       │ │ CC 服务器  │ │ sjll-agent │
     │ Claude     │ │ Claude     │ │ 龙虾       │
     │ 本地       │ │ 远程       │ │ WSL        │
     └────────────┘ └────────────┘ └────────────┘
```

---

## 任务路由

### 使用 router.sh

```bash
# 路由到 CC 服务器 (重型任务)
./router.sh task.json cc

# 路由到 SJLL 龙虾 (Windows 任务)
./router.sh task.json sjll

# 路由到本地 mycc (一般任务)
./router.sh task.json local
```

### 任务格式

```json
{
  "id": "task-001",
  "title": "任务标题",
  "description": "任务描述",
  "created_at": "2026-03-05T12:00:00Z",
  "status": "pending",
  "source": "qwq-local",
  "target": "cc-server",
  "expected_model": "z-ai/glm5",
  "priority": "normal"
}
```

---

## 共享目录

| Agent | 目录 |
|-------|------|
| qwq | `/root/air/qwq/shared-tasks/` |
| mycc | `/root/air/mycc/shared-tasks-qwq/` |
| CC 服务器 | `/data/mycc/shared-tasks/` |
| sjll | `~/.openclaw/tasks/` |

---

## 状态同步

```bash
# 手动同步
./sync-to-mycc.sh

# 同步到 CC 服务器
scp task.json CC:/data/mycc/shared-tasks/inbox/

# 同步到 SJLL
scp task.json sjll-agent:~/.openclaw/tasks/inbox/
```

---

## 最佳实践

1. **轻量任务**: 本地 mycc 处理
2. **重型任务**: CC 服务器 (GLM5)
3. **Windows 任务**: SJLL 龙虾
4. **代码审查**: 任意 Agent

---

*Last updated: 2026-03-05 20:57*
