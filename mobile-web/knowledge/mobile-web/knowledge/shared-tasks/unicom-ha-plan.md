# 联通云 HA 方案 - One-API 高可用配置

> 参考 antigravitytools 实现的 HA 重试退避系统

---

## 📊 当前 One-API 渠道状态

| ID | 名称 | Type | Status | Priority | 备注 |
|----|------|------|--------|----------|------|
| 1 | Nvidia-Free | 50 | ✅ | 0 | 联通云套餐 |
| 2 | SiliconFlow-VIP | 44 | ✅ | 0 | 主渠道 |
| 3 | NVIDIA-02 | 1 | ✅ | 0 | 已修复 |
| 4 | NVIDIA-All | 50 | ✅ | 0 | 联通云 |
| 6 | OpenRouter-Free | 20 | ✅ | 0 | 备用 |
| 7 | CC-Antigravity-SVIP | 1 | ✅ | 1 | **antigravity 代理** |
| 8 | VIP-Channel | 1 | ✅ | 2 | 本地 One-API |
| 9 | 智谱 GLM z-ai | 16 | ✅ | 0 | 国产兜底 |

---

## 🎯 HA 设计目标

### 1. 优先级架构
```
用户请求
    │
    ▼
┌─────────────────────────────────┐
│   One-API Gateway (CC 服务器)   │
│   192.168.100.228:3000          │
└────────────┬────────────────────┘
             │
    ┌────────┼────────┬───────────┐
    │        │        │           │
    ▼        ▼        ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│渠道 7   │ │渠道 2  │ │渠道 9  │ │渠道 6  │
│联通云  │ │Silicon │ │智谱 GLM│ │OpenRouter│
│Priority│ │Priority│ │Priority│ │Priority│
│   1    │ │   0    │ │   0    │ │   0    │
└────────┘ └────────┘ └────────┘ └────────┘
```

### 2. 重试退避逻辑 (参考 antigravitytools)

**核心机制**:
- ✅ 自动重试 3 次
- ✅ 指数退避 (100ms → 200ms → 400ms)
- ✅ 失败自动降级到下一优先级渠道
- ✅ 健康检查 (5 分钟间隔)
- ✅ 审计日志 (request_logs.db)

**antigravity 关键发现**:
```rust
// proxy_db.rs - 记录每次请求
- request_logs 表记录所有请求
- 包含 status, duration, error, account_email
- 支持快速统计和故障排查

// networkMonitorStore.ts - 前端监控
- 实时显示请求状态
- 记录 pending/success/error
- 保留最近 100 条请求
```

---

## 🔧 配置步骤

### Step 1: 设置渠道优先级

```bash
# SSH 到 CC 服务器
ssh CC

# 复制数据库到本地
docker cp one-api:/data/one-api.db /tmp/one-api.db

# 备份
cp /tmp/one-api.db /tmp/one-api.db.backup.$(date +%Y%m%d)

# 设置优先级 (数字越小越优先)
sqlite3 /tmp/one-api.db <<EOF
-- 联通云套餐优先 (antigravity 代理)
UPDATE channels SET priority=1 WHERE id=7;

-- SiliconFlow 主渠道
UPDATE channels SET priority=2 WHERE id=2;

-- 智谱 GLM 备用
UPDATE channels SET priority=3 WHERE id=9;

-- OpenRouter 备用
UPDATE channels SET priority=4 WHERE id=6;

-- 验证
SELECT id, name, priority, status FROM channels ORDER BY priority;
EOF

# 复制回容器
docker cp /tmp/one-api.db one-api:/data/one-api.db

# 重启 One-API
docker restart one-api
```

### Step 2: 配置重试机制

One-API 内置重试配置 (环境变量):

```bash
# CC 服务器上编辑 docker-compose.yml 或 docker run 环境变量
docker inspect one-api | grep -A 20 Env

# 添加/修改以下环境变量:
ONEAPI_RETRY_TIMES=3          # 重试次数
ONEAPI_TIMEOUT=30             # 超时 (秒)
ONEAPI_AUTO_FALLBACK=true     # 自动降级
```

### Step 3: 启用健康检查

One-API 内置健康检查:
- 每 5 分钟自动测试渠道
- 自动标记失效渠道
- 记录 `response_time` 字段

```bash
# 查看健康状态
curl http://localhost:3000/api/channel \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f"
```

---

## 📝 模型映射配置

### 联通云套餐 (渠道 7 - antigravity)

支持模型:
- `claude-3-5-sonnet-20241022`
- `claude-3-5-sonnet-20240620`
- `claude-3-haiku`
- `gemini-*`

### SiliconFlow (渠道 2)

支持模型:
- `z-ai/glm-4-air`
- `z-ai/glm-4-flash`
- `deepseek-ai/DeepSeek-V3`
- `deepseek-ai/DeepSeek-R1`
- `Qwen/Qwen2.5-72B-Instruct`

### 智谱 GLM (渠道 9)

支持模型:
- `z-ai/glm5`
- `glm-4`
- `glm-4-flash`

---

## ✅ 验证测试

### 测试 1: 主渠道响应

```bash
curl -X POST http://192.168.100.228:3000/v1/chat/completions \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 测试 2: 降级策略

```bash
# 使用不存在的模型触发降级
curl -X POST http://192.168.100.228:3000/v1/chat/completions \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "non-existent-model",
    "messages": [{"role": "user", "content": "test fallback"}]
  }'
```

### 测试 3: 查看请求日志

```bash
# antigravity 的请求日志
curl http://172.17.0.1:8045/admin/logs \
  -H "Authorization: Bearer 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"
```

---

## 🔍 故障排查

### 问题 1: 渠道不生效

```bash
# 检查渠道状态
sqlite3 /tmp/one-api.db "SELECT id, name, status, priority FROM channels;"

# 检查模型列表
curl http://localhost:3000/v1/models \
  -H "Authorization: Bearer sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f"
```

### 问题 2: 降级不工作

```bash
# 查看 One-API 日志
docker logs oneapi --tail 100 | grep -i fallback
```

### 问题 3: antigravity 连接失败

```bash
# 检查 antigravity 服务
systemctl status antigravity

# 检查端口
netstat -tlnp | grep 8045
```

---

## 📊 监控指标

### 渠道健康度

| 指标 | 目标值 | 告警阈值 |
|------|--------|----------|
| 响应时间 | < 500ms | > 2000ms |
| 成功率 | > 99% | < 95% |
| 重试率 | < 5% | > 20% |

### 日报生成

```bash
# 每日 8:00 自动生成
ssh CC "docker logs oneapi --since 24h | grep -E '404|500|timeout' | wc -l"
```

---

## 🔄 与 mycc 集成

### cc-switch 技能

```bash
# 在 mycc 中使用
/cc-switch set-priority --channel 7 --value 1
/cc-switch enable-ha --retry 3 --timeout 30
```

### scheduler 定时任务

```bash
# 每 5 分钟健康检查
0 */5 * * * /data/mycc/scripts/health-check.sh

# 每日 8:00 日报
0 8 * * * /data/mycc/scripts/daily-report.sh
```

---

*版本：v1.0 | 创建者：qwq | 创建时间：2026-03-05 21:30*
