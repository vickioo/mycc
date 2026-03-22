#!/bin/bash
# Qwen Code Context Injection Script
# Usage: source scripts/inject-context.sh  OR  ./scripts/inject-context.sh

# Generate current timestamp
export QWQ_CONTEXT_TIMESTAMP=$(date '+%Y-%m-%d %H:%M %A')

# Output context block (can be prepended to prompts)
cat << 'EOF'
<context>
<timestamp>$(date '+%Y-%m-%d %H:%M %A')</timestamp>
<project>/root/air/qwq</project>
<memory-file>/root/air/qwq/QWEN.md</memory-file>
</context>
EOF

# Auto-load QWEN.md summary if exists
if [ -f "QWEN.md" ]; then
    echo ""
    echo "=== QWEN.md Memory Loaded ==="
    head -50 QWEN.md
fi
