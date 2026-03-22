# Termux 优化计划

**创建日期**: 2026-03-07  
**状态**: 📋 待执行  
**优先级**: P0

---

## 📊 当前状态

### 已确认问题

| 问题 | 状态 | 影响 |
|------|------|------|
| sshd 进程运行 | ✅ | 正常 |
| 8022 端口监听 | ❌ | 无法连接 |
| service-daemon | ❌ 未运行 | 息屏后断开 |
| 服务目录 | ❌ 不存在 | 无法使用 sv 管理 |

### 系统信息

```
Termux 版本：latest
Android 版本：待确认
SSH 端口：8022
SSH 用户：u0_a351
```

---

## 🎯 优化目标

### P0 - 立即执行

1. **修复 SSH 连接**
   - 重启 sshd 服务
   - 确认 8022 端口监听
   - 测试 U22 连接

2. **安装 termux-services**
   - 获取后台保活
   - 防止系统杀死进程
   - 自动重启服务

3. **配置开机自启**
   - 安装 Termux:Boot
   - 创建启动脚本
   - 测试重启生效

### P1 - 本周完成

4. **API 能力集成**
   - termux-wifi-info (WiFi 信息)
   - termux-network-status (网络状态)
   - termux-tts-speak (语音播放)
   - termux-notification (通知)

5. **网络环境识别**
   - 检测当前 WiFi 名称
   - 区分家庭/公司网络
   - 自动切换配置

### P2 - 本月完成

6. **移动能力扩展**
   - 传感器读取
   - 位置信息
   - 电池状态
   - 剪贴板访问

7. **语音交互**
   - 本地 TTS
   - 语音通知
   - 离线语音

---

## 🔧 实施步骤

### Step 1: 修复 SSH 连接

```bash
# 在 Termux 中执行
pkill sshd
sshd

# 验证
ss -tlnp | grep 8022
```

### Step 2: 安装 termux-services

```bash
# 安装
pkg install termux-services

# 创建服务目录
mkdir -p ~/.termux/services

# 复制 sshd 服务
cp $PREFIX/etc/services/sshd.sh ~/.termux/services/

# 启用服务
termux-services enable sshd.sh

# 验证
termux-services list
```

### Step 3: 安装 Termux:Boot

```bash
# 1. 安装 Termux:Boot App (从 F-Droid 或 Play Store)

# 2. 创建启动脚本
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/start-services.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
sleep 5
sshd &
EOF

chmod +x ~/.termux/boot/start-services.sh

# 3. 重启手机测试
```

### Step 4: 安装 Termux:API

```bash
# 安装 API 包
pkg install termux-api

# 安装 API App (从 F-Droid 或 Play Store)

# 测试命令
termux-battery-status
termux-wifi-info
termux-notification --title "测试" --text "通知测试"
```

---

## 📋 检查清单

### 基础服务

- [ ] sshd 运行正常
- [ ] 8022 端口监听
- [ ] U22 可连接
- [ ] service-daemon 运行
- [ ] 息屏后保持连接

### Termux:Boot

- [ ] App 已安装
- [ ] 启动脚本创建
- [ ] 权限已授予
- [ ] 重启测试通过

### Termux:API

- [ ] API 包安装
- [ ] API App 安装
- [ ] 权限已授予
- [ ] 命令测试通过

### 网络识别

- [ ] WiFi 名称检测
- [ ] 网络环境判断
- [ ] 自动配置切换

---

## 📊 预期效果

### 优化前

```
❌ SSH 连接不稳定
❌ 息屏后断开
❌ 需要手动重启
❌ 无网络感知能力
```

### 优化后

```
✅ SSH 连接稳定
✅ 后台持续运行
✅ 开机自动启动
✅ 自动识别网络
✅ 丰富的 API 能力
```

---

## 🔗 相关文档

- `/root/air/qwq/0-System/termux-service-daemon.md`
- `/root/air/qwq/0-System/architecture-v7.md`
- `/root/air/qwq/0-System/termux-architecture.md`

---

## 📞 执行方式

### 远程执行 (推荐)

```bash
# 从 U22 执行
ssh -p 8022 localhost 'bash -s' < termux-optimization.sh
```

### 手动执行

在 Termux App 中直接执行上述命令。

---

*计划版本：V1.0*  
*创建日期：2026-03-07*  
*下次审查：2026-03-08*
