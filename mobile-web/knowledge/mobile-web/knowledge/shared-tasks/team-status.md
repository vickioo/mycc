# AI 助理团队状态与任务分配

**更新时间**: 2026-03-06 18:45  
**协调者**: qwq (Qwen Code - 当前会话)

---

## 👥 助理团队状态

### ✅ 运行中 (活跃)

| 助理 | 位置 | PID | 运行时间 | 状态 | 当前任务 |
|------|------|-----|----------|------|----------|
| **mycc (Claude)** | CC 服务器 | 2634904 | 2h 16m | 🟢 活跃 | Gemini 代理诊断 |
| **Gemini CLI #1** | CC 服务器 | 2623453 | 11h+ | 🟡 挂起 | resume 会话 |
| **Gemini CLI #2** | CC 服务器 | 2623477 | 11h+ | 🟡 挂起 | resume 会话 |

### ❌ 离线

| 助理 | 位置 | 状态 | 说明 |
|------|------|------|------|
| **sjll-agent (龙虾)** | sj-liuliang.local | 🔴 不可达 | SSH 隧道断开 |
| **openclaw** | CC 服务器 | ⚪ 待机 | 脚本未运行 |

---

## 📋 当前任务队列

### 🔴 高优先级 (进行中)

**任务**: `gemini-proxy-test.json`  
**分配给**: mycc (Claude)  
**状态**: in_progress  
**进度**: 5/9 完成

**待办**:
1. 修复 Termux SSH 隧道 IPv4/IPv6 绑定问题
2. 测试 Termux → gate → CC Clash 完整链路
3. 测试 Gemini CLI

**可协助**: Gemini CLI (如果唤醒)

---

### 🟡 中优先级 (待处理)

**任务**: `task-001.json`, `task-002.json`  
**位置**: mycc inbox  
**状态**: pending  
**可分配**: 任意空闲助理

---

## 🎯 可立即推进的任务

### 1. Gemini 代理修复 (需要 mycc + Gemini CLI 协作)

**当前阻塞**: Termux SSH 隧道端口绑定问题

**需要执行**:
```bash
# 在 Termux 中执行
pkill -f 'ssh.*-D 7891'
nohup ssh -N -4 -D 127.0.0.1:7891 gate &
sleep 2
curl -s --socks5-hostname 127.0.0.1:7891 https://api.ip.sb/ip
```

**可分配**:
- mycc: 执行 Termux 命令并测试
- Gemini CLI: 验证代理连通性

---

### 2. sjll-agent (龙虾) 重连

**问题**: SSH 隧道断开

**需要执行**:
```bash
# 刷新 gate 隧道
ssh -p 8022 localhost "pkill -f 'ssh.*8821'; sleep 1; ssh -N -f -L 8821:sj-liuliang.local:22 gate"

# 测试连接
ssh -p 8821 sjll-agent "echo OK"
```

**可分配**: mycc

---

### 3. openclaw 激活

**位置**: `/data/openclaw-workspace/`

**需要执行**:
```bash
# 在 CC 服务器上
cd /data/openclaw-workspace
./start.sh
```

**可分配**: 任意助理

---

### 4. Antigravity Manager 集成

**位置**: `/data/Antigravity-Manager-4.1.11/`

**用途**: Gemini/Claude 代理管理

**可探索**:
- 配置检查
- 与当前 Clash 隧道对比
- 可能的优化方案

**可分配**: mycc + Gemini CLI

---

## 🤖 助理能力矩阵

| 助理 | SSH | 网络 | 配置 | 测试 | 文档 |
|------|-----|------|------|------|------|
| qwq (我) | ✅ | ✅ | ✅ | ✅ | ✅ |
| mycc | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| sjll-agent | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |
| openclaw | ⚪ | ⚪ | ⚪ | ✅ | ✅ |

✅ 擅长 | ⚪ 一般 | ❌ 不擅长

---

## 📊 推荐任务分配

### 立即执行 (mycc)

1. **修复 Termux SSH 隧道** (5 分钟)
2. **测试完整代理链路** (5 分钟)
3. **测试 Gemini CLI** (10 分钟)

### 并行执行 (Gemini CLI - 如果唤醒)

1. **验证代理配置** (与 mycc 协作)
2. **测试 Antigravity Manager** (独立任务)

### 后续执行 (sjll-agent 重连后)

1. **同步龙虾配置**
2. **测试跨 Agent 通信**

---

## 🔧 协作机制

### 任务同步目录

```
/data/mycc/shared-tasks/
├── inbox/         ← 新任务
├── processing/    ← 进行中
└── completed/     ← 已完成

/root/air/qwq/shared-tasks/
├── inbox/         ← U22 新任务
├── processing/    ← U22 进行中
└── completed/     ← U22 已完成
```

### 状态更新

- 任务文件 JSON 格式
- 更新 `status` 和 `progress` 字段
- 完成后移动到 `completed/`

---

## 📝 下一步行动

1. **mycc**: 修复 Termux SSH 隧道，完成 Gemini 代理测试
2. **qwq (我)**: 监控进度，准备文档
3. **Gemini CLI**: 唤醒后验证代理
4. **sjll-agent**: 重连后同步配置

---

*Last updated: 2026-03-06 18:45*
