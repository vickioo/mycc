# Agents Team - 分布式协同系统

> 去中心化架构 · 并行处理 · 后台执行 · 云端协同

---

## 🎯 核心能力

### 1. 并行后台处理
- ✅ 多 Worker 并发执行
- ✅ 任务队列自动调度
- ✅ 无需等待用户交互

### 2. 分布式节点
| 节点 | 位置 | 用途 |
|------|------|------|
| local | 本地 | 快速任务 |
| cc | CC 服务器 | 重型任务 |
| termux | 移动端 | 移动场景 |

### 3. 后台持续执行
- ✅ 手机息屏后继续运行
- ✅ 云端 Worker 接管任务
- ✅ 定时任务自动触发

### 4. 健康监控
- 每 5 分钟节点检查
- 自动故障转移
- 成功率统计

---

## 🚀 快速启动

```bash
# 启动 Agents Team
/root/air/qwq/agents-team/start.sh

# 查看状态
python3 monitor/monitor.py

# 运行回测
python3 backtest.py
```

---

## 📋 任务提交

### Python API
```python
from queue.task_queue import TaskQueue

q = TaskQueue()

# 提交本地任务
q.submit({
    "name": "我的任务",
    "command": "echo hello",
    "target": "local",
    "timeout": 60
})

# 提交到 CC 服务器
q.submit({
    "name": "云端任务",
    "command": "uptime",
    "target": "cc"
})
```

### 命令行
```bash
# 查看队列状态
python3 queue/task_queue.py
```

---

## 📊 架构回测

### 测试结果
运行回测查看当前架构能力：
```bash
python3 backtest.py
```

### 测试项目
- 本地命令执行
- CC 服务器连接
- Termux 连接
- 文件操作
- 延迟统计

---

## 🔧 组件说明

### 任务队列 (queue/task_queue.py)
- 待处理队列
- 处理中队列
- 已完成队列
- 失败队列

### Worker (workers/worker.py)
- 本地 Worker
- CC Worker
- Termux Worker

### 调度器 (scheduler/scheduler.py)
- 定时任务
- 间隔执行
- 自动提交

### 监控器 (monitor/monitor.py)
- 健康检查
- 延迟测试
- 统计报告

---

## 📈 监控命令

```bash
# 健康报告
python3 monitor/monitor.py

# 查看日志
tail -f logs/*.log

# 查看任务队列
python3 queue/task_queue.py

# 查看回测报告
ls -la reports/backtest/
```

---

## 🎯 使用场景

### 场景 1: 后台处理
```python
# 提交长时间任务，无需等待
q.submit({
    "name": "数据分析",
    "command": "python3 analyze.py",
    "target": "cc",
    "timeout": 3600
})
```

### 场景 2: 手机息屏
```
手机息屏 → Termux Worker 停止
         → CC Worker 自动接管
         → 任务继续执行
```

### 场景 3: 定时任务
```python
# 添加定时监控
s.add_schedule(
    name="服务检查",
    command="/root/bin/sv/sv status",
    interval="5m",
    target="local"
)
```

---

## 📊 成功率统计

回测报告位置：
```
/root/air/qwq/agents-team/reports/backtest/
```

查看最新报告：
```bash
cat reports/backtest/backtest-*.json | tail -1
```

---

*Last updated: 2026-03-07*
