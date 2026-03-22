#!/bin/bash
#
# 启动 AI Team Mobile Web Interface V1 (经典版)
#

cd /root/air/qwq/mobile-web-v1

echo "╔════════════════════════════════════════════════╗"
echo "║     AI Team Mobile V1 (经典版)                 ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "0.0.0.0")

echo "🚀 启动服务..."
echo ""
echo "📱 访问地址:"
echo "   本机：http://localhost:8765"
echo "   局域网：http://$LOCAL_IP:8765"
echo ""
echo "🔄 V2 新版：http://localhost:8766"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
