# 🌐 连通性检查报告

**检查时间**: 2026-03-10 07:35  
**检查者**: qwq (本地监控系统)  
**模式**: 非侵入式测试记录

---

## 📊 Tailscale 网络拓扑

```
┌─────────────────────────────────────────────────────────────┐
│                    Tailscale Network (jackljl007)            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  100.70.32.116   cc              ✅ linux (在线)            │
│  100.100.1.6     sj-liuliang     🟡 windows (在线)          │
│  100.100.1.8     victory         ❌ linux (SSH 拒绝)         │
│  100.117.29.20   vickimacbook    🔴 macOS (offline)         │
│  100.70.72.102   xiaomi-phone    🟡 android (在线)          │
│                                                              │
│  本地出口：113.57.105.174 (Clash Tunnel)                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 连通性测试结果

### 本地环境 (qwq)

| 目标 | 状态 | 延迟 | 备注 |
|------|------|------|------|
| Clash 隧道 | ✅ 正常 | - | 出口 IP: 113.57.105.174 |
| NVIDIA API | ✅ 正常 | ~200ms | 通过 Clash 隧道 |
| CC-Server | ✅ 正常 | ~50ms | SSH + Tailscale |
| Victory | ❌ 失败 | - | SSH 端口 22 拒绝 |
| Surface | ❌ 失败 | Timeout | SSH 超时 (可能睡眠) |

### CC-Server (100.70.32.116)

| 服务 | 状态 | 备注 |
|------|------|------|
| Tailscale | ✅ 运行中 | jackljl007@cc |
| One-API | ✅ 运行中 | Docker 容器 |
| Clash | ✅ 运行中 | 出口节点 |
| SSH | ✅ 正常 | 端口 22 |

### Victory (100.100.1.8)

| 服务 | 状态 | 备注 |
|------|------|------|
| Tailscale | ✅ 运行中 | jackljl007@victory |
| SSH | ❌ 拒绝 | 端口 22 未开放 |

### Surface (192.168.3.200 / Tailscale: 未知)

| 服务 | 状态 | 备注 |
|------|------|------|
| 本地 SSH | ❌ 超时 | 192.168.3.200:22 |
| Tailscale | ❓ 未知 | 无法连接检查 |
| Qwen CLI | ⚠️ 需登录 | OAuth token 有效 |
| OpenClaw | ✅ 运行中 | PID 491155 |
| 龙虾服务 | ✅ 运行中 | PID 104151 |

---

## 🚇 隧道连接方式

### 当前可用隧道

| 隧道类型 | 状态 | 端点 | 用途 |
|----------|------|------|------|
| **Clash Tunnel** | ✅ 运行中 | localhost:7890 | 科学上网 |
| **SSH Tunnel (CC)** | ✅ 运行中 | CC-Server → localhost:7890 | 共享 Clash |
| **Tailscale** | ✅ 运行中 | 100.x.x.x.x | 内网组网 |

### Cloudflare Tunnel

**状态**: ❌ 未找到配置

检查位置:
- Docker 容器：无 cloudflared
- Systemd 服务：无 cloudflared.service
- SSH 配置：无相关配置

---

## 📋 建议连接方式

### 连接 Surface

由于 Surface 可能睡眠/防火墙，建议：

1. **等待 Surface 唤醒** - 稍后重试 SSH
2. **Tailscale 直连** - 如果 Surface 在线：
   ```bash
   # 获取 Surface Tailscale IP
   ssh CC "tailscale status | grep -i surface"
   
   # 通过 Tailscale 连接
   ssh -o ConnectTimeout=10 vicki@<tailscale-ip>
   ```

3. **通过 CC-Server 中转** (如果 Surface 在线):
   ```bash
   ssh -J CC vicki@<Surface-Tailscale-IP>
   ```

### 连接 Victory

Victory SSH 端口 22 拒绝，可能：
- SSH 未运行
- 防火墙阻止
- 使用非标准端口

建议检查：
```bash
# 扫描 Victory 的 SSH 端口
nmap -p 22,2222,22222 100.100.1.8

# 或通过 Tailscale Web UI 查看
tailscale netcheck
```

---

## 📊 网络状态总结

| 组件 | 状态 | 连接方式 |
|------|------|----------|
| 本地 → 外网 | ✅ | Clash 隧道 |
| 本地 → CC-Server | ✅ | Tailscale 直连 |
| 本地 → Victory | ❌ | SSH 拒绝 |
| 本地 → Surface | ❌ | SSH 超时 |
| CC-Server → 外网 | ✅ | Clash 出口 |
| Tailscale 组网 | ✅ | 5 节点在线 |

---

## 🔍 下一步建议

1. **等待 Surface 唤醒** - 10-15 分钟后重试
2. **检查 Victory SSH 配置** - 确认端口和防火墙
3. **考虑 Cloudflare Tunnel** - 如需公网访问内网服务
4. **使用 Tailscale Funnel** - 临时暴露服务到公网

---

*检查完成时间：2026-03-10 07:35*  
*检查者：qwq (本地 Qwen Code 监控系统)*
