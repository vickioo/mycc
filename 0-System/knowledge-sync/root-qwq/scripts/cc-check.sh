#!/bin/bash
# cc-check.sh - System Health Dashboard (CC & Env)
# Optimized for accuracy and conflict prevention

set -o pipefail

# ANSI Color Codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Config
LOCK_FILE="/tmp/cc-check.lock"
TIMEOUT_SHORT=2
TIMEOUT_LONG=5
PM2_APP="free-claude-code"
PM2_PORT=8082
SSH_HOST_PORT=8022
MYCC_CONFIG="/root/.mycc/current.json"

# Prevent concurrent execution
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo -e "${YELLOW}⚠ Another instance is running. Exiting.${NC}"
    exit 1
fi
trap 'rm -f "$LOCK_FILE"' EXIT

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   System Health Dashboard (CC & Env)  ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo ""

# 1. Check CC Service (free-claude-code proxy)
echo -e "${YELLOW}--- 代理服务 (free-claude-code :$PM2_PORT) ---${NC}"
HEALTH_URL="http://localhost:$PM2_PORT/health"
CC_RESPONSE=$(curl -s --max-time $TIMEOUT_LONG "$HEALTH_URL" 2>&1)
CC_EXIT=$?

if [[ $CC_EXIT -eq 0 ]] && [[ -n "$CC_RESPONSE" ]]; then
    if echo "$CC_RESPONSE" | grep -qi "healthy\|ok\|status"; then
        echo -e "服务状态: ${GREEN}● UP & HEALTHY${NC}"
    else
        echo -e "服务状态: ${YELLOW}● RESPONDING (check content)${NC}"
    fi
    echo -e "接口响应: ${CYAN}$CC_RESPONSE${NC}"
else
    # Fallback: Check PM2 status
    PM2_STATUS=$(pm2 jlist 2>/dev/null | jq -r ".[] | select(.name==\"$PM2_APP\") | .pm2_env.status" 2>/dev/null)
    if [[ "$PM2_STATUS" == "online" ]]; then
        echo -e "服务状态: ${YELLOW}● PM2 ONLINE but API UNREACHABLE${NC}"
        echo -e "可能原因：端口变更或服务卡死"
    else
        echo -e "服务状态: ${RED}● DOWN or NOT RUNNING${NC}"
    fi
    [[ $CC_EXIT -ne 0 ]] && echo -e "错误代码: ${RED}curl exit $CC_EXIT${NC}"
fi
echo ""

# 2. Check Host Tmux/SSH
echo -e "${YELLOW}--- 宿主 SSH/Tmux (localhost:$SSH_HOST_PORT) ---${NC}"
TMUX_OUTPUT=$(ssh -o ConnectTimeout=$TIMEOUT_SHORT -o StrictHostKeyChecking=no -p $SSH_HOST_PORT localhost "tmux ls 2>/dev/null" 2>&1)
SSH_EXIT=$?

if [[ $SSH_EXIT -eq 0 ]] && [[ -n "$TMUX_OUTPUT" ]]; then
    echo -e "会话状态: ${GREEN}● RUNNING${NC}"
    echo -e "会话详情: ${CYAN}$TMUX_OUTPUT${NC}"
else
    if [[ $SSH_EXIT -eq 255 ]] || echo "$TMUX_OUTPUT" | grep -q "Connection refused"; then
        echo -e "会话状态: ${RED}● SSH CONNECTION FAILED${NC}"
    elif echo "$TMUX_OUTPUT" | grep -q "no server running"; then
        echo -e "会话状态: ${YELLOW}● SSH OK but NO TMUX SERVER${NC}"
    else
        echo -e "会话状态: ${RED}● CHECK FAILED${NC}"
        echo -e "错误信息: $TMUX_OUTPUT"
    fi
fi
echo ""

# 3. Check MyCC Connectivity
echo -e "${YELLOW}--- MyCC 连接状态 ---${NC}"
if [[ -f "$MYCC_CONFIG" ]]; then
    URL=$(jq -r '.tunnelUrl // empty' "$MYCC_CONFIG" 2>/dev/null)
    TOKEN=$(jq -r '.routeToken // empty' "$MYCC_CONFIG" 2>/dev/null)
    
    if [[ -n "$URL" ]] && [[ "$URL" != "null" ]]; then
        echo -e "隧道 URL: ${CYAN}$URL${NC}"
        echo -e "连接码：${CYAN}$TOKEN${NC}"
        
        MYCC_HEALTH=$(curl -s --max-time $TIMEOUT_LONG "$URL/health" 2>&1)
        if echo "$MYCC_HEALTH" | grep -qi "ok"; then
            echo -e "公网状态: ${GREEN}● ACCESSIBLE${NC}"
        else
            echo -e "公网状态: ${RED}● FAILED${NC}"
            [[ -n "$MYCC_HEALTH" ]] && echo -e "响应内容: $MYCC_HEALTH"
        fi
    else
        echo -e "配置状态: ${RED}● tunnelUrl MISSING${NC}"
    fi
else
    echo -e "配置状态: ${RED}● $MYCC_CONFIG NOT FOUND${NC}"
fi
echo ""

# 4. Container Resources
echo -e "${YELLOW}--- 容器资源占用 ---${NC}"
DISK_USAGE=$(df -h / 2>/dev/null | awk 'NR==2{print $5 " used (" $3 "/" $2 ")"}')
echo -e "磁盘 (/): ${CYAN}$DISK_USAGE${NC}"

MEM_INFO=$(free -h 2>/dev/null | awk 'NR==2{printf "Total: %s, Used: %s, Free: %s (%.1f%%)", $2, $3, $4, $3*100/$2}')
echo -e "内存：${CYAN}$MEM_INFO${NC}"
echo ""

# 5. Gemini CLI Status
echo -n "Gemini CLI: "
if [[ -f "/root/.geminiignore" ]]; then
    echo -e "${GREEN}Optimized${NC}"
else
    echo -e "${YELLOW}Not optimized${NC}"
fi

# 6. CC Clash Tunnel Status
echo -n "CC Clash Tunnel: "
CLASH_IP=$(curl -s --socks5-hostname localhost:7890 --connect-timeout 3 https://api.ip.sb/ip 2>/dev/null)
if [[ -n "$CLASH_IP" ]] && [[ "$CLASH_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${GREEN}Running (Exit IP: $CLASH_IP)${NC}"
else
    echo -e "${YELLOW}Not working${NC}"
fi

echo ""
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   Check completed at $(date '+%H:%M:%S')${NC}"
echo -e "${BLUE}=======================================${NC}"
