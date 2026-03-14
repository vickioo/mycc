# SSH 统一配置与防 Ban 指南

**日期**: 2026-03-06  
**状态**: ✅ 已完成

---

## ⚠️ 重要：避免 SSH 反复重试被 Ban

### 问题

多次 SSH 认证失败会导致服务器端 fail2ban 或类似机制封禁 IP。

### 解决方案

1. **统一 SSH 密钥**：U22 和 Termux 使用相同的密钥
2. **测试连通性**：先测试再启动服务
3. **指数退避**：失败后等待时间递增

---

## 🔑 统一 SSH 配置

### 当前配置

| 项目 | U22 | Termux |
|------|-----|--------|
| **私钥** | `/root/.ssh/id_ed25519` | `~/.ssh/id_ed25519` |
| **公钥** | `/root/.ssh/id_ed25519.pub` | `~/.ssh/id_ed25519.pub` |
| **指纹** | `SHA256:lV5Xuhsy8/YW2mE/39+KyBOPuhrbNEtVNeLxNnelxd0` | 相同 |
| **服务器** | `gate (113.57.105.174:8822)` | 相同 |
| **用户** | `vicki` | 相同 |

### 同步脚本

```bash
#!/bin/bash
# sync-ssh-to-termux.sh

TERMUX_SSH="/data/data/com.termux/files/home/.ssh"

# 复制密钥
cp /root/.ssh/id_ed25519 "$TERMUX_SSH/id_ed25519"
cp /root/.ssh/id_ed25519.pub "$TERMUX_SSH/id_ed25519.pub"
cp /root/.ssh/config "$TERMUX_SSH/config"
cp /root/.ssh/known_hosts "$TERMUX_SSH/known_hosts"

# 设置权限
chmod 600 "$TERMUX_SSH/id_ed25519" "$TERMUX_SSH/config"
chmod 644 "$TERMUX_SSH/id_ed25519.pub" "$TERMUX_SSH/known_hosts"

echo "✅ SSH 配置已同步到 Termux"
```

### 服务器端配置

```bash
# 添加公钥到服务器 authorized_keys
cat /root/.ssh/id_ed25519.pub | ssh CC "cat >> ~/.ssh/authorized_keys"

# 修复权限
ssh CC "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
```

---

## 🧪 测试流程

### 1. 测试 U22 连接

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 gate "echo OK"
```

### 2. 测试 Termux 连接

```bash
ssh -p 8022 localhost "ssh -o BatchMode=yes -o ConnectTimeout=5 gate 'echo OK'"
```

### 3. 启动 Clash 隧道

```bash
ssh -p 8022 localhost "bash ~/start-clash-tunnel.sh"
```

### 4. 测试代理

```bash
ssh -p 8022 localhost "curl -s --socks5-hostname localhost:7891 https://api.ip.sb/ip"
```

---

## 📋 配置文件

### U22 SSH Config (`/root/.ssh/config`)

```
Host gate
    HostName 113.57.105.174
    Port 8822
    User vicki
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent Yes
    LocalForward 3390 database.local:13193
    LocalForward 3391 sj-liuliang.local:3389
    LocalForward 3394 ECS-C6-2XLARGE-.local:23389
    LocalForward 3395 dbx.local:3389
    LocalForward 3396 AmPosERP.local:3389
    LocalForward 8006 192.168.100.222:8006
    LocalForward 8045 127.0.0.1:8045
    LocalForward 8821 sj-liuliang.local:22

Host CC
    HostName 192.168.100.228
    User root
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump gate
```

### Termux SSH Config (`~/.ssh/config`)

与 U22 相同，通过同步脚本复制。

---

## 🚫 避免被 Ban 的最佳实践

### 1. 使用 BatchMode

```bash
# 好：失败立即返回，不重试
ssh -o BatchMode=yes gate "command"

# 不好：可能多次重试
ssh gate "command"
```

### 2. 设置合理超时

```bash
ssh -o ConnectTimeout=5 -o ServerAliveInterval=15 gate
```

### 3. 失败后等待

```bash
#!/bin/bash
for i in 1 2 3; do
    ssh gate "command" && break
    echo "失败，等待 \$((i*10)) 秒后重试..."
    sleep \$((i*10))
done
```

### 4. 检查服务器状态

```bash
# Ping 测试
ping -c 3 113.57.105.174

# 端口测试
nc -zv 113.57.105.174 8822

# 如果失败，不要立即重试
```

---

## 🔧 故障排查

### 问题：Permission denied (publickey,password)

**原因**：
1. 密钥不匹配
2. 服务器 authorized_keys 没有公钥
3. 权限问题

**解决**：
```bash
# 检查密钥指纹
ssh-keygen -lf ~/.ssh/id_ed25519

# 检查服务器 authorized_keys
ssh CC "cat ~/.ssh/authorized_keys"

# 添加公钥
cat ~/.ssh/id_ed25519.pub | ssh CC "cat >> ~/.ssh/authorized_keys"

# 修复权限
ssh CC "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
```

### 问题：Connection refused

**原因**：
1. 服务器离线
2. 防火墙阻止
3. 端口错误

**解决**：
```bash
# 检查服务器
ping 113.57.105.174

# 检查端口
nc -zv 113.57.105.174 8822

# 如果失败，等待服务器恢复
```

---

## 📝 Hook 配置

### U22 启动前 Hook

```bash
# ~/.bashrc 或 ~/.profile
check_gate_before_connect() {
    if ! ssh -o BatchMode=yes -o ConnectTimeout=3 gate "echo OK" 2>/dev/null; then
        echo "⚠️  Gate 服务器不可用，跳过连接"
        return 1
    fi
}

# 在连接 gate 前自动检查
alias ssh-gate='check_gate_before_connect && ssh gate'
```

### Termux 启动前 Hook

```bash
# ~/.bashrc in Termux
check_gate_before_connect() {
    if ! ssh -p 8022 localhost "ssh -o BatchMode=yes -o ConnectTimeout=3 gate 'echo OK'" 2>/dev/null; then
        echo "⚠️  Gate 服务器不可用"
        return 1
    fi
}
```

---

## ✅ 验证清单

- [ ] U22 和 Termux 使用相同密钥
- [ ] 密钥指纹一致
- [ ] 服务器 authorized_keys 包含公钥
- [ ] SSH 配置指定 IdentityFile
- [ ] 权限正确 (600/644)
- [ ] BatchMode 测试通过
- [ ] Clash 隧道正常
- [ ] 代理可用

---

*Last updated: 2026-03-06 18:08*
