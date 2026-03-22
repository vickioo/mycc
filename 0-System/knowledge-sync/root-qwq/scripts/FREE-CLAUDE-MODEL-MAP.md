# free-claude-code 模型路由映射指南

## 📊 当前配置总览

**默认模型**: `nvidia_nim/minimaxai/minimax-m2.5`

**提供商优先级**: `nvidia_nim → open_router → silicon_flow`

---

## 🗺️ 模型映射表 (MODEL_MAP)

当 Claude CLI 请求某个模型时，会被路由到以下实际模型：

| Claude 模型请求 | 实际路由模型 | 提供商 | 说明 |
|----------------|-------------|--------|------|
| `claude-3-5-sonnet-20241022` | `silicon_flow/Qwen/Qwen2.5-Coder-32B-Instruct` | SiliconFlow | 千问 2.5 Coder 32B |
| `claude-3-5-haiku-20241022` | `silicon_flow/stepfun-ai/Step-3.5-Flash` | SiliconFlow | 阶跃 3.5 Flash |
| `claude-3-opus-20240229` | `nvidia_nim/deepseek-ai/deepseek-v3.1` | NVIDIA NIM | 深度求索 V3.1 |
| `claude-3-5-sonnet-20240620` | `nvidia_nim/meta/llama-3.3-70b-instruct` | NVIDIA NIM | Llama 3.3 70B |
| **其他/默认** | `nvidia_nim/minimaxai/minimax-m2.5` | NVIDIA NIM | MiniMax M2.5 |

---

## 🎭 显示名称映射 (MODEL_DISPLAY_MAP)

在 Claude CLI 界面中显示的模型名称：

| 实际模型 | 显示名称 |
|---------|---------|
| `silicon_flow/Qwen/Qwen2.5-Coder-32B-Instruct` | Claude 3.5 Sonnet → Qwen 2.5 Coder |
| `silicon_flow/stepfun-ai/Step-3.5-Flash` | Claude 3.5 Haiku → Step-1-Flash |
| `nvidia_nim/deepseek-ai/deepseek-v3` | Claude 3 Opus → DeepSeek-V3 |
| `nvidia_nim/meta/llama-3.3-70b-instruct` | Claude 3.5 (Old) → Llama-3.3-70B |

---

## 🔄 路由逻辑流程

```
用户请求 (Claude CLI)
    │
    ▼
请求模型：claude-3-5-sonnet-20241022
    │
    ▼
检查 MODEL_MAP
    │
    ├─→ 有映射 → silicon_flow/Qwen/Qwen2.5-Coder-32B-Instruct
    │
    └─→ 无映射 → 使用默认 MODEL
                    │
                    ▼
            nvidia_nim/minimaxai/minimax-m2.5
    │
    ▼
根据提供商优先级选择
    │
    ├─→ nvidia_nim (优先)
    ├─→ open_router (备选 1)
    └─→ silicon_flow (备选 2)
    │
    ▼
调用对应 Provider API
```

---

## 📦 各提供商可用模型

### NVIDIA NIM (推荐)

**优质模型**:
| 模型 | 说明 | 适用场景 |
|------|------|---------|
| `deepseek-ai/deepseek-v3.1` | 深度求索 V3.1 | 通用对话、代码 |
| `meta/llama-3.3-70b-instruct` | Llama 3.3 70B | 通用对话 |
| `meta/llama-3.1-70b-instruct` | Llama 3.1 70B | 通用对话 |
| `minimaxai/minimax-m2.5` | MiniMax M2.5 | 长文本、对话 |
| `google/gemma-2-27b-it` | Gemma 2 27B | 轻量对话 |
| `ibm/granite-3.0-8b-instruct` | Granite 3.0 8B | 轻量任务 |
| `deepseek-ai/deepseek-coder-6.7b-instruct` | DeepSeek Coder | 代码生成 |

### SiliconFlow

| 模型 | 说明 |
|------|------|
| `Qwen/Qwen2.5-Coder-32B-Instruct` | 千问 2.5 Coder |
| `stepfun-ai/Step-3.5-Flash` | 阶跃 3.5 Flash |

### OpenRouter

支持更多模型，需查看 OpenRouter 文档。

---

## 🔧 如何切换模型

### 方法 1: 修改默认模型

编辑 `/root/free-claude-code/.env`:

```bash
# 改为 DeepSeek V3.1
MODEL="nvidia_nim/deepseek-ai/deepseek-v3.1"

# 改为 Llama 3.3 70B
MODEL="nvidia_nim/meta/llama-3.3-70b-instruct"
```

重启服务:
```bash
pm2 restart free-claude-code
```

### 方法 2: 添加特定映射

编辑 `/root/free-claude-code/.env` 中的 `MODEL_MAP`:

```json
MODEL_MAP='{
  "claude-3-5-sonnet-20241022": "nvidia_nim/deepseek-ai/deepseek-v3.1",
  "claude-3-5-haiku-20241022": "nvidia_nim/meta/llama-3.1-70b-instruct",
  "claude-3-opus-20240229": "nvidia_nim/deepseek-ai/deepseek-v3.1"
}'
```

### 方法 3: Claude CLI 中直接指定

在 Claude CLI 中使用 `/model` 命令切换（如果支持）。

---

## 📋 常见问题

### Q: 如果我请求 `claude-3-5-haiku`，实际用哪个模型？

**A**: `silicon_flow/stepfun-ai/Step-3.5-Flash`（阶跃 3.5 Flash）

### Q: 如果我请求 `claude-3-opus`，实际用哪个模型？

**A**: `nvidia_nim/deepseek-ai/deepseek-v3.1`（深度求索 V3.1）

### Q: 如果我请求 `claude-sonnet-4-20250514`（未映射的模型），实际用哪个？

**A**: 默认模型 `nvidia_nim/minimaxai/minimax-m2.5`

### Q: 如何查看所有可用的 NVIDIA NIM 模型？

**A**: 查看 `/root/free-claude-code/nvidia_nim_models.json`

### Q: 如果 NVIDIA NIM 失败，会怎样？

**A**: 自动 failover 到 OpenRouter → SiliconFlow（按优先级）

---

## 🎯 推荐配置

### 代码开发场景

```env
MODEL="nvidia_nim/deepseek-ai/deepseek-coder-6.7b-instruct"
MODEL_MAP='{
  "claude-3-5-sonnet-20241022": "nvidia_nim/deepseek-ai/deepseek-coder-6.7b-instruct",
  "claude-3-5-haiku-20241022": "nvidia_nim/meta/llama-3.1-8b-instruct"
}'
```

### 通用对话场景

```env
MODEL="nvidia_nim/meta/llama-3.3-70b-instruct"
MODEL_MAP='{
  "claude-3-5-sonnet-20241022": "nvidia_nim/meta/llama-3.3-70b-instruct",
  "claude-3-opus-20240229": "nvidia_nim/deepseek-ai/deepseek-v3.1"
}'
```

### 长文本场景

```env
MODEL="nvidia_nim/minimaxai/minimax-m2.5"
```

---

*Last updated: 2026-03-13*
