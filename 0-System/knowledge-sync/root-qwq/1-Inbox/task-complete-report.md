# ✅ API Error 诊断与技能固化完成报告

**完成时间**: 2026-03-10 21:35  
**诊断者**: qwq

---

## 1️⃣ API Error 诊断

### 错误现象

`✕ [API Error: terminated]`

### 根源分析

| 组件 | 状态 | 原因 |
|------|------|------|
| **continuous-monitor** | ⚠️ 运行中 | 持续尝试恢复失败的服务 |
| **mobile-web** | ❌ 未运行 | 服务未启动或端口 8766 无响应 |
| **CC Clash Tunnel** | ❌ 未运行 | SSH 隧道中断 |

### 触发链

```
continuous-monitor (每 30 秒检查)
  ├─ 检测 mobile-web 异常
  ├─ 检测 CC Clash Tunnel 异常
  └─ 尝试恢复失败 → 记录错误日志
```

### 解决方案

```bash
# 1. 启动 mobile-web
cd /root/air/mycc && pm2 start mobile-web

# 2. 重启 Clash Tunnel
bash /root/cc-clash-tunnel.sh restart

# 3. 或停止误报 (如果不需要这些服务)
pm2 stop continuous-monitor
```

### 详细报告

`/root/air/qwq/1-Inbox/api-error-diagnosis.md`

---

## 2️⃣ 聊天信息还原/吸收

### 当前导出格式

**位置**: `/root/vio_snap/backups/agent-memory/`

| 格式 | 文件 | 用途 |
|------|------|------|
| **JSONL** | `*.jsonl` | 机器处理，可被大模型吸收 |
| **Markdown** | `*.md` | 人类可读 |
| **ZIP** | `*.zip` | 完整归档 |

### 大模型吸收格式

```jsonl
{"format_version":"universal-agent-memory-v2","conversation":{"id":"abc123","title":"对话","agent":"qwq","messages":[{"role":"user","content":"..."}]}}
```

**兼容性**:
- ✅ DataClaw 格式
- ✅ Claude Code 格式
- ✅ OpenClaw 格式
- ✅ Qwen Code 格式

### 使用方法

1. **本地训练**: 使用导出的 JSONL 文件进行微调
2. **RAG 检索**: 导入到向量数据库
3. **上下文恢复**: 加载 JSONL 恢复对话历史

---

## 3️⃣ 技能组固化

### 已创建技能 (3 个)

| 技能 | 版本 | 位置 | 功能 |
|------|------|------|------|
| **agent-export** | v1.0.0 | `0-System/skills/agent-export/` | AI 记忆导出归档 |
| **dingtalk-notify** | v1.0.0 | `0-System/skills/dingtalk-notify/` | 钉钉通知发送 |
| **continuous-monitor** | v1.0.0 | `0-System/skills/continuous-monitor/` | 持续监控 |

### 目录结构

```
/root/air/qwq/0-System/skills/
├── README.md                          # 技能索引
├── agent-export/
│   ├── SKILL.md                       # 技能说明
│   ├── agent-memory-exporter.py       # 导出工具 (v2.0)
│   └── agent-export-service.py        # HTTP 服务 (端口 8765)
├── dingtalk-notify/
│   ├── SKILL.md                       # 技能说明
│   └── dingtalk-notify.js             # 通知脚本
└── continuous-monitor/
    ├── SKILL.md                       # 技能说明
    ├── continuous-monitor.sh          # 监控脚本
    └── crash-wrapper.sh               # 防崩溃包装
```

### 技能规范

**SKILL.md 包含**:
- 功能说明
- 触发词
- 用法示例
- 文件位置
- 配置说明
- 错误处理

### 使用技能

```bash
# 查看技能列表
ls -la /root/air/qwq/0-System/skills/

# 查看技能详情
cat /root/air/qwq/0-System/skills/agent-export/SKILL.md

# 使用技能
python3 /root/air/qwq/0-System/skills/agent-export/agent-memory-exporter.py --all
```

---

## 📊 统计

| 项目 | 数量 |
|------|------|
| **技能数** | 3 |
| **脚本文件** | 6 |
| **文档** | 4 |
| **归档对话** | 200 条 |
| **归档大小** | 1.8 MB |

---

## 🔗 相关文档

- **API Error 诊断**: `/root/air/qwq/1-Inbox/api-error-diagnosis.md`
- **归档指南**: `/root/vio_snap/backups/agent-memory/ARCHIVE-GUIDE.md`
- **技能索引**: `/root/air/qwq/0-System/skills/README.md`

---

*报告生成时间：2026-03-10 21:35*  
*生成者：qwq*
