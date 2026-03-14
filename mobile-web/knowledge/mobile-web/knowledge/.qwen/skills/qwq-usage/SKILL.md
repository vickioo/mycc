---
name: qwq-usage
description: 查看 Qwen Code 的 token 用量统计。按日期×模型维度拆分，支持按天数、会话过滤。触发词："/qwq-usage"、"看看用量"、"token 消耗"、"用量统计"
---

# qwq-usage — Token 用量统计

扫描本地 Qwen Code 日志（`~/.qwen/tmp/*/logs.json`），按 **日期 × 模型** 维度统计 token 消耗。

纯 Python 3 脚本，无需安装任何依赖。

## 触发词

- "/qwq-usage"
- "看看用量"
- "token 消耗"
- "用量统计"
- "Qwen 用量"

## 执行步骤

1. 运行分析脚本
2. 把结果整理成**易读的 Markdown 表格**返回

## 脚本位置

```
.qwen/skills/qwq-usage/scripts/analyzer.py
```

## 用法

```bash
# 默认：全部历史
python3 .qwen/skills/qwq-usage/scripts/analyzer.py

# 最近 N 天
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --days 7

# 只看某会话（按 session ID）
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --session 1ec6ccb7-e2f2-4fbc-958e-a5ff118071f2

# 输出 CSV（可导入 Excel）
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --csv

# 只看模型汇总
python3 .qwen/skills/qwq-usage/scripts/analyzer.py --summary
```

## 默认行为

用户没指定天数时，默认跑 `--days 7`（最近 7 天）。

## 输出要求

脚本跑完后，AI 应该：
1. 把关键数据整理成 Markdown 表格（按天 × 模型）
2. 给出日小计和总计
3. 附上模型汇总
4. 如有异常（某天突然暴涨），主动指出

## 日志格式

Qwen Code 日志位于 `~/.qwen/tmp/*/logs.json`，格式：
```json
[
  {
    "sessionId": "xxx",
    "messageId": 0,
    "type": "user|assistant",
    "message": "用户消息或 AI 回复",
    "timestamp": "2026-03-05T11:11:48.043Z"
  }
]
```

## 维护提示

新模型上线时需更新脚本里的 `MODEL_PRICING` 字典。
