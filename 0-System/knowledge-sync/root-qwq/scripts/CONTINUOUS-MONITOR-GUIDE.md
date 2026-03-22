# 持续监控系统 - 使用指南

## 📋 概述

这套系统提供：
1. **每 5 分钟进度汇报** - 定期检查服务状态
2. **持续监控** - 30 秒间隔检查，自动恢复异常服务
3. **防崩溃包装器** - 捕获异常退出，自动重启
4. **多模式通知** - 前台/后台/静默模式

## 🚀 快速启动

### 启动监控服务
```bash
cd /root/air/qwq
chmod +x scripts/*.sh

# 方式 1: 使用 PM2（推荐，自动重启）
pm2 start scripts/pm2/monitor.config.js

# 方式 2: 直接启动守护进程
nohup bash scripts/5min-report.sh daemon > /tmp/5min-report-daemon.log 2>&1 &

# 方式 3: 使用 crash-wrapper 启动（防崩溃）
bash scripts/crash-wrapper.sh bash scripts/continuous-monitor.sh
```

### 查看状态
```bash
# PM2 方式
pm2 status
pm2 logs 5min-report
pm2 logs continuous-monitor

# 直接方式
tail -f /tmp/5min-report.log
tail -f /tmp/qwq-monitor/monitor.log
```

## 🔧 通知模式

### 设置通知模式
```bash
# 前台通知（有 DISPLAY 环境）
export NOTIFICATION_MODE=foreground

# 后台通知（无图形界面）
export NOTIFICATION_MODE=background

# 静默模式（只记录日志）
export NOTIFICATION_MODE=silent

# 自动检测（默认）
export NOTIFICATION_MODE=auto
```

### Termux 通知
需要安装 Termux:API:
```bash
pkg install termux-api
termux-notification --title "测试" --content "通知正常"
```

## 🛡️ 防崩溃机制

### 问题原因
进程异常退出通常由以下原因：
1. 后台线程占用资源
2. 内存不足被系统杀死
3. 网络异常导致超时
4. 输入命令导致会话终止

### 解决方案

#### 1. 使用 crash-wrapper
```bash
# 包装任何关键进程
bash scripts/crash-wrapper.sh bash scripts/continuous-monitor.sh

# 自定义参数
RESTART_DELAY=5 MAX_RESTARTS=10 bash scripts/crash-wrapper.sh <command>
```

#### 2. 使用 PM2（推荐）
```bash
# PM2 自动管理重启
pm2 start scripts/continuous-monitor.sh --name monitor
pm2 save  # 保存进程列表，开机自启
```

#### 3. SSH 会话保护
```bash
# 使用 screen 或 tmux
screen -S monitor
bash scripts/continuous-monitor.sh
# Ctrl+A, D 分离会话

# 或使用 nohup
nohup bash scripts/continuous-monitor.sh > /tmp/monitor.log 2>&1 &
```

## 📊 监控指标

### 心跳文件
- `/tmp/heartbeat-counter.txt` - 心跳计数
- `/tmp/5min-report.log` - 汇报日志
- `/tmp/qwq-monitor/monitor.log` - 监控日志

### 检查服务状态
```bash
# 快速检查
bash scripts/5min-report.sh check

# 查看详细状态
pm2 status
curl http://localhost:8766/api/health
curl -s --socks5-hostname localhost:7890 https://api.ip.sb/ip
```

## 🔍 故障排查

### 查看日志
```bash
# 最近 50 行
tail -50 /tmp/5min-report.log
tail -50 /tmp/qwq-monitor/monitor.log

# PM2 日志
pm2 logs --lines 50
```

### 手动测试
```bash
# 测试单次汇报
bash scripts/5min-report.sh report

# 测试服务检查
bash scripts/5min-report.sh check

# 测试通知
termux-notification --title "测试" --content "通知正常"
```

### 恢复服务
```bash
# 重启所有监控
pm2 restart all

# 或单独重启
pm2 restart 5min-report
pm2 restart continuous-monitor
```

## 📝 配置选项

### continuous-monitor.sh
- `interval`: 汇报间隔（默认 300 秒）
- `check_interval`: 检查间隔（默认 30 秒）
- `LOG_DIR`: 日志目录（默认 /tmp/qwq-monitor）

### crash-wrapper.sh
- `RESTART_DELAY`: 重启延迟（默认 3 秒）
- `MAX_RESTARTS`: 最大重启次数（默认 5 次）
- `RESTART_WINDOW`: 重启时间窗口（默认 60 秒）

## 🎯 最佳实践

1. **使用 PM2 管理所有服务** - 自动重启、日志管理
2. **定期导出日志** - 避免日志文件过大
3. **设置告警阈值** - 连续失败时通知
4. **使用 SSH 会话保护** - screen/tmux/nohup
5. **定期健康检查** - 检查所有依赖服务
