#!/usr/bin/env python3
"""
Qwen Code Context Injection Script
Injects session context (timestamp + memory summary) into conversation.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def get_timestamp():
    """Get formatted current timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M %A')

def get_project_root():
    """Get project root directory."""
    return Path('/root/air/qwq')

def read_qwen_md():
    """Read and summarize QWEN.md memory file."""
    qwen_md = get_project_root() / 'QWEN.md'
    if not qwen_md.exists():
        return "No QWEN.md found."
    
    content = qwen_md.read_text()
    lines = content.split('\n')
    
    # Extract key sections
    summary = []
    in_section = False
    section_name = ""
    
    for line in lines[:60]:  # First 60 lines for summary
        if line.startswith('### '):
            section_name = line[4:].strip()
            in_section = True
            continue
        if line.startswith('## '):
            in_section = False
            continue
        if in_section and line.strip() and not line.startswith('#'):
            summary.append(line.strip())
    
    return '\n'.join(summary[:15])  # Limit to 15 lines

def list_skills():
    """List available skills."""
    skills_dir = get_project_root() / '.qwen' / 'skills'
    if not skills_dir.exists():
        return []
    
    skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_md = skill_dir / 'SKILL.md'
            if skill_md.exists():
                skills.append(skill_dir.name)
    return skills

def inject_context(quick=False, memory_only=False):
    """Main context injection function."""
    timestamp = get_timestamp()
    
    if quick:
        print(f"<timestamp>{timestamp}</timestamp>")
        return
    
    if memory_only:
        print(read_qwen_md())
        return
    
    # Full context
    print("<session-context>")
    print(f"<timestamp>{timestamp}</timestamp>")
    print(f"<project>{get_project_root()}</project>")
    print(f"<user>vicki</user>")
    print()
    print("<memory-summary>")
    print(read_qwen_md())
    print("</memory-summary>")
    print()
    print("<skills>")
    for skill in list_skills():
        print(f"  - {skill}")
    print("</skills>")
    print("</session-context>")

if __name__ == '__main__':
    quick = '--quick' in sys.argv
    memory_only = '--memory' in sys.argv
    inject_context(quick=quick, memory_only=memory_only)
