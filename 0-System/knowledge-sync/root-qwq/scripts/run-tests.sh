#!/bin/bash
#
# AI Team 全面测试脚本
#

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     AI Team 全面测试                            ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "测试时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 测试 1: 服务状态
echo "═══════════════════════════════════════════════"
echo "📊 测试 1: 服务状态检查"
echo "═══════════════════════════════════════════════"

echo -n "AI Team Hub (8772): "
curl -s http://localhost:8772/api/health | grep -q "ok" && pass "运行中" || fail "未运行"

echo -n "free-claude-code (8083): "
curl -s http://localhost:8083/ | grep -q "status" && pass "运行中" || fail "未运行"

echo -n "ssh-gate: "
/root/bin/sv/sv status ssh-gate 2>&1 | grep -q "运行中" && pass "运行中" || fail "未运行"

echo ""

# 测试 2: 对话功能
echo "═══════════════════════════════════════════════"
echo "💬 测试 2: 对话功能"
echo "═══════════════════════════════════════════════"

echo "测试：现在几点了"
curl -s -X POST http://localhost:8772/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"qwq","message":"现在几点了"}' > /tmp/test_chat.json 2>&1

if grep -q "当前时间" /tmp/test_chat.json; then
    pass "自然语言对话 (时间)"
    grep -o '"response":"[^"]*"' /tmp/test_chat.json | head -1
else
    fail "自然语言对话 (时间)"
    cat /tmp/test_chat.json
fi

echo ""
echo "测试：你好"
curl -s -X POST http://localhost:8772/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"qwq","message":"你好"}' > /tmp/test_chat.json 2>&1

if grep -q "助手" /tmp/test_chat.json; then
    pass "问候对话"
else
    fail "问候对话"
fi

echo ""
echo "测试：test"
curl -s -X POST http://localhost:8772/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"qwq","message":"test"}' > /tmp/test_chat.json 2>&1

if grep -q "测试成功" /tmp/test_chat.json; then
    pass "测试命令"
else
    fail "测试命令"
fi

echo ""
echo "测试：date 命令"
curl -s -X POST http://localhost:8772/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"qwq","message":"date"}' > /tmp/test_chat.json 2>&1

if grep -qE "[A-Z][a-z]{2}" /tmp/test_chat.json; then
    pass "命令执行"
else
    fail "命令执行"
fi

echo ""

# 测试 3: 页面访问
echo "═══════════════════════════════════════════════"
echo "🌐 测试 3: 页面访问测试"
echo "═══════════════════════════════════════════════"

echo -n "主页 (/): "
curl -s http://localhost:8772/ | grep -q "AI Team" && pass "可访问" || fail "不可访问"

echo -n "对话 (/chat): "
curl -s http://localhost:8772/chat | grep -q "AI 对话" && pass "可访问" || fail "不可访问"

echo -n "监控 (/monitor): "
curl -s http://localhost:8772/monitor | grep -q "系统监控" && pass "可访问" || fail "不可访问"

echo -n "进度 (/progress): "
curl -s http://localhost:8772/progress | grep -q "进度追踪" && pass "可访问" || fail "不可访问"

echo -n "知识库 (/kb-docs): "
curl -s http://localhost:8772/kb-docs | grep -q "知识库" && pass "可访问" || fail "不可访问"

echo -n "龙虾 (/lobster): "
curl -s http://localhost:8772/lobster | grep -q "龙虾" && pass "可访问" || fail "不可访问"

echo ""

# 测试 4: Termux API
echo "═══════════════════════════════════════════════"
echo "📱 测试 4: Termux API"
echo "═══════════════════════════════════════════════"

echo -n "SSH 连接 (Termux): "
ssh -o ConnectTimeout=5 -p 8022 localhost "echo OK" 2>/dev/null && pass "可连接" || fail "不可连接"

echo ""
echo "Termux API 测试:"

echo -n "  电池状态："
ssh -p 8022 -o ConnectTimeout=10 localhost "termux-battery-status 2>/dev/null | grep -o '\"percentage\": [0-9]*'" && pass "正常" || fail "失败"

echo -n "  弹窗测试："
ssh -p 8022 -o ConnectTimeout=10 localhost "termux-toast '测试' 2>/dev/null" && pass "成功" || fail "失败"

echo -n "  震动测试："
ssh -p 8022 -o ConnectTimeout=10 localhost "termux-vibrate -d 100 2>/dev/null" && pass "成功" || fail "失败"

echo ""

# 测试 5: 历史记录
echo "═══════════════════════════════════════════════"
echo "📝 测试 5: 对话历史记录"
echo "═══════════════════════════════════════════════"

echo -n "历史记录 API: "
curl -s http://localhost:8772/api/history | grep -q "history" && pass "正常" || fail "异常"

echo ""
echo "═══════════════════════════════════════════════"
echo "测试完成！"
echo "═══════════════════════════════════════════════"
