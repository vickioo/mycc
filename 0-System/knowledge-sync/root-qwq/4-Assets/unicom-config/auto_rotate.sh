#!/bin/bash
# 自动轮换/备灾模型切换脚本 (联通云优先版)

# 定义模型优先级列表
# 规则：联通云 Claude -> NVIDIA 免费 -> 智谱赠送额度 -> 硅基代金券 -> OpenRouter 免费
MODELS=(
    "Unicloud-Claude-3.5-Sonnet|unicloud/claude-3-5-sonnet-20241022"
    "Unicloud-Claude-3-Haiku|unicloud/claude-3-haiku"
    "NVIDIA-Qwen3-Coder|nvidia_nim/qwen/qwen3-coder-480b-a35b-instruct"
    "Zhipu-GLM-4.5-Air|zhipu/glm-4.5-air"
    "SiliconFlow-DeepSeek-V3|silicon_flow/deepseek-ai/DeepSeek-V3"
    "SiliconFlow-Qwen2.5-Coder-32B|silicon_flow/Qwen/Qwen2.5-Coder-32B-Instruct"
    "OpenRouter-Step-Free|open_router/stepfun/step-3.5-flash:free"
)

SKILL_DIR="/root/air/mycc/.claude/skills/cc-switch"
SWITCH_SCRIPT="${SKILL_DIR}/scripts/switch.sh"

echo ">> 启动模型轮替实际连通性测试..."
echo ">> 优先级：联通云 Claude -> NVIDIA -> 智谱 -> SiliconFlow -> OpenRouter"

for M_INFO in "${MODELS[@]}"; do
    NAME=$(echo $M_INFO | cut -d'|' -f1)
    MODEL_PATH=$(echo $M_INFO | cut -d'|' -f2)
    
    echo "------------------------------------------------"
    echo ">> [TEST] 正在切换至：$NAME ($MODEL_PATH)"
    
    if bash "$SWITCH_SCRIPT" "$MODEL_PATH"; then
        echo "SUCCESS: $NAME 切换并接口测试成功！"
        echo ">> 找到可用模型，停止测试。当前使用：$NAME"
        exit 0
    else
        echo "FAIL: $NAME 测试失败，尝试下一个..."
    fi
done

echo "------------------------------------------------"
echo ">> 轮替测试结束。无可用模型，请检查配置。"
exit 1
