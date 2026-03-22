---
name: cc-audit
description: free-claude-code 安全审计。记录每日 token 消耗、超过阈值报警、生成消耗报告。触发词："/cc-audit"、"安全审计"、"token 报警"
---

# cc-audit — free-claude-code 安全审计

监控 free-claude-code 的 token 消耗，记录日志，超过阈值时报警，并生成消耗报告。

## 触发词

- "/cc-audit"
- "安全审计"
- "token 报警"
- "看看消耗"

## 执行步骤

1. 根据用户需求确定参数（天数、阈值、通知方式）
2. 运行分析脚本
3. 检查是否超过阈值，如超过则发送通知
4. 把结果整理成**易读的 Markdown 表格**返回给用户

## 脚本位置

```bash
.claude/skills/cc-audit/scripts/analyzer.py
```

## 用法

```bash
# 默认：今天消耗统计
python3 .claude/skills/cc-audit/scripts/analyzer.py

# 最近 N 天
python3 .claude/skills/cc-audit/scripts/analyzer.py --days 7

# 自定义阈值（单位：M tokens）
python3 .claude/skills/cc-audit/scripts/analyzer.py --threshold 100

# 输出 CSV
python3 .claude/skills/cc-audit/scripts/analyzer.py --csv

# 启用飞书通知
python3 .claude/skills/cc-audit/scripts/analyzer.py --notify feishu

# 启用 Telegram 通知
python3 .claude/skills/cc-audit/scripts/analyzer.py --notify telegram
```

## 默认行为

- 用户没指定天数时，默认跑 `--days 1`（今天）
- 默认阈值：50M tokens
- 日志位置：`~/.claude/projects/*/`

## 阈值说明

- 当日 token 消耗超过阈值时，自动发送通知
- 通知方式：飞书、Telegram（需要在 .env 中配置）
- 通知内容：包含日期、消耗量、预估费用、超过阈值的比例

## 维护提示

- 可以在 scheduler 中配置每日自动运行
- 阈值建议根据实际使用情况调整

## 日志格式

free-claude-code 的日志中需要包含 token 使用信息：
- `input_tokens`
- `output_tokens`
- `cache_creation_input_tokens`
- `cache_read_input_tokens`