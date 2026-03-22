#!/usr/bin/env python3
"""
Universal AI Agent Memory Exporter
多 Agent 记忆标准化导出归档工具

兼容格式:
- Anthropic Claude Code (.md, .json)
- OpenClaw (.json, .md)
- Qwen Code (.md)
- Generic Chat (.jsonl)

参考 GitHub 项目:
- https://github.com/anthropics/claude-code
- https://github.com/OpenClaw/openclaw
- https://github.com/aborroy/claude-conversation-exporter

输出格式:
- JSONL (标准化行式 JSON)
- Markdown (人类可读)
- ZIP (完整归档包)

用法:
    python agent-memory-exporter.py --all
    python agent-memory-exporter.py --agents qwq,mycc,sjll --format jsonl
    python agent-memory-exporter.py --output /path/to/archive
"""

import os
import sys
import json
import argparse
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

# ============================================================================
# 配置
# ============================================================================

VERSION = "2.0.0"
EXPORT_FORMAT_VERSION = "universal-agent-memory-v2"

# 各 Agent 根目录
AGENT_DIRS = {
    "qwq": Path("/root/air/qwq"),
    "mycc": Path("/root/air/mycc"),
    "sjll": Path("/c/Users/vicki"),  # Windows path (WSL)
}

# 输出目录（支持多位置）
DEFAULT_OUTPUT_DIR = Path("/root/air/qwq/5-Archive/agent-memory")
VIO_SNAP_BACKUP_DIR = Path("/root/vio_snap/backups/agent-memory")  # Termux 备份目录

# DataClaw 格式支持
DATACLAW_FORMAT = {
    "sources": ["claude-code", "codex", "gemini-cli", "openclaw", "qwen-code"],
    "privacy_filters": ["file_paths", "usernames", "api_keys", "secrets"],
    "output_format": "jsonl",
    "huggingface_upload": True,
}

# ============================================================================
# 数据模型 (标准化格式)
# ============================================================================

@dataclass
class Message:
    """标准化消息格式"""
    role: str  # user, assistant, system
    content: str
    timestamp: Optional[str] = None
    model: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    metadata: Optional[Dict] = None

@dataclass
class Conversation:
    """标准化对话格式"""
    id: str
    title: str
    agent: str
    messages: List[Message]
    created_at: str
    updated_at: str
    source_path: str
    word_count: int
    metadata: Optional[Dict] = None

@dataclass
class ExportManifest:
    """导出清单"""
    format_version: str
    exported_at: str
    exporter_version: str
    agents: List[str]
    total_conversations: int
    total_messages: int
    total_size_bytes: int
    conversations: List[Dict]

# ============================================================================
# 解析器
# ============================================================================

class AgentParser:
    """Agent 对话解析器基类"""
    
    def __init__(self, agent_id: str, base_dir: Path):
        self.agent_id = agent_id
        self.base_dir = base_dir
    
    def find_conversation_files(self) -> List[Path]:
        """查找所有对话文件"""
        files = []
        for pattern in ["**/*.md", "**/*.json", "**/*.jsonl"]:
            files.extend(self.base_dir.glob(pattern))
        return [f for f in files if self._is_conversation_file(f)]
    
    def _is_conversation_file(self, path: Path) -> bool:
        """判断是否为对话文件"""
        exclude = ["README", "CHANGELOG", "VERSIONS", "FIXES", "CONFIG", "SKILL"]
        name = path.stem.upper()
        return not any(e in name for e in exclude)
    
    def parse_file(self, path: Path) -> Optional[Conversation]:
        """解析单个文件"""
        raise NotImplementedError


class MarkdownParser(AgentParser):
    """Markdown 格式解析器 (Claude Code, Qwen Code)"""
    
    def parse_file(self, path: Path) -> Optional[Conversation]:
        try:
            content = path.read_text(encoding="utf-8")
            
            # 提取元数据
            conv_id = hashlib.md5(f"{self.agent_id}:{path}".encode()).hexdigest()[:12]
            title = path.stem
            created = self._extract_date(path)
            
            # 解析消息 (简化：整个文件作为单条消息)
            messages = [
                Message(
                    role="assistant",
                    content=content[:50000],  # 限制长度
                    timestamp=created,
                    metadata={"source": str(path), "full_length": len(content)}
                )
            ]
            
            return Conversation(
                id=conv_id,
                title=title,
                agent=self.agent_id,
                messages=messages,
                created_at=created,
                updated_at=created,
                source_path=str(path),
                word_count=len(content.split()),
                metadata={"parser": "markdown", "agent_type": "claude-code"}
            )
        except Exception as e:
            print(f"⚠️  解析失败 {path}: {e}")
            return None
    
    def _extract_date(self, path: Path) -> str:
        import re
        match = re.search(r"(\d{4}-\d{2}-\d{2})", path.stem)
        if match:
            return match.group(1)
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


class OpenClawParser(AgentParser):
    """OpenClaw 格式解析器 (SJLL/龙虾)"""
    
    def parse_file(self, path: Path) -> Optional[Conversation]:
        try:
            if path.suffix == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
                
                conv_id = data.get("id", hashlib.md5(str(path).encode()).hexdigest()[:12])
                title = data.get("title", path.stem)
                created = data.get("created_at", datetime.now().isoformat())
                
                # OpenClaw 任务格式
                messages = [
                    Message(
                        role="user",
                        content=data.get("description", ""),
                        timestamp=created,
                        metadata={"action": data.get("action", {})}
                    )
                ]
                
                return Conversation(
                    id=conv_id,
                    title=title,
                    agent=self.agent_id,
                    messages=messages,
                    created_at=created,
                    updated_at=created,
                    source_path=str(path),
                    word_count=len(str(data).split()),
                    metadata={"parser": "openclaw", "agent_type": "openclaw"}
                )
        except Exception as e:
            print(f"⚠️  解析失败 {path}: {e}")
        return None


class JSONLParser(AgentParser):
    """JSONL 格式解析器 (通用)"""
    
    def parse_file(self, path: Path) -> Optional[Conversation]:
        try:
            messages = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        messages.append(Message(
                            role=data.get("role", "unknown"),
                            content=data.get("content", ""),
                            timestamp=data.get("timestamp"),
                            model=data.get("model"),
                            tool_calls=data.get("tool_calls")
                        ))
            
            if not messages:
                return None
            
            conv_id = hashlib.md5(str(path).encode()).hexdigest()[:12]
            
            return Conversation(
                id=conv_id,
                title=path.stem,
                agent=self.agent_id,
                messages=messages,
                created_at=messages[0].timestamp or datetime.now().isoformat(),
                updated_at=messages[-1].timestamp or datetime.now().isoformat(),
                source_path=str(path),
                word_count=sum(len(m.content.split()) for m in messages),
                metadata={"parser": "jsonl", "agent_type": "generic"}
            )
        except Exception as e:
            print(f"⚠️  解析失败 {path}: {e}")
            return None

# ============================================================================
# 导出器
# ============================================================================

class DataClawParser(AgentParser):
    """DataClaw 格式解析器 (参考 GitHub DataClaw 项目)"""
    
    def parse_file(self, path: Path) -> Optional[Conversation]:
        """解析 DataClaw 格式的 JSONL 文件"""
        try:
            if path.suffix == ".jsonl":
                messages = []
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            # DataClaw 格式
                            messages.append(Message(
                                role=data.get("role", "unknown"),
                                content=data.get("content", ""),
                                timestamp=data.get("timestamp"),
                                model=data.get("model"),
                                metadata={
                                    "source": data.get("source", "dataclaw"),
                                    "privacy_filtered": data.get("privacy_filtered", False)
                                }
                            ))
                
                if not messages:
                    return None
                
                conv_id = hashlib.md5(str(path).encode()).hexdigest()[:12]
                
                return Conversation(
                    id=conv_id,
                    title=path.stem,
                    agent="dataclaw",
                    messages=messages,
                    created_at=messages[0].timestamp or datetime.now().isoformat(),
                    updated_at=messages[-1].timestamp or datetime.now().isoformat(),
                    source_path=str(path),
                    word_count=sum(len(m.content.split()) for m in messages),
                    metadata={"parser": "dataclaw", "agent_type": "dataclaw"}
                )
        except Exception as e:
            print(f"⚠️  解析失败 {path}: {e}")
        return None


class UniversalExporter:
    """通用导出器"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or DEFAULT_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.conversations: List[Conversation] = []
    
    def add_conversations(self, convs: List[Conversation]):
        self.conversations.extend(convs)
    
    def export_jsonl(self) -> Path:
        """导出为 JSONL 格式 (标准化)"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.output_dir / f"agent-memory-{timestamp}.jsonl"
        
        with open(output_file, "w", encoding="utf-8") as f:
            for conv in self.conversations:
                line = {
                    "format_version": EXPORT_FORMAT_VERSION,
                    "conversation": asdict(conv)
                }
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
        
        return output_file
    
    def export_markdown(self) -> Path:
        """导出为 Markdown 格式"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.output_dir / f"agent-memory-{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Universal AI Agent Memory Archive\n\n")
            f.write(f"**Exported**: {datetime.now().isoformat()}\n")
            f.write(f"**Format**: {EXPORT_FORMAT_VERSION}\n")
            f.write(f"**Total Conversations**: {len(self.conversations)}\n\n")
            f.write("---\n\n")
            
            # 按 Agent 分组
            by_agent = {}
            for conv in self.conversations:
                if conv.agent not in by_agent:
                    by_agent[conv.agent] = []
                by_agent[conv.agent].append(conv)
            
            for agent, convs in sorted(by_agent.items()):
                f.write(f"## 🤖 {agent.upper()}\n\n")
                f.write(f"**Count**: {len(convs)}\n\n")
                
                for conv in convs[:50]:  # 限制数量
                    f.write(f"### {conv.title}\n\n")
                    f.write(f"**ID**: `{conv.id}`  \n")
                    f.write(f"**Date**: {conv.created_at}  \n")
                    f.write(f"**Words**: {conv.word_count}\n\n")
                    
                    for msg in conv.messages[:3]:  # 限制消息数量
                        f.write(f"**{msg.role}**: {msg.content[:500]}...\n\n")
                    
                    f.write("---\n\n")
        
        return output_file
    
    def export_manifest(self) -> Path:
        """导出清单文件"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.output_dir / f"MANIFEST-{timestamp}.json"
        
        # 计算统计
        total_messages = sum(len(c.messages) for c in self.conversations)
        total_size = sum(c.word_count * 10 for c in self.conversations)  # 估算
        
        manifest = ExportManifest(
            format_version=EXPORT_FORMAT_VERSION,
            exported_at=datetime.now().isoformat(),
            exporter_version=VERSION,
            agents=list(set(c.agent for c in self.conversations)),
            total_conversations=len(self.conversations),
            total_messages=total_messages,
            total_size_bytes=total_size,
            conversations=[asdict(c) for c in self.conversations]
        )
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(asdict(manifest), f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def export_zip(self, sync_to_vio_snap: bool = True) -> Path:
        """导出为 ZIP 归档包"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        zip_file = self.output_dir / f"agent-memory-archive-{timestamp}.zip"
        
        # 先导出各种格式
        jsonl_file = self.export_jsonl()
        md_file = self.export_markdown()
        manifest_file = self.export_manifest()
        
        # 打包
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in [jsonl_file, md_file, manifest_file]:
                if f.exists():
                    zf.write(f, f.name)
        
        # 清理临时文件
        jsonl_file.unlink()
        md_file.unlink()
        manifest_file.unlink()
        
        # 同步到 vio_snap (Termux 备份目录)
        if sync_to_vio_snap and VIO_SNAP_BACKUP_DIR.exists():
            import shutil
            # 如果输出目录已经是 vio_snap，跳过复制
            if self.output_dir != VIO_SNAP_BACKUP_DIR:
                backup_zip = VIO_SNAP_BACKUP_DIR / zip_file.name
                shutil.copy2(zip_file, backup_zip)
                print(f"  📦 已同步到 vio_snap: {backup_zip}")
        
        return zip_file

# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Universal AI Agent Memory Exporter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python agent-memory-exporter.py --all
  python agent-memory-exporter.py --agents qwq,mycc,sjll
  python agent-memory-exporter.py --format jsonl
  python agent-memory-exporter.py --format zip
  python agent-memory-exporter.py --output /path/to/archive

输出格式:
  - jsonl: 标准化行式 JSON (推荐)
  - markdown: 人类可读格式
  - zip: 完整归档包 (包含所有格式)
        """
    )
    
    parser.add_argument("--all", action="store_true", help="导出所有 Agent")
    parser.add_argument("--agents", default="", help="Agent 列表 (逗号分隔)")
    parser.add_argument("--format", default="all", choices=["jsonl", "markdown", "md", "zip", "all"])
    parser.add_argument("--output", help="输出目录")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    
    args = parser.parse_args()
    
    # 确定 Agent 列表
    if args.all:
        agents = list(AGENT_DIRS.keys())
    elif args.agents:
        agents = [a.strip() for a in args.agents.split(",")]
    else:
        agents = ["qwq", "mycc"]  # 默认
    
    # 设置输出目录
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🗄️  Universal AI Agent Memory Exporter")
    print(f"   Version: {VERSION}")
    print(f"   Format: {EXPORT_FORMAT_VERSION}")
    print("=" * 60)
    print()
    print(f"📂 Agents: {', '.join(agents)}")
    print(f"📁 Output: {output_dir}")
    print(f"📄 Format: {args.format}")
    print()
    
    # 创建导出器
    exporter = UniversalExporter(output_dir)
    
    # 解析并导出
    parsers = {
        "qwq": MarkdownParser,
        "mycc": MarkdownParser,
        "sjll": OpenClawParser,
    }
    
    for agent_id in agents:
        print(f"⏳ 处理 {agent_id}...")
        
        if agent_id not in AGENT_DIRS:
            print(f"  ⚠️  未知 Agent: {agent_id}")
            continue
        
        base_dir = AGENT_DIRS[agent_id]
        if not base_dir.exists():
            print(f"  ⚠️  目录不存在：{base_dir}")
            continue
        
        # 选择解析器
        parser_class = parsers.get(agent_id, MarkdownParser)
        parser = parser_class(agent_id, base_dir)
        
        # 解析文件
        files = parser.find_conversation_files()
        print(f"  📁 找到 {len(files)} 个文件")
        
        for file in files[:100]:  # 限制数量
            conv = parser.parse_file(file)
            if conv:
                exporter.add_conversations([conv])
        
        print(f"  ✅ 完成 {agent_id}")
    
    print()
    print("📤 导出中...")
    
    # 执行导出
    output_files = []
    fmt = args.format
    
    if fmt in ["jsonl", "all"]:
        f = exporter.export_jsonl()
        output_files.append(f)
        print(f"  ✅ JSONL: {f}")
    
    if fmt in ["markdown", "md", "all"]:
        f = exporter.export_markdown()
        output_files.append(f)
        print(f"  ✅ Markdown: {f}")
    
    if fmt in ["zip", "all"]:
        f = exporter.export_zip()
        output_files.append(f)
        print(f"  ✅ ZIP: {f}")
    
    # 导出清单
    manifest = exporter.export_manifest()
    print(f"  ✅ Manifest: {manifest}")
    
    print()
    print("=" * 60)
    print(f"✅ 完成！共导出 {len(exporter.conversations)} 条对话")
    print(f"   输出文件：{len(output_files) + 1} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
