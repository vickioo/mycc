---
name: termux-notify
description: 手机端弹窗和语音提醒。需要 Termux 和 Termux:API。触发词："/notify"、"弹窗提醒"、"手机通知"
---

# termux-notify

手机端弹窗 + 语音提醒。通过 Termux:API 实现，需要在手机上安装 Termux 和 Termux:API 应用。

## 安装依赖（手机上执行）

```bash
# 打开 Termux 执行
pkg update
pkg install termux-api

# 确认安装成功
termux-notification -h
termux-tts-speak -h
```

## 触发词

- "/notify"
- "弹窗提醒"
- "手机通知"

## 使用方式

### 方式 1：弹窗 + 振动

```bash
termux-notification -t "标题" -c "内容" --vibrate 1000
```

### 方式 2：语音播报

```bash
termux-tts-speak "要播报的文字"
```

### 方式 3：弹窗 + 语音（组合）

```bash
termux-notification -t "CC 提醒" -c "任务完成了" && termux-tts-speak "任务完成了"
```

---

## 快速测试

在手机上执行以下命令测试：

```bash
# 测试弹窗
termux-notification -t "测试" -c "CC 连接成功"

# 测试语音
termux-tts-speak "你好，我是 CC"
```