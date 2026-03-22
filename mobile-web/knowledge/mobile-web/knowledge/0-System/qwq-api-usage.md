# Qwen Code API 配置与用量统计

**日期**: 2026-03-05

---

## 当前 API 配置

### 使用的 API

| 项目 | 配置 |
|------|------|
| **API 提供商** | free-claude-code Proxy |
| **API 端点** | `http://localhost:8082/v1` |
| **API Key** | `sk-ant-api03-localproxy-*` |
| **环境变量** | `ANTHROPIC_API_KEY`, `CLAUDE_BASE_URL` |
| **实际模型** | Claude 3.5 Sonnet (via NVIDIA NIM) |

### 当前模型

Qwen Code 通过 **free-claude-code Proxy** 调用 AI 模型：
- **默认模型**: `claude-3-5-sonnet-20241022` (NVIDIA NIM)
- **备用模型**: OpenRouter, SiliconFlow, Zhipu (降级)

---

## 与 mycc (Claude Code) 的区别

| 特性 | Qwen Code (qwq) | Claude Code (mycc) |
|------|-----------------|-------------------|
| API 协议 | Anthropic | Anthropic |
| 日志格式 | `~/.qwen/tmp/*/logs.json` | `~/.claude/projects/*/` |
| 用量统计 | ✅ qwq-usage | ✅ cc-usage |
| One-API 集成 | ⚠️ 需配置 | ✅ 已配置 |

---

## 用量统计工具

### qwq-usage (Qwen Code)

**位置**: `.qwen/skills/qwq-usage/SKILL.md`

```bash
# 查看最近 7 天用量
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --days 7

# 查看所有历史
python3 .qwen/skills/qwq-usage/scripts/analyzer.py

# 按模型汇总
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --summary

# 输出 CSV
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --csv
```

### cc-usage (Claude Code)

**位置**: `mycc/.claude/skills/cc-usage/SKILL.md`

```bash
# 在 mycc 中执行
python3 .claude/skills/cc-usage/scripts/analyzer.py --days 7
```

---

## One-API 集成

### CC 服务器 One-API

CC 服务器运行 One-API 服务，提供：
- 多模型聚合（Claude、Qwen、GLM 等）
- 用量统计和计费
- 自动降级和重试

**访问方式**:
```bash
# 通过 SSH 隧道
ssh -L 3000:localhost:3000 CC

# API 端点
http://localhost:3000/v1
```

### 本地配置

在 `~/.bashrc` 中配置：
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-localproxy-xxx"
```

---

## 用量统计对比

### mycc 的 cc-usage 功能

✅ **完整功能**:
- 按 日期 × 模型 维度统计
- 实际 token 使用量（从 API 响应获取）
- API 费用估算
- 缓存命中率统计

### qwq 的 qwq-usage 功能

✅ **基础功能**:
- 按 日期 × 模型 维度统计
- 估算 token 使用量（按字符数）
- API 费用估算（参考价格）
- 会话数量统计

⚠️ **限制**:
- Qwen Code 日志不记录实际 token 使用量
- 使用字符数估算（可能不准确）

---

## 获取准确用量数据

### 方案 1: 集成 One-API

在 Qwen Code 配置中添加 One-API 端点：

```bash
export ANTHROPIC_BASE_URL="http://localhost:3000/v1"
export ANTHROPIC_API_KEY="sk-xxx"
```

### 方案 2: 日志增强

修改 Qwen Code 配置，记录 API 响应中的 usage 信息：

```json
{
  "hooks": {
    "AssistantResponse": [
      {
        "type": "command",
        "command": "echo '{\"usage\": $USAGE}' >> ~/.qwen/usage.jsonl"
      }
    ]
  }
}
```

### 方案 3: 使用 CC 服务器统计

通过 One-API 的管理界面查看：
```bash
# 访问 CC 服务器 One-API 管理后台
ssh CC
docker logs oneapi --tail 100
```

---

## 价格参考

### Qwen API 价格 (每百万 tokens, USD)

| 模型 | Input | Output |
|------|-------|--------|
| qwen-max | $0.04 | $0.12 |
| qwen-plus | $0.01 | $0.03 |
| qwen-turbo | $0.002 | $0.006 |

### Claude API 价格 (每百万 tokens, USD)

| 模型 | Input | Output | Cache Create | Cache Read |
|------|-------|--------|--------------|------------|
| opus-4.5 | $15 | $75 | $18.75 | $1.50 |
| sonnet-4 | $3 | $15 | $3.75 | $0.30 |
| haiku-4.5 | $0.8 | $4 | $1.0 | $0.08 |

---

## 快速查看用量

### Qwen Code 用量

```bash
# 在 qwq 目录执行
cd /root/air/qwq
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --days 7
```

### Claude Code 用量

```bash
# 在 mycc 目录执行
cd /root/air/mycc
python3 .claude/skills/cc-usage/scripts/analyzer.py --days 7
```

### One-API 用量

```bash
# 通过 CC 服务器查看
ssh CC "curl -s http://localhost:3000/api/billing | jq ."
```

---

## 优化建议

### 1. 统一用量统计

建议将 qwq-usage 和 cc-usage 合并，统一输出格式。

### 2. 实时同步到 mycc

用量数据同步到 mycc 看板：
```bash
cp /root/air/qwq/.qwen/skills/qwq-usage/report.md \
   /root/air/mycc/0-System/agents/qwq/usage.md
```

### 3. 设置用量告警

当日用量超过阈值时通知：
```bash
# 添加到 crontab
0 * * * * /root/air/qwq/.qwen/skills/qwq-usage/scripts/check-limit.sh
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `.qwen/skills/qwq-usage/SKILL.md` | qwq-usage 技能定义 |
| `.qwen/skills/qwq-usage/scripts/analyzer.py` | 用量分析脚本 |
| `0-System/termux-done.md` | 架构完成报告 |
| `~/.bashrc` | API 配置 |
