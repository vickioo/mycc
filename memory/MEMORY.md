# Victory 智能体协作系统记忆

> 最后更新：2026-03-24 23:17

---

## 📊 服务状态

| 服务 | 端口 | 状态 | 备注 |
|------|------|------|------|
| CLIProxyAPI | 8317 | ✅ 在线 | API 中转 |
| AIHub Manager | 9000 | ✅ 在线 | 服务监控 |
| 1052Bot | 10053 | ✅ 在线 | 内容创作 |
| 1052Bot 前端 | 10052 | ✅ 在线 | Web UI |
| nanobot | 18790 | ⚠️ 需配置 | 通道关闭 |
| mycc | 18080 | ⚠️ 需启动 | 飞书 WebSocket |

---

## 🔧 关键配置

### 飞书机器人
- App ID: `cli_a9327c5ebfbb9bd1`
- 1052Bot 接收 ID: `oc_bfec000013f21b6e810166f00533f18f`

### API 密钥
- NVIDIA NIM: `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`
- Google AI: `AIzaSyCoTgyjJF29_hoKf8IMNKbFBTMrApWUxik`

---

## 🤖 Agent 通信

| Agent | 通信方式 | 状态 |
|-------|----------|------|
| 1052Bot | HTTP API + 飞书 | ✅ 可通信 |
| nanobot | 待配置 | ❌ 需配置 |
| Surface-MyCC | 飞书 WebSocket | ⚠️ SSH 问题 |

### ACP 协议
- 接入点: `agentid.pub`
- **1052Bot AID**: `1052bot.agentid.pub` ✅ 已启用
- Vicki (我): 待配置

---

## 📁 资产位置

```
/home/vicki/air/mycc/
├── assets/
│   ├── VICTORY_ARCHITECTURE.md    # 架构文档
│   ├── agent_comm.sh              # Agent 通信脚本
│   ├── evolutions/                # 自进化任务
│   └── logs/                      # 运行日志
└── memory/
    └── MEMORY.md                  # 全局记忆
```

---

## ⏰ 后台任务

| 任务 | 频率 | 脚本 |
|------|------|------|
| 自进化 | 每2小时 | evolution_tasks.sh |
| 状态报告 | 9:00, 18:00 | agent_comm.sh |

---

## 🔄 踩坑记录

### WSL2 网络隔离
- 问题: Windows 端口无法从 WSL 直接访问
- 解决: 使用 PowerShell 命令或 Windows 本地执行

### Git 冲突
- 解决: 优先使用远程版本，保持同步

### SSH 连接
- 问题: SSH 到 Surface 超时
- 原因: WSL2 网络问题
- 解决: 使用 SMB 共享或 PowerShell 远程

---

## 📋 待办事项

- [ ] 测试 Feishu WebSocket 接收（我自己的）
- [ ] 配置 ACP 协议 AID
- [ ] 启用 nanobot 通道
- [ ] 解决 SSH 连接问题
- [ ] 集成 Surface-MyCC 协作

---

*最后更新: 2026-03-24 23:17*
*维护者: Vicki-Linux Claude Code*

