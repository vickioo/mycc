---
name: cc-switch
description: 动态切换 free-claude-code 底层代理模型的指令。当用户要求切换模型（如使用 qwen, coder, 70b 或完整模型名）时触发此技能。
---

# cc-switch 模型热切换

使用此技能可以在不中断 Claude Code 会话的情况下，安全地切换背后的代理模型，并附带失败自动回退机制。

## 触发场景
- 用户输入 `/cc-switch [模型名]` 或 `/model [模型名]`
- 用户说"帮我切换到联通云"、"启用 Claude 优先"、"切换到 claude-3-5-sonnet"
- 用户说"启动灾备模式"、"模型自动轮换"、"主模型不行了换一个"等

## 执行步骤

### 联通云优先模式
1. 用户输入 `/unicom` 或 "切换到联通云"
2. 执行 `scripts/switch_to_unicom.sh`
3. 切换到联通云 Claude 优先，失败自动降级

### 自动灾备模式
1. 用户请求"灾备"或"轮换"模式
2. 调用 `scripts/auto_rotate.sh`
3. 按优先级顺序测试：联通云 Claude -> NVIDIA -> 智谱 -> SiliconFlow -> OpenRouter
4. 找到第一个可用模型并切换

### 手动指定模型
1. 用户提供了具体的模型关键词（例如 qwen 或 coder）
2. 执行 `scripts/search_models.sh <关键词>` 搜索模型名
3. 调用脚本 `scripts/switch.sh <模型完整路径>` 执行物理切换和重启
4. 如果脚本输出 "SUCCESS"，告诉用户模型切换成功
5. 如果脚本输出 "FALLBACK"，告诉用户模型测试失败，已回退到原模型

## 模型优先级

**联通云优先模式**:
1. 联通云 Claude (antigravity)
2. NVIDIA NIM
3. SiliconFlow
4. OpenRouter
5. 智谱 GLM

## 快捷命令

| 命令 | 功能 |
|------|------|
| `/unicom` | 切换到联通云 Claude 优先 |
| `/rotate` | 启动自动灾备轮换 |
| `/cc-switch <model>` | 切换到指定模型 |

