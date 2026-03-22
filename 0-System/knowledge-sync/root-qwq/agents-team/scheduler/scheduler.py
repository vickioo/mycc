#!/usr/bin/env python3
"""任务调度器 - 定时任务和后台处理"""

import json, subprocess, os
from pathlib import Path
from datetime import datetime, timedelta

QUEUE_DIR = Path("/root/air/qwq/agents-team/queue")
SCHEDULES_FILE = QUEUE_DIR.parent / "scheduler" / "schedules.json"

class Scheduler:
    def __init__(self):
        self.schedules = self.load_schedules()
    
    def load_schedules(self):
        if SCHEDULES_FILE.exists():
            with open(SCHEDULES_FILE) as f:
                return json.load(f)
        return []
    
    def save_schedules(self):
        with open(SCHEDULES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.schedules, f, ensure_ascii=False, indent=2)
    
    def add_schedule(self, name: str, command: str, interval: str, target: str = "local"):
        """添加定时任务
        interval: cron 格式或简单间隔 (如 5m, 1h, 1d)
        """
        schedule = {
            "id": f"schedule-{len(self.schedules)+1}",
            "name": name,
            "command": command,
            "interval": interval,
            "target": target,
            "enabled": True,
            "last_run": None,
            "next_run": datetime.now().isoformat()
        }
        self.schedules.append(schedule)
        self.save_schedules()
        return schedule["id"]
    
    def check_and_run(self):
        """检查并运行到期的任务"""
        now = datetime.now()
        
        for schedule in self.schedules:
            if not schedule["enabled"]:
                continue
            
            next_run = datetime.fromisoformat(schedule["next_run"])
            if now >= next_run:
                # 提交任务到队列
                self.submit_task(schedule)
                # 计算下次运行时间
                schedule["next_run"] = self.calc_next_run(schedule["interval"]).isoformat()
                schedule["last_run"] = now.isoformat()
        
        self.save_schedules()
    
    def calc_next_run(self, interval: str) -> datetime:
        """计算下次运行时间"""
        if interval.endswith('m'):
            return datetime.now() + timedelta(minutes=int(interval[:-1]))
        elif interval.endswith('h'):
            return datetime.now() + timedelta(hours=int(interval[:-1]))
        elif interval.endswith('d'):
            return datetime.now() + timedelta(days=int(interval[:-1]))
        return datetime.now() + timedelta(hours=1)
    
    def submit_task(self, schedule: dict):
        """提交定时任务到队列"""
        from queue.task_queue import TaskQueue
        q = TaskQueue()
        
        task = {
            "name": f"[定时] {schedule['name']}",
            "command": schedule["command"],
            "target": schedule["target"],
            "timeout": 300,
            "priority": "normal"
        }
        q.submit(task)

if __name__ == "__main__":
    s = Scheduler()
    s.check_and_run()
    print("调度器检查完成")
