# CC Clash Tunnel - Systemd 服务配置指南

## 问题分析

### 原 PM2 方案的问题

1. **SIGINT 信号问题**: PM2 的 fork 模式会发送 SIGINT 信号，导致 SSH 隧道断开
2. **日志误报**: `exited with code [0]` 被 PM2 视为正常退出，实际是异常断开
3. **/proc 挂载问题**: 容器环境中 `/proc/uptime` 不可用，导致 PM2 警告
4. **端口占用误报**: 脚本在端口被占用时仍报告成功

### 为什么选择 systemd

| 特性 | PM2 | systemd |
|------|-----|---------|
| 长连接支持 | ❌ 信号干扰 | ✅ 原生支持 |
| 日志管理 | ⚠️ 需 PM2 日志 | ✅ journalctl 统一 |
| 启动顺序 | ⚠️ 需手动配置 | ✅ 依赖管理 |
| 资源限制 | ⚠️ 有限 | ✅ cgroups 完整 |
| 安全加固 | ❌ 无 | ✅ 多种隔离 |
| 系统整合 | ⚠️ 用户态 | ✅ 系统级 |

---

## 安装步骤

### 1. 停止 PM2 服务

```bash
pm2 stop cc-clash-tunnel cc-clash-watchdog
pm2 delete cc-clash-tunnel cc-clash-watchdog
```

### 2. 复制服务文件

```bash
sudo cp /root/air/qwq/scripts/systemd/cc-clash-tunnel.service /etc/systemd/system/
sudo cp /root/air/qwq/scripts/systemd/cc-clash-watchdog.service /etc/systemd/system/
```

### 3. 重新加载 systemd

```bash
sudo systemctl daemon-reload
```

### 4. 启用并启动服务

```bash
# 启用开机自启
sudo systemctl enable cc-clash-tunnel
sudo systemctl enable cc-clash-watchdog

# 启动服务
sudo systemctl start cc-clash-tunnel
sudo systemctl start cc-clash-watchdog
```

### 5. 验证状态

```bash
# 查看服务状态
sudo systemctl status cc-clash-tunnel
sudo systemctl status cc-clash-watchdog

# 查看日志
journalctl -u cc-clash-tunnel -f
journalctl -u cc-clash-watchdog -f

# 测试代理
curl --socks5-hostname localhost:7890 https://api.ip.sb/ip
```

---

## 管理命令

```bash
# 启动/停止/重启
sudo systemctl start cc-clash-tunnel
sudo systemctl stop cc-clash-tunnel
sudo systemctl restart cc-clash-tunnel

# 查看状态
sudo systemctl status cc-clash-tunnel

# 查看日志
journalctl -u cc-clash-tunnel -n 50      # 最近 50 行
journalctl -u cc-clash-tunnel -f         # 实时追踪
journalctl -u cc-clash-tunnel --since today  # 今日日志

# 禁用开机自启
sudo systemctl disable cc-clash-tunnel
```

---

## 故障排查

### 服务无法启动

```bash
# 检查服务状态
sudo systemctl status cc-clash-tunnel

# 查看详细日志
journalctl -u cc-clash-tunnel -xb

# 测试手动启动
/root/cc-clash-tunnel.sh start
```

### 隧道连接失败

```bash
# 检查 SSH 连接
ssh -v CC "echo test"

# 检查端口占用
ss -tlnp | grep 7890

# 测试代理
curl --socks5-hostname localhost:7890 --connect-timeout 5 https://api.ip.sb/ip
```

### Watchdog 频繁重启

```bash
# 查看 watchdog 日志
journalctl -u cc-clash-watchdog -f

# 检查重启原因
# 如果看到 "Tunnel unhealthy"，检查隧道状态
/root/cc-clash-tunnel.sh status
```

---

## 卸载

```bash
# 停止服务
sudo systemctl stop cc-clash-tunnel
sudo systemctl stop cc-clash-watchdog

# 禁用服务
sudo systemctl disable cc-clash-tunnel
sudo systemctl disable cc-clash-watchdog

# 删除服务文件
sudo rm /etc/systemd/system/cc-clash-tunnel.service
sudo rm /etc/systemd/system/cc-clash-watchdog.service

# 重新加载
sudo systemctl daemon-reload
```

---

## 脚本说明

### cc-clash-tunnel.sh

- `start`: 启动 SSH 隧道（使用 exec 保持进程）
- `stop`: 停止隧道并清理进程
- `restart`: 重启隧道
- `status`: 检查隧道健康状态（实际测试代理）

### cc-clash-watchdog.sh

- 每 30 秒检查隧道健康
- 最多自动重启 5 次
- 详细日志记录
- 健康时重置重启计数

---

*Last updated: 2026-03-07*
