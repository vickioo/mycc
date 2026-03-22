# 语音交互集成方案

**日期**: 2026-03-07  
**参考**: 微信文章语音交互功能  
**目标**: 在 AI Team Hub 中实现语音回复交互

---

## 📋 需求分析

### 用户需求
1. 在 Surface 龙虾上安装语音交互功能
2. 本地网页有入口与龙虾对话
3. 测试语音回复效果
4. 跳转到龙虾网关直接交互

### 当前状态

| 组件 | 状态 | 说明 |
|------|------|------|
| **SJLL SSH** | ❌ 未连接 | 8821 端口未监听 |
| **ssh-gate** | ❌ 未运行 | 需要启动 |
| **龙虾网关** | 🟡 待确认 | Surface 设备 |
| **语音功能** | 📋 待安装 | 微信文章方案 |

---

## 🔧 实施步骤

### Phase 1: 恢复 SJLL 连接

#### 1.1 启动 ssh-gate 服务
```bash
# U22 上执行
/root/bin/sv/sv start ssh-gate
/root/bin/sv/sv status
```

#### 1.2 验证连接
```bash
# 测试 8821 端口
ssh -p 8821 sjll-agent "echo OK"

# 或直接连接
ssh sjll-agent "echo OK"
```

### Phase 2: 语音功能安装

#### 2.1 微信文章方案分析

**需要文章内容**:
- 使用的语音识别引擎 (Whisper? Azure? Google?)
- TTS 引擎 (Edge TTS? Azure?)
- 部署方式 (Docker? 原生?)
- 需要的账号/API Key

#### 2.2 安装清单

**Surface 龙虾端**:
- [ ] 安装语音识别模块
- [ ] 安装 TTS 引擎
- [ ] 配置 API Key
- [ ] 测试语音输入输出
- [ ] 集成到 Cherry Studio/OpenClaw

**本地 U22 端**:
- [ ] 网页语音入口
- [ ] 音频流转发
- [ ] WebSocket 实时通信

### Phase 3: 网页集成

#### 3.1 龙虾对话入口

在 AI Team Hub 中添加：
```html
<a href="http://sjll-agent:PORT" target="_blank" class="agent-card">
  <div class="agent-icon">🦞</div>
  <div class="agent-name">SJLL 龙虾</div>
  <div class="agent-status">● 在线</div>
  <div class="agent-desc">语音交互 · Windows 环境</div>
</a>
```

#### 3.2 直接网关跳转

```javascript
// 龙虾网关地址
const LOBSTER_GATEWAY = 'http://sj-liuliang.local:PORT';

// 或使用 SSH 隧道
const LOBSTER_LOCAL = 'http://localhost:8088';

// 打开对话窗口
window.open(LOBSTER_LOCAL, '_blank');
```

---

## 🏗️ 架构设计

### 方案 A: 直接跳转 (简单)

```
┌─────────────┐
│ AI Team Hub │
│  (U22)      │
└──────┬──────┘
       │ 点击入口
       ▼
┌─────────────┐
│ SJLL 龙虾    │
│ (Surface)   │
│ 语音交互    │
└─────────────┘
```

### 方案 B: 代理转发 (推荐)

```
┌─────────────┐     SSH 隧道     ┌─────────────┐
│ AI Team Hub │─────────────────▶│ SJLL 龙虾    │
│  (U22)      │   端口转发       │ (Surface)   │
│             │◀─────────────────│             │
│  /lobster   │   HTTP 代理      │  语音服务   │
└─────────────┘                  └─────────────┘
```

### 方案 C: 完全集成 (复杂)

```
┌─────────────────────────────────────────┐
│          AI Team Hub                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Qwen   │  │ Claude  │  │ 龙虾    │ │
│  │  文本   │  │ 文本    │  │ 语音    │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
```

---

## 📝 需要支持

### API Key / 账号

| 服务 | 用途 | 状态 |
|------|------|------|
| Azure Speech | 语音识别/合成 | 📋 需要申请 |
| Whisper API | 语音转文字 | 📋 需要配置 |
| Edge TTS | 文字转语音 | ✅ 免费 |
| 微信开放平台 | 语音接口 | 📋 需要确认 |

### 网络配置

| 配置 | 说明 | 状态 |
|------|------|------|
| SSH 隧道 | U22 → gate → sjll | 📋 需要启动 |
| 端口转发 | 8821 → sjll:22 | 📋 需要配置 |
| HTTP 代理 | 龙虾语音服务 | 📋 需要确认端口 |

---

## 🚀 实施时间线

| 阶段 | 任务 | 预计时间 |
|------|------|----------|
| **Phase 1** | 恢复 SJLL 连接 | 10 分钟 |
| **Phase 2** | 分析微信文章方案 | 30 分钟 |
| **Phase 3** | Surface 安装语音 | 1 小时 |
| **Phase 4** | 网页入口集成 | 30 分钟 |
| **Phase 5** | 联调测试 | 30 分钟 |

---

## 📞 联系方式

### Surface 龙虾操作
- 设备：Surface (Windows)
- 用户：vicki
- 连接：SSH via gate

### 本地 U22 操作
- 设备：U22 (Ubuntu)
- 用户：root
- 连接：直接

---

*创建日期：2026-03-07*  
*状态：等待微信文章内容*
