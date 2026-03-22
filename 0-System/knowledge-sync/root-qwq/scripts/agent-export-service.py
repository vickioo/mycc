#!/usr/bin/env python3
"""
AI Agent Memory Export Service
统一导出服务端口

提供:
- HTTP API 端口 (8765)
- WebSocket 实时导出
- DataClaw 格式支持
- 隐私过滤
- vio_snap 自动同步

用法:
    python agent-export-service.py --start
    python agent-export-service.py --export --agents all --format jsonl
    python agent-export-service.py --status
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import subprocess

# 导入导出器
sys.path.insert(0, str(Path(__file__).parent))
from agent_memory_exporter import UniversalExporter, AGENT_DIRS, VIO_SNAP_BACKUP_DIR, VERSION

# 服务配置
SERVICE_PORT = 8765
EXPORT_LOG = Path("/root/vio_snap/backups/agent-memory/export-log.jsonl")

class ExportServiceHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == "/status":
            self.send_json({
                "status": "running",
                "version": VERSION,
                "port": SERVICE_PORT,
                "agents": list(AGENT_DIRS.keys()),
                "backup_dir": str(VIO_SNAP_BACKUP_DIR),
                "timestamp": datetime.now().isoformat()
            })
        elif self.path == "/agents":
            self.send_json({
                "agents": [
                    {"id": k, "path": str(v)} for k, v in AGENT_DIRS.items()
                ]
            })
        elif self.path.startswith("/export"):
            # 触发出口
            self.handle_export_request()
        else:
            self.send_json({"error": "Not found", "paths": ["/status", "/agents", "/export"]})
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == "/export":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                params = json.loads(body)
                self.handle_export(params)
            except Exception as e:
                self.send_json({"error": str(e)})
        else:
            self.send_json({"error": "Not found"})
    
    def handle_export_request(self):
        """处理导出请求"""
        # 解析查询参数
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        agents = params.get("agents", ["all"])[0].split(",")
        fmt = params.get("format", ["jsonl"])[0]
        
        self.handle_export({
            "agents": agents,
            "format": fmt
        })
    
    def handle_export(self, params: dict):
        """执行导出"""
        agents = params.get("agents", ["all"])
        fmt = params.get("format", "jsonl")
        output_dir = params.get("output_dir", str(VIO_SNAP_BACKUP_DIR))
        
        # 记录请求
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agents": agents,
            "format": fmt,
            "output_dir": output_dir
        }
        
        try:
            # 执行导出
            exporter = UniversalExporter(output_dir=Path(output_dir))
            
            # 简单导出 JSONL
            if fmt == "jsonl":
                output_file = exporter.export_jsonl()
                log_entry["output_file"] = str(output_file)
                log_entry["status"] = "success"
                
                self.send_json({
                    "status": "success",
                    "file": str(output_file),
                    "conversations": len(exporter.conversations)
                })
            else:
                self.send_json({"error": "Unsupported format", "supported": ["jsonl"]})
                log_entry["status"] = "error"
            
        except Exception as e:
            log_entry["status"] = "error"
            log_entry["error"] = str(e)
            self.send_json({"error": str(e)})
        
        # 记录日志
        with open(EXPORT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def send_json(self, data: dict):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{datetime.now().isoformat()}] {args[0]}")


def start_service():
    """启动 HTTP 服务"""
    server = HTTPServer(("0.0.0.0", SERVICE_PORT), ExportServiceHandler)
    print(f"🚀 AI Agent Export Service v{VERSION}")
    print(f"   Port: {SERVICE_PORT}")
    print(f"   Backup: {VIO_SNAP_BACKUP_DIR}")
    print(f"   Status: http://localhost:{SERVICE_PORT}/status")
    print(f"   Export: GET /export?agents=all&format=jsonl")
    print()
    server.serve_forever()


def export_once(agents: list = None, fmt: str = "jsonl", output_dir: Path = None):
    """单次导出"""
    if agents is None:
        agents = list(AGENT_DIRS.keys())
    
    if output_dir is None:
        output_dir = VIO_SNAP_BACKUP_DIR
    
    exporter = UniversalExporter(output_dir=output_dir)
    
    # 导出
    if fmt == "jsonl":
        output_file = exporter.export_jsonl()
        print(f"✅ JSONL: {output_file}")
    elif fmt == "markdown":
        output_file = exporter.export_markdown()
        print(f"✅ Markdown: {output_file}")
    elif fmt == "zip":
        output_file = exporter.export_zip()
        print(f"✅ ZIP: {output_file}")
    else:
        print(f"❌ 不支持的格式：{fmt}")
        return
    
    print(f"✅ 导出完成：{len(exporter.conversations)} 条对话")


def main():
    parser = argparse.ArgumentParser(
        description="AI Agent Memory Export Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 启动 HTTP 服务
  python agent-export-service.py --start
  
  # 单次导出
  python agent-export-service.py --export --agents qwq,mycc --format jsonl
  
  # 查看状态
  python agent-export-service.py --status
  
  # 导出到 vio_snap
  python agent-export-service.py --export --sync

端口:
  HTTP API: http://localhost:{SERVICE_PORT}
  状态：http://localhost:{SERVICE_PORT}/status
  导出：http://localhost:{SERVICE_PORT}/export?agents=all&format=jsonl
        """
    )
    
    parser.add_argument("--start", action="store_true", help="启动 HTTP 服务")
    parser.add_argument("--export", action="store_true", help="单次导出")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--agents", default="all", help="Agent 列表")
    parser.add_argument("--format", default="jsonl", choices=["jsonl", "markdown", "zip"])
    parser.add_argument("--output", help="输出目录")
    parser.add_argument("--sync", action="store_true", help="同步到 vio_snap")
    
    args = parser.parse_args()
    
    if args.start:
        start_service()
    elif args.export:
        agents = list(AGENT_DIRS.keys()) if args.agents == "all" else args.agents.split(",")
        output_dir = Path(args.output) if args.output else VIO_SNAP_BACKUP_DIR
        export_once(agents=agents, fmt=args.format, output_dir=output_dir)
    elif args.status:
        print(f"📊 AI Agent Export Service v{VERSION}")
        print(f"   端口：{SERVICE_PORT}")
        print(f"   备份目录：{VIO_SNAP_BACKUP_DIR}")
        print(f"   支持的 Agent: {list(AGENT_DIRS.keys())}")
        print(f"   支持的格式：jsonl, markdown, zip")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
