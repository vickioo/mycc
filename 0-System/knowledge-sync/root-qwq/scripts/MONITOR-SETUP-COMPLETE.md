# 持续监控系统 - 部署完成

## ✅ 已部署组件

### 1. 5 分钟汇报服务
- **文件**: `/root/air/qwq/scripts/5min-report.sh`
- **PM2 名称**: `5min-report`
- **功能**: 每 5 分钟生成进度汇报，支持通知
- **模式**: 
  - `report` - 单次汇报
  - `daemon` - 守护模式（PM2 使用）
  - `check` - 仅检查状态

### 2. 持续监控服务
- **文件**: `/root/air/qwq/scripts/continuous-monitor.sh`
- **PM2 名称**: `continuous-monitor`
- **功能**: 每 30 秒检查服务，自动恢复异常
- **监控项**: mobile-web, CC Clash Tunnel, PM2

### 3. 防崩溃包装器
- **文件**: `/root/air/qwq/scripts/crash-wrapper.sh`
- **功能**: 捕获异常退出，自动重启（最多 5 次/60 秒）

### 4. 快速状态检查
- **文件**: `/root/air/qwq/scripts/quick-status.sh`
- **功能**: 一键检查所有服务状态

## 🚀 启动命令

```bash
# 启动监控
pm2 start /root/air/qwq/scripts/pm2/monitor.config.js

# 查看状态
pm2 status
pm2 logs --lines 20

# 快速检查
bash /root/air/qwq/scripts/quick-status.sh

# 手动汇报
bash /root/air/qwq/scripts/5min-report.sh report
```

## 📊 当前状态

```
✅ PM2 进程：运行中
✅ 心跳计数：已初始化
⚠️  mobile-web: 未运行（正常，按需启动）
⚠️  CC Clash Tunnel: 未运行（正常，按需启动）
✅ 监控系统：正常运行
```

## 🔧 通知模式配置

编辑 PM2 配置文件设置通知模式：
```javascript
env: {
  NOTIFICATION_MODE: 'auto'  // auto, foreground, background, silent
}
```

## 🛡️ 防崩溃机制

### 问题原因
进程突然退出通常因为：
1. SSH 会话终止
2. 后台线程占用资源
3. 内存不足
4. 网络异常

### 解决方案
1. **PM2 守护**（已部署）- 自动重启
2. **crash-wrapper** - 捕获异常，延迟重启
3. **nohup/screen** - 会话保护

## 📝 日志位置

| 组件 | 日志文件 |
|------|----------|
| 5min-report | `/tmp/5min-report.log` |
| continuous-monitor | `/tmp/qwq-monitor/monitor.log` |
| PM2 5min-report | `/tmp/pm2-5min-report.out.log` |
| PM2 continuous-monitor | `/tmp/pm2-continuous-monitor.out.log` |

## 🔍 故障排查

### 查看实时日志
```bash
pm2 logs 5min-report --lines 50
pm2 logs continuous-monitor --lines 50
```

### 重启监控
```bash
pm2 restart all
```

### 测试通知
```bash
termux-notification --title "测试" --content "通知正常"
```

## 📈 下次汇报

监控系统已启动，将在：
- 每 5 分钟生成汇报
- 每 30 秒检查服务状态
- 发现异常自动恢复

**第一次汇报已生成**，查看：
```bash
cat /tmp/5min-report.log
```

## 🎯 避免进程异常退出的最佳实践

1. **始终使用 PM2 管理关键进程**
   ```bash
   pm2 start <script> --name <name>
   pm2 save  # 开机自启
   ```

2. **使用 crash-wrapper 包装**
   ```bash
   bash scripts/crash-wrapper.sh <command>
   ```

3. **SSH 会话保护**
   ```bash
   screen -S <session-name>
   # 或
   tmux new -s <session-name>
   ```

4. **避免在交互式 shell 中直接运行长进程**
   - 使用 `nohup` 或 `disown`
   - 或直接使用 PM2

5. **设置合理的超时和重试**
   - SSH: `ServerAliveInterval=15`
   - HTTP: `--connect-timeout 2`
