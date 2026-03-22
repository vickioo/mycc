# Termux 导航肩膀矩阵 (2026-03-16)

## 布局逻辑
- **对齐**：3x2 垂直对齐矩阵，解决错位问题。
- **导航肩膀**：PGUP/PGDN 分列 UP 左右。
- **隐身复合**：上滑触发二级功能但不显示提示，保持界面整洁。

## 按键矩阵
| Row 1 | CTRL | ALT | SHIFT | PGUP (HOME) | UP | PGDN (END) | TAB (ESC) | DRW (KB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Row 2 | DEL | / | | LEFT | DOWN | RIGHT | ~ ($) | ENTER |

## 配置文件路径
`~/.termux/termux.properties`

## 系统别名 (Bash Aliases)
- **p**: PM2 列表
- **claudev**: 以 VK 身份运行 Claude (Bypass)
- **cv/qv**: 查看 Claude/Qwen 内部状态
- **mycc/qwq**: 快速切换目录
