# One-API 高可用配置方案

> CC 服务器 (192.168.100.228) One-API 模型映射和 HA 配置指南

---

## 🎯 目标

- 禁用失效的 NVIDIA NIM 渠道
- 启用 SiliconFlow 作为主渠道
- 配置多层降级策略
- 实现模型调用高可用

---

## 📊 渠道架构

```
                    用户请求
                        │
                        ▼
              ┌─────────────────┐
              │   One-API Gateway │
              │  (192.168.100.228:3000) │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │渠道 1    │   │渠道 2    │   │渠道 3    │
   │Silicon  │   │智谱 GLM  │   │OpenRouter│
   │Flow     │   │(备用 1)  │   │(备用 2)  │
   │优先级 1  │   │优先级 2  │   │优先级 3  │
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │
        ▼             ▼             ▼
   自动重试 3 次   自动重试 3 次   自动重试 3 次
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
                  返回结果
```

---

## 🔧 配置步骤

### Step 1: 检查当前状态

```bash
# 登录 CC 服务器
ssh root@192.168.100.228

# 检查 One-API 容器状态
docker ps | grep oneapi

# 查看 One-API 日志
docker logs oneapi --tail 50

# 测试当前 API
curl -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  http://192.168.100.228:3000/v1/models
```

### Step 2: 访问 One-API 管理界面

One-API 通常有 Web 管理界面：
- 地址：`http://192.168.100.228:3000/admin`
- 或：`http://192.168.100.228:3001` (如果配置了独立管理端口)

### Step 3: 禁用失效渠道

在 One-API 管理界面中：
1. 进入 **渠道管理**
2. 找到渠道 3 和 4 (NVIDIA NIM)
3. 点击 **禁用** 或 **删除**

或通过 API：
```bash
# 禁用渠道 3
curl -X PUT http://192.168.100.228:3000/api/channel/3 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'

# 禁用渠道 4
curl -X PUT http://192.168.100.228:3000/api/channel/4 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

### Step 4: 添加 SiliconFlow 渠道

#### 4.1 获取 SiliconFlow API Key

访问 https://cloud.siliconflow.cn 获取 API Key

#### 4.2 在 One-API 中添加渠道

**渠道配置**:
| 字段 | 值 |
|------|-----|
| 渠道类型 | SiliconFlow |
| API Key | `YOUR_SILICONFLOW_KEY` |
| 优先级 | 1 |
| 启用 | ✅ |

**模型映射**:
```json
{
  "z-ai/glm-4-air": "z-ai/glm-4-air",
  "z-ai/glm-4-flash": "z-ai/glm-4-flash",
  "deepseek-ai/DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
  "deepseek-ai/DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
  "Qwen/Qwen2.5-72B-Instruct": "Qwen/Qwen2.5-72B-Instruct",
  "Qwen/Qwen2.5-Coder-32B-Instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",
  "01-ai/Yi-1.5-34B-Chat": "01-ai/Yi-1.5-34B-Chat"
}
```

#### 4.3 使用 API 添加

```bash
curl -X POST http://192.168.100.228:3000/api/channel \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SiliconFlow",
    "key": "YOUR_SILICONFLOW_KEY",
    "name": "SiliconFlow-Main",
    "priority": 1,
    "models": ["z-ai/glm-4-air", "deepseek-ai/DeepSeek-V3", "Qwen/Qwen2.5-72B-Instruct"]
  }'
```

### Step 5: 添加备用渠道

#### 5.1 智谱 GLM (备用 1)

**渠道配置**:
| 字段 | 值 |
|------|-----|
| 渠道类型 | 智谱 AI |
| API Key | `YOUR_ZHIPU_KEY` |
| 优先级 | 2 |
| 启用 | ✅ |

#### 5.2 OpenRouter (备用 2)

**渠道配置**:
| 字段 | 值 |
|------|-----|
| 渠道类型 | OpenRouter |
| API Key | `YOUR_OPENROUTER_KEY` |
| 优先级 | 3 |
| 启用 | ✅ |

### Step 6: 配置重试和降级

One-API 内置重试机制，配置如下：

```bash
# 设置重试次数 (环境变量或配置文件)
ONEAPI_RETRY_TIMES=3

# 设置超时 (秒)
ONEAPI_TIMEOUT=30

# 启用自动降级
ONEAPI_AUTO_FALLBACK=true
```

或在 `config.json` 中：
```json
{
  "retry": {
    "times": 3,
    "timeout": 30
  },
  "fallback": {
    "enabled": true,
    "strategy": "priority"
  }
}
```

---

## ✅ 验证测试

### 测试主渠道

```bash
curl -X POST http://192.168.100.228:3000/v1/chat/completions \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "z-ai/glm-4-air",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, who are you?"}
    ]
  }'
```

### 测试降级策略

```bash
# 使用不存在的模型触发降级
curl -X POST http://192.168.100.228:3000/v1/chat/completions \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "non-existent-model",
    "messages": [{"role": "user", "content": "test"}]
  }'
# 应该自动降级到备用渠道
```

---

## 📊 模型映射表

| 用户请求模型 | 实际渠道 | 渠道模型 | 优先级 |
|-------------|----------|----------|--------|
| `z-ai/glm-4-air` | SiliconFlow | `z-ai/glm-4-air` | 1 |
| `z-ai/glm-4-flash` | SiliconFlow | `z-ai/glm-4-flash` | 1 |
| `deepseek-ai/DeepSeek-V3` | SiliconFlow | `deepseek-ai/DeepSeek-V3` | 1 |
| `Qwen/Qwen2.5-72B-Instruct` | SiliconFlow | `Qwen/Qwen2.5-72B-Instruct` | 1 |
| `z-ai/glm5` | 智谱 GLM | `glm-4` | 2 |

---

## 🔍 故障排查

### 问题 1: 渠道不生效

```bash
# 检查渠道状态
curl http://192.168.100.228:3000/api/channel \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 检查模型列表
curl http://192.168.100.228:3000/v1/models \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f"
```

### 问题 2: 降级不工作

检查 One-API 日志：
```bash
docker logs oneapi --tail 100 | grep -i fallback
```

### 问题 3: API Key 失效

更新渠道配置：
```bash
curl -X PUT http://192.168.100.228:3000/api/channel/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "NEW_API_KEY"}'
```

---

## 📝 配置备份

```bash
# 备份 One-API 配置
docker exec oneapi cat /app/config.json > /data/oneapi/config.backup.$(date +%Y%m%d).json

# 恢复配置
docker exec -i oneapi cat /app/config.json < /data/oneapi/config.backup.json
```

---

## 🔄 定期维护

- **每周**: 检查渠道健康状态
- **每月**: 更新 API Key (如有轮换)
- **每季度**: 评估新渠道和模型

---

*版本：v1.0 | 创建者：cc-local + CC-Server-Gemini | 创建时间：2026-03-05*
