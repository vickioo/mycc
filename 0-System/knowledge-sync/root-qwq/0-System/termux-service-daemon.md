# Termux service-daemon 说明

**日期**: 2026-03-07  
**状态**: 分析完成

---

## 📋 service-daemon 是什么？

### 定义

`termux-service-daemon` 是 Termux 后台服务管理器，负责：

1. **后台进程保活** - 防止 Android 系统杀死后台服务
2. **服务注册** - 注册系统级服务
3. **自动重启** - 服务崩溃后自动重启
4. **电源管理** - 获取唤醒锁防止休眠

### 为什么需要？

Android 系统会主动杀死后台进程以节省电量。`service-daemon` 通过 Android 的 `Service` 机制让进程获得更高优先级。

---

## 🔍 当前状态分析

### Termux sshd 状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| sshd 进程 | ✅ 运行中 | PID 19625 |
| sshd-session | ✅ 运行中 | PID 25022/25025 |
| runsv sshd | ✅ 运行中 | PID 27177 |
| svlogd | ✅ 运行中 | PID 27209 |
| 8022 端口 | ❌ 未监听 | 端口绑定失败 |
| service-daemon | ❌ 未运行 | 无后台保护 |

### 问题分析

1. **sshd 进程存在但端口未监听**
   - sshd 进程在运行
   - 但 8022 端口无法访问
   - 可能是 Android 网络权限问题

2. **sv start sshd 失败**
   ```
   fail: sshd: unable to change to service directory: file does not exist
   ```
   - 缺少 service 目录
   - 需要创建 `~/.termux/services/`

3. **service-daemon 未运行**
   - 没有后台保护
   - 屏幕关闭后可能被杀死

---

## 🔧 解决方案

### 方案 A: 使用 termux-services (推荐)

```bash
# 在 Termux 中执行
pkg install termux-services

# 创建服务目录
mkdir -p ~/.termux/services

# 复制 sshd 服务脚本
cp /data/data/com.termux/files/usr/etc/services/sshd.sh ~/.termux/services/

# 启动 service-daemon
termux-services enable sshd.sh
```

### 方案 B: 手动创建服务

```bash
# 在 Termux 中执行
mkdir -p ~/.termux/services

# 创建 sshd 服务脚本
cat > ~/.termux/services/sshd.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec sshd -D -e -R
EOF

chmod +x ~/.termux/services/sshd.sh

# 重启 Termux 或手动启动
pkill sshd
sshd -D -e -R &
```

### 方案 C: 使用 Termux:Boot (开机自启)

```bash
# 安装 Termux:Boot App
# 创建启动脚本
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/start-sshd.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
sleep 5
sshd -D -e -R &
EOF

chmod +x ~/.termux/boot/start-sshd.sh
```

---

## 📊 对比分析

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **termux-services** | 自动保活、重启 | 需要额外安装 | ⭐⭐⭐⭐⭐ |
| **手动服务** | 简单直接 | 无自动保护 | ⭐⭐⭐ |
| **Termux:Boot** | 开机自启 | 需要 App | ⭐⭐⭐⭐ |
| **纯手动** | 最简单 | 息屏即断 | ⭐ |

---

## 🎯 当前建议

### 短期方案

由于 sshd 进程已在运行但端口未监听：

```bash
# 在 Termux 中重启 sshd
pkill sshd
sshd

# 检查端口
ss -tlnp | grep 8022
```

### 长期方案

安装 termux-services 获得完整保护：

```bash
# 在 Termux 中执行
pkg install termux-services
termux-services enable sshd
```

---

## 🔗 U22 隧道状态

### ssh-gate 服务

| 检查项 | 状态 |
|--------|------|
| ssh-gate | ⚠️ 运行但不健康 |
| 8821 端口 | ❌ 未监听 |
| gate 连接 | ✅ 正常 |

### 修复建议

```bash
# 重启 ssh-gate
/root/bin/sv/sv restart ssh-gate

# 检查日志
tail -20 /root/.local/sv/ssh-gate/log/current
```

---

## 📝 总结

### service-daemon 的作用

1. **后台保活** - 防止 Android 杀死服务
2. **自动重启** - 服务崩溃自动恢复
3. **电源管理** - 获取唤醒锁
4. **服务注册** - 系统级服务管理

### 是否需要？

**是的，需要！** 原因：

- Android 会主动杀死后台进程
- 没有 service-daemon，息屏后 SSH 会断开
- 长期运行需要 service-daemon 保护

### 下一步

1. 在 Termux 安装 termux-services
2. 配置 sshd 服务
3. 测试息屏保活
4. 修复 U22 隧道

---

*分析时间：2026-03-07 13:55*
