# Termux SSHD 长期运行指南

**问题**: Termux 的 SSHD 默认不会自启动，需要配置

---

## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| Termux:Boot | ✅ 系统级自启<br>✅ 开机自动运行 | ⚠️ 需安装额外应用 | ⭐⭐⭐⭐⭐ |
| Tasker 自动化 | ✅ 功能强大<br>✅ 可定制条件 | ⚠️ 需 Tasker 应用<br>⚠️ 付费 | ⭐⭐⭐⭐ |
| 前台服务通知 | ✅ 无需额外应用<br>✅ 系统保活 | ⚠️ 有通知栏图标 | ⭐⭐⭐ |
| 手动启动 | ✅ 简单 | ❌ 重启后失效 | ⭐ |

---

## 方案 1: Termux:Boot (推荐)

### 安装

1. 下载 **Termux:Boot** (F-Droid 或 GitHub)
   - GitHub: https://github.com/termux/termux-boot/releases
   - F-Droid: https://f-droid.org/packages/com.termux.boot/

2. 安装后打开应用授予权限

### 配置

已完成 ✅ 脚本位置：
```bash
~/.termux/boot/start-sshd.sh       # SSH 守护进程
~/.termux/boot/start-sv-services.sh # sv 服务
```

### 测试

```bash
# 在 Termux 中测试 boot 脚本
~/.termux/boot/start-sshd.sh
```

### 注意事项

- 脚本在系统启动完成后运行
- 需要等待网络就绪（脚本已包含 sleep）
- 首次启动可能需要 30 秒

---

## 方案 2: Tasker 自动化

### 安装

- Tasker (付费): https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm
- 或 ATasker (免费替代)

### 配置步骤

1. **创建 Profile**:
   - 触发器：设备启动 (Device Boot)
   - 或：网络可用 (Network Available)

2. **创建 Task**:
   ```
   名称：Start SSHD
   类型：Code
   内容：
   ```

3. **添加 Action**:
   ```bash
   # 等待网络
   Wait: 10 秒
   
   # 启动 sshd
   Run Shell:
     Command: sshd -p 8022 -h ~/.ssh/hostkeys
     Use Root: 否
   
   # 验证
   Run Shell:
     Command: pgrep -f sshd
     Store Result In: %SSHD_PID
   
   # 通知
   If: %SSHD_PID != ""
     Then: 显示通知 "SSHD 已启动"
   ```

### 导入配置

已创建 Tasker 配置导出文件：
```bash
~/.termux/tasker/start-sshd.xml
```

---

## 方案 3: 前台服务保活

### 使用 termux-api

```bash
# 安装 termux-api
pkg install termux-api

# 创建前台服务脚本
cat > ~/start-foreground-sshd.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

# 发送通知
termux-notification --id sshd-service \
    --title "SSH 守护进程" \
    --text "运行中 - 端口 8022" \
    --ongoing true \
    --channel sshd

# 启动 sshd
sshd -p 8022 -h ~/.ssh/hostkeys

# 保持运行
while true; do
    pgrep -f sshd >/dev/null || sshd -p 8022 -h ~/.ssh/hostkeys
    sleep 30
done
EOF

chmod +x ~/start-foreground-sshd.sh
```

### 创建服务频道

```bash
termux-notification --channel sshd \
    --channel-name "SSH 服务" \
    --channel-importance low
```

---

## 方案 4: 电池优化白名单

### 添加电池优化例外

```bash
# 在 Android 设置中：
设置 → 应用 → Termux → 电池 → 无限制
```

### ADB 命令（需要电脑）

```bash
adb shell pm grant com.termux android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
```

---

## 当前配置状态

### ✅ 已完成

| 项目 | 状态 | 位置 |
|------|------|------|
| SSHD 脚本 | ✅ | `~/.termux/boot/start-sshd.sh` |
| SV 服务脚本 | ✅ | `~/.termux/boot/start-sv-services.sh` |
| SSH 密钥 | ✅ | `~/.ssh/id_ed25519_vi` |
| SSH 配置 | ✅ | `~/.ssh/config` |
| 主机密钥 | ✅ | `~/.ssh/hostkeys/` |

### ⚠️ 待完成

| 项目 | 说明 |
|------|------|
| 安装 Termux:Boot | 从 F-Droid 或 GitHub 下载 |
| 授予自启权限 | 在 Android 设置中 |
| 电池优化白名单 | 设置 → 应用 → Termux → 电池 |

---

## 快速验证

```bash
# 1. 检查 sshd 是否运行
ssh -p 8022 localhost "pgrep -f sshd"

# 2. 测试 boot 脚本
ssh -p 8022 localhost "~/.termux/boot/start-sshd.sh"

# 3. 检查文件权限
ssh -p 8022 localhost "ls -la ~/.termux/boot/"
```

---

## 故障排查

### SSHD 无法启动

```bash
# 检查端口占用
ssh -p 8022 localhost "netstat -tlnp | grep 8022"

# 手动启动测试
ssh -p 8022 localhost "sshd -d -p 8022"

# 查看日志
ssh -p 8022 localhost "logcat -s termux:*"
```

### Boot 脚本不执行

```bash
# 检查权限
ssh -p 8022 localhost "chmod +x ~/.termux/boot/*.sh"

# 检查 Termux:Boot 是否安装
ls /data/data/com.termux.boot/

# 手动测试
~/.termux/boot/start-sshd.sh
```

### 重启后失效

1. 确认 Termux:Boot 已安装
2. 授予自启动权限
3. 电池优化设为无限制
4. 检查脚本权限 `chmod +x`

---

## 推荐配置流程

```
1. 安装 Termux:Boot (F-Droid)
       ↓
2. 授予自启动权限 (Android 设置)
       ↓
3. 电池优化白名单
       ↓
4. 测试 boot 脚本
       ↓
5. 重启手机验证
```

---

## 长期运行建议

### 1. 系统设置

- 关闭电池优化
- 锁定 Termux 到最近应用
- 允许后台活动

### 2. 监控脚本

创建健康检查脚本：
```bash
cat > ~/check-sshd.sh << 'EOF'
#!/bin/bash
if ! pgrep -f "sshd.*8022" >/dev/null; then
    sshd -p 8022 -h ~/.ssh/hostkeys
    echo "[$(date)] SSHD restarted" >> ~/sshd.log
fi
EOF
```

### 3. 定时检查

使用 termux-job 或 cron:
```bash
# 每 5 分钟检查
crontab -e
*/5 * * * * ~/check-sshd.sh
```

---

## 资源

- Termux:Boot GitHub: https://github.com/termux/termux-boot
- Termux Wiki: https://wiki.termux.com
- Termux:Boot 配置：https://github.com/termux/termux-boot#readme
