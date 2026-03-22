#!/usr/bin/env python3
"""回测任务系统 - 测试分布式架构能力"""

import json, subprocess, time
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path("/root/air/qwq/agents-team/results")
BACKTEST_DIR = Path("/root/air/qwq/agents-team/reports/backtest")
BACKTEST_DIR.mkdir(parents=True, exist_ok=True)

def run_backtest():
    """运行回测任务"""
    print("╔════════════════════════════════════════════════╗")
    print("║     分布式架构回测                             ║" )
    print("╚════════════════════════════════════════════════╝")
    print()
    
    # 测试任务列表
    tasks = [
        {"name": "本地命令", "command": "echo 'local test'", "target": "local"},
        {"name": "CC 服务器", "command": "uptime", "target": "cc"},
        {"name": "Termux", "command": "echo 'termux test'", "target": "termux"},
        {"name": "CC 文件列表", "command": "ls /root/air", "target": "cc"},
        {"name": "本地时间", "command": "date", "target": "local"},
    ]
    
    results = []
    
    for task in tasks:
        print(f"📝 测试：{task['name']} ({task['target']})...")
        
        start = time.time()
        try:
            if task["target"] == "cc":
                cmd = f"ssh -o BatchMode=yes -o ConnectTimeout=5 CC '{task['command']}'"
            elif task["target"] == "termux":
                cmd = f"ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=5 localhost '{task['command']}'"
            else:
                cmd = task["command"]
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            elapsed = time.time() - start
            
            success = result.returncode == 0
            results.append({
                "name": task["name"],
                "target": task["target"],
                "success": success,
                "elapsed_ms": int(elapsed * 1000),
                "output": result.stdout[:200] if success else result.stderr[:200]
            })
            
            icon = "✅" if success else "❌"
            print(f"   {icon} {task['name']}: {int(elapsed*1000)}ms")
            
        except Exception as e:
            results.append({
                "name": task["name"],
                "target": task["target"],
                "success": False,
                "error": str(e)
            })
            print(f"   ❌ {task['name']}: {e}")
    
    # 统计
    total = len(results)
    success = sum(1 for r in results if r.get("success"))
    success_rate = success / total * 100 if total > 0 else 0
    avg_elapsed = sum(r.get("elapsed_ms", 0) for r in results if r.get("success")) / success if success > 0 else 0
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "success": success,
        "success_rate": success_rate,
        "avg_elapsed_ms": avg_elapsed,
        "results": results
    }
    
    # 保存报告
    report_file = BACKTEST_DIR / f"backtest-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"成功率：{success}/{total} ({success_rate:.1f}%)")
    print(f"平均延迟：{avg_elapsed:.0f}ms")
    print(f"报告：{report_file}")
    
    return report

if __name__ == "__main__":
    run_backtest()
