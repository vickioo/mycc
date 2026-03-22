#!/usr/bin/env python3
"""分布式 Worker 节点"""

import sys, json, subprocess, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "queue"))
from task_queue import TaskQueue, log

class Worker:
    def __init__(self, worker_id: str, capabilities: list):
        self.worker_id = worker_id
        self.capabilities = capabilities
        self.queue = TaskQueue()
    
    def execute(self, task: dict) -> dict:
        """执行任务"""
        log(f"执行任务：{task['id']} - {task.get('name', 'unnamed')}")
        
        cmd = task.get("command", "")
        timeout = task.get("timeout", 300)
        target = task.get("target", "local")  # local, cc, termux
        
        try:
            if target == "cc":
                # 在 CC 服务器上执行
                result = subprocess.run(
                    f"ssh -o BatchMode=yes CC '{cmd}'",
                    shell=True, capture_output=True, text=True, timeout=timeout
                )
            elif target == "termux":
                # 在 Termux 中执行
                result = subprocess.run(
                    f"ssh -p 8022 localhost '{cmd}'",
                    shell=True, capture_output=True, text=True, timeout=timeout
                )
            else:
                # 本地执行
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, timeout=timeout
                )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"超时 ({timeout}s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self):
        """Worker 主循环"""
        log(f"Worker 启动：{self.worker_id} (能力：{self.capabilities})")
        
        while True:
            task = self.queue.claim(self.worker_id)
            if task:
                result = self.execute(task)
                if result.get("success"):
                    self.queue.complete(task["id"], result)
                else:
                    self.queue.fail(task["id"], result.get("error", "Unknown error"))
            else:
                import time
                time.sleep(5)  # 无任务时等待

if __name__ == "__main__":
    worker_id = sys.argv[1] if len(sys.argv) > 1 else "worker-1"
    capabilities = sys.argv[2:] if len(sys.argv) > 2 else ["local"]
    
    w = Worker(worker_id, capabilities)
    w.run()
