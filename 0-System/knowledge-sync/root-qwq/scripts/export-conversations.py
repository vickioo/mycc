#!/usr/bin/env python3
"""
Multi-Agent Conversation Exporter
标准化导出多个 AI Agent 的对话记录

支持：qwq, mycc, CC Server, sjll (龙虾) 等

参考 GitHub 热门项目：
- https://github.com/aborroy/claude-conversation-exporter
- https://github.com/sunner/chatgpt-to-markdown

用法:
    python export-conversations.py [--agents all] [--format markdown|json] [--output-dir DIR]
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 配置
QWQ_DIR = Path("/root/air/qwq")
MYCC_DIR = Path("/root/air/mycc")
EXPORT_DIR = QWQ_DIR / "6-Diaries" / "conversations"

# Agent 配置
AGENTS_CONFIG = {
    "qwq": {
        "name": "Qwen Code",
        "dirs": [
            QWQ_DIR / "0-System",
            QWQ_DIR / "shared-tasks",
            QWQ_DIR / "tasks",
        ],
        "log_pattern": "*.md"
    },
    "mycc": {
        "name": "Claude Code (Local)",
        "dirs": [
            MYCC_DIR / "0-System",
            MYCC_DIR / "shared-tasks",
            MYCC_DIR / "tasks",
        ],
        "log_pattern": "*.md"
    },
    "cc": {
        "name": "CC Server (Claude)",
        "dirs": [
            QWQ_DIR / "0-System" / "agents" / "cc",
        ],
        "log_pattern": "*.md"
    },
    "sjll": {
        "name": "SJLL (龙虾)",
        "dirs": [
            QWQ_DIR / "0-System" / "agents" / "sjll",
        ],
        "log_pattern": "*.md"
    }
}


class ConversationExporter:
    def __init__(self, agents: List[str] = None, output_format: str = "markdown"):
        self.agents = agents or list(AGENTS_CONFIG.keys())
        self.output_format = output_format
        self.export_dir = EXPORT_DIR
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_conversations(self) -> Dict[str, List[Dict]]:
        """收集所有 Agent 的对话数据"""
        conversations = {}
        
        for agent_id in self.agents:
            if agent_id not in AGENTS_CONFIG:
                continue
            
            config = AGENTS_CONFIG[agent_id]
            agent_convs = []
            
            for base_dir in config["dirs"]:
                if not base_dir.exists():
                    continue
                
                # 扫描 markdown 文件
                for md_file in base_dir.rglob(config["log_pattern"]):
                    if self._is_conversation_file(md_file):
                        conv = self._parse_conversation(md_file, agent_id)
                        if conv:
                            agent_convs.append(conv)
            
            conversations[agent_id] = agent_convs
        
        return conversations
    
    def _is_conversation_file(self, path: Path) -> bool:
        """判断文件是否为对话文件"""
        # 排除系统文件
        exclude_patterns = ["README", "CHANGELOG", "VERSIONS", "FIXES"]
        name = path.stem.upper()
        for pattern in exclude_patterns:
            if pattern in name:
                return False
        return True
    
    def _parse_conversation(self, path: Path, agent_id: str) -> Dict:
        """解析对话文件"""
        try:
            content = path.read_text(encoding="utf-8")
            
            # 提取元数据
            meta = {
                "source": str(path),
                "agent": agent_id,
                "created_at": self._extract_date(path),
                "title": path.stem,
            }
            
            return {
                "meta": meta,
                "content": content,
                "word_count": len(content.split()),
            }
        except Exception as e:
            print(f"⚠️  解析失败 {path}: {e}")
            return None
    
    def _extract_date(self, path: Path) -> str:
        """从文件提取日期"""
        # 尝试从文件名提取
        import re
        date_pattern = r"(\d{4}-\d{2}-\d{2})"
        match = re.search(date_pattern, path.stem)
        if match:
            return match.group(1)
        
        # 使用文件修改时间
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    
    def export_markdown(self, conversations: Dict) -> Path:
        """导出为 Markdown 格式"""
        date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.export_dir / f"conversations-{date_str}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Multi-Agent Conversations\n\n")
            f.write(f"**Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for agent_id, convs in conversations.items():
                agent_name = AGENTS_CONFIG.get(agent_id, {}).get("name", agent_id)
                f.write(f"## 🤖 {agent_name} ({agent_id})\n\n")
                
                if not convs:
                    f.write("*No conversations*\n\n")
                    continue
                
                for conv in convs:
                    f.write(f"### {conv['meta']['title']}\n\n")
                    f.write(f"**Date**: {conv['meta']['created_at']}  \n")
                    f.write(f"**Source**: `{conv['meta']['source']}`  \n")
                    f.write(f"**Words**: {conv['word_count']}\n\n")
                    f.write("```\n")
                    f.write(conv['content'][:5000])  # 限制长度
                    f.write("\n```\n\n")
                    f.write("---\n\n")
        
        return output_file
    
    def export_json(self, conversations: Dict) -> Path:
        """导出为 JSON 格式"""
        date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.export_dir / f"conversations-{date_str}.json"
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "agents": self.agents,
            "conversations": conversations,
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def export(self, output_format: str = None) -> List[Path]:
        """执行导出"""
        fmt = output_format or self.output_format
        conversations = self.collect_conversations()
        
        output_files = []
        
        if fmt in ["markdown", "md", "all"]:
            md_file = self.export_markdown(conversations)
            output_files.append(md_file)
            print(f"✅ Markdown: {md_file}")
        
        if fmt in ["json", "all"]:
            json_file = self.export_json(conversations)
            output_files.append(json_file)
            print(f"✅ JSON: {json_file}")
        
        return output_files


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Conversation Exporter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python export-conversations.py                    # 导出所有 Agent (Markdown)
  python export-conversations.py --agents qwq,mycc  # 指定 Agent
  python export-conversations.py --format json      # JSON 格式
  python export-conversations.py --format all       # 两种格式
        """
    )
    
    parser.add_argument(
        "--agents",
        default="all",
        help="Agent 列表 (逗号分隔) 或 'all'"
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "md", "json", "all"],
        help="输出格式"
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录"
    )
    
    args = parser.parse_args()
    
    # 解析 Agent 列表
    if args.agents == "all":
        agents = list(AGENTS_CONFIG.keys())
    else:
        agents = [a.strip() for a in args.agents.split(",")]
    
    # 设置输出目录
    if args.output_dir:
        export_dir = Path(args.output_dir)
    else:
        export_dir = EXPORT_DIR
    
    # 执行导出
    exporter = ConversationExporter(agents=agents, output_format=args.format)
    exporter.export_dir = export_dir
    
    print(f"📥 导出多 Agent 对话记录...")
    print(f"   Agents: {', '.join(agents)}")
    print(f"   格式：{args.format}")
    print(f"   目录：{export_dir}")
    print()
    
    output_files = exporter.export()
    
    print()
    print(f"✅ 完成！导出 {len(output_files)} 个文件")


if __name__ == "__main__":
    main()
