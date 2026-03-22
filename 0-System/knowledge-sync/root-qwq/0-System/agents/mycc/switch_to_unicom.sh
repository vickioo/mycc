#!/bin/bash
# 切换到联通云 Claude 优先模式

ENV_FILE="/root/free-claude-code/.env"
PROXY_DIR="/root/free-claude-code"
PORT=8083

echo ">> 切换到联通云 Claude 优先模式..."

# 备份当前配置
cp $ENV_FILE ${ENV_FILE}.bak

# 更新 PROVIDER_PRIORITY
sed -i 's|^PROVIDER_PRIORITY=.*|PROVIDER_PRIORITY="unicloud,nvidia_nim,silicon_flow,open_router,zhipu"|g' $ENV_FILE

# 更新默认模型为联通云 Claude
sed -i 's|^MODEL=.*|MODEL="unicloud/claude-3-5-sonnet-20241022"|g' $ENV_FILE

echo ">> 配置已更新，重启代理服务..."
pm2 restart claude-proxy

sleep 3

# 测试连通性
echo ">> 测试联通云 Claude 接口..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:$PORT/v1/messages/count_tokens \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"unicloud/claude-3-5-sonnet-20241022\", \"messages\": [{\"role\": \"user\", \"content\": \"test\"}]}")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "SUCCESS: 联通云 Claude 已启用！"
    echo ">> 优先级：联通云 -> NVIDIA -> SiliconFlow -> OpenRouter"
    exit 0
else
    echo "ERROR: 联通云测试失败 (HTTP $HTTP_STATUS)"
    echo ">> 恢复原配置..."
    mv ${ENV_FILE}.bak $ENV_FILE
    pm2 restart claude-proxy
    echo "FALLBACK: 已回退到原配置"
    exit 1
fi
