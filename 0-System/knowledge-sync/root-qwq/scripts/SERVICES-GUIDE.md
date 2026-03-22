# U22 服务管理指南

## 问题分析

### 原始问题

> "U22 系统启动的脚本一直报零之类的错误"

**根本原因**:

1. **PM2 不适合管理 SSH 隧道**
   - PM2 的 fork 模式会发送 SIGINT 信号
   - SSH 隧道收到 SIGINT 后立即退出
   - 日志显示 `exited with code [0] via signal [SIGINT]`

2. **脚本误报成功**
   - 端口被占用时仍输出 "✅ Tunnel started"
   - 没有实际验证代理是否工作

3. **/proc 未挂载**
   - 容器环境中 `/proc/uptime` 不可用
   - PM2 不断警告 `We couldn't find uptime from /proc/uptime`

---

## 解决方案

### 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **nohup 直启** | ✅ 简单可靠<br>✅ 无信号干扰<br>✅ 资源占用低 | ⚠️ 无自动重启 | 容器/无 systemd |
| **systemd** | ✅ 系统级管理<br>✅ 自动重启<br>✅ 日志完善 | ❌ 需要 systemd | 完整 Linux 系统 |
| **PM2** | ✅ 统一管理<br>✅ 日志聚合 | ❌ SSH 隧道不兼容 | Node.js 应用 |
| **Supervisord** | ✅ 进程管理完善 | ⚠️ 需额外安装 | Python 环境 |

### 当前方案：nohup + Watchdog

**架构**:
```
┌─────────────────────────────────────────┐
│  cc-clash-watchdog.sh (每 30 秒检查)     │
│    │                                    │
│    ▼ 发现异常时重启                      │
│  ┌─────────────────────────────────┐    │
│  │  cc-clash-tunnel.sh (SSH 隧道)   │    │
│  │    │                            │    │
│  │    ▼                            │    │
│  │  SSH -N -D 7890 CC              │    │
│  └─────────────────────────────────┘    │
│                                          │
│    ▼                                    │
│  CC Server Clash → 互联网                │
└─────────────────────────────────────────┘
```

---

## 使用方法

### 一键管理所有服务

```bash
# 查看状态
/root/air/qwq/scripts/services-manager.sh status

# 启动所有
/root/air/qwq/scripts/services-manager.sh start

# 停止所有
/root/air/qwq/scripts/services-manager.sh stop

# 重启所有
/root/air/qwq/scripts/services-manager.sh restart
```

### 单独管理

```bash
# Clash 隧道
/root/cc-clash-tunnel.sh {start|stop|restart|status}

# 查看日志
tail -f /tmp/cc-clash-tunnel.log

# Watchdog 日志
tail -f /tmp/cc-clash-watchdog.log
```

### PM2 服务

```bash
# free-claude-code
pm2 start|stop|restart free-claude-code
pm2 logs free-claude-code

# 查看 PM2 状态
pm2 list
```

---

## 服务列表

| 服务 | 管理方式 | 端口 | 说明 |
|------|----------|------|------|
| cc-clash-tunnel | nohup | 7890 | SSH 隧道 |
| cc-clash-watchdog | nohup | - | 守护进程 |
| free-claude-code | PM2 | 8083 | Claude 代理 |
| mobile-web | nohup | 8769 | 移动端 V8 |
| mycc | nohup | 18080 | MyCC 后端 |

---

## 开机自启

### 方案 1: Crontab (@reboot)

```bash
# 编辑 crontab
crontab -e

# 添加
@reboot /root/air/qwq/scripts/services-manager.sh start
```

### 方案 2: /etc/rc.local

```bash
# 编辑 rc.local
sudo nano /etc/rc.local

# 添加
/root/air/qwq/scripts/services-manager.sh start &

# 确保可执行
sudo chmod +x /etc/rc.local
```

### 方案 3: Systemd (如果支持)

```bash
# 复制服务文件
sudo cp /root/air/qwq/scripts/systemd/cc-clash-*.service /etc/systemd/system/

# 启用
sudo systemctl enable cc-clash-tunnel
sudo systemctl enable cc-clash-watchdog
```

---

## 故障排查

### 隧道无法启动

```bash
# 1. 检查端口占用
fuser 7890/tcp

# 2. 清理旧进程
pkill -f "ssh -N -D 7890"

# 3. 手动启动测试
/root/cc-clash-tunnel.sh start

# 4. 查看日志
tail -f /tmp/cc-clash-tunnel.log
```

### Watchdog 频繁重启

```bash
# 查看 watchdog 日志
tail -f /tmp/cc-clash-watchdog.log

# 检查重启原因
# - "Tunnel unhealthy" = 隧道真的有问题
# - 达到 MAX_RESTARTS = 需要手动干预
```

### 代理不工作

```bash
# 测试隧道
curl --socks5-hostname localhost:7890 https://api.ip.sb/ip

# 检查 SSH 连接
ssh -v CC "echo test"

# 查看隧道进程
ps aux | grep "ssh -N"
```

---

## 脚本说明

### cc-clash-tunnel.sh

```bash
# 功能
- start:   启动 SSH 隧道（使用 exec 保持进程）
- stop:    停止隧道并清理
- restart: 重启隧道
- status:  检查健康状态（实际测试代理）

# 关键改进
1. 启动时清空日志
2. 启动前检查是否已运行且健康
3. 使用 exec 保持 SSH 进程
4. status 命令实际测试代理连通性
```

### cc-clash-watchdog.sh

```bash
# 功能
- 每 30 秒检查隧道健康
- 最多自动重启 5 次
- 详细日志记录
- 健康时重置重启计数

# 检查逻辑
1. PID 文件存在
2. 进程运行中
3. 代理实际可用 (curl 测试)
```

### services-manager.sh

```bash
# 功能
- start:   按顺序启动所有服务
- stop:    优雅停止所有服务
- restart: 重启所有服务
- status:  显示所有服务状态

# 服务列表
1. cc-clash-tunnel
2. cc-clash-watchdog
3. free-claude-code (PM2)
4. mobile-web
5. mycc
```

---

## 最佳实践

### 1. 定期检查

```bash
# 添加到 crontab，每小时检查
0 * * * * /root/air/qwq/scripts/services-manager.sh status >> /tmp/services-check.log 2>&1
```

### 2. 日志轮转

```bash
# 添加到 crontab，每天清理旧日志
0 0 * * * find /tmp -name "*.log" -mtime +7 -delete
```

### 3. 监控告警

```bash
# 简单监控脚本
cat > /root/check-services.sh << 'EOF'
#!/bin/bash
if ! curl -s --socks5-hostname localhost:7890 https://api.ip.sb/ip >/dev/null 2>&1; then
    echo "Clash tunnel down!" | mail -s "Alert" admin@example.com
    /root/air/qwq/scripts/services-manager.sh restart
fi
EOF
chmod +x /root/check-services.sh
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-07 | 初始版本，nohup + watchdog |
| v1.1 | 2026-03-07 | 添加 services-manager.sh |
| v1.2 | 2026-03-07 | 添加 systemd 配置（可选） |

---

*Last updated: 2026-03-07*
