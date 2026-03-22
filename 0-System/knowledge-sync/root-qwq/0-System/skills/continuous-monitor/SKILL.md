# 🛠️ Skill: continuous-monitor

**版本**: v1.0.0  
**描述**: 持续监控和自动恢复服务  
**触发词**: `/monitor`, `监控状态`, `服务健康`

---

## 功能

1. **服务检查** — 每 30 秒检查关键服务
2. **自动恢复** — 检测异常时自动重启
3. **日志记录** — 详细的监控日志
4. **PM2 管理** — 通过 PM2 守护进程

---

## 监控的服务

| 服务 | 检查方式 | 恢复方式 |
|------|----------|----------|
| **mobile-web** | HTTP GET /api/health | pm2 restart |
| **CC Clash Tunnel** | SOCKS5 代理测试 | ssh tunnel restart |
| **PM2** | pm2 list | pm2 resurrect |

---

## 用法

### 启动服务

```bash
# 通过 PM2
pm2 start /root/air/qwq/scripts/continuous-monitor.sh --name continuous-monitor

# 查看状态
pm2 status continuous-monitor

# 查看日志
pm2 logs continuous-monitor
```

### 手动检查

```bash
# 检查服务状态
bash /root/air/qwq/scripts/continuous-monitor.sh check

# 查看监控日志
tail -f /tmp/qwq-monitor/monitor.log
```

---

## 文件位置

| 文件 | 路径 |
|------|------|
| **主程序** | `/root/air/qwq/scripts/continuous-monitor.sh` |
| **防崩溃包装** | `/root/air/qwq/scripts/crash-wrapper.sh` |
| **监控日志** | `/tmp/qwq-monitor/monitor.log` |

---

## 配置

### 检查间隔

```bash
local interval=600  # 汇报间隔 (10 分钟)
local check_interval=30  # 检查间隔 (30 秒)
```

### 恢复限制

```bash
MAX_RESTARTS=5  # 最大重启次数
RESTART_WINDOW=60  # 时间窗口 (秒)
```

---

## 错误处理

### 常见问题

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| mobile-web 异常 | 服务未启动 | `pm2 start mobile-web` |
| Clash Tunnel 异常 | SSH 中断 | `bash /root/cc-clash-tunnel.sh restart` |
| 恢复失败 | 权限不足 | 检查 SSH 密钥配置 |

---

## 日志示例

```
[2026-03-10 20:57:48] ⚠️  检测到问题:
[2026-03-10 20:57:48]   - mobile-web 服务异常
[2026-03-10 20:57:48] 🔄 尝试恢复服务：mobile-web 服务异常
[2026-03-10 20:57:53] ❌ 恢复失败：mobile-web 服务异常
```

---

*创建*: 2026-03-10  
*维护者*: qwq
