#!/bin/bash
# Codex CLI wrapper - 通过 free-claude-code 代理调用
# 用法：./codex-proxy.sh "你的提示词"

API_URL="http://localhost:8083/v1/messages"
API_KEY="sk-ant-api03-localproxy-00000000000000000000000000000000000000000000000"
MODEL="claude-3-5-sonnet-20241022"

if [ -z "$1" ]; then
    echo "用法：$0 \"提示词\""
    echo ""
    echo "示例:"
    echo "  $0 \"帮我写一个 Python 函数计算斐波那契数列\""
    echo "  $0 \"检查当前目录的代码结构\""
    exit 1
fi

PROMPT="$1"

# 调用 API
curl -s "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d "{
        \"model\": \"$MODEL\",
        \"messages\": [{\"role\": \"user\", \"content\": \"$PROMPT\"}],
        \"max_tokens\": 4096
    }" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'content' in data:
        print(data['content'])
    elif 'choices' in data:
        print(data['choices'][0]['message']['content'])
    else:
        print(json.dumps(data, indent=2))
except:
    print(sys.stdin.read())
"
