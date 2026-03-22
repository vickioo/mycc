# Daily Diary System

> Structured daily journals aggregated from all AI agent conversations

---

## 📁 Directory Structure

```
6-Diaries/
├── 2026-03/
│   ├── 2026-03-07.md    # Today's diary
│   └── ...
└── README.md            # This file
```

---

## 🚀 Quick Start

### Export Today's Diary

```bash
# Simple export
python3 /root/air/qwq/scripts/export-diary.py

# Export with grammar correction
python3 /root/air/qwq/scripts/export-diary.py --correct

# Export specific date
python3 /root/air/qwq/scripts/export-diary.py --date 2026-03-07

# Custom output path
python3 /root/air/qwq/scripts/export-diary.py -o /path/to/diary.md
```

### Bash Script (Alternative)

```bash
/root/air/qwq/scripts/export-daily-diary.sh
```

---

## 📊 Data Sources

The diary aggregates content from:

| Source | Location | Content |
|--------|----------|---------|
| **qwq** | `0-System/status.md` | Short-term memory (today) |
| **qwq** | `0-System/context.md` | Mid-term memory (week) |
| **mycc** | `0-System/agents/mycc/` | Agent logs and tasks |
| **Shared** | `shared-tasks/completed/` | Completed tasks |
| **Shared** | `shared-tasks/processing/` | In-progress tasks |
| **Tasks** | `tasks/*.md` | Active task documents |

---

## 📝 Diary Structure

Each daily diary includes:

1. **Date** - Current date
2. **qwq Conversations** - Local Qwen Code agent data
3. **mycc Conversations** - Claude Code agent logs
4. **Shared Tasks** - Completed and processing tasks
5. **Active Tasks** - Current work items
6. **Summary** - Key achievements, challenges, learnings
7. **Tomorrow's Focus** - Next day priorities

---

## 🔧 Grammar Correction

The `--correct` flag applies conservative text corrections:

- Common character normalization (e.g., 登陆 → 登录)
- Technical term standardization
- Preserves original style and meaning

To add more corrections, edit `correct_text()` in `export-diary.py`.

---

## 📅 Daily Workflow

### Morning
```bash
# Review yesterday's diary
cat 6-Diaries/2026-03/2026-03-06.md
```

### Evening
```bash
# Export today's diary
python3 scripts/export-diary.py --correct
```

### Weekly Review
```bash
# List all diaries this week
ls -la 6-Diaries/2026-03/
```

---

## 🎯 Tips

1. **Preserve Original**: The export keeps original content intact
2. **Minimal Correction**: Only obvious typos are fixed
3. **Structured Format**: Easy to parse for periodic summaries
4. **Incremental**: Run multiple times - always overwrites current day

---

## 📈 Future Enhancements

- [ ] LLM-based grammar correction
- [ ] Weekly/monthly summary generation
- [ ] Cross-agent conversation threading
- [ ] Searchable index
- [ ] PDF export option

---

*System Version: 1.0*
*Last Updated: 2026-03-07*
