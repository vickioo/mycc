---
name: cc-switch
description: 模型切换工具，支持在不同AI模型之间快速切换，包括主要模型和备用模型。触发词："/switch"、"切换模型"、"模型切换"
---

# cc-switch — 模型切换工具

提供模型切换功能，支持在不同AI模型之间快速切换，包括主要模型和备用模型。

## 触发词

- "/switch"
- "切换模型"
- "模型切换"

## 执行步骤

1. 显示当前可用的模型列表
2. 根据用户选择切换到指定模型
3. 测试模型可用性
4. 显示切换结果

## 脚本位置

```
.claude/skills/cc-switch/scripts/switcher.py
```

## 用法

```bash
# 列出可用模型
python3 .claude/skills/cc-switch/scripts/switcher.py --list

# 切换到指定模型
python3 .claude/skills/cc-switch/scripts/switcher.py --model glm47

# 测试模型可用性
python3 .claude/skills/cc-switch/scripts/switcher.py --test glm47

# 自动选择可用模型
python3 .claude/skills/cc-switch/scripts/switcher.py --auto
```

## 支持的模型

### 主要模型
- glm47: GLM4.7 (z-ai/glm4.7)
- minimax: Minimax M2.1 (minimaxai/minimax-m2.1)
- kimi: KIMI (moonshotai/kimi-k2.5)

### 备用模型
- llama3: Llama 3 (meta/llama3-70b)
- gemini: Gemini Pro (google/gemini-pro)
- claude: Claude 3 Haiku (anthropic/claude-3-haiku-20240307)

## 模型稳定性说明

- GLM4.7: 稳定，适合长期使用
- Minimax M2.1: 稳定，擅长中文
- KIMI: 稳定，知识覆盖广泛
- Llama 3: 稳定，通用能力强
- Gemini Pro: 稳定，多模态能力强
- Claude 3 Haiku: 稳定，响应速度快

所有备用模型均可稳定运行1个月以上，提供可靠的模型替代方案。