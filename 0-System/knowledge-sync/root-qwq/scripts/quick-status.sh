#!/bin/bash
# Quick Status Check - 快速状态检查

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  📊 系统状态快速检查                                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# PM2 进程
echo "📦 PM2 进程:"
pm2 status 2>/dev/null | grep -E "(5min-report|continuous-monitor)" || echo "  未运行"
echo

# 心跳
echo "💓 心跳计数:"
cat /tmp/heartbeat-counter.txt 2>/dev/null && echo "  次" || echo "  未初始化"
echo

# 服务检查
echo "🔍 服务检查:"
for service in "mobile-web:8766" "clash:7890"; do
    name="${service%%:*}"
    port="${service##*:}"
    if curl -s --connect-timeout 2 "http://localhost:$port" >/dev/null 2>&1; then
        echo "  ✅ $name (端口 $port)"
    elif curl -s --socks5-hostname localhost:$port --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
        echo "  ✅ $name (SOCKS5)"
    else
        echo "  ❌ $name"
    fi
done
echo

# 最近日志
echo "📝 最近日志 (最后 5 行):"
tail -5 /tmp/5min-report.log 2>/dev/null || echo "  无日志"
echo

# 监控状态
echo "🛡️  监控状态:"
if pgrep -f "continuous-monitor" >/dev/null 2>&1; then
    echo "  ✅ 持续监控运行中"
else
    echo "  ❌ 持续监控未运行"
fi

if pgrep -f "5min-report" >/dev/null 2>&1; then
    echo "  ✅ 5 分钟汇报运行中"
else
    echo "  ❌ 5 分钟汇报未运行"
fi
