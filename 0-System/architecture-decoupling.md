# 系统架构解耦方案

**日期**: 2026-03-05  
**当前状态**: 全部运行在 U22 (Ubuntu 22.04 for Android)  
**目标**: 分层解耦，Termux 与 U22 协同

---

## 当前架构 (全部在 U22)

```
┌─────────────────────────────────────────────────────────┐
│                    U22 (Ubuntu 22.04)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  /root/.local/sv/                                   │ │
│  │  ├── ssh-gate/    ← SSH 端口转发服务                │ │
│  │  └── watchdog/    ← 健康检查守护进程               │ │
│  │                                                      │ │
│  │  /root/bin/sv/                                      │ │
│  │  └── sv           ← 服务管理命令                    │ │
│  │                                                      │ │
│  │  /root/.ssh/config ← SSH 配置 (gate, dbi, CC 等)     │ │
│  │                                                      │ │
│  │  /root/air/                                         │ │
│  │  ├── qwq/         ← Qwen Code 工作目录              │ │
│  │  └── mycc/        ← Claude Code 工作目录            │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 问题分析

1. **SSH 守护进程在 U22** - 容器权限限制可能导致不稳定
2. **/proc 访问受限** - `ps`, `ss`, `pgrep` 等命令失败
3. **Termux 能力未利用** - Termux 的网络权限更完整
4. **单点故障** - U22 重启后服务需要手动恢复

---

## 目标架构 (分层解耦)

```
┌─────────────────────────────────────────────────────────┐
│              Termux (Android 原生终端)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  ~/.termux/sv/                                      │ │
│  │  ├── ssh-gate/    ← SSH 端口转发 (稳定)            │ │
│  │  │   ├── run      ← 使用 Termux 原生 SSH            │ │
│  │  │   └── conf     ← 配置 (SSH_HOST=gate)           │ │
│  │  ├── cc-clash/    ← CC Clash 隧道 (如果解决)       │ │
│  │  └── watchdog/    ← 健康检查守护进程               │ │
│  │                                                      │ │
│  │  ~/bin/sv         ← 服务管理命令 (统一接口)        │ │
│  │  ~/.ssh/config    ← SSH 配置 (与 U22 共享)          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ SSH 隧道端口
                          │ (localhost:7890, 8045, etc)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    U22 (Ubuntu 22.04)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  /root/air/                                         │ │
│  │  ├── qwq/         ← Qwen Code 工作目录              │ │
│  │  └── mycc/        ← Claude Code 工作目录            │ │
│  │                                                      │ │
│  │  通过 localhost 访问 Termux 提供的端口转发           │ │
│  │  - ALL_PROXY=socks5h://localhost:7890              │ │
│  │  - SSH CC → 通过 gate 跳转                          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 解耦方案

### 方案 A: Termux 运行 SSH 服务 (推荐)

**适合场景**: Termux 常驻后台，U22 可重启

```
Termux 层:
├── ssh-gate 服务 (端口转发)
├── cc-clash 服务 (VPN 隧道)
└── watchdog 服务 (健康检查)

U22 层:
├── AI Agents (qwq, mycc)
├── 任务调度器
└── 应用层服务
```

**优点**:
- ✅ Termux 网络权限完整，无 /proc 限制
- ✅ SSH 隧道更稳定
- ✅ U22 重启不影响底层连接
- ✅ Termux 可通过 任务应用 保活

**缺点**:
- ⚠️ 需要 Termux:Boot 或 任务应用 自动启动
- ⚠️ U22 访问 Termux 端口需要配置

---

### 方案 B: 混合部署 (折中)

**适合场景**: 快速迁移，逐步解耦

```
U22 层 (保留):
├── ssh-gate 服务 (仅内网转发)
└── AI Agents

Termux 层 (新增):
├── gate-external 服务 (公网 SSH 跳板)
└── clash 服务 (VPN)
```

**配置示例**:
```bash
# Termux ~/.ssh/config
Host gate-external
    HostName 113.57.105.174
    Port 8822
    User vicki
    LocalForward 2222 gate:22  # 转发 gate SSH 到本地

# U22 ~/.ssh/config  
Host gate
    HostName localhost
    Port 2222  # 通过 Termux 转发
    # 不再需要公网连接配置
```

---

### 方案 C: 完全解耦 (长期目标)

```
Termux 层 (基础设施):
├── 网络层
│   ├── ssh-gate      (端口转发)
│   ├── cc-clash      (VPN 隧道)
│   └── dns-proxy     (DNS 解析)
├── 服务层
│   ├── sv-manager    (服务管理)
│   └── watchdog      (健康检查)
└── 存储层
    └── /data/data/com.termux/files/home/.local/sv/

U22 层 (应用):
├── AI Agents
│   ├── qwq (Qwen Code)
│   └── mycc (Claude Code)
├── 任务系统
│   ├── scheduler
│   └── router
└── 配置管理
    └── /root/air/qwq/0-System/

共享层 (数据同步):
└── /root/air/ (通过存储权限共享)
```

---

## 实施步骤

### 阶段 1: Termux 基础环境准备

```bash
# Termux 上执行
pkg install openssh sshpass
mkdir -p ~/.local/sv ~/.bin

# 复制 SSH 配置
cp /root/.ssh/config ~/.ssh/config
cp -r /root/.ssh/id_* ~/.ssh/
chmod 600 ~/.ssh/id_*
```

### 阶段 2: 迁移 ssh-gate 服务

```bash
# Termux 上创建服务
cat > ~/.local/sv/ssh-gate/run << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Termux ssh-gate 服务
exec ssh -N \
    -L 3390:database.local:13193 \
    -L 3391:sj-liuliang.local:3389 \
    -L 8006:192.168.100.222:8006 \
    -L 8045:127.0.0.1:8045 \
    -L 8821:sj-liuliang.local:22 \
    -o ServerAliveInterval=15 \
    gate
EOF
chmod +x ~/.local/sv/ssh-gate/run
```

### 阶段 3: U22 配置调整

```bash
# U22 上修改 ~/.ssh/config
Host gate
    HostName localhost
    # 端口根据 Termux 转发配置调整
    # LocalForward 全部移除 (Termux 已提供)
```

### 阶段 4: 验证与切换

```bash
# Termux 启动服务
sv start ssh-gate

# U22 验证连接
ssh CC "echo OK"
curl --socks5-hostname localhost:7890 https://api.ip.sb/ip
```

---

## 端口映射规划

| 服务 | Termux 端口 | U22 访问方式 |
|------|------------|-------------|
| SSH Gate | 2222 | localhost:2222 |
| SOCKS5 Proxy | 7890 | localhost:7890 |
| CC Internal | 8045 | localhost:8045 |
| PVE Manager | 8006 | localhost:8006 |
| SJLL SSH | 8821 | localhost:8821 |
| RDP 转发 | 3390-3396 | localhost:339X |

---

## Termux 保活方案

### 方案 1: Tasker + Termux:Task

```
Tasker 配置:
├── 配置：屏幕关闭时
│   └── 动作：运行 sv status, 异常则 sv restart
└── 配置：充电时
    └── 动作：检查服务状态
```

### 方案 2: Termux:Boot (需要 root)

```bash
# ~/.termux/boot/boot.sh
#!/data/data/com.termux/files/usr/bin/bash
sleep 10  # 等待网络
sv start ssh-gate
sv start watchdog
```

### 方案 3: 前台服务 + 通知

```bash
# 创建前台服务脚本
termux-notification --id sv-service --ongoing
sv start ssh-gate
```

---

## 配置同步机制

### 共享 SSH 配置

```bash
# 创建配置同步脚本
cat > /root/bin/sync-ssh-config << 'EOF'
#!/bin/bash
# 同步 SSH 配置到 Termux
TERMUX_SSH="/data/data/com.termux/files/home/.ssh"
U22_SSH="/root/.ssh"

cp "$U22_SSH/config" "$TERMUX_SSH/"
cp "$U22_SSH"/id_* "$TERMUX_SSH/"
chmod 600 "$TERMUX_SSH"/id_*
echo "✅ SSH 配置已同步到 Termux"
EOF
```

### 共享服务脚本

```bash
# 服务脚本放在共享位置
mkdir -p /sdcard/air-services/sv
# Termux 和 U22 都可以访问 /sdcard
```

---

## 迁移检查清单

- [ ] Termux 安装 openssh
- [ ] Termux 配置 SSH 密钥
- [ ] 创建 Termux sv 服务目录
- [ ] 迁移 ssh-gate 服务
- [ ] 迁移 cc-clash 服务 (如适用)
- [ ] 迁移 watchdog 服务
- [ ] 配置 Termux 保活机制
- [ ] 更新 U22 SSH 配置
- [ ] 验证端口转发
- [ ] 验证 AI Agents 连接
- [ ] 配置自动启动
- [ ] 文档更新

---

## 回滚方案

如果 Termux 方案不稳定，可以快速回滚：

```bash
# U22 恢复原配置
mv ~/.ssh/config.backup ~/.ssh/config
sv start ssh-gate
```

---

## 性能对比

| 指标 | U22 方案 | Termux 方案 |
|------|---------|------------|
| SSH 稳定性 | ⚠️ 受容器限制 | ✅ 原生支持 |
| 网络权限 | ⚠️ 受限 | ✅ 完整 |
| /proc 访问 | ❌ 失败 | ✅ 正常 |
| 保活能力 | ⚠️ 依赖 U22 | ✅ Tasker 支持 |
| 资源占用 | 低 | 低 |
| 配置复杂度 | 低 | 中 |

---

## 推荐实施顺序

1. **立即**: 在 Termux 测试 SSH 连接 (`ssh gate`)
2. **短期**: 迁移 ssh-gate 到 Termux
3. **中期**: 配置 Termux 保活机制
4. **长期**: 完全解耦，U22 仅运行 AI Agents
