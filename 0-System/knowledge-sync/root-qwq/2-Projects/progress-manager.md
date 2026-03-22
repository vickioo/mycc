# AI Team 进度管理

**创建**: 2026-03-07 15:00  
**版本**: V7.0

---

## 📊 当前状态总览

| 模块 | 状态 | 进度 | 说明 |
|------|------|------|------|
| **对话界面** | ✅ | 100% | 侧边栏可收折 |
| **自然语言对话** | ⚠️ | 90% | 代码完成，等待重启 |
| **命令前缀优化** | 📋 | 0% | 待实现 (/命令) |
| **Termux 服务** | ✅ | 80% | 已配置，待重启生效 |
| **Surface 语音** | ✅ | 100% | NoizAI 已安装 |
| **导航优化** | ✅ | 100% | 全部页面完成 |
| **进度追踪** | ✅ | 100% | 页面已上线 |

---

## 🎯 待办事项

### P0 - 立即执行
- [ ] **重启 U22 容器** - 加载新代码
- [ ] **命令前缀优化** - 使用 `/命令` 格式
- [ ] **Termux 原生命令挖掘** - 探索可用 API

### P1 - 本周完成
- [ ] Termux:API 完整集成
- [ ] WiFi/网络环境识别
- [ ] 语音通知系统

### P2 - 本月完成
- [ ] 公司主机发现 (Qorder)
- [ ] Victory Windows 集成
- [ ] SJLL 隧道重建

---

## 🔧 命令前缀优化方案

### 当前问题
- 自然语言和命令混用，难以区分
- 需要逐个检测关键词
- 容易误判

### 优化方案
```
# 命令格式
/help          # 帮助
/status        # 服务状态
/tasks         # 任务队列
/usage         # 用量统计
/proxy         # 代理检查
/time          # 当前时间
/whoami        # 我是谁

# 自然语言（可选支持）
你好           # 问候
现在几点了     # 时间查询
```

### 实现方式
```python
if message.startswith('/'):
    # 命令模式
    command = message.split()[0]
    if command == '/help':
        response = "帮助信息..."
    elif command == '/status':
        response = run_cmd('sv status')
    # ...
else:
    # 自然语言模式（可选）
    response = nlp_response(message)
```

---

## 📱 Termux 原生命令挖掘

### 已确认可用
| 命令 | 功能 | 状态 |
|------|------|------|
| `termux-battery-status` | 电池状态 | 📋 |
| `termux-wifi-info` | WiFi 信息 | 📋 |
| `termux-network-status` | 网络状态 | 📋 |
| `termux-tts-speak` | 语音播放 | 📋 |
| `termux-notification` | 通知 | 📋 |
| `termux-location` | 位置 | 📋 |
| `termux-sensor` | 传感器 | 📋 |
| `termux-clipboard-get` | 剪贴板读取 | 📋 |
| `termux-clipboard-set` | 剪贴板写入 | 📋 |
| `termux-vibrate` | 震动 | 📋 |
| `termux-toast` | 弹窗提示 | 📋 |

### 使用示例
```bash
# 电池状态
termux-battery-status

# WiFi 信息（用于识别家庭/公司网络）
termux-wifi-info

# 语音播放
termux-tts-speak "你好，这是 Termux 语音通知"

# 通知
termux-notification --title "标题" --text "内容"

# 剪贴板
termux-clipboard-set "复制的内容"
termux-clipboard-get

# 震动反馈
termux-vibrate -d 200

# 弹窗
termux-toast "操作完成"
```

### 集成计划
1. **网络环境识别** - 通过 WiFi SSID 判断位置
2. **语音通知** - 重要事件语音播报
3. **剪贴板集成** - 快速复制命令输出
4. **震动反馈** - 操作确认

---

## 🔄 U22 容器重启方案

### 方案 A: 自动重启 (尝试)
```bash
# 尝试通过 reboot 命令
sudo reboot

# 或通过 init 命令
init 6

# 或通过 systemd
systemctl reboot
```

### 方案 B: 通知用户
```
⚠️ 需要重启 U22 容器以加载新代码

请执行以下操作之一：
1. 重启 U22 App
2. 执行：pkill -9 com.termux.u22
3. 重启手机

重启后自动恢复服务：
- AI Team Hub (8772)
- Termux SSH (8022)
- ssh-gate 隧道
```

### 方案 C: Resume 命令
```bash
# 创建重启后自动恢复脚本
cat > /root/bin/resume-services.sh << 'EOF'
#!/bin/bash
# 重启后自动恢复服务

# 启动 AI Team Hub
cd /root/air/qwq/mobile-web
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8772 > /tmp/mobile-web.log 2>&1 &

# 启动 Termux SSH 隧道
/root/bin/sv/sv start ssh-gate

echo "服务已恢复"
EOF

chmod +x /root/bin/resume-services.sh
```

---

## 📋 重启检查清单

### 重启前
- [ ] 保存所有数据
- [ ] 记录当前状态
- [ ] 创建恢复脚本

### 重启后
- [ ] 检查 AI Team Hub (8772)
- [ ] 检查 Termux SSH (8022)
- [ ] 检查 ssh-gate 隧道
- [ ] 测试对话功能
- [ ] 测试命令功能

---

*最后更新：2026-03-07 15:00*  
*下次审查：重启后*
