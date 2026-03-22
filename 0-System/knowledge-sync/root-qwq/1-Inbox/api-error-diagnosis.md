# 🔧 API Error 诊断报告

**错误**: `✕ [API Error: terminated]`  
**诊断时间**: 2026-03-10 21:00

---

## 🔍 错误根源

### 触发链

```
continuous-monitor (PM2)
  ├─ 每 30 秒检查服务状态
  ├─ 检测到 mobile-web 异常
  ├─ 检测到 CC Clash Tunnel 异常
  └─ 尝试恢复失败 → 记录错误日志
```

### 具体问题

| 服务 | 状态 | 原因 |
|------|------|------|
| **mobile-web** | ❌ 未运行 | 服务未启动或端口 8766 无响应 |
| **CC Clash Tunnel** | ❌ 未运行 | SSH 隧道中断或超时 |

---

## 📋 解决方案

### 1. 启动 mobile-web

```bash
# 检查是否在 mycc 目录
cd /root/air/mycc && pm2 start mobile-web

# 或检查端口占用
lsof -i :8766
```

### 2. 重启 Clash Tunnel

```bash
# 使用脚本重启
bash /root/cc-clash-tunnel.sh restart

# 或手动启动
ssh -N -D 7890 -o ServerAliveInterval=15 CC &
```

### 3. 停止误报 (可选)

如果这些服务不需要运行：

```bash
# 编辑 continuous-monitor.sh，移除这些检查
# 或停止 PM2 服务
pm2 stop continuous-monitor
```

---

## 🔗 相关调用链

### mycc API 调用

```javascript
// /root/air/mycc/.claude/skills/mycc/scripts/dist/channels/feishu.js
fetch("https://open.feishu.cn/open-apis/im/v1/messages")

// /root/air/mycc/.claude/skills/mycc/scripts/dist/index.js
fetch(`${WORKER_URL}/register`)

// /root/air/mycc/.claude/skills/mycc/scripts/dist/tunnel-provider.js
fetch(`${this.tunnelUrl}/health`)
```

**注意**: 这些是飞书通知和隧道健康检查，与当前错误无关。

---

*诊断完成时间：2026-03-10 21:00*
