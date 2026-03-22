#!/usr/bin/env python3
"""分布式任务队列系统"""

import json, os, uuid, time
from datetime import datetime
from pathlib import Path

QUEUE_DIR = Path("/root/air/qwq/agents-team/queue")
WORKERS_DIR = Path("/root/air/qwq/agents-team/workers")
RESULTS_DIR = Path("/root/air/qwq/agents-team/results")
LOGS_DIR = Path("/root/air/qwq/agents-team/logs")

class TaskQueue:
    def __init__(self):
        self.pending = QUEUE_DIR / "pending"
        self.processing = QUEUE_DIR / "processing"
        self.completed = RESULTS_DIR / "completed"
        self.failed = RESULTS_DIR / "failed"
        for d in [self.pending, self.processing, self.completed, self.failed]:
            d.mkdir(parents=True, exist_ok=True)
    
    def submit(self, task: dict) -> str:
        task_id = str(uuid.uuid4())[:8]
        task["id"] = task_id
        task["created_at"] = datetime.now().isoformat()
        task["status"] = "pending"
        
        task_file = self.pending / f"{task_id}.json"
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        
        log(f"任务提交：{task_id} - {task.get('name', 'unnamed')}")
        return task_id
    
    def claim(self, worker_id: str) -> dict | None:
        for task_file in sorted(self.pending.glob("*.json")):
            try:
                with open(task_file) as f:
                    task = json.load(f)
                
                # 移动到 processing
                task["worker_id"] = worker_id
                task["started_at"] = datetime.now().isoformat()
                task["status"] = "processing"
                
                processing_file = self.processing / task_file.name
                with open(processing_file, 'w', encoding='utf-8') as f:
                    json.dump(task, f, ensure_ascii=False, indent=2)
                task_file.unlink()
                
                log(f"任务领取：{task['id']} by {worker_id}")
                return task
            except Exception as e:
                log(f"领取任务失败：{e}")
        return None
    
    def complete(self, task_id: str, result: dict):
        processing_file = self.processing / f"{task_id}.json"
        if processing_file.exists():
            with open(processing_file) as f:
                task = json.load(f)
            
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()
            task["status"] = "completed"
            
            result_file = self.completed / f"{task_id}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            processing_file.unlink()
            
            log(f"任务完成：{task_id}")
    
    def fail(self, task_id: str, error: str):
        processing_file = self.processing / f"{task_id}.json"
        if processing_file.exists():
            with open(processing_file) as f:
                task = json.load(f)
            
            task["error"] = error
            task["failed_at"] = datetime.now().isoformat()
            task["status"] = "failed"
            
            result_file = self.failed / f"{task_id}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            processing_file.unlink()
            
            log(f"任务失败：{task_id} - {error}")
    
    def status(self) -> dict:
        return {
            "pending": len(list(self.pending.glob("*.json"))),
            "processing": len(list(self.processing.glob("*.json"))),
            "completed": len(list(self.completed.glob("*.json"))),
            "failed": len(list(self.failed.glob("*.json")))
        }

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    log_file = LOGS_DIR / f"{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

if __name__ == "__main__":
    q = TaskQueue()
    print("任务队列状态:", q.status())
