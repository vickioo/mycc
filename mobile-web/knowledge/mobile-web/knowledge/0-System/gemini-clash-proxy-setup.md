# Gemini CLI Clash 代理设置指南

**日期**: 2026-03-06  
**状态**: ⚠️ CC 服务器暂时不可用

---

## 问题总结

### 当前状态

1. **Gemini CLI**: 已安装，OAuth 已配置
2. **CC Clash Tunnel**: ❌ 无法启动
3. **CC 服务器**: ❌ 暂时不可用 (Connection refused)

### 根本原因

**CC 服务器 (113.57.105.174:8822) 连接被拒绝**

这不是 SSH 密钥或配置问题，而是：
- 服务器可能离线
- 防火墙阻止连接
- 网络路由问题

---

## 解决方案

### 方案 1: 等待 CC 服务器恢复 (推荐)

CC 服务器恢复后，执行：

```bash
# 在 Termux 中启动 Clash 隧道
ssh -p 8022 localhost "bash ~/start-clash-tunnel.sh"

# 设置代理环境变量
export ALL_PROXY=socks5h://localhost:7891
export HTTPS_PROXY=socks5h://localhost:7891

# 测试 Gemini
gemini "Hello"
```

### 方案 2: 使用其他代理

如果有其他 SOCKS5 代理：

```bash
# 设置代理
export ALL_PROXY=socks5h://proxy-host:port
export HTTPS_PROXY=socks5h://proxy-host:port

# 测试
gemini "Hello"
```

### 方案 3: 直接在 Termux 中使用 Gemini

在 Termux 中安装 Gemini CLI：

```bash
# 在 Termux 中
pkg install nodejs
npm install -g @anthropic-ai/claude-code

# 配置 OAuth
claude-code --login

# 使用
claude-code "Hello"
```

---

## 已完成的配置

### Termux Clash 隧道脚本

已创建：`/data/data/com.termux/files/home/start-clash-tunnel.sh`

```bash
#!/data/data/com.termux/files/usr/bin/bash
# Termux Clash Tunnel for Gemini

PIDFILE="$PREFIX/tmp/clash-tunnel.pid"
LOGFILE="$HOME/clash-tunnel.log"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }

# 停止旧的
if [ -f "$PIDFILE" ]; then
    kill $(cat "$PIDFILE") 2>/dev/null
    rm -f "$PIDFILE"
fi

# 启动新的
log "启动 Clash 隧道..."
nohup ssh -N \
  -D 7891 \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o ServerAliveInterval=15 \
  -o ServerAliveCountMax=2 \
  -o ExitOnForwardFailure=yes \
  -o TCPKeepAlive=yes \
  -o ClearAllForwardings=yes \
  gate >> "$LOGFILE" 2>&1 &

echo $! > "$PIDFILE"
sleep 3

if kill -0 $(cat "$PIDFILE") 2>/dev/null; then
    log "✅ Clash 隧道已启动 (PID: $(cat $PIDFILE))"
    echo "代理地址：socks5h://localhost:7891"
else
    log "❌ 启动失败，检查日志"
    rm -f "$PIDFILE"
fi
```

### SSH 配置

已完成：
- ✅ Termux SSH 配置已更新
- ✅ SSH 密钥已复制 (`id_ed25519`)
- ✅ 公钥已添加到 CC 服务器 authorized_keys
- ✅ StrictHostKeyChecking 已禁用

### U22 代理设置脚本

已创建：`/root/air/qwq/0-System/setup-gemini-proxy.sh`

---

## 测试命令

### 测试 CC 服务器连通性

```bash
# 从 U22 测试
ssh -o ConnectTimeout=5 -o BatchMode=yes CC "echo OK"

# 从 Termux 测试
ssh -p 8022 localhost "ssh -o ConnectTimeout=5 -o BatchMode=yes gate 'echo OK'"
```

### 测试代理

```bash
# 测试 SOCKS5 代理
curl -s --socks5-hostname localhost:7891 --connect-timeout 5 https://api.ip.sb/ip

# 测试 Google 访问
curl -s --socks5-hostname localhost:7891 --connect-timeout 5 https://www.google.com
```

### 测试 Gemini

```bash
# 设置代理后
export ALL_PROXY=socks5h://localhost:7891
gemini "Hello, are you connected?"
```

---

## 故障排查

### CC 服务器不可用

```bash
# 检查连接
ping -c 3 113.57.105.174

# 检查端口
nc -zv 113.57.105.174 8822

# 检查路由
traceroute 113.57.105.174
```

### SSH 密钥问题

```bash
# 检查 Termux 密钥
ssh -p 8022 localhost "ls -la ~/.ssh/id_ed25519*"

# 检查公钥指纹
ssh -p 8022 localhost "ssh-keygen -lf ~/.ssh/id_ed25519"

# 检查服务器 authorized_keys
ssh CC "cat ~/.ssh/authorized_keys"
```

### 代理端口未开放

```bash
# 检查端口
timeout 2 bash -c "echo > /dev/tcp/localhost/7891" && echo "OK" || echo "Failed"

# 查看隧道日志
ssh -p 8022 localhost "cat ~/clash-tunnel.log"
```

---

## 下一步行动

1. **检查 CC 服务器状态**
   - 联系服务器管理员
   - 检查服务器是否在线
   - 确认防火墙规则

2. **服务器恢复后**
   ```bash
   # 在 Termux 中
   bash ~/start-clash-tunnel.sh
   
   # 设置代理
   export ALL_PROXY=socks5h://localhost:7891
   
   # 测试 Gemini
   gemini "Hello"
   ```

3. **如果 CC 服务器长期不可用**
   - 考虑使用其他代理方案
   - 或在 Termux 中直接配置其他 VPN/代理

---

## 相关文件

| 文件 | 位置 |
|------|------|
| Termux 隧道脚本 | `~/.termux/files/home/start-clash-tunnel.sh` |
| U22 设置脚本 | `/root/air/qwq/0-System/setup-gemini-proxy.sh` |
| SSH 配置 (Termux) | `~/.termux/files/home/.ssh/config` |
| SSH 密钥 (Termux) | `~/.termux/files/home/.ssh/id_ed25519` |
| 隧道日志 | `~/.termux/files/home/clash-tunnel.log` |

---

*Last updated: 2026-03-06 08:57*
