# 🛠️ Skill: agent-export

**版本**: v1.0.0  
**描述**: AI Agent 记忆导出归档工具  
**触发词**: `/export`, `导出对话`, `归档记忆`, `backup`

---

## 功能

1. **多 Agent 导出** — 支持 qwq, mycc, sjll, OpenClaw, DataClaw 格式
2. **标准化格式** — JSONL, Markdown, ZIP
3. **隐私过滤** — 自动脱敏文件路径、用户名、API 密钥
4. **vio_snap 同步** — 自动备份到 Termux 统一归档目录
5. **HTTP API** — 提供 8765 端口服务

---

## 用法

### 命令行

```bash
# 导出所有 Agent
/export --all

# 导出指定 Agent
/export --agents qwq,mycc

# 指定格式
/export --format jsonl
/export --format zip

# 同步到 vio_snap
/export --sync
```

### HTTP API

```bash
# 启动服务
python3 /root/air/qwq/scripts/agent-export-service.py --start

# 查看状态
curl http://localhost:8765/status

# 导出
curl "http://localhost:8765/export?agents=all&format=jsonl"
```

---

## 文件位置

| 文件 | 路径 |
|------|------|
| **主程序** | `/root/air/qwq/scripts/agent-memory-exporter.py` |
| **服务** | `/root/air/qwq/scripts/agent-export-service.py` |
| **归档目录** | `/root/vio_snap/backups/agent-memory/` |
| **指南** | `/root/vio_snap/backups/agent-memory/ARCHIVE-GUIDE.md` |

---

## 输出格式

### JSONL (标准化)

```jsonl
{"format_version":"universal-agent-memory-v2","conversation":{"id":"abc123","title":"对话","agent":"qwq","messages":[{"role":"user","content":"..."}]}}
```

### Markdown

```markdown
# 🤖 QWQ

### 对话标题

**Date**: 2026-03-10  
**Words**: 1234

内容...
```

### ZIP 归档包

包含所有格式 + Manifest 清单

---

## 配置

### 支持的 Agent

- `qwq` - Qwen Code
- `mycc` - Claude Code (Local)
- `sjll` - OpenClaw (SJLL/龙虾)
- `dataclaw` - DataClaw 格式

### 支持的格式

- `jsonl` - 标准化 JSONL
- `markdown` - Markdown
- `zip` - ZIP 归档包
- `all` - 所有格式

### 输出目录

- 默认：`/root/air/qwq/5-Archive/agent-memory/`
- vio_snap: `/root/vio_snap/backups/agent-memory/`

---

## 示例

### 完整导出

```bash
python3 /root/air/qwq/scripts/agent-memory-exporter.py --all --format zip --sync
```

### 使用服务

```bash
# 后台启动
pm2 start /root/air/qwq/scripts/agent-export-service.py --name export-service

# 查看状态
pm2 status export-service
```

---

## 隐私保护

### 自动过滤

| 类型 | 处理方式 |
|------|----------|
| 文件路径 | 仅保留相对路径 |
| 用户名 | 替换为匿名编码 |
| API 密钥 | 自动识别并抹除 |
| 数据库密码 | 自动识别并抹除 |

### 手动检查

```bash
# 搜索敏感信息
grep -i "password\|secret\|key" /root/vio_snap/backups/agent-memory/*.jsonl
```

---

## 参考

- **DataClaw**: https://github.com/peteromallet/dataclaw
- **微信文章**: https://mp.weixin.qq.com/s/uxvIDYpqsnNGysY4dhPYAQ
- **归档指南**: `/root/vio_snap/backups/agent-memory/ARCHIVE-GUIDE.md`

---

*创建*: 2026-03-10  
*维护者*: qwq (本地 Qwen Code 监控系统)
