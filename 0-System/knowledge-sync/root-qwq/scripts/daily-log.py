#!/usr/bin/env python3
"""
日记自动生成脚本
- 日更：每天自动生成基础模板
- 周结：每周日生成周总结模板
- 统计：自动统计当日/当周数据
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

DIARIES_DIR = Path("/root/air/qwq/6-Diaries")
TEMPLATES_DIR = DIARIES_DIR / "templates"

def get_week_number(date=None):
    """获取 ISO 周数"""
    d = date or datetime.now()
    return d.isocalendar()[1]

def get_week_range(date=None):
    """获取本周起止日期"""
    d = date or datetime.now()
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def create_daily_log(date=None):
    """创建或获取今日日志"""
    d = date or datetime.now()
    date_str = d.strftime("%Y-%m-%d")
    year_month = d.strftime("%Y-%m")
    
    # 创建月份目录
    month_dir = DIARIES_DIR / year_month
    month_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件路径
    log_file = month_dir / f"{date_str}.md"
    
    if log_file.exists():
        print(f"✅ 今日日志已存在：{log_file}")
        return log_file
    
    # 读取模板
    template_file = TEMPLATES_DIR / "daily-template.md"
    if not template_file.exists():
        print("❌ 模板文件不存在")
        return None
    
    template = template_file.read_text(encoding='utf-8')
    
    # 替换变量
    content = template.replace("{{DATE}}", date_str)
    content = content.replace("{{WEEKDAY}}", d.strftime("%A"))
    content = content.replace("{{TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # 写入文件
    log_file.write_text(content, encoding='utf-8')
    print(f"✅ 已创建今日日志：{log_file}")
    
    return log_file

def create_weekly_log(date=None):
    """创建或获取本周总结"""
    d = date or datetime.now()
    week_num = get_week_number(d)
    year = d.year
    
    # 创建年度目录
    year_dir = DIARIES_DIR / "weekly" / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件路径
    log_file = year_dir / f"{year}-W{week_num:02d}.md"
    
    if log_file.exists():
        print(f"✅ 本周总结已存在：{log_file}")
        return log_file
    
    # 读取模板
    template_file = TEMPLATES_DIR / "weekly-template.md"
    if not template_file.exists():
        print("❌ 模板文件不存在")
        return None
    
    template = template_file.read_text(encoding='utf-8')
    
    # 替换变量
    start, end = get_week_range(d)
    content = template.replace("{{WEEK_NUMBER}}", str(week_num))
    content = content.replace("{{START_DATE}}", start)
    content = content.replace("{{END_DATE}}", end)
    content = content.replace("{{DATE}}", d.strftime("%Y-%m-%d"))
    content = content.replace("{{TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # 写入文件
    log_file.write_text(content, encoding='utf-8')
    print(f"✅ 已创建本周总结：{log_file}")
    
    return log_file

def generate_stats(date=None):
    """生成统计数据"""
    d = date or datetime.now()
    date_str = d.strftime("%Y-%m-%d")
    
    stats = {
        "date": date_str,
        "files_created": 0,
        "lines_added": 0,
    }
    
    # 统计今日 Git 提交
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "--since=00:00", "--until=23:59", "--oneline"],
            cwd="/root/air/qwq",
            capture_output=True,
            text=True
        )
        stats["commits"] = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
    except:
        stats["commits"] = 0
    
    return stats

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="日记自动生成脚本")
    parser.add_argument("--daily", action="store_true", help="创建今日日志")
    parser.add_argument("--weekly", action="store_true", help="创建本周总结")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    if args.daily:
        create_daily_log()
    
    if args.weekly:
        create_weekly_log()
    
    if args.stats:
        stats = generate_stats()
        print(f"\n📊 今日统计:")
        print(f"  日期：{stats['date']}")
        print(f"  Git 提交：{stats.get('commits', 'N/A')} 次")
    
    if not any([args.daily, args.weekly, args.stats]):
        # 默认：创建今日日志
        create_daily_log()
        stats = generate_stats()
        print(f"\n📊 今日统计:")
        print(f"  Git 提交：{stats.get('commits', 'N/A')} 次")

if __name__ == "__main__":
    main()
