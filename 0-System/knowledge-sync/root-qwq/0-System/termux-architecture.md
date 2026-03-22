# Termux + U22 分层架构指南

**日期**: 2026-03-05  
**状态**: 混合模式 (U22 运行，Termux 可选迁移)

---

## 当前架构

```
┌─────────────────────────────────────────┐
│  U22 (Ubuntu 22.04 for Android)         │
│  ┌────────────────────────────────────┐ │
│  │  sv-style 服务管理                  │ │
│  │  ├── ssh-gate ✅ (端口转发)        │ │
│  │  └── watchdog ✅ (健康检查)        │ │
│  │                                     │ │
│  │  AI Agents                          │ │
│  │  ├── qwq (Qwen Code)               │ │
│  │  └── mycc (Claude Code)            │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**现状**: 由于 U22 无法直接执行 Termux 二进制文件，当前服务继续运行在 U22 上。

---

## Termux 迁移方案 (可选)

如果 U22 服务不稳定（容器权限问题），可以迁移到 Termux。

### 方法 1: 自动设置脚本

```bash
# 1. 打开 Termux 应用
# 2. 执行设置脚本
bash ~/air/qwq/0-System/termux-setup.sh

# 3. 启动服务
sv start ssh-gate
sv start watchdog

# 4. 验证
sv status
ssh CC "echo OK"
```

### 方法 2: 手动设置

```bash
# 在 Termux 中执行：

# 1. 安装 openssh
pkg install openssh

# 2. 复制 SSH 配置
cp /root/.ssh/config ~/.ssh/
cp /root/.ssh/id_ed25519_vi ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519

# 3. 创建服务目录
mkdir -p $HOME/.local/sv/ssh-gate/log $HOME/.local/sv/watchdog/log $HOME/bin

# 4. 创建 ssh-gate 服务
cat > $HOME/.local/sv/ssh-gate/run << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
PIDFILE="$PREFIX/tmp/ssh-gate.pid"
LOGFILE="$HOME/.local/sv/ssh-gate/log/current"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }
check_running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
start() {
  check_running && { log "已在运行"; return 0; }
  log "启动 ssh-gate..."
  pkill -f "ssh -N.*gate" 2>/dev/null || true
  nohup ssh -N -L 8045:127.0.0.1:8045 -L 8006:192.168.100.222:8006 -o ServerAliveInterval=15 gate >> "$LOGFILE" 2>&1 &
  echo $! > "$PIDFILE"
  sleep 2 && kill -0 $! 2>/dev/null && { log "✅ 已启动"; return 0; }
  log "❌ 失败"; rm -f "$PIDFILE"; return 1
}
stop() { check_running || return 0; kill "$(cat "$PIDFILE")" 2>/dev/null; rm -f "$PIDFILE"; log "已停止"; }
restart() { stop; sleep 1; start; }
status() { check_running && echo "✅ 运行中" || echo "❌ 未运行"; }
health() { check_running && timeout 2 bash -c "echo > /dev/tcp/localhost/8045" 2>/dev/null && echo "healthy" || echo "unhealthy"; }
case "$1" in start) start;; stop) stop;; restart) restart;; status) status;; health) health;; *) echo "用法：$0 {start|stop|restart|status|health}";; esac
EOF
chmod +x $HOME/.local/sv/ssh-gate/run

# 5. 创建 sv 命令
cat > $HOME/bin/sv << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
SV_BASE="$HOME/.local/sv"
[ -x "$SV_BASE/$2/run" ] && "$SV_BASE/$2/run" "$1" || { [ -z "$2" ] && { for d in $SV_BASE/*/; do [ -x "$d/run" ] && "$(basename "$d")/run" "$1"; done; } || echo "❌ 服务不存在"; }
EOF
chmod +x $HOME/bin/sv

# 6. 启动并验证
sv start ssh-gate
sv status
```

---

## U22 服务管理

### 基本命令

```bash
# 查看状态
/root/bin/sv/sv status

# 启动服务
/root/bin/sv/sv start ssh-gate

# 重启服务
/root/bin/sv/sv restart ssh-gate

# 查看日志
/root/bin/sv/sv log ssh-gate 100
```

### 添加到 PATH

```bash
# 添加到 ~/.bashrc
echo 'export PATH="$PATH:/root/bin/sv"' >> ~/.bashrc
source ~/.bashrc

# 之后可以直接使用 sv 命令
sv status
```

---

## 端口转发列表

| 端口 | 目标 | 用途 |
|------|------|------|
| 8045 | 127.0.0.1:8045 | CC 内部服务 |
| 8006 | 192.168.100.222:8006 | PVE 管理 |
| 8821 | sj-liuliang.local:22 | SJLL SSH |
| 3390 | database.local:13193 | 数据库 |
| 3391 | sj-liuliang.local:3389 | 流量 SJLL |
| 3394 | ECS-C6-2XLARGE:23389 | ECS 服务器 |
| 3395 | dbx.local:3389 | DBX |
| 3396 | AmPosERP.local:3389 | ERP |

---

## 故障排查

### U22 服务失败

```bash
# 检查服务状态
sv status

# 查看详细日志
sv log ssh-gate 200

# 手动测试 SSH 连接
ssh -v -N -L 8045:127.0.0.1:8045 gate

# 检查 /proc 是否挂载
mount proc /proc -t proc 2>/dev/null || echo "无法挂载 /proc"
```

### Termux 服务失败

```bash
# 在 Termux 中检查
sv status

# 查看日志
sv log ssh-gate

# 测试 SSH 连接
ssh -v gate
```

---

## 开机自启

### U22 (需要 root)

```bash
# 添加到 /etc/rc.local
cat >> /etc/rc.local << 'EOF'
sleep 10
/root/bin/sv/sv start ssh-gate
/root/bin/sv/sv start watchdog
EOF
chmod +x /etc/rc.local
```

### Termux (需要 Termux:Boot)

```bash
# 创建 ~/.termux/boot/boot.sh
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/boot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
sleep 10
sv start ssh-gate
sv start watchdog
EOF
chmod +x ~/.termux/boot/boot.sh
```

---

## 架构对比

| 特性 | U22 方案 | Termux 方案 |
|------|---------|------------|
| 网络权限 | ⚠️ 受限 | ✅ 完整 |
| /proc 访问 | ❌ 失败 | ✅ 正常 |
| 执行权限 | ✅ 可执行 root 工具 | ⚠️ 受限 |
| 保活能力 | ⚠️ 依赖系统 | ✅ Tasker 支持 |
| 配置复杂度 | 低 | 中 |
| 推荐场景 | 开发测试 | 生产环境 |

---

## 推荐方案

**当前**: U22 运行服务（开发环境）

**如果遇到问题**（SSH 端口转发失败、/proc 错误）：
1. 在 Termux 中执行 `bash ~/air/qwq/0-System/termux-setup.sh`
2. 启动 Termux 服务 `sv start ssh-gate`
3. U22 通过 localhost 访问转发端口

---

## 文件位置

| 文件 | U22 路径 | Termux 路径 |
|------|---------|------------|
| SSH 配置 | `/root/.ssh/` | `~/.ssh/` |
| sv 服务 | `/root/.local/sv/` | `~/.local/sv/` |
| sv 命令 | `/root/bin/sv/` | `~/bin/` |
| 日志 | `/root/.local/sv/*/log/` | `~/.local/sv/*/log/` |
| 设置脚本 | `/root/air/qwq/0-System/` | `~/air/qwq/0-System/` |
