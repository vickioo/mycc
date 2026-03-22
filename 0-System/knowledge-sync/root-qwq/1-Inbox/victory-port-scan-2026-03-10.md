# 🔍 Victory 主机端口扫描报告

**扫描时间**: 2026-03-10 07:45  
**扫描者**: qwq (本地监控系统)  
**目标**: Victory (100.100.1.8) - Tailscale 节点

---

## 📊 扫描结果总结

### 主机状态

| 检测方式 | 状态 | 延迟 | 备注 |
|----------|------|------|------|
| **Tailscale Ping** | ✅ 在线 | ~180ms | via DERP(hkg) |
| **ICMP Ping** | ❌ 100% 丢包 | - | 被防火墙阻止 |
| **SSH (22)** | ❌ 关闭 | - | Connection refused |
| **HTTP (80)** | ❌ 关闭 | - | 无响应 |
| **HTTPS (443)** | ❌ 关闭 | - | 无响应 |

---

## 🔍 端口扫描详情

### 扫描范围：16 个常用端口

| 端口 | 服务 | 状态 |
|------|------|------|
| 22 | SSH | ❌ Closed |
| 80 | HTTP | ❌ Closed |
| 443 | HTTPS | ❌ Closed |
| 3000 | One-API | ❌ Closed |
| 3306 | MySQL | ❌ Closed |
| 5000 | Docker Registry | ❌ Closed |
| 5432 | PostgreSQL | ❌ Closed |
| 6379 | Redis | ❌ Closed |
| 8000 | HTTP Alt | ❌ Closed |
| 8080 | HTTP Proxy | ❌ Closed |
| 8888 | HTTP Alt | ❌ Closed |
| 9000 | Portainer | ❌ Closed |
| 2222 | SSH Alt | ❌ Closed |
| 22222 | SSH Alt | ❌ Closed |
| 18789 | OpenClaw | ❌ Closed |
| 18790 | Qwen | ❌ Closed |

**结论**: **所有端口均被防火墙阻止**

---

## 🔥 防火墙分析

### 现象

1. ✅ **Tailscale DERP 可通** - 延迟 180ms (香港节点)
2. ❌ **直连被阻止** - ICMP 100% 丢包
3. ❌ **所有端口关闭** - TCP 连接被拒绝

### 可能原因

| 原因 | 可能性 | 说明 |
|------|--------|------|
| **UFW/iptables 阻止** | 🔴 高 | Linux 防火墙默认策略 |
| **安全组规则** | 🟡 中 | 云服务器安全组 |
| **SSH 未运行** | 🟡 中 | sshd 服务未启动 |
| **主机睡眠** | 🟢 低 | Tailscale 在线，排除 |

---

## 💡 解决方案

### 方案 A: 通过 Tailscale SSH (推荐)

Tailscale 提供内置 SSH 中继：

```bash
# 使用 Tailscale SSH (如果启用)
ssh vicki@victory.ts.net

# 或通过 Tailscale 功能
tailscale ssh vicki@victory
```

**前提**: Victory 需启用 Tailscale SSH：
```bash
# 在 Victory 上执行
tailscale set --ssh=true
```

### 方案 B: 配置防火墙规则

在 Victory 上执行：

```bash
# 允许 SSH
sudo ufw allow 22/tcp

# 或添加特定 IP
sudo ufw allow from 100.70.32.116 to any port 22 proto tcp

# 查看状态
sudo ufw status
```

### 方案 C: 使用 Tailscale Funnel

临时暴露服务到公网：

```bash
# 在 Victory 上执行
tailscale funnel 22
```

**注意**: Funnel 会将服务暴露到公网，需谨慎使用。

### 方案 D: 等待用户手动开启

联系 vicki 在 Victory 上：
1. 检查 SSH 服务：`systemctl status sshd`
2. 开放防火墙：`sudo ufw allow 22`
3. 确认 Tailscale 状态：`tailscale status`

---

## 📋 当前可用连接路径

```
本地 (qwq)
  │
  ├─✅ CC-Server (100.70.32.116) - SSH 正常
  │   └─✅ Clash 出口 (113.57.105.174)
  │
  ├─❌ Victory (100.100.1.8) - 防火墙阻止
  │   └─⚠️ 仅 Tailscale DERP 可通 (180ms)
  │
  └─❌ Surface (192.168.3.200) - SSH 超时
      └─🔴 可能睡眠/关机
```

---

## 🎯 建议操作

### 立即执行

1. **检查 Tailscale SSH 是否可用**:
   ```bash
   ssh CC "tailscale status | grep victory"
   ```

2. **尝试 Tailscale 内置 SSH**:
   ```bash
   tailscale ssh vicki@victory 2>&1 | head -10
   ```

### 联系用户

发送消息给 vicki：
```
Victory 主机 (100.100.1.8) 防火墙阻止了所有连接。

请在 Victory 上执行：
1. sudo ufw allow 22/tcp
2. sudo systemctl restart sshd
3. tailscale status

或通过 Tailscale Web UI 检查防火墙设置。
```

---

*扫描完成时间：2026-03-10 07:45*  
*扫描者：qwq (本地 Qwen Code 监控系统)*
