#!/usr/bin/env python3
"""
Qwen Code Token Usage Analyzer
扫描本地 Qwen Code 日志，按 日期 × 模型 统计 token 消耗

用法：
    python3 qwq-usage-analyzer.py              # 默认扫描所有项目
    python3 qwq-usage-analyzer.py --days 7     # 只看最近 7 天
    python3 qwq-usage-analyzer.py --session xxx  # 只看某个会话
    python3 qwq-usage-analyzer.py --csv        # 输出 CSV 格式
    python3 qwq-usage-analyzer.py --summary    # 只看模型汇总

日志位置：~/.qwen/tmp/*/logs.json
"""

import json
import os
import glob
import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# 模型简称映射 - Qwen Code 实际使用的模型
MODEL_SHORT = {
    # Qwen Code 模型
    'coder-model': 'qwen-code',
    'qwen-code': 'qwen-code',
    'qwen-3.5': 'qwen-3.5',
    'qwen3.5': 'qwen-3.5',
    'qwen-3': 'qwen-3',
    'qwen3': 'qwen-3',
    'qwen-max': 'qwen-max',
    'qwen-plus': 'qwen-plus',
    'qwen-turbo': 'qwen-turbo',
    
    # Claude 模型（备用）
    'claude-3-5-sonnet': 'claude-3.5-sonnet',
    'claude-3-sonnet': 'claude-3-sonnet',
    'claude-3-opus': 'claude-3-opus',
    'claude-3-haiku': 'claude-3-haiku',
    
    # 默认
    'unknown': 'qwen-code',
}

# API 定价（每百万 tokens，CNY 人民币）
# Qwen 价格（阿里云官方价格）
MODEL_PRICING = {
    # Qwen Code
    'qwen-code':   {'input': 0.0, 'output': 0.0},  # OAuth 免费额度
    'qwen-3.5':    {'input': 0.0, 'output': 0.0},  # OAuth 免费额度
    'qwen-3':      {'input': 0.0, 'output': 0.0},  # OAuth 免费额度
    
    # Qwen 付费模型（如果有）
    'qwen-max':    {'input': 0.04, 'output': 0.12},
    'qwen-plus':   {'input': 0.01, 'output': 0.03},
    'qwen-turbo':  {'input': 0.002, 'output': 0.006},
    
    # Claude（备用）
    'claude-3.5-sonnet': {'input': 21.0, 'output': 105.0},  # 约 $3/$15 USD
    'claude-3-sonnet':   {'input': 21.0, 'output': 105.0},
    'claude-3-opus':     {'input': 105.0, 'output': 525.0},
    'claude-3-haiku':    {'input': 5.6, 'output': 28.0},
    
    # Unknown (默认免费)
    'unknown':     {'input': 0.0, 'output': 0.0},
}


def shorten_model(model_id):
    """模型 ID → 简称"""
    if not model_id:
        return 'unknown'
    model_id = model_id.lower()
    for key, short in MODEL_SHORT.items():
        if key in model_id:
            return short
    # 兜底：返回原始 ID
    return model_id.split('/')[-1] if '/' in model_id else model_id


def calc_cost(model_short, input_tokens, output_tokens):
    """计算 API 等价费用"""
    pricing = MODEL_PRICING.get(model_short)
    if not pricing:
        return 0.0
    cost = (
        input_tokens * pricing['input'] / 1_000_000 +
        output_tokens * pricing['output'] / 1_000_000
    )
    return cost


def format_tokens(n):
    """格式化 token 数"""
    if n >= 1_000_000_000:
        return f'{n/1_000_000_000:.2f}B'
    if n >= 1_000_000:
        return f'{n/1_000_000:.1f}M'
    if n >= 1_000:
        return f'{n/1_000:.1f}K'
    return str(n)


def parse_timestamp(ts):
    """解析 ISO 时间戳到本地日期"""
    try:
        # 处理 Z 后缀
        ts = ts.rstrip('Z')
        # 尝试不同格式
        for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
            try:
                dt_naive = datetime.strptime(ts, fmt)
                dt = dt_naive.replace(tzinfo=timezone.utc)
                dt_local = dt.astimezone()
                return dt_local.strftime('%Y-%m-%d')
            except ValueError:
                continue
    except:
        pass
    return None


def scan_logs(logs_dir, session_filter=None, min_date=None):
    """扫描所有日志，返回 {(date, model): stats}"""
    stats = defaultdict(lambda: {
        'input': 0, 'output': 0,
        'count': 0, 'sessions': set()
    })

    # 查找所有 jsonl 日志文件（完整格式，包含 usageMetadata）
    log_files = glob.glob(os.path.join(logs_dir, '../projects/*/chats/*.jsonl'))
    # 也查找 tmp 日志（简化格式）
    log_files += glob.glob(os.path.join(logs_dir, '*/logs.json'))
    
    total_files = len(log_files)
    scanned_files = 0
    errors = 0

    for fpath in sorted(log_files):
        scanned_files += 1
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                if fpath.endswith('.jsonl'):
                    # JSONL 格式（完整日志，包含 usageMetadata）
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            entry = json.loads(line)
                            session_id = entry.get('sessionId', '')
                            msg_type = entry.get('type', '')
                            timestamp = entry.get('timestamp', '')
                            usage = entry.get('usageMetadata', {})

                            # 只统计 assistant 类型的消息
                            if msg_type != 'assistant':
                                continue

                            # 会话过滤
                            if session_filter and session_filter not in session_id:
                                continue

                            # 解析日期
                            date_str = parse_timestamp(timestamp)
                            if not date_str:
                                continue

                            # 日期过滤
                            if min_date and date_str < min_date:
                                continue

                            # 获取实际 token 数
                            input_tokens = usage.get('promptTokenCount', 0)
                            output_tokens = usage.get('candidatesTokenCount', 0)
                            model_id = entry.get('model', 'coder-model')

                            if input_tokens == 0 and output_tokens == 0:
                                continue

                            model_short = shorten_model(model_id)
                            key = (date_str, model_short)

                            stats[key]['input'] += input_tokens
                            stats[key]['output'] += output_tokens
                            stats[key]['count'] += 1
                            stats[key]['sessions'].add(session_id)

                        except Exception:
                            errors += 1
                else:
                    # JSON 格式（简化日志，无 usageMetadata）
                    content = f.read()
                    try:
                        data = json.loads(content)
                        entries = data if isinstance(data, list) else [data]
                    except:
                        continue

                    for entry in entries:
                        try:
                            session_id = entry.get('sessionId', '')
                            msg_type = entry.get('type', '')
                            timestamp = entry.get('timestamp', '')

                            if msg_type not in ('user', 'assistant'):
                                continue
                            if session_filter and session_filter not in session_id:
                                continue

                            date_str = parse_timestamp(timestamp)
                            if not date_str:
                                continue
                            if min_date and date_str < min_date:
                                continue

                            # 简化日志无 usage 信息，跳过
                            errors += 1

                        except Exception:
                            errors += 1

        except Exception:
            errors += 1

    return stats, scanned_files, total_files, errors


def print_table(stats, show_csv=False):
    """按日期分组打印表格"""
    if not stats:
        print('No data found.')
        return

    dates = sorted(set(k[0] for k in stats.keys()))
    models = sorted(set(k[1] for k in stats.keys()))

    if show_csv:
        print('date,model,input,output,total_tokens,cost_usd,messages,sessions')
        for date in dates:
            for model in models:
                key = (date, model)
                if key not in stats:
                    continue
                s = stats[key]
                total = s['input'] + s['output']
                cost = calc_cost(model, s['input'], s['output'])
                print(f'{date},{model},{s["input"]},{s["output"]},{total},{cost:.2f},{s["count"]},{len(s["sessions"])}')
        return

    # 表头
    header = f'{"Date":<12} {"Model":<14} {"Input":>10} {"Output":>10} {"Total":>10} {"Cost":>10} {"Msgs":>6}'
    sep = '-' * len(header)

    print(f'\n{"="*len(header)}')
    print(f'  Qwen Code Token Usage - Per Model Per Day')
    print(f'{"="*len(header)}')
    print(header)
    print(sep)

    grand_total = {'input': 0, 'output': 0, 'count': 0}
    grand_cost = 0.0

    for date in dates:
        day_total = 0
        day_cost = 0.0
        day_rows = []

        for model in models:
            key = (date, model)
            if key not in stats:
                continue
            s = stats[key]
            total = s['input'] + s['output']
            cost = calc_cost(model, s['input'], s['output'])

            day_rows.append(
                f'{date:<12} {model:<14} {format_tokens(s["input"]):>10} {format_tokens(s["output"]):>10} '
                f'{format_tokens(total):>10} {"$"+f"{cost:.2f}":>10} {s["count"]:>6}'
            )

            day_total += total
            day_cost += cost

            for k in ['input', 'output', 'count']:
                grand_total[k] += s[k]
            grand_cost += cost

        for row in day_rows:
            print(row)

        # 日小计
        if len(day_rows) > 1:
            print(f'{"":.<12} {"[day total]":<14} {"":>10} {"":>10} {format_tokens(day_total):>10} {"$"+f"{day_cost:.2f}":>10}')

        print(sep)

    # 总计
    g_total = grand_total['input'] + grand_total['output']
    print(f'{"TOTAL":<12} {"ALL":<14} {format_tokens(grand_total["input"]):>10} {format_tokens(grand_total["output"]):>10} '
          f'{format_tokens(g_total):>10} {"$"+f"{grand_cost:.2f}":>10} {grand_total["count"]:>6}')
    print(f'{"="*len(header)}\n')


def print_summary(stats):
    """按模型汇总"""
    model_totals = defaultdict(lambda: {'input': 0, 'output': 0, 'count': 0, 'days': set()})

    for (date, model), s in stats.items():
        for k in ['input', 'output', 'count']:
            model_totals[model][k] += s[k]
        model_totals[model]['days'].add(date)

    print(f'\n{"="*80}')
    print(f'  Model Summary (all time)')
    print(f'{"="*80}')
    print(f'{"Model":<14} {"Input":>10} {"Output":>10} {"Total":>10} {"Cost":>10} {"Days":>6} {"Msgs":>6}')
    print('-' * 80)

    total_cost = 0.0
    total_tokens = 0

    for model in sorted(model_totals.keys()):
        s = model_totals[model]
        total = s['input'] + s['output']
        cost = calc_cost(model, s['input'], s['output'])
        total_cost += cost
        total_tokens += total

        print(f'{model:<14} {format_tokens(s["input"]):>10} {format_tokens(s["output"]):>10} '
              f'{format_tokens(total):>10} {"$"+f"{cost:.2f}":>10} {len(s["days"]):>6} {s["count"]:>6}')

    print('-' * 80)
    print(f'{"TOTAL":<14} {"":>10} {"":>10} {format_tokens(total_tokens):>10} {"$"+f"{total_cost:.2f}":>10}')
    print(f'{"="*80}\n')


def main():
    parser = argparse.ArgumentParser(description='Qwen Code Token Usage Analyzer')
    parser.add_argument('--days', type=int, help='只看最近 N 天')
    parser.add_argument('--session', type=str, help='只看包含此关键词的会话')
    parser.add_argument('--csv', action='store_true', help='输出 CSV 格式')
    parser.add_argument('--summary', action='store_true', help='按模型汇总')
    parser.add_argument('--dir', type=str, 
                        default=os.path.expanduser('~/.qwen/tmp'),
                        help='Qwen Code 日志目录路径')
    args = parser.parse_args()

    min_date = None
    if args.days:
        min_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')

    print(f'Scanning {args.dir} ...')
    stats, scanned, total, errors = scan_logs(args.dir, args.session, min_date)
    print(f'Scanned {scanned}/{total} files, {len(stats)} date×model combos, {errors} errors\n')

    if args.summary:
        print_summary(stats)
    else:
        print_table(stats, show_csv=args.csv)

    if not args.csv:
        print_summary(stats)


if __name__ == '__main__':
    main()
