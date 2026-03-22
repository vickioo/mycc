# 🛠️ Qwen Code Skills - 技能组索引

**版本**: v1.0.0  
**更新**: 2026-03-10  
**位置**: `/root/air/qwq/0-System/skills/`

---

## 📋 技能列表

| 技能 | 版本 | 描述 | 触发词 |
|------|------|------|--------|
| **agent-export** | v1.0.0 | AI Agent 记忆导出归档 | `/export`, `导出对话` |
| **dingtalk-notify** | v1.0.0 | 钉钉群通知发送 | `/notify`, `发送通知` |
| **continuous-monitor** | v1.0.0 | 持续监控和自动恢复 | `/monitor`, `监控状态` |

---

## 📁 目录结构

```
0-System/skills/
├── README.md                      # 本索引
├── agent-export/
│   ├── SKILL.md                   # 技能说明
│   ├── agent-memory-exporter.py   # 导出工具
│   └── agent-export-service.py    # 导出服务
├── dingtalk-notify/
│   ├── SKILL.md                   # 技能说明
│   └── dingtalk-notify.js         # 通知脚本
└── continuous-monitor/
    ├── SKILL.md                   # 技能说明
    ├── continuous-monitor.sh      # 监控脚本
    └── crash-wrapper.sh           # 防崩溃包装
```

---

## 🔧 使用指南

### 查看所有技能

```bash
ls -la /root/air/qwq/0-System/skills/
```

### 查看技能详情

```bash
cat /root/air/qwq/0-System/skills/{skill-name}/SKILL.md
```

### 使用技能

```bash
# 导出 Agent 记忆
python3 /root/air/qwq/0-System/skills/agent-export/agent-memory-exporter.py --all

# 发送钉钉通知
node /root/air/qwq/0-System/skills/dingtalk-notify/dingtalk-notify.js "标题" "内容"

# 检查监控状态
bash /root/air/qwq/0-System/skills/continuous-monitor/continuous-monitor.sh check
```

---

## 📐 技能开发规范

### 目录结构

```
{skill-name}/
├── SKILL.md          # 必需：技能说明
├── *.py / *.js / *.sh  # 实现文件
└── README.md         # 可选：详细说明
```

### SKILL.md 模板

```markdown
# 🛠️ Skill: {skill-name}

**版本**: v1.0.0  
**描述**: 简短描述  
**触发词**: `/trigger`, `关键词`

## 功能

1. 功能 1
2. 功能 2

## 用法

```bash
command example
```

## 文件位置

| 文件 | 路径 |
|------|------|
| **主程序** | `/path/to/file` |

## 配置

配置说明...

## 示例

使用示例...
```

---

## 🔄 更新日志

### v1.0.0 (2026-03-10)

- ✅ agent-export - AI 记忆导出
- ✅ dingtalk-notify - 钉钉通知
- ✅ continuous-monitor - 持续监控

---

*维护者*: qwq (本地 Qwen Code 监控系统)
