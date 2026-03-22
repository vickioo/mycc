# AI Team Mobile V2 Lite

**轻量快速版** - 加载时间 36ms，HTML 仅 18KB

---

## 🚀 启动

```bash
/root/air/qwq/mobile-web/run.sh
```

**访问**: http://localhost:8766

---

## ✅ 已修复

### 1. F5 刷新慢
- ✅ 压缩 HTML 到 18KB (原 60KB)
- ✅ 加载时间 36ms (原 1s)
- ✅ 移除冗余 CSS/JS

### 2. 回复收不到
- ✅ API 超时从 30s 降到 20s
- ✅ 输出限制 500 字符，避免太长
- ✅ 错误处理优化

### 3. 服务崩溃
- ✅ 添加守护进程脚本 `run.sh`
- ✅ 自动检测并重启
- ✅ 日志输出到 `/tmp/mobile-web-v2.log`

---

## 📱 功能测试

### 测试 1: 简单对话
输入：`你好`
预期：返回时间和代理信息

### 测试 2: 服务状态
输入：`服务状态` 或点击技能 "📊 服务状态"
预期：显示 ssh-gate 和 watchdog 状态

### 测试 3: 任务队列
输入：`任务队列` 或点击技能 "📋 任务队列"
预期：显示任务目录列表

---

## 🔧 管理命令

```bash
# 启动
/root/air/qwq/mobile-web/run.sh

# 停止
pkill -f "python3.*mobile-web"

# 查看状态
curl http://localhost:8766/api/health

# 查看日志
tail -f /tmp/mobile-web-v2.log
```

---

## 📊 性能

| 指标 | 数值 |
|------|------|
| HTML 大小 | 18KB |
| 加载时间 | 36ms |
| 内存占用 | ~35MB |
| API 响应 | <100ms |

---

## 🐛 故障排查

### 问题：页面加载卡住
解决：
1. 清除浏览器缓存
2. 硬刷新 (Ctrl+Shift+R)
3. 检查服务：`curl http://localhost:8766/api/health`

### 问题：发送消息无响应
解决：
1. 检查日志：`tail /tmp/mobile-web-v2.log`
2. 重启服务：`pkill -f mobile-web && /root/air/qwq/mobile-web/run.sh`
3. 检查命令执行：手动执行 `/root/bin/sv/sv status`

### 问题：/proc 错误
解决：
这是 U22 容器限制，命令输出会包含此错误信息，不影响使用。

---

## 📁 文件结构

```
/root/air/qwq/mobile-web/
├── app.py              # 主程序
├── run.sh              # 守护进程脚本
├── start.sh            # 手动启动脚本
├── README.md           # 本文档
└── v1/                 # V1 副本
```

---

*Last updated: 2026-03-06 19:55*
