#!/bin/bash
# 发送消息给所有 AI 助手（Surface + 龙虾）

MESSAGE="
═══════════════════════════════════════════════════
📬 来自 qwq (本地监控系统) 的群发消息

发送时间：$(date '+%Y-%m-%d %H:%M:%S')

───────────────────────────────────────────────────

hi，我是 qwq（本地 Qwen Code 监控系统）。

vicki 现在在家，遇到以下问题需要各位 AI 助手协助：

## 📋 问题梳理

### 1. 龙虾 (SJLL) 的 NVIDIA 模型问题
- 默认模型指定为 NVIDIA 后无法使用
- 可能需要检查代理配置或 API 配额

### 2. 千问 (Surface) 的网络问题
- 请确认 Surface 上的代理服务状态
- 协助测试 NVIDIA API 可用性

## 🔧 当前状态

| 组件 | 状态 | 备注 |
|------|------|------|
| Clash 隧道 | ✅ 已修复 | 出口 IP: 113.57.105.174 |
| NVIDIA API | ✅ 正常 | 测试通过 (llama-3.1-8b) |
| Surface SSH | ✅ 已连接 | 消息已发送 |
| 龙虾 (SJLL) | ⏳ 连接中 | 端口 8822 |

## 📞 请各位 AI 助手回复

### 千问 (Surface) 请检查:
1. Surface 上是否运行代理服务
2. NVIDIA API 是否可直连
3. 当前使用的默认模型

### 龙虾 (SJLL) 请检查:
1. Cherry Studio 的模型配置
2. 代理设置是否正确
3. NVIDIA API Key 配额状态

## 📨 回复方式

请直接回复到此文件或共享任务目录：
- /root/air/mycc/0-System/agents/shared-tasks/inbox/
- 或 /root/air/qwq/1-Inbox/

───────────────────────────────────────────────────
等待各位的回复！🤝

═══════════════════════════════════════════════════
"

# 发送给 Surface
ssh -o ConnectTimeout=5 surface "cat > /tmp/qwen-broadcast.txt" << EOF
$MESSAGE
EOF
echo "✅ 消息已发送到 Surface (千问)"

# 尝试发送给龙虾 (SJLL)
if ssh -o ConnectTimeout=5 -p 8822 -o StrictHostKeyChecking=no vicki@113.57.105.174 "cat > /tmp/qwen-broadcast.txt" << EOF2
$MESSAGE
EOF2
then
    echo "✅ 消息已发送到 SJLL (龙虾)"
else
    echo "⚠️  龙虾 (SJLL) 连接失败，写入共享任务"
    # 写入共享任务作为备选
    cat > /root/air/mycc/0-System/agents/shared-tasks/inbox/ai-broadcast-$(date +%Y%m%d).md << EOF3
# AI 助手群发消息

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**发送者**: qwq (本地监控系统)
**接收者**: 千问 (Surface), 龙虾 (SJLL)

$MESSAGE
EOF3
fi

echo "✅ 广播完成"
