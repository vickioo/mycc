# 钉钉机器人 V2 架构文档

> 2026-03-18 创建

---

## 架构概述

```
钉钉 Stream 消息
       ↓
   消息路由层
    ↙    ↘
管理员模式    安全模式
    ↓          ↓
全能力访问    受限访问
```

---

## 两种模式对比

### 管理员模式 (Admin Mode)

| 能力 | 状态 | 说明 |
|------|------|------|
| 文件读写 | ✅ | 完整的 Read/Write/Edit |
| 命令执行 | ✅ | Bash 工具 |
| 网络请求 | ✅ | WebFetch/WebSearch |
| Skills | ✅ | 所有 skill 可用 |
| MCP | ✅ | 所有 MCP server 可用 |
| 敏感信息 | ✅ | 可访问配置、密钥 |

**适用场景**：系统管理员、开发者

### 安全模式 (Safe Mode)

| 能力 | 状态 | 说明 |
|------|------|------|
| 文件读写 | ❌ | 禁止 |
| 命令执行 | ❌ | 禁止 |
| 网络请求 | ❌ | 禁止 |
| Skills | ❌ | 禁止 |
| MCP | ❌ | 禁止 |
| 敏感信息 | ❌ | 过滤 |

**适用场景**：普通用户、外部访客

---

## 配置文件位置

- `/data/mycc/.claude/skills/dingtalk/scripts-v2/config-v2.json`

## 启动命令

```bash
cd /data/mycc/.claude/skills/dingtalk/scripts-v2
nohup node bot-v2.js > /tmp/dingtalk-bot-v2.log 2>&1 &
```

---

## 管理员列表

- 刘亮 (staffId: 1626074212671638)
