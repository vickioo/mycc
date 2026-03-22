---
name: inject-context
description: Inject session context (timestamp + memory summary) into conversation. Triggers: "/inject-context", "load context", "session context"
---

# inject-context — Session Context Injection

Injects current timestamp and project memory summary into the conversation context.

## Triggers

- "/inject-context"
- "load context"
- "session context"
- "show memory"

## Execution

1. Run the context injection script
2. Output timestamp block
3. Summarize QWEN.md key points
4. List available skills and commands

## Script Location

```
.qwen/skills/inject-context/scripts/inject.py
```

## Usage

```bash
# Full context injection
python3 .qwen/skills/inject-context/scripts/inject.py

# Quick timestamp only
python3 .qwen/skills/inject-context/scripts/inject.py --quick

# Memory summary only
python3 .qwen/skills/inject-context/scripts/inject.py --memory
```

## Output Format

```
<session-context>
<timestamp>2026-03-07 14:30 Saturday</timestamp>
<project>/root/air/qwq</project>
<memory-summary>...key points from QWEN.md...</memory-summary>
</session-context>
```
