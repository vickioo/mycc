# U18 远端代理测试方案

**日期**: 2026-03-07 22:15  
**状态**: 📋 规划中  
**目标**: 测试 U18 通过手机 VPN 远端代理访问外网

---

## 🎯 测试目标

验证 U18 系统通过手机 VPN 的远端代理访问外网，而不是依赖本地 Clash 隧道。

### 优势

- ✅ 不依赖 CC 服务器 Clash
- ✅ 减少中间环节
- ✅ 直接利用手机 VPN 出口
- ✅ 更低的延迟

---

## 📱 网络拓扑

```
┌─────────────────────────────────────────────────────────┐
│                    Internet                              │
│                                                          │
│    ┌─────────────┐                                      │
│    │  手机 VPN   │ ← 用户手机 (VPN 已启动)                │
│    │  出口 IP    │                                      │
│    └──────┬──────┘                                      │
│           │                                              │
│           │ SSH 反向隧道                                │
│           ▼                                              │
└───────────┼──────────────────────────────────────────────┘
            │
┌───────────┴──────────────────────────────────────────────┐
│              U18 容器 (localhost:8022)                    │
│                                                           │
│  ┌─────────────┐         ┌─────────────┐                │
│  │  SSH 反向隧道 │         │  测试脚本   │                │
│  │  :1080      │         │  curl 测试  │                │
│  └─────────────┘         └─────────────┘                │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 配置步骤

### 步骤 1: U18 SSH 配置

在 U18 上创建 SSH 配置：

```bash
# ~/.ssh/config (U18)
Host gate-vpn
    HostName 113.57.105.174
    Port 8822
    User vicki
    IdentityFile ~/.ssh/id_ed25519_vi
    DynamicForward 1080
```

### 步骤 2: 启动反向隧道

在 U18 上执行：

```bash
# 启动 SSH 反向隧道到 gate
ssh -N -D 1080 gate-vpn
```

### 步骤 3: 测试连通性

```bash
# 测试 Google 访问
curl -s --socks5-h localhost:1080 https://www.google.com -o /dev/null && echo "✅ Google OK"

# 测试 IP 查询
curl -s --socks5-h localhost:1080 https://api.ip.sb/ip

# 测试 Gemini CLI
export ALL_PROXY=socks5h://localhost:1080
gemini 'Hello, are you available?'
```

---

## 📋 测试脚本

### test-remote-proxy.sh

```bash
#!/bin/bash
# U18 远端代理测试脚本

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[TEST]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[FAIL]${NC} $1"; }

echo "╔════════════════════════════════════════════════╗"
echo "║     U18 远端代理测试 (手机 VPN)                  ║"
echo "╚════════════════════════════════════════════════╝"

# 1. 检查 SSH 隧道
log "检查 SSH 隧道..."
if pgrep -f "ssh.*-D 1080" > /dev/null; then
    echo "  ✅ SSH 隧道运行中"
else
    warn "SSH 隧道未运行，启动中..."
    ssh -N -f -D 1080 gate-vpn
    sleep 2
fi

# 2. 测试基础连通性
log "测试基础连通性..."
curl -s --socks5-h localhost:1080 https://api.ip.sb/ip --connect-timeout 10 && echo " ✅" || error "失败"

# 3. 测试 Google
log "测试 Google 访问..."
curl -s --socks5-h localhost:1080 https://www.google.com -o /dev/null --connect-timeout 10 && echo "  ✅ Google OK" || error "Google 失败"

# 4. 测试 GitHub
log "测试 GitHub 访问..."
curl -s --socks5-h localhost:1080 https://api.github.com -o /dev/null --connect-timeout 10 && echo "  ✅ GitHub OK" || error "GitHub 失败"

# 5. 测试 Gemini CLI
log "测试 Gemini CLI..."
export ALL_PROXY=socks5h://localhost:1080
timeout 30 gemini 'Hello' 2>&1 | head -5

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║     测试完成                                    ║"
echo "╚════════════════════════════════════════════════╝"
```

---

## 🔄 与本地 Clash 对比

| 特性 | 本地 Clash | 远端代理 (手机 VPN) |
|------|-----------|-------------------|
| 依赖 | CC 服务器 | 手机 VPN |
| 延迟 | 较高 (多跳) | 较低 (直连) |
| 稳定性 | ⚠️ 频繁重启 | ✅ 手机 VPN 稳定 |
| 配置复杂度 | 中 | 低 |
| 适用场景 | 固定服务器 | 移动办公 |

---

## 📊 预期结果

### 成功标志

- [x] SSH 隧道正常运行
- [x] `curl --socks5-h localhost:1080` 返回出口 IP
- [x] Google/GitHub 访问成功
- [x] Gemini CLI 响应正常

### 失败处理

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| SSH 连接失败 | 网络不通 | 检查手机 VPN |
| 隧道断开 | SSH 超时 | 添加 `ServerAliveInterval` |
| 代理无效 | 端口错误 | 确认 1080 端口 |
| Gemini 超时 | API 限流 | 稍后重试 |

---

## 🚀 自动化方案

### systemd 服务 (可选)

```ini
# /etc/systemd/system/remote-proxy.service
[Unit]
Description=Remote Proxy via Phone VPN
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/ssh -N -f -D 1080 gate-vpn
ExecStop=/usr/bin/pkill -f "ssh.*-D 1080"
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

*创建：2026-03-07 22:15*  
*维护者：qwq (Qwen Code)*
