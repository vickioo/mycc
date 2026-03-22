#!/usr/bin/env python3
"""
知识库索引生成器
扫描 Markdown 文件，生成网页版索引
"""

import os
import re
from pathlib import Path
from datetime import datetime

QWQ_DIR = Path("/root/air/qwq")
OUTPUT_DIR = QWQ_DIR / "mobile-web" / "knowledge"

# 目录映射（中文显示名）
DIR_NAMES = {
    "0-System": "🧠 系统记忆",
    "1-Inbox": "📥 收集箱",
    "2-Projects": "🚀 项目",
    "3-Thinking": "💡 思考",
    "4-Assets": "📦 资产",
    "5-Archive": "🗄️ 归档",
    "6-Diaries": "📔 日记",
    "tasks": "📋 任务",
    "shared-tasks": "🤖 协同任务",
    "agents-team": "🤖 Agent 团队",
    "mobile-web": "📱 移动端",
    ".qwen/skills": "⚡ 技能",
}

# 排除的目录
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", ".qwen/tmp"}

# 排除的文件
EXCLUDE_FILES = {"CHANGELOG.md", "VERSIONS.md", "FIXES.md"}


def extract_title(content: str) -> str:
    """从 Markdown 内容提取标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def extract_date_from_path(path: Path) -> str:
    """从路径提取日期"""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', str(path))
    if match:
        return match.group(1)
    return ""


def scan_markdown_files() -> dict:
    """扫描所有 Markdown 文件"""
    index = {}
    
    for md_file in QWQ_DIR.rglob("*.md"):
        # 跳过排除目录
        if any(exclude in str(md_file) for exclude in EXCLUDE_DIRS):
            continue
        
        # 跳过排除文件
        if md_file.name in EXCLUDE_FILES:
            continue
        
        # 获取相对路径
        rel_path = md_file.relative_to(QWQ_DIR)
        parts = rel_path.parts
        
        # 获取一级目录
        root_dir = parts[0] if len(parts) > 1 else "."
        
        if root_dir not in index:
            index[root_dir] = []
        
        # 读取文件内容
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            title = extract_title(content) or md_file.stem
            word_count = len(content.split())
            created_date = extract_date_from_path(md_file)
        except:
            title = md_file.stem
            word_count = 0
            created_date = ""
        
        index[root_dir].append({
            "path": str(rel_path),
            "title": title,
            "file": md_file.name,
            "dir": str(rel_path.parent),
            "words": word_count,
            "date": created_date,
        })
    
    # 排序
    for dir_name in index:
        index[dir_name].sort(key=lambda x: x["date"] or "", reverse=True)
    
    return index


def generate_html(index: dict) -> str:
    """生成 HTML 索引页面"""
    
    # 生成目录导航
    nav_items = []
    for dir_name, files in sorted(index.items()):
        display_name = DIR_NAMES.get(dir_name, dir_name)
        nav_items.append(f'<a href="#{dir_name}" class="nav-item">{display_name} ({len(files)})</a>')
    
    nav_html = '\n'.join(nav_items)
    
    # 生成文件列表
    sections = []
    for dir_name, files in sorted(index.items()):
        display_name = DIR_NAMES.get(dir_name, dir_name)
        
        file_items = []
        for f in files:
            date_badge = f'<span class="date-badge">{f["date"]}</span>' if f["date"] else ''
            file_items.append(f'''
            <div class="file-item">
                <a href="/knowledge/{f['path']}" class="file-link">
                    <span class="file-title">{f["title"]}</span>
                    {date_badge}
                </a>
                <span class="file-meta">{f["words"]} 字</span>
            </div>
            ''')
        
        files_html = '\n'.join(file_items)
        
        sections.append(f'''
        <section id="{dir_name}" class="section">
            <h2 class="section-title">{display_name}</h2>
            <div class="file-list">
                {files_html}
            </div>
        </section>
        ''')
    
    sections_html = '\n'.join(sections)
    
    # 统计
    total_files = sum(len(files) for files in index.values())
    total_words = sum(f["words"] for files in index.values() for f in files)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识库索引 - qwq</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 15px;
        }}
        .stat {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }}
        .nav {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            position: sticky;
            top: 20px;
            z-index: 100;
        }}
        .nav-item {{
            background: #f0f0f0;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            color: #333;
            font-size: 0.9em;
            transition: all 0.3s;
        }}
        .nav-item:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}
        .section {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .section-title {{
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .file-list {{
            display: grid;
            gap: 10px;
        }}
        .file-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        .file-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
        }}
        .file-link {{
            text-decoration: none;
            color: #333;
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .file-title {{
            font-weight: 500;
        }}
        .date-badge {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
        .file-meta {{
            color: #6c757d;
            font-size: 0.85em;
        }}
        .search-box {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            margin-bottom: 20px;
        }}
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            h1 {{ font-size: 1.5em; }}
            .nav {{
                position: static;
                flex-direction: column;
            }}
            .stats {{ flex-direction: column; gap: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 知识库索引</h1>
            <p>本地知识库网页版 - 支持全文链接跳转</p>
            <div class="stats">
                <div class="stat">📄 {total_files} 文档</div>
                <div class="stat">📝 {total_words:,} 字</div>
                <div class="stat">📁 {len(index)} 目录</div>
                <div class="stat">🕐 {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
            </div>
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 搜索文档标题..." onkeyup="filterFiles()">
        </header>
        
        <nav class="nav">
            {nav_html}
        </nav>
        
        <main>
            {sections_html}
        </main>
    </div>
    
    <script>
        function filterFiles() {{
            const query = document.getElementById('searchBox').value.toLowerCase();
            document.querySelectorAll('.file-item').forEach(item => {{
                const title = item.querySelector('.file-title').textContent.toLowerCase();
                item.style.display = title.includes(query) ? '' : 'none';
            }});
        }}
        
        // 平滑滚动
        document.querySelectorAll('.nav-item').forEach(link => {{
            link.addEventListener('click', e => {{
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }});
        }});
    </script>
</body>
</html>
'''
    return html


def copy_markdown_files(index: dict):
    """复制 Markdown 文件到 knowledge 目录"""
    for dir_name, files in index.items():
        for f in files:
            src = QWQ_DIR / f["path"]
            dst = OUTPUT_DIR / f["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
            except Exception as e:
                print(f"⚠️  复制失败 {f['path']}: {e}")


def update_html_links(index: dict):
    """更新 HTML 中的链接路径"""
    html_path = OUTPUT_DIR / "index.html"
    if not html_path.exists():
        return
    
    content = html_path.read_text(encoding='utf-8')
    # 将 /knowledge/ 路径替换为 /kb-files/
    content = content.replace('href="/knowledge/', 'href="/kb-files/')
    html_path.write_text(content, encoding='utf-8')


def main():
    print("📚 生成知识库索引...")
    
    # 扫描文件
    index = scan_markdown_files()
    print(f"✅ 扫描到 {sum(len(f) for f in index.values())} 个 Markdown 文件")
    
    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 复制 Markdown 文件
    print("📋 复制 Markdown 文件...")
    copy_markdown_files(index)
    
    # 生成 HTML
    print("🌐 生成 HTML 索引...")
    html = generate_html(index)
    (OUTPUT_DIR / "index.html").write_text(html, encoding='utf-8')
    
    # 更新链接路径
    print("🔗 更新链接路径...")
    update_html_links(index)
    
    # 生成 README
    readme = f"""# 知识库网页版

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**文档数量**: {sum(len(f) for f in index.values())}
**总字数**: {sum(f["words"] for files in index.values() for f in files):,}

## 访问方式

1. 启动 mobile-web 服务
2. 访问：http://localhost:8769/kb

## 目录结构

"""
    for dir_name, files in sorted(index.items()):
        display_name = DIR_NAMES.get(dir_name, dir_name)
        readme += f"- **{display_name}**: {len(files)} 文档\n"
    
    (OUTPUT_DIR / "README.md").write_text(readme, encoding='utf-8')
    
    print("✅ 完成！访问：http://localhost:8769/kb")


if __name__ == "__main__":
    main()
