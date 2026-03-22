#!/usr/bin/env python3
"""系统监控和健康检查"""

import json, subprocess
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path("/root/air/qwq/agents-team/results")
REPORTS_DIR = Path("/root/air/qwq/agents-team/reports")

class Monitor:
    def __init__(self):
        self.nodes = {
            "local": {"cmd": "echo 'local ok'", "timeout": 5},
            "cc": {"cmd": "ssh -o BatchMode=yes CC 'echo cc ok'", "timeout": 10},
            "termux": {"cmd": "ssh -p 8022 localhost 'echo termux ok'", "timeout": 10}
        }
    
    def check_node(self, name: str) -> dict:
        """检查节点健康状态"""
        node = self.nodes.get(name)
        if not node:
            return {"status": "unknown", "error": f"未知节点：{name}"}
        
        try:
            result = subprocess.run(
                node["cmd"], shell=True, capture_output=True, text=True, timeout=node["timeout"]
            )
            return {
                "status": "online" if result.returncode == 0 else "offline",
                "output": result.stdout.strip(),
                "latency_ms": node["timeout"] * 1000
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "latency_ms": node["timeout"] * 1000}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def check_all(self) -> dict:
        """检查所有节点"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "nodes": {}
        }
        
        for name in self.nodes:
            report["nodes"][name] = self.check_node(name)
        
        # 保存报告
        report_file = REPORTS_DIR / f"health-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def generate_report(self) -> str:
        """生成统计报告"""
        report = self.check_all()
        
        online = sum(1 for n in report["nodes"].values() if n.get("status") == "online")
        total = len(report["nodes"])
        
        output = f"""
╔════════════════════════════════════════════════╗
║     Agents Team 健康报告                       ║
╚════════════════════════════════════════════════╝

时间：{report['timestamp']}

节点状态：{online}/{total} 在线

"""
        for name, status in report["nodes"].items():
            icon = "🟢" if status.get("status") == "online" else "🔴"
            output += f"{icon} {name}: {status.get('status', 'unknown')}\n"
        
        # 任务统计
        completed = len(list((RESULTS_DIR / "completed").glob("*.json")))
        failed = len(list((RESULTS_DIR / "failed").glob("*.json")))
        success_rate = completed / (completed + failed) * 100 if (completed + failed) > 0 else 0
        
        output += f"""
任务统计:
  完成：{completed}
  失败：{failed}
  成功率：{success_rate:.1f}%

"""
        return output

if __name__ == "__main__":
    m = Monitor()
    print(m.generate_report())
