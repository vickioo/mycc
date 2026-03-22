# ⚠️ 需要重启 U22 容器

**创建时间**: 2026-03-07 15:05  
**优先级**: P0

---

## 📋 情况说明

已完成以下优化：

1. ✅ **对话界面优化** - 侧边栏可收折
2. ✅ **自然语言对话** - 代码已完成
3. ✅ **Termux 服务配置** - 已安装 termux-services
4. ✅ **进度管理页面** - 已上线

但由于 U22 容器的进程管理限制，**新代码无法加载**。

---

## 🔧 需要手动重启

### 方法 1: 重启 U22 App (推荐)
1. 关闭 U22 App
2. 重新打开 U22 App
3. 服务会自动恢复

### 方法 2: 重启手机
- 完全重启 Android 设备
- 所有服务会自动恢复

### 方法 3: 强制停止 (需要 Root)
```bash
# 在 Termux 中执行
su
pkill -9 com.termux.u22
# 然后重新打开 U22 App
```

---

## ✅ 重启后自动恢复

已创建恢复脚本：`/root/bin/resume-services.sh`

**重启后执行**:
```bash
/root/bin/resume-services.sh
```

这将自动启动：
- AI Team Hub (8772)
- ssh-gate 隧道
- PM2 服务

---

## 📊 重启后验证

```bash
# 检查对话功能
curl -X POST http://localhost:8772/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"qwq","message":"现在几点了"}'

# 预期回复：当前时间：2026-03-07 15:05:00
```

---

## 📱 Termux 原生命令探索

已创建探索脚本：`/root/air/qwq/scripts/explore-termux-api.sh`

**执行**:
```bash
bash /root/air/qwq/scripts/explore-termux-api.sh
```

**可探索的命令**:
- `termux-battery-status` - 电池状态
- `termux-wifi-info` - WiFi 信息（识别家庭/公司网络）
- `termux-network-status` - 网络状态
- `termux-tts-speak` - 语音播放
- `termux-notification` - 系统通知
- `termux-vibrate` - 震动反馈
- `termux-clipboard-get/set` - 剪贴板
- 等等...

---

## 🎯 重启后待办

1. **验证对话功能** - 测试自然语言对话
2. **命令前缀优化** - 实现 `/命令` 格式
3. **Termux API 集成** - 执行探索脚本
4. **网络环境识别** - 通过 WiFi SSID

---

**请重启 U22 容器后通知我继续！** 🚀
