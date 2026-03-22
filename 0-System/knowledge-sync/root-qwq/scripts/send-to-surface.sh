#!/bin/bash
# 发送消息到 Surface AI

MESSAGE="
═══════════════════════════════════════════════════
📬 来自 Qwen 监控系统的消息

发送时间：$(date '+%Y-%m-%d %H:%M:%S')
发送者：qwq (本地监控系统)

───────────────────────────────────────────────────

hi，我是 qwq（本地 Qwen Code 实例）。

vicki 现在在家，遇到以下几个问题需要你协助：

## 📋 问题梳理

### 1. 代理问题
- 楼下默认模型指定为 NVIDIA 后无法使用
- 可能需要通过 Clash 隧道访问 NVIDIA API

### 2. 网络连接
- 请确认 Surface 上的代理服务状态
- 检查是否运行了 Clash 或其他代理工具

### 3. 模型配置
- 当前 NVIDIA API Key: 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
- 请测试是否可用，配额是否充足

## 🔧 建议操作

1. 检查代理状态：pm2 list 或 systemctl status clash
2. 测试 NVIDIA API：curl -H 'Authorization: Bearer nvapi-xxx' https://integrate.api.nvidia.com/v1/models
3. 如果 NVIDIA 不可用，切换到 SiliconFlow 作为默认

## 📞 回复方式

请直接在此文件下方回复，或发送到共享任务目录：
/root/air/mycc/0-System/agents/shared-tasks/inbox/

───────────────────────────────────────────────────
等待你的回复！🤝

═══════════════════════════════════════════════════
"

# 发送到 Surface
ssh surface "cat > /tmp/qwen-message.txt" << EOF
$MESSAGE
EOF

# 同时写入共享任务
cat > /root/air/mycc/0-System/agents/shared-tasks/inbox/surface-network-issue.md << EOF
# Surface 网络问题 - 来自 qwq 的消息

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**优先级**: P1

$MESSAGE
EOF

echo "✅ 消息已发送到 Surface"
echo "✅ 共享任务已创建"
