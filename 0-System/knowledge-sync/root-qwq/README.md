# qwq 系统总结

> 多 Agent 协同开发系统 - 完整文档

---

## 🏗️ 系统架构

```
                    ┌─────────────────────────┐
                    │    qwq (Qwen Code)      │
                    │   /root/air/qwq         │
                    │   主协调器/路由器        │
                    └───────────┬─────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   mycc      │     │  CC Server  │     │  sjll-agent │
    │ Claude Code │     │   Claude    │     │  龙虾/Cherry│
    │  本地协同   │     │  重型任务   │     │  Windows    │
    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📁 目录结构

```
/root/air/qwq/
├── 0-System/                 # 记忆系统
│   ├── status.md            # 短期记忆 (今日快照)
│   ├── context.md           # 中期记忆 (本周上下文)
│   └── about-me/            # 长期记忆
│       ├── profile.md       # 用户画像
│       └── sjll-lobster.md  # SJLL 连接信息
├── shared-tasks/            # 任务协同目录
│   ├── inbox/              # 待处理任务
│   ├── processing/         # 处理中任务
│   ├── completed/          # 已完成任务
│   ├── router.sh           # 任务路由器
│   ├── sync-to-mycc.sh     # 状态同步
│   ├── healthcheck.sh      # 健康检查
│   ├── tracker.sh          # 任务追踪
│   ├── WORKFLOW.md         # 协同工作流
│   └── DASHBOARD.md        # 统一看板
├── tasks/                  # 任务文档
└── QWEN.md                # 全局记忆配置
```

---

## 🔄 任务路由

### router.sh 用法

```bash
# 路由到 CC 服务器 (重型任务/GLM5)
./shared-tasks/router.sh task.json cc

# 路由到 SJLL 龙虾 (Windows 任务)
./shared-tasks/router.sh task.json sjll

# 路由到本地 mycc (一般任务)
./shared-tasks/router.sh task.json local
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

## 🔧 工具命令

| 命令 | 功能 |
|------|------|
| `./shared-tasks/healthcheck.sh` | Agent 网络健康检查 |
| `./shared-tasks/tracker.sh` | 任务状态追踪 |
| `./shared-tasks/sync-to-mycc.sh` | 同步状态到 mycc |
| `./shared-tasks/router.sh` | 任务路由 |

---

## 📊 监控体系

### 健康检查

- qwq (Qwen Code) - 本地
- mycc (Claude Code) - 本地
- CC Server - SSH 连接
- SJLL - SSH 隧道 (经 databasei)
- One-API - HTTP 状态
- Scheduler - 进程检查

### 任务统计

- Inbox 数量
- Processing 数量
- Completed 数量

---

## 🤖 Agent 能力矩阵

| Agent | 位置 | 模型 | 用途 |
|-------|------|------|------|
| qwq | 本地 | 多种 | 协调/路由 |
| mycc | 本地 | Claude | 代码/文档 |
| CC | 远程 | GLM5 | 重型任务 |
| sjll | WSL | Claude | Windows 任务 |

---

## 📝 记忆系统

### 三层记忆

1. **短期** (`status.md`): 今日快照，实时更新
2. **中期** (`context.md`): 本周上下文
3. **长期** (`about-me/`): 用户画像，偏好

### 共享机制

- qwq 状态 → mycc/0-System/agents/qwq/
- 任务目录 → 各 Agent 共享

---

*Last updated: 2026-03-05 21:00*
