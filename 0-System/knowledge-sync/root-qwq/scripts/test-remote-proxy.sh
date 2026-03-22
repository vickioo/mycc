#!/bin/bash
#
# U18 远端代理测试脚本
# 用途：测试通过手机 VPN 的 SSH 反向隧道访问外网
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "${BLUE}[i]${NC} $1"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     U18 远端代理测试 (手机 VPN)                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Configuration
PROXY_PORT="${1:-1080}"
SSH_HOST="${2:-gate}"
TIMEOUT=10

info "配置：代理端口=$PROXY_PORT, SSH 主机=$SSH_HOST, 超时=${TIMEOUT}s"
echo ""

# 1. 检查 SSH 隧道
info "检查 SSH 隧道状态..."
if pgrep -f "ssh.*-D $PROXY_PORT" > /dev/null 2>&1; then
    log "SSH 隧道运行中 (端口 $PROXY_PORT)"
else
    warn "SSH 隧道未运行"
    echo "    启动命令：ssh -N -f -D $PROXY_PORT $SSH_HOST"
    echo ""
    read -p "是否现在启动？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ssh -N -f -D $PROXY_PORT $SSH_HOST
        sleep 2
        if pgrep -f "ssh.*-D $PROXY_PORT" > /dev/null 2>&1; then
            log "SSH 隧道已启动"
        else
            error "SSH 隧道启动失败"
            exit 1
        fi
    fi
fi
echo ""

# 2. 测试基础连通性
info "测试基础连通性 (获取出口 IP)..."
EXIT_IP=$(curl -s --socks5-h localhost:$PROXY_PORT https://api.ip.sb/ip --connect-timeout $TIMEOUT 2>/dev/null || echo "")
if [ -n "$EXIT_IP" ]; then
    log "出口 IP: $EXIT_IP"
else
    error "无法获取出口 IP"
fi
echo ""

# 3. 测试 Google 访问
info "测试 Google 访问..."
GOOGLE_CODE=$(curl -s --socks5-h localhost:$PROXY_PORT https://www.google.com -o /dev/null -w '%{http_code}' --connect-timeout $TIMEOUT 2>/dev/null || echo "000")
if [ "$GOOGLE_CODE" = "200" ] || [ "$GOOGLE_CODE" = "301" ]; then
    log "Google 访问成功 (HTTP $GOOGLE_CODE)"
else
    error "Google 访问失败 (HTTP $GOOGLE_CODE)"
fi
echo ""

# 4. 测试 GitHub 访问
info "测试 GitHub API 访问..."
GITHUB_CODE=$(curl -s --socks5-h localhost:$PROXY_PORT https://api.github.com -o /dev/null -w '%{http_code}' --connect-timeout $TIMEOUT 2>/dev/null || echo "000")
if [ "$GITHUB_CODE" = "200" ]; then
    log "GitHub API 访问成功 (HTTP $GITHUB_CODE)"
else
    error "GitHub API 访问失败 (HTTP $GITHUB_CODE)"
fi
echo ""

# 5. 测试 Anthropic API (Claude)
info "测试 Anthropic API 访问..."
ANTHROPIC_CODE=$(curl -s --socks5-h localhost:$PROXY_PORT https://api.anthropic.com -o /dev/null -w '%{http_code}' --connect-timeout $TIMEOUT 2>/dev/null || echo "000")
if [ "$ANTHROPIC_CODE" = "200" ] || [ "$ANTHROPIC_CODE" = "401" ]; then
    log "Anthropic API 可访问 (HTTP $ANTHROPIC_CODE)"
else
    error "Anthropic API 访问失败 (HTTP $ANTHROPIC_CODE)"
fi
echo ""

# 6. 测试 Gemini CLI (如果已安装)
if command -v gemini &> /dev/null; then
    info "测试 Gemini CLI..."
    export ALL_PROXY=socks5h://localhost:$PROXY_PORT
    GEMINI_OUTPUT=$(timeout 30 gemini 'Hello, just say OK' 2>&1 | head -3 || echo "Timeout/Error")
    if echo "$GEMINI_OUTPUT" | grep -q "Loaded cached credentials"; then
        log "Gemini CLI 凭据已加载"
    else
        warn "Gemini CLI 输出：$GEMINI_OUTPUT"
    fi
    unset ALL_PROXY
    echo ""
fi

# 7. 速度测试 (可选)
info "速度测试 (下载测试文件)..."
START_TIME=$(date +%s.%N)
DOWNLOAD_SIZE=$(curl -s --socks5-h localhost:$PROXY_PORT https://speed.hetzner.de/100MB.bin -o /dev/null -w '%{size_download}' --connect-timeout $TIMEOUT --max-time 30 2>/dev/null || echo "0")
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc 2>/dev/null || echo "N/A")
if [ "$DOWNLOAD_SIZE" != "0" ] && [ -n "$DURATION" ] && [ "$DURATION" != "N/A" ]; then
    SPEED=$(echo "scale=2; $DOWNLOAD_SIZE / $DURATION / 1024 / 1024" | bc 2>/dev/null || echo "N/A")
    log "下载速度：${SPEED} MB/s (${DOWNLOAD_SIZE} bytes in ${DURATION}s)"
else
    warn "速度测试失败或超时"
fi
echo ""

# 总结
echo "╔════════════════════════════════════════════════╗"
echo "║     测试总结                                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

if [ -n "$EXIT_IP" ] && { [ "$GOOGLE_CODE" = "200" ] || [ "$GOOGLE_CODE" = "301" ]; }; then
    log "✅ 远端代理工作正常"
    echo ""
    echo "出口 IP: $EXIT_IP"
    echo "使用方式:"
    echo "  export ALL_PROXY=socks5h://localhost:$PROXY_PORT"
    echo "  gemini 'Hello'"
else
    error "❌ 远端代理存在问题"
    echo ""
    echo "建议检查:"
    echo "  1. 手机 VPN 是否已启动"
    echo "  2. SSH 连接是否正常"
    echo "  3. gate 服务器是否可达"
fi
echo ""
