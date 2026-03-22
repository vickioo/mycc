# sv-style 服务管理系统文档

**日期**: 2026-03-05  
**状态**: ✅ 已部署并运行

---

## 架构概述

### 为什么选择 sv-style 而不是 PM2

| 对比项 | PM2 | sv-style (自研) |
|--------|-----|-----------------|
| 依赖 | Node.js | 纯 Bash |
| 资源占用 | 高 (数十 MB) | 极低 (<1MB) |
| 启动速度 | 秒级 | 毫秒级 |
| 配置复杂度 | 中 | 低 |
| 日志管理 | 需要插件 | 内置轮转 |
| 容器兼容 | 需 /proc | 完全兼容 |

### 设计理念

仿 FreeBSD rc.d / Termux sv：
- 每个服务一个目录
- `run` 脚本包含所有逻辑
- `conf` 文件存储配置
- 统一的 `sv` 命令管理

---

## 目录结构

```
/root/.local/sv/
├── ssh-gate/          # SSH 端口转发服务
│   ├── run            # 执行脚本 (112 行)
│   ├── conf           # 配置文件
│   └── log/
│       └── current    # 当前日志
└── watchdog/          # 健康检查守护进程
    ├── run            # 执行脚本 (85 行)
    └── log/
        └── current

/root/bin/sv/
├── sv                 # 服务管理命令
└── logrotate          # 日志轮转脚本
```

---

## 服务说明

### ssh-gate

**功能**: SSH 端口转发网关

**转发端口**:
| 本地端口 | 目标 | 用途 |
|---------|------|------|
| 3390 | database.local:13193 | 数据库服务 |
| 3391 | sj-liuliang.local:3389 | 流量 SJLL |
| 3394 | ECS-C6-2XLARGE:23389 | ECS 服务器 |
| 3395 | dbx.local:3389 | DBX 服务器 |
| 3396 | AmPosERP.local:3389 | ERP 系统 |
| 8006 | 192.168.100.222:8006 | PVE 管理 |
| 8045 | 127.0.0.1:8045 | CC 内部服务 |
| 8821 | sj-liuliang.local:22 | SJLL SSH |

**健康检查**:
- 检查 SSH 进程是否存在
- 检查端口 8045 (CC) 是否可通
- 检查端口 8006 (PVE) 是否可通

### watchdog

**功能**: 服务健康检查守护进程

**工作逻辑**:
1. 每 30 秒检查一次服务
2. 发现不健康服务自动重启
3. 记录所有操作日志

---

## 使用指南

### 基本命令

```bash
# 查看所有服务状态
sv status

# 启动服务
sv start ssh-gate
sv start watchdog

# 停止服务
sv stop ssh-gate

# 重启服务
sv restart ssh-gate

# 查看日志
sv log ssh-gate 100    # 最后 100 行
sv log ssh-gate | tail -f  # 实时查看
```

### 服务脚本直接调用

```bash
# 每个服务的 run 脚本可以直接调用
/root/.local/sv/ssh-gate/run start
/root/.local/sv/ssh-gate/run status
/root/.local/sv/ssh-gate/run health
```

---

## SSH 配置变更

### 新架构

```
gate (新别名，带所有端口转发)
├── 继承 databasei 的连接参数
├── 8 个 LocalForward 规则
└── 用于所有需要转发的场景

dbi (纯净跳板)
└── 仅用于 SSH 跳转，无默认转发

databasei (底层连接)
└── 公网接入点 (113.57.105.174:8822)
```

### 使用示例

```bash
# 自动使用端口转发
ssh CC         # 通过 gate 跳转 +8045 转发
ssh sjll       # 通过 gate 跳转 +8821 转发

# 不使用端口转发（纯净连接）
ssh dbi        # 直接连接到 databasei，无转发
ssh -o ClearAllForwardings=yes CC  # 临时禁用转发
```

---

## 开机自启

### 方法 1: 添加到 /etc/rc.local

```bash
#!/bin/bash
sleep 10  # 等待网络就绪
/root/bin/sv/sv start ssh-gate
/root/bin/sv/sv start watchdog
```

### 方法 2: systemd 服务

```ini
# /etc/systemd/system/ssh-gate.service
[Unit]
Description=SSH Gate Tunnel
After=network.target

[Service]
Type=forking
ExecStart=/root/.local/sv/ssh-gate/run start
ExecStop=/root/.local/sv/ssh-gate/run stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## 故障排查

### 服务启动失败

```bash
# 查看详细日志
sv log ssh-gate 200

# 手动测试 SSH 连接
ssh -v -N -L 8045:127.0.0.1:8045 gate

# 检查 SSH 配置
ssh -G gate | grep -E "hostname|user|port"
```

### 端口转发不工作

```bash
# 检查端口是否监听
timeout 2 bash -c "echo > /dev/tcp/localhost/8045" && echo OK || echo FAIL

# 检查 SSH 进程
ps aux | grep "ssh.*gate"

# 查看 SSH 错误日志
cat /root/.local/sv/ssh-gate/log/current | tail -50
```

### Watchdog 不工作

```bash
# 检查 watchdog 状态
sv status watchdog

# 手动运行一次检查
/root/.local/sv/ssh-gate/run health

# 查看 watchdog 日志
cat /root/.local/sv/watchdog/log/current
```

---

## 性能指标

| 指标 | 数值 |
|------|------|
| ssh-gate 内存占用 | ~2.5 MB |
| watchdog 内存占用 | ~1.5 MB |
| 健康检查延迟 | <100ms |
| 服务启动时间 | ~3 秒 |
| 日志文件大小 | 自动轮转 (<5MB) |

---

## 扩展服务

添加新服务的步骤：

1. 创建服务目录
```bash
mkdir -p /root/.local/sv/my-service/log
```

2. 创建 run 脚本
```bash
cat > /root/.local/sv/my-service/run << 'EOF'
#!/bin/bash
# my-service 服务脚本
# 复制 ssh-gate/run 模板修改
EOF
chmod +x /root/.local/sv/my-service/run
```

3. 创建配置文件
```bash
cat > /root/.local/sv/my-service/conf << 'EOF'
# 配置参数
EOF
```

4. 测试并启动
```bash
/root/.local/sv/my-service/run start
sv status
```
