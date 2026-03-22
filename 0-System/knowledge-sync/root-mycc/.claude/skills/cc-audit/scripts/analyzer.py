#!/usr/bin/env python3
"""
free-claude-code Token Usage & Security Audit Analyzer
扫描 free-claude-code 日志，统计 token 消耗，检查阈值，发送报警

用法：
 python3 analyzer.py                    # 今天消耗统计
 python3 analyzer.py --days 7           # 最近 7 天
 python3 analyzer.py --threshold 100    # 阈值 100M tokens
 python3 analyzer.py --csv              # 输出 CSV
 python3 analyzer.py --notify feishu    # 发送飞书通知
 python3 analyzer.py --dir /path/to/log # 自定义日志目录

日志格式要求：
每行包含 JSON 格式的日志，包含以下字段之一即视为 token 使用记录：
- input_tokens, output_tokens (直接的 token 字段)
- usage.input_tokens, usage.output_tokens (嵌套的 usage 字段)
"""

import json
import os
import sys
import glob
import argparse
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 默认阈值（M tokens）
DEFAULT_THRESHOLD_M = 50

# 模型定价（每百万 tokens，USD）- 复用 cc-usage 的定价
PRICING = {
    'claude-opus-4-6': {'input': 15, 'output': 75},
    'claude-opus-4-5': {'input': 15, 'output': 75},
    'claude-opus-4-1': {'input': 15, 'output': 75},
    'claude-sonnet-4-5': {'input': 3, 'output': 15},
    'claude-sonnet-4': {'input': 3, 'output': 15},
    'claude-haiku-4-5': {'input': 0.8, 'output': 4},
    # 免费/开源模型
    'llama': {'input': 0, 'output': 0},
    'qwen': {'input': 0, 'output': 0},
    'deepseek': {'input': 0.1, 'output': 0.1},
    'default': {'input': 1, 'output': 5},
}


def detect_model_from_log(log_entry: dict) -> str:
    """从日志条目中检测使用的模型"""
    # 检查 model 字段
    model = log_entry.get('model', '')
    if model:
        return model

    # 检查消息内容中的模型信息
    message = log_entry.get('message', '')
    if message:
        # 常见的模型标识
        patterns = [
            r'claude-(opus|sonnet|haiku)-[\d.-]+',
            r'llama[_-]?[\d.]+',
            r'qwen[\d.]+',
            r'deepseek[_-]?v?[\d.]+',
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(0)

    return 'unknown'


def extract_tokens_from_log(line: str) -> dict | None:
    """从日志行中提取 token 使用信息

    支持多种日志格式：
    1. JSON 格式：{"input_tokens": 100, "output_tokens": 50, ...}
    2. 纯文本格式：input_tokens=100,output_tokens=50
    3. 日志格式：TOKEN_USAGE: input=100 output=50 model=xxx
    """
    try:
        # 尝试 JSON 格式
        data = json.loads(line)
        usage = {}

        # 直接字段
        if 'input_tokens' in data:
            usage['input'] = data.get('input_tokens', 0)
        if 'output_tokens' in data:
            usage['output'] = data.get('output_tokens', 0)

        # 嵌套 usage 字段
        if 'usage' in data and isinstance(data['usage'], dict):
            usage['input'] = data['usage'].get('input_tokens', 0)
            usage['output'] = data['usage'].get('output_tokens', 0)

        if usage.get('input') or usage.get('output'):
            return {
                'input': usage.get('input', 0),
                'output': usage.get('output', 0),
                'model': data.get('model', 'unknown'),
                'timestamp': data.get('timestamp', ''),
            }

    except json.JSONDecodeError:
        pass

    # 尝试日志格式：TOKEN_USAGE: ...
    line = line.strip()
    token_match = re.search(r'TOKEN_USAGE:', line, re.IGNORECASE)
    if token_match:
        # 提取 key=value 对
        kwargs = {}
        for match in re.finditer(r'(\w+)=(\d+)', line):
            key, value = match.groups()
            if key in ('input', 'output', 'input_tokens', 'output_tokens'):
                field = 'input' if 'input' in key else 'output'
                kwargs[field] = int(value)
        if kwargs:
            model_match = re.search(r'model=(\S+)', line)
            return {
                **kwargs,
                'model': model_match.group(1) if model_match else 'unknown',
                'timestamp': '',
            }

    return None


def scan_log_directory(log_dir: str, min_date: str = None) -> dict:
    """扫描日志目录，返回 {date: usage_stats}"""
    stats = defaultdict(lambda: {
        'input': 0,
        'output': 0,
        'count': 0,
        'models': set(),
    })

    if not os.path.exists(log_dir):
        print(f"Warning: Log directory not found: {log_dir}")
        return stats

    # 扫描日志文件
    log_files = []
    for pattern in ['*.log', '*.jsonl', 'server.log', '**/*.log']:
        log_files.extend(glob.glob(os.path.join(log_dir, pattern), recursive=True))

    # 去重
    log_files = list(set(log_files))

    print(f"Scanning {len(log_files)} log files in {log_dir}...")

    for fpath in log_files:
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    usage = extract_tokens_from_log(line)
                    if not usage:
                        continue

                    # 解析日期
                    timestamp = usage.get('timestamp', '')
                    if timestamp:
                        try:
                            ts = timestamp.rstrip('Z')
                            for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
                                try:
                                    dt_naive = datetime.strptime(ts, fmt)
                                    dt = dt_naive.replace(tzinfo=timezone.utc)
                                    dt_local = dt.astimezone()
                                    date_str = dt_local.strftime('%Y-%m-%d')
                                    break
                                except ValueError:
                                    continue
                            else:
                                continue
                        except Exception:
                            continue

                        # 日期过滤
                        if min_date and date_str < min_date:
                            continue
                    else:
                        # 没有时间戳则使用文件修改时间
                        date_str = datetime.fromtimestamp(
                            os.path.getmtime(fpath)
                        ).strftime('%Y-%m-%d')

                    # 记录统计数据
                    stats[date_str]['input'] += usage.get('input', 0)
                    stats[date_str]['output'] += usage.get('output', 0)
                    stats[date_str]['count'] += 1
                    if usage.get('model'):
                        stats[date_str]['models'].add(usage['model'])

        except Exception as e:
            print(f"Error reading {fpath}: {e}")

    return dict(stats)


def calc_cost(model: str, usage: dict) -> float:
    """计算 API 费用"""
    # 尝试匹配模型
    model_lower = model.lower()
    pricing = PRICING.get('default')

    for key, p in PRICING.items():
        if key in model_lower:
            pricing = p
            break

    input_cost = usage.get('input', 0) * pricing['input'] / 1_000_000
    output_cost = usage.get('output', 0) * pricing['output'] / 1_000_000
    return input_cost + output_cost


def format_tokens(n: int) -> str:
    """格式化 token 数量"""
    if n >= 1_000_000_000:
        return f'{n/1_000_000_000:.2f}B'
    if n >= 1_000_000:
        return f'{n/1_000_000:.1f}M'
    if n >= 1_000:
        return f'{n/1_000:.1f}K'
    return str(n)


def check_threshold(stats: dict, threshold_m: float) -> list:
    """检查是否超过阈值"""
    alerts = []
    threshold_tokens = threshold_m * 1_000_000

    for date, data in stats.items():
        total = data['input'] + data['output']
        if total > threshold_tokens:
            percent = (total / threshold_tokens - 1) * 100
            alerts.append({
                'date': date,
                'total': total,
                'cost': calc_cost('default', data),
                'percent': percent,
            })

    return alerts


def send_notification(alerts: list, notify_type: str) -> bool:
    """发送通知"""
    if not alerts:
        print("No alerts to send.")
        return True

    if notify_type == 'feishu':
        # TODO: 实现飞书通知
        print("Feishu notification not implemented yet.")
        return False
    elif notify_type == 'telegram':
        # TODO: 实现 Telegram 通知
        print("Telegram notification not implemented yet.")
        return False
    else:
        print(f"Unknown notification type: {notify_type}")
        return False


def print_report(stats: dict, threshold_m: float):
    """打印报告"""
    if not stats:
        print("No data found.")
        return

    # 按日期排序
    dates = sorted(stats.keys(), reverse=True)

    # 表头
    header = f'{"Date":<12} {"Input":>10} {"Output":>10} {"Total":>10} {"Cost":>12} {"Msgs":>6} {"Models":<20}'
    sep = '-' * len(header)

    print(f'\n{"="*len(header)}')
    print(f' free-claude-code Token Usage Audit')
    print(f'{"="*len(header)}')
    print(header)
    print(sep)

    grand_total = {'input': 0, 'output': 0, 'count': 0}
    grand_cost = 0.0

    for date in dates:
        data = stats[date]
        total = data['input'] + data['output']
        cost = calc_cost('default', data)
        models = ', '.join(list(data['models'])[:3]) if data['models'] else 'N/A'

        # 检查是否超过阈值
        threshold_tokens = threshold_m * 1_000_000
        flag = ' ⚠️ EXCEEDED' if total > threshold_tokens else ''

        print(f'{date:<12} {format_tokens(data["input"]):>10} {format_tokens(data["output"]):>10} '
              f'{format_tokens(total):>10} ${cost:>10.2f} {data["count"]:>6} {models:<20}{flag}')

        grand_total['input'] += data['input']
        grand_total['output'] += data['output']
        grand_total['count'] += data['count']
        grand_cost += cost

    print(sep)

    g_total = grand_total['input'] + grand_total['output']
    print(f'{"TOTAL":<12} {format_tokens(grand_total["input"]):>10} {format_tokens(grand_total["output"]):>10} '
          f'{format_tokens(g_total):>10} ${grand_cost:>10.2f} {grand_total["count"]:>6}')
    print(f'{"="*len(header)}\n')

    # 阈值检查
    alerts = check_threshold(stats, threshold_m)
    if alerts:
        print(f'\n⚠️  ALERT: {len(alerts)} day(s) exceeded threshold ({threshold_m}M tokens):')
        for alert in alerts:
            print(f'  - {alert["date"]}: {format_tokens(alert["total"])} ({alert["percent"]:.1f}% over, ~${alert["cost"]:.2f})')
        print()


def main():
    parser = argparse.ArgumentParser(description='free-claude-code Token Usage & Security Audit')
    parser.add_argument('--days', type=int, help='Number of recent days to analyze')
    parser.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD_M,
                        help=f'Threshold in millions of tokens (default: {DEFAULT_THRESHOLD_M}M)')
    parser.add_argument('--dir', type=str, default=None,
                        help='Log directory path (default: auto-detect)')
    parser.add_argument('--csv', action='store_true', help='Output CSV format')
    parser.add_argument('--notify', type=str, choices=['feishu', 'telegram', 'none'], default='none',
                        help='Send notification when threshold exceeded')
    parser.add_argument('--quiet', action='store_true', help='Only output alerts')
    args = parser.parse_args()

    # 确定日志目录
    if args.dir:
        log_dir = args.dir
    else:
        # 尝试自动检测
        candidates = [
            os.path.expanduser('~/.claude/projects/free-claude-code'),
            '/root/free-claude-code',
            './free-claude-code',
        ]
        log_dir = None
        for candidate in candidates:
            if os.path.exists(candidate):
                log_dir = candidate
                break
        if not log_dir:
            log_dir = candidates[0]  # 使用第一个候选作为默认值

    # 计算日期范围
    min_date = None
    if args.days:
        min_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')

    # 扫描日志
    stats = scan_log_directory(log_dir, min_date)

    if args.quiet:
        # 只输出警告
        alerts = check_threshold(stats, args.threshold)
        if alerts:
            print(f'⚠️  {len(alerts)} day(s) exceeded threshold: {", ".join(a["date"] for a in alerts)}')
            sys.exit(1)
        else:
            print(f'✓ All days within threshold')
            sys.exit(0)

    # 输出报告
    if args.csv:
        print('date,input,output,total,cost,messages')
        for date in sorted(stats.keys()):
            data = stats[date]
            total = data['input'] + data['output']
            cost = calc_cost('default', data)
            print(f'{date},{data["input"]},{data["output"]},{total},{cost:.2f},{data["count"]}')
    else:
        print_report(stats, args.threshold)

    # 检查并通知
    alerts = check_threshold(stats, args.threshold)
    if alerts and args.notify != 'none':
        send_notification(alerts, args.notify)


if __name__ == '__main__':
    main()