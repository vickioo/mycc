#!/bin/bash
#
# Termux 原生命令探索脚本
# 用途：发现和测试可用的 Termux API 命令
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     Termux 原生命令探索                         ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查 termux-api 是否安装
log "检查 Termux API..."
if command -v termux-battery-status &> /dev/null; then
    log "✅ Termux API 已安装"
else
    warn "❌ Termux API 未安装，执行：pkg install termux-api"
    exit 1
fi

# 命令列表
declare -A COMMANDS=(
    ["termux-battery-status"]="电池状态"
    ["termux-wifi-info"]="WiFi 信息"
    ["termux-network-status"]="网络状态"
    ["termux-location"]="位置信息"
    ["termux-sensor"]="传感器数据"
    ["termux-toast"]="弹窗提示"
    ["termux-vibrate"]="震动反馈"
    ["termux-notification"]="系统通知"
    ["termux-clipboard-get"]="剪贴板读取"
    ["termux-clipboard-set"]="剪贴板写入"
    ["termux-tts-speak"]="语音播放"
    ["termux-volume-set"]="音量控制"
    ["termux-wallpaper"]="壁纸设置"
    ["termux-media-player"]="媒体播放"
    ["termux-camera-photo"]="拍照"
)

echo ""
echo "=== 可用命令列表 ==="
for cmd in "${!COMMANDS[@]}"; do
    if command -v $cmd &> /dev/null; then
        echo -e "  ${GREEN}✅${NC} $cmd - ${COMMANDS[$cmd]}"
    else
        echo -e "  ${RED}❌${NC} $cmd - ${COMMANDS[$cmd]}"
    fi
done

echo ""
echo "=== 实时测试 ==="

# 电池状态
log "测试：电池状态"
termux-battery-status 2>&1 | head -5 || warn "测试失败"
echo ""

# WiFi 信息
log "测试：WiFi 信息"
termux-wifi-info 2>&1 | head -5 || warn "测试失败"
echo ""

# 网络状态
log "测试：网络状态"
termux-network-status 2>&1 | head -5 || warn "测试失败"
echo ""

# 弹窗提示
log "测试：弹窗提示"
termux-toast "Termux API 测试成功" 2>&1 || warn "测试失败"
echo ""

# 震动反馈
log "测试：震动反馈"
termux-vibrate -d 200 2>&1 || warn "测试失败"
echo ""

# 剪贴板测试
log "测试：剪贴板"
echo "Termux 剪贴板测试" | termux-clipboard-set 2>&1 || warn "写入失败"
termux-clipboard-get 2>&1 || warn "读取失败"
echo ""

# 语音播放
log "测试：语音播放"
termux-tts-speak "你好，这是 Termux 语音测试" 2>&1 || warn "测试失败"
echo ""

# 通知测试
log "测试：系统通知"
termux-notification --title "Termux API" --text "通知测试成功" 2>&1 || warn "测试失败"
echo ""

echo "╔════════════════════════════════════════════════╗"
echo "║     测试完成                                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "📋 使用建议:"
echo ""
echo "1. 网络环境识别"
echo "   termux-wifi-info | grep SSID"
echo ""
echo "2. 自动通知"
echo "   termux-notification --title '完成' --text '任务已完成'"
echo ""
echo "3. 语音播报"
echo "   termux-tts-speak '系统消息内容'"
echo ""
echo "4. 剪贴板集成"
echo "   command | termux-clipboard-set"
echo ""
echo "5. 震动反馈"
echo "   termux-vibrate -d 200  # 200ms 震动"
echo ""
