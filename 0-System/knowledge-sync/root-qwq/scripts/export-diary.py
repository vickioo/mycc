#!/usr/bin/env python3
"""
Daily Diary Export - Advanced Version
Aggregates conversations from all AI agents with optional grammar correction.

Usage:
    python export-diary.py [--date YYYY-MM-DD] [--correct] [--output FILE]
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

QWQ_DIR = Path("/root/air/qwq")
DIARIES_DIR = QWQ_DIR / "6-Diaries"


def read_markdown_section(filepath: Path, section_header: str, max_lines: int = 50) -> str:
    """Extract content under a specific markdown section."""
    if not filepath.exists():
        return ""
    
    content = []
    in_section = False
    lines_read = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("## ") and section_header in line:
                in_section = True
                continue
            elif in_section:
                if line.startswith("## "):
                    break
                content.append(line)
                lines_read += 1
                if lines_read >= max_lines:
                    break
    
    return "".join(content).strip()


def read_file_content(filepath: Path, max_lines: int = 100) -> str:
    """Read file content with line limit."""
    if not filepath.exists():
        return ""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = []
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            lines.append(line)
        return "".join(lines)


def correct_text(text: str) -> str:
    """
    Basic grammar/spelling correction.
    Currently performs minimal corrections to preserve original meaning.
    Can be enhanced with LLM-based correction.
    """
    # Common corrections (conservative - preserve original style)
    corrections = {
        "砼": "混凝土",  # Technical term normalization
        "登陆": "登录",  # Common normalization
    }
    
    result = text
    for wrong, correct in corrections.items():
        result = result.replace(wrong, correct)
    
    return result


def collect_qwq_data() -> dict:
    """Collect data from qwq (Qwen Code) agent."""
    data = {
        "status": "",
        "context": "",
        "tasks": []
    }
    
    # Short-term memory
    status_file = QWQ_DIR / "0-System" / "status.md"
    data["status"] = read_markdown_section(status_file, "今日快照")
    
    # Mid-term memory
    context_file = QWQ_DIR / "0-System" / "context.md"
    data["context"] = read_markdown_section(context_file, "本周快照")
    
    # Active tasks
    tasks_dir = QWQ_DIR / "tasks"
    if tasks_dir.exists():
        for task_file in tasks_dir.glob("*.md"):
            data["tasks"].append({
                "name": task_file.stem,
                "content": read_file_content(task_file, 30)
            })
    
    return data


def collect_mycc_data() -> dict:
    """Collect data from mycc (Claude Code) agent."""
    data = {
        "logs": [],
        "tasks": []
    }
    
    mycc_dir = QWQ_DIR / "0-System" / "agents" / "mycc"
    if mycc_dir.exists():
        for log_file in mycc_dir.glob("*.md"):
            data["logs"].append({
                "name": log_file.stem,
                "content": read_file_content(log_file)
            })
    
    return data


def collect_shared_tasks() -> dict:
    """Collect data from shared-tasks directory."""
    data = {
        "completed": [],
        "processing": [],
        "inbox": []
    }
    
    base_dir = QWQ_DIR / "shared-tasks"
    
    for status in ["completed", "processing", "inbox"]:
        status_dir = base_dir / status
        if status_dir.exists():
            for task_file in status_dir.glob("*.md"):
                data[status].append({
                    "name": task_file.stem,
                    "content": read_file_content(task_file)
                })
    
    return data


def generate_diary(date_str: str, apply_correction: bool = False) -> str:
    """Generate daily diary content."""
    
    # Collect all data
    qwq_data = collect_qwq_data()
    mycc_data = collect_mycc_data()
    shared_data = collect_shared_tasks()
    
    # Build diary
    diary = []
    diary.append("# Daily Diary\n")
    diary.append("---\n")
    diary.append(f"\n## 📅 Date\n")
    diary.append(f"\n**{date_str}**\n")
    diary.append("\n---\n")
    
    # qwq section
    diary.append("\n## 🤖 qwq (Qwen Code) - Local\n")
    if qwq_data["status"]:
        diary.append("\n### 今日快照\n")
        content = qwq_data["status"]
        if apply_correction:
            content = correct_text(content)
        diary.append(content)
        diary.append("\n")
    
    if qwq_data["context"]:
        diary.append("\n### 本周上下文\n")
        content = qwq_data["context"]
        if apply_correction:
            content = correct_text(content)
        diary.append(content)
        diary.append("\n")
    
    # mycc section
    if mycc_data["logs"]:
        diary.append("\n## 🤖 mycc (Claude Code) - Local\n")
        for log in mycc_data["logs"]:
            diary.append(f"\n### {log['name']}\n")
            content = log["content"]
            if apply_correction:
                content = correct_text(content)
            diary.append(content)
            diary.append("\n")
    
    # Shared tasks - completed
    if shared_data["completed"]:
        diary.append("\n## ✅ Completed Tasks (Shared)\n")
        for task in shared_data["completed"]:
            diary.append(f"\n### {task['name']}\n")
            content = task["content"]
            if apply_correction:
                content = correct_text(content)
            diary.append(content)
            diary.append("\n")
    
    # Shared tasks - processing
    if shared_data["processing"]:
        diary.append("\n## ⏳ Processing Tasks\n")
        for task in shared_data["processing"]:
            diary.append(f"\n### {task['name']}\n")
            content = task["content"]
            if apply_correction:
                content = correct_text(content)
            diary.append(content)
            diary.append("\n")
    
    # Active tasks
    if qwq_data["tasks"]:
        diary.append("\n## 📋 Active Tasks\n")
        for task in qwq_data["tasks"]:
            diary.append(f"\n### {task['name']}\n")
            content = task["content"]
            if apply_correction:
                content = correct_text(content)
            diary.append(content)
            diary.append("\n")
    
    # Summary section
    diary.append("\n---\n")
    diary.append("\n## 📝 Summary\n")
    diary.append("\n**Key Achievements:**\n")
    diary.append("- \n")
    diary.append("\n**Challenges:**\n")
    diary.append("- \n")
    diary.append("\n**Learnings:**\n")
    diary.append("- \n")
    diary.append("\n**Next Steps:**\n")
    diary.append("- \n")
    
    diary.append("\n---\n")
    diary.append("\n## 🎯 Tomorrow's Focus\n")
    diary.append("\n- \n")
    diary.append("\n---\n")
    diary.append(f"\n*Generated by export-diary.py on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    return "".join(diary)


def main():
    parser = argparse.ArgumentParser(description="Export daily diary from AI agent conversations")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="Date for diary (YYYY-MM-DD)")
    parser.add_argument("--correct", action="store_true",
                        help="Apply grammar/spelling correction")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    # Generate diary
    diary_content = generate_diary(args.date, args.correct)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        year_month = args.date[:7]  # YYYY-MM
        output_dir = DIARIES_DIR / year_month
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{args.date}.md"
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(diary_content)
    
    print(f"✅ Diary exported to: {output_path}")
    print(f"📂 Location: {output_path.parent}")


if __name__ == "__main__":
    main()
