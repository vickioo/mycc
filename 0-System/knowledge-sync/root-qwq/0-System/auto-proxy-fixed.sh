#!/bin/bash
#
# 自动代理配置脚本 - 添加到 ~/.bashrc 或 ~/.zshrc
# 功能：检测 CC Clash Tunnel 状态，自动配置代理环境变量
#
# 极速优化：使用 ss 命令检测端口，零延迟
# 修复：移除后台任务，避免阻塞

setup_cc_proxy() {
    local PROXY_HOST="localhost"
    local SOCKS_PORT="7890"
    local HTTP_PORT="7891"

    # 最快检查：使用 ss 命令检测端口监听状态（内核级别，零延迟）
    local TUNNEL_RUNNING=false

    if command -v ss &>/dev/null; then
        # ss 命令直接查询内核网络栈，无网络开销
        if ss -tlnp 2>/dev/null | grep -q ":${SOCKS_PORT}.*ssh"; then
            TUNNEL_RUNNING=true
        fi
    else
        # 降级方案：检查 PID 文件
        if [ -f "/tmp/cc-clash-tunnel.pid" ]; then
            local PID=$(cat /tmp/cc-clash-tunnel.pid 2>/dev/null)
            if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
                TUNNEL_RUNNING=true
            fi
        fi
    fi

    # 如果隧道运行中，自动设置代理
    if [ "$TUNNEL_RUNNING" = true ]; then
        export ALL_PROXY="socks5h://${PROXY_HOST}:${SOCKS_PORT}"
        export http_proxy="http://${PROXY_HOST}:${HTTP_PORT}"
        export https_proxy="http://${PROXY_HOST}:${HTTP_PORT}"
        export HTTP_PROXY="http://${PROXY_HOST}:${HTTP_PORT}"
        export HTTPS_PROXY="http://${PROXY_HOST}:${HTTP_PORT}"
        # 只在交互式 shell 输出提示
        if [ -t 1 ]; then
            echo -e "\033[0;32m✅ CC Clash Tunnel 已激活 - 代理：${PROXY_HOST}:${SOCKS_PORT}\033[0m"
        fi
    fi
}

# 立即执行（用于新 shell 会话）- 直接调用，不阻塞
setup_cc_proxy
