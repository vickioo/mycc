# Victory 智能体协作系统记忆

> 最后更新：2026-03-25 12:47

---

## 📊 服务状态

| 服务 | 端口 | 状态 | 备注 |
|------|------|------|------|
| CLIProxyAPI | 8317 | ✅ 在线 | API 中转 |
| AIHub Manager | 9000 | ✅ 在线 | 服务监控 |
| 1052Bot | 10053 | ✅ 在线 | 内容创作 |
| 1052Bot 前端 | 10052 | ✅ 在线 | Web UI |
| nanobot | 18790 | ❌ 离线 | Docker 未运行 |
| mycc | 18080 | ✅ 在线 | 飞书 WebSocket |

---

## 🤖 Victory Agent 群落

### ACP Agent 身份

| Agent | AID | 角色 | 状态 |
|-------|-----|------|------|
| **Victor-CC** | `victor-cc.agentid.pub` | 指挥官/管理器 | ✅ 已配置 |
| **victory-1052** | `1052bot.agentid.pub` | 内容创作者 | ✅ 已配置 |
| **victory-qwen** | - | 通用助手 | ❌ 待配置 |
| **victory-gemini** | - | 搜索专家 | ❌ 待登录 |

### Agent 角色定义

| Agent | 主要职能 |
|-------|----------|
| Victor-CC | 核心推理、架构设计、记忆管理、中央协调 |
| victory-1052 | 小说创作、自动化任务、内容生成 |
| victory-qwen | 日常对话、简单任务 |
| victory-gemini | 联网搜索、信息采集 |

### 1:N 对话架构

```
用户 → [Router] → 分发到对应 Agent
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Victor-CC  victory-1052  ...
(默认/管理)  (创作)
```

---

## 🔧 关键配置

### ACP 接入点
- **接入点**: `agentid.pub`
- **CA 服务器**: `acp3.agentid.pub`

### 飞书机器人
- App ID: `cli_a9327c5ebfbb9bd1`
- 接收 ID: `oc_bfec000013f21b6e810166f00533f18f`

### ACP 数据目录
- Victor-CC: `D:\python\victor-acp`
- victory-1052: `D:\python\1052V2.1\data\acp`

---

## 📁 重要文件位置

```
/home/vicki/air/mycc/
├── memory/MEMORY.md           # 全局记忆
├── assets/
│   ├── VICTORY_ARCHITECTURE.md  # 架构文档
│   ├── PROGRESS_REVIEW.md       # 进度梳理
│   ├── setup_victor_acp.py     # Victor ACP 配置脚本
│   ├── agent_comm.sh           # Agent 通信脚本
│   └── evolutions/            # 自进化任务
│       └── evolution_tasks.sh
```

---

## ⏰ 后台任务

| 任务 | 频率 | 脚本 |
|------|------|------|
| 自进化 | 每2小时 | evolution_tasks.sh |
| 状态报告 | 9:00, 18:00 | agent_comm.sh |

---

## 📋 待办事项

- [x] 配置 Victor-CC ACP 身份
- [x] 配置 victory-1052 ACP 身份
- [ ] 配置 victory-qwen ACP 身份
- [ ] 配置 victory-gemini ACP 身份
- [ ] 测试 ACP Agent 间通信
- [ ] nanobot 通道配置
- [ ] 设计 Router 消息分发逻辑

---

## 🔄 踩坑记录

### ACP AID 创建参数顺序
- **问题**: `create_aid(ap, agent_name)` 参数顺序
- **错误**: `create_aid('victor-cc', 'agentid.pub')`
- **正确**: `create_aid('agentid.pub', 'victor-cc')`

### WSL2 网络隔离
- 问题: Windows 端口无法从 WSL 直接访问
- 解决: 使用 PowerShell 命令

---

*最后更新: 2026-03-25 12:47*
*维护者: Victor-CC (Claude Code)*
