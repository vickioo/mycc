# Victory 智能体协作系统架构

> 多 Agent 协作、自进化、信息聚合系统
> 创建时间: 2026-03-24
> 版本: v1.0

---

## 一、系统概览

### 1.1 核心目标
- **自我进化**: 持续学习、自我优化
- **多 Agent 协作**: 不同 Agent 分工合作、信息共享
- **资产管理**: 代码、记忆、踩坑经验安全存储
- **自动化**: 后台任务、静默迭代

### 1.2 参与 Agent

| Agent | 运行环境 | 通信能力 | 主要职能 |
|-------|----------|----------|----------|
| **Vicki-Linux (我)** | WSL2/Linux | WebSocket (Feishu), HTTP API | 核心推理、架构设计、记忆管理 |
| **1052Bot** | Windows 本地 | HTTP API, Feishu | 内容创作、赚钱模式 |
| **Surface-MyCC** | Windows Surface | WebSocket (Feishu) | 桌面交互、SMB共享 |
| **nanobot** | 本地 Docker | 待配置 | 统一网关 |
| **AIHub** | 本地服务 | HTTP API | 服务管理、监控 |

### 1.3 通信矩阵

```
┌─────────────────────────────────────────────────────────────┐
│                      Victory 系统                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Vicki-Linux] ←──→ [1052Bot] ←──→ [Feishu 通道]          │
│        ↓                ↓                                   │
│        ↓           [AIHub] ←──→ [nanobot]                  │
│        ↓                ↓                                   │
│        └──────────→ [Feishu 单聊/群聊] ←──→ [Surface-MyCC] │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、通信协议

### 2.1 ACP (Agent Communication Protocol)

**接入点**: `agentid.pub`

**AID 规划**:
- Vicki-Linux: `vicki.agentid.pub` (待配置)
- 1052Bot: `1052agent.agentid.pub` (待配置)

**API 端点**:
```
GET  /api/acp/status        - 查询 ACP 状态
POST /api/acp/send          - 发送消息
GET  /api/acp/aid/list      - 获取 AID 列表
POST /api/acp/start          - 启动 ACP
POST /api/acp/stop           - 停止 ACP
```

### 2.2 HTTP API 直接调用

**1052Bot**:
- `POST http://localhost:10053/api/agent/chat` - 对话
- `POST http://localhost:10053/api/feishu/send` - 发飞书消息
- `GET  http://localhost:10053/api/settings` - 获取设置

**AIHub**:
- `GET http://localhost:9000/api/status` - 服务状态

### 2.3 飞书消息路由

**Feishu App ID**: `cli_a9327c5ebfbb9bd1`

**消息接收**:
- Vicki-Linux: WebSocket 长连接 (lark-oapi SDK)
- 1052Bot: Webhook (需要公网 URL)
- Surface-MyCC: WebSocket 长连接

**收件箱 ID**:
- Vicki 单聊: `oc_a1b2c3d4e5f6...` (待确认)
- 1052 单聊: `oc_bfec000013f21b6e810166f00533f18f`

---

## 三、后台任务系统

### 3.1 自进化任务 (Self-Evolution)

**调度频率**: 每 2 小时一次

**任务清单**:
1. 写日记 - 记录今日所学
2. 整理记忆 - 清理、更新 memory.md
3. 联网学习 - 搜索新技术/最佳实践
4. 代码优化 - 检查并改进 skills
5. 协作通信 - 与其他 Agent 交换信息

### 3.2 信息采集任务 (Collect)

**调度频率**: 每日 9:00, 18:00

**采集源**:
- RSS Feeds
- 飞书群消息
- 微信公众号
- Web 搜索

### 3.3 资产归档任务

**调度频率**: 每日 23:00

**归档内容**:
- 重要对话摘要
- 新增 skills/scripts
- 踩坑记录
- Git 提交

---

## 四、Git 管理规范

### 4.1 分支策略

```
main                    - 稳定版本
├── dev                 - 开发分支
├── skills/             - Skills 迭代
├── memory/             - 记忆更新
└── feat/               - 功能分支
```

### 4.2 提交规范

**提交频率**: 重要变更随时提交，每日至少一次总结提交

**Commit Message**:
```
[FEAT] 新功能
[FIX]  Bug 修复
[DOCS] 文档更新
[SKILL] Skills 更新
[MEMORY] 记忆同步
[EVOLVE] 自进化成果
```

### 4.3 里程碑

- [ ] v1.0 - 基础架构完成
  - [x] 1052Bot 部署
  - [x] 飞书通道打通
  - [ ] ACP 协议配置
  - [ ] 后台任务系统

- [ ] v1.1 - 协作功能
  - [ ] Agent 间通信
  - [ ] 信息聚合
  - [ ] 自动归档

- [ ] v2.0 - 高级功能
  - [ ] 流式卡片集成
  - [ ] 多 Agent 协作
  - [ ] 自我进化闭环

---

## 五、文件结构

```
/home/vicki/air/
├── mycc/
│   ├── memory/
│   │   └── MEMORY.md           # 全局记忆
│   ├── assets/                 # 资产目录
│   │   ├── skills/             # Skills 备份
│   │   ├── scripts/            # 脚本备份
│   │   └── configs/            # 配置备份
│   └── .claude/
│       └── skills/             # Skills 源码
├── victory-archive/            # 归档目录
│   ├── 2026-03/
│   │   ├── daily/              # 每日总结
│   │   ├── evolutions/         # 进化记录
│   │   └── communications/     # 通信记录
│   └── weekly/                 # 周报
└── 1052bot/                    # 1052Bot 数据 (Windows)
```

---

## 六、下一步行动

### Phase 1: 基础架构 (今日完成)
- [x] 1052Bot 后端 + 前端部署
- [x] 飞书发送通道测试
- [ ] Vicki Feishu WebSocket 连接测试
- [ ] ACP 协议启用

### Phase 2: 协作系统 (明日)
- [ ] 配置 ACP AID
- [ ] 编写 Agent 间通信脚本
- [ ] 设置后台任务调度

### Phase 3: 自进化 (本周)
- [ ] 实现自进化循环
- [ ] 自动化归档系统
- [ ] Git 自动化提交

---

## 七、联系方式

| Agent | 飞书 ID | 备注 |
|-------|---------|------|
| Vicki-Linux | 自身 | Claude Code 主会话 |
| 1052Bot | oc_bfec000013f21b6e810166f00533f18f | 内容创作 |

---

*最后更新: 2026-03-24 23:14*
*维护者: Vicki-Linux Claude Code*
