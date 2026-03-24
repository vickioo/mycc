---
name: desktop
description: 桌面操控。让 CC 看屏幕、动鼠标、点按钮、输文字。基于 OCR 触觉反馈，不截全屏传 AI，极致省 token。支持 macOS 和 Linux。触发词："/desktop"、"帮我操作桌面"、"点一下那个按钮"、"看看屏幕上有什么"
layer: 基础层
authorization: B区（执行后通知）
output_levels: L1
status: stable
platform: cross (macOS + Linux/Xubuntu)
linux_deps: [maim, xdotool, tesseract-ocr, tesseract-ocr-chi-sim]
---

# Desktop — CC 桌面操控

## 核心理念：触觉反馈

不截全屏传 AI（慢、贵），而是用 OCR 当"触觉"。
鼠标移到哪 → OCR 哪 → Agent 知道手在哪、摸到什么。

## CLI 工具栈

### Linux / Xubuntu

```bash
# ===== 眼（感知） =====

# 全屏截图
maim /tmp/desktop-screenshot.png

# 局部截图（鼠标拖拽）
maim -s /tmp/desktop-region.png

# 鼠标附近截图
X=$(xdotool getmouselocation --shell 2>/dev/null | grep X= | cut -d= -f2)
Y=$(xdotool getmouselocation --shell 2>/dev/null | grep Y= | cut -d= -f2)
maim -g 300x200 ${X},${Y} /tmp/desktop-cursor.png

# 全屏 OCR
tesseract /tmp/desktop-screenshot.png stdout -l chi_sim+eng 2>/dev/null

# 局部 OCR
tesseract /tmp/desktop-region.png stdout -l chi_sim+eng 2>/dev/null

# ===== 手（操控） =====

# 获取鼠标位置
xdotool getmouselocation --shell

# 移动鼠标
xdotool mousemove 500 300

# 点击（左键）
xdotool click 1

# 双击
xdotool click --repeat 2 1

# 右键
xdotool click 3

# 输入文字
xdotool type "Hello World"

# 按键
xdotool key Return
xdotool key Tab
xdotool key Escape

# 键盘快捷键
xdotool key Ctrl+c
xdotool key Ctrl+v
xdotool key Ctrl+s
xdotool key Ctrl+a

# ===== 感知（窗口/应用状态） =====

# 窗口列表
wmctrl -l

# 激活窗口（按名称）
xdotool windowactivate $(xdotool search --onlyvisible --name "微信" | head -1)

# 全屏截图（Claude 视觉兜底）
maim /tmp/desktop-screenshot.png
```

### macOS

```bash
# OCR（需 ~/tools/ocr-env/）
OCR="$HOME/tools/ocr-env/bin/python3 .claude/skills/desktop/ocr.py"
$OCR --screen --bbox

# 截图
screencapture -x /tmp/desktop-screenshot.png

# 鼠标/点击
cliclick p:.          # 位置
cliclick m:500,300    # 移动
cliclick c:500,300    # 点击
cliclick dc:500,300   # 双击
cliclick rc:500,300   # 右键
cliclick t:"hello"    # 输入

# 窗口/应用
osascript -e 'tell application "System Events" to get name of every process whose visible is true'
```

## 操作流程

### 标准流程：点击按钮

```
1. 全屏截图 + OCR 找目标
   maim /tmp/screen.png
   tesseract /tmp/screen.png stdout -l chi_sim+eng
   → 找到 "保存" 在某坐标

2. 移动鼠标 + 触觉确认
   xdotool mousemove X Y
   maim -g 300x200 ${X},${Y} /tmp/cursor.png
   tesseract /tmp/cursor.png stdout -l chi_sim+eng
   → 确认目标在鼠标下方 ✓

3. 点击
   xdotool click 1

4. 触觉验证
   maim -g 300x200 ${X},${Y} /tmp/verify.png
   tesseract /tmp/verify.png stdout -l chi_sim+eng
   → 确认操作成功
```

### OCR 找不到时的兜底

```
1. 全屏截图
   maim /tmp/desktop-screenshot.png

2. 用 Read 工具读取截图（Claude 视觉）
   → Claude 自动分析截图内容

3. 根据 Claude 的分析结果决定操作
```

## 安全规则

| 级别 | 操作 | 策略 |
|------|------|------|
| 绿色 | 截图、OCR、列窗口、移动鼠标 | 自动执行 |
| 黄色 | 点击、输入文字、切换窗口 | 执行并告知用户 |
| 红色 | 涉及密码、支付、删除、发消息 | 先问用户 |

**禁区**：
- 不操控 Terminal（防 GUI 绕过权限控制）
- 不输入密码
- 不操作支付页面
- 不修改系统安全设置

## 性能参考（Linux）

| 操作 | 耗时 |
|------|------|
| 鼠标移动/点击 | < 10ms |
| 截图（maim 全屏） | ~100ms |
| OCR（tesseract 全屏） | ~2-5s |
| 获取窗口列表 | < 50ms |
