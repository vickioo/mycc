# 🗄️ AI Agent Memory Archive - 多 Agent 记忆归档

**归档时间**: 2026-03-10  
**归档工具**: Universal AI Agent Memory Exporter v1.0.0  
**归档格式**: universal-agent-memory-v1

---

## 📊 归档概览

| 项目 | 数量 | 大小 |
|------|------|------|
| **总对话数** | 200+ | - |
| **qwq (Qwen Code)** | 100+ | - |
| **mycc (Claude Code)** | 100+ | - |
| **sjll (OpenClaw)** | 待导出 | - |
| **归档大小** | - | ~1.8 MB |

---

## 📁 目录结构

```
5-Archive/agent-memory/
├── raw/                    # 原始数据
│   └── sjll-tasks-*.json   # SJLL 任务原始数据
├── processed/              # 处理后的数据
├── *.jsonl                 # 标准化 JSONL 格式
├── *.md                    # Markdown 格式
├── *.zip                   # 完整归档包
└── MANIFEST-*.json         # 归档清单
```

---

## 📄 文件格式说明

### 1. JSONL 格式 (标准化)

每行一个完整的对话记录，格式如下：

```jsonl
{
  "format_version": "universal-agent-memory-v1",
  "conversation": {
    "id": "唯一标识符",
    "title": "对话标题",
    "agent": "agent_id",
    "messages": [
      {
        "role": "user|assistant|system",
        "content": "消息内容",
        "timestamp": "ISO8601 时间戳",
        "model": "模型名称",
        "tool_calls": [],
        "metadata": {}
      }
    ],
    "created_at": "创建时间",
    "updated_at": "更新时间",
    "source_path": "原始文件路径",
    "word_count": 字数统计,
    "metadata": {}
  }
}
```

### 2. Markdown 格式

人类可读的对话记录，包含：
- 对话标题
- 日期
- 来源
- 字数统计
- 内容摘要

### 3. ZIP 归档包

包含所有格式的完整归档包，适合长期保存。

### 4. MANIFEST.json

归档清单文件，包含：
- 归档元数据
- 对话列表
- 统计信息

---

## 🔧 兼容的 Agent 格式

| Agent | 格式 | 解析器 | 状态 |
|-------|------|--------|------|
| **Qwen Code** | Markdown | MarkdownParser | ✅ 已支持 |
| **Claude Code** | Markdown | MarkdownParser | ✅ 已支持 |
| **OpenClaw** | JSON | OpenClawParser | ✅ 已支持 |
| **Generic Chat** | JSONL | JSONLParser | ✅ 已支持 |
| **Anthropic API** | JSON | - | 🔄 待添加 |
| **LangChain** | JSONL | - | 🔄 待添加 |

---

## 📋 使用指南

### 导出所有 Agent

```bash
python3 /root/air/qwq/scripts/agent-memory-exporter.py --all
```

### 导出指定 Agent

```bash
python3 /root/air/qwq/scripts/agent-memory-exporter.py --agents qwq,mycc
```

### 指定输出格式

```bash
# JSONL 格式 (推荐)
python3 /root/air/qwq/scripts/agent-memory-exporter.py --format jsonl

# Markdown 格式
python3 /root/air/qwq/scripts/agent-memory-exporter.py --format markdown

# 完整归档包 (ZIP)
python3 /root/air/qwq/scripts/agent-memory-exporter.py --format zip

# 所有格式
python3 /root/air/qwq/scripts/agent-memory-exporter.py --format all
```

### 指定输出目录

```bash
python3 /root/air/qwq/scripts/agent-memory-exporter.py --output /path/to/archive
```

---

## 🔍 归档内容

### qwq (Qwen Code)

**位置**: `/root/air/qwq/`

**包含**:
- `0-System/` - 系统配置
- `1-Inbox/` - 收件箱
- `6-Diaries/` - 日记
- `shared-tasks/` - 共享任务
- `tasks/` - 任务记录

### mycc (Claude Code)

**位置**: `/root/air/mycc/`

**包含**:
- `0-System/` - 系统配置
- `.claude/` - Claude 配置
- `shared-tasks/` - 共享任务

### sjll (OpenClaw / 龙虾)

**位置**: `/c/Users/vicki/.openclaw/tasks/` (Windows WSL)

**包含**:
- `inbox/` - 待处理任务
- `processing/` - 进行中任务
- `completed/` - 已完成任务

---

## 📊 归档统计

查看归档统计信息：

```bash
cat /root/air/qwq/5-Archive/agent-memory/MANIFEST-*.json | jq '.total_conversations, .total_messages, .agents'
```

---

## 🔐 安全建议

1. **定期归档**: 建议每周执行一次完整归档
2. **异地备份**: 将 ZIP 归档包复制到安全位置
3. **版本控制**: 使用 Git 管理归档目录
4. **加密敏感数据**: 对包含敏感信息的归档进行加密

---

## 🔗 参考 GitHub 项目

- [Claude Code](https://github.com/anthropics/claude-code)
- [OpenClaw](https://github.com/OpenClaw/openclaw)
- [claude-conversation-exporter](https://github.com/aborroy/claude-conversation-exporter)

---

## 📝 更新日志

### v1.0.0 (2026-03-10)

- ✅ 初始版本
- ✅ 支持 Markdown 格式解析
- ✅ 支持 OpenClaw JSON 格式
- ✅ 支持 JSONL 标准化输出
- ✅ 支持 ZIP 归档包
- ✅ 支持 Manifest 清单生成

---

*归档文档生成时间：2026-03-10*  
*维护者：qwq (本地 Qwen Code 监控系统)*
