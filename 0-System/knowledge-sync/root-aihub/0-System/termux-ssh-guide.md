# 从 U22 SSH 连接到 Termux

**问题**: U22 无法直接执行 Termux 二进制文件（不同的运行环境）

**解决方案**: 在 Termux 中启动 SSH 守护进程，然后从 U22 SSH 连接

---

## 快速设置（一次性操作）

### 方法 1: 使用自动脚本

```bash
# 在 Termux 应用中执行：
bash ~/air/qwq/0-System/enable-termux-ssh.sh

# 或者
bash ~/start-sshd.sh
```

### 方法 2: 手动执行

```bash
# 在 Termux 中执行：

# 1. 启动 SSH 守护进程
sshd

# 2. 验证运行
pgrep -f sshd

# 3. 从 U22 测试连接
# （在 U22 中执行）
ssh -p 8022 -o StrictHostKeyChecking=no localhost "echo OK"
```

---

## 完整设置步骤

### 步骤 1: 在 Termux 中准备环境

```bash
# 打开 Termux 应用

# 安装 openssh（如果未安装）
pkg install openssh

# 生成 SSH 密钥
ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ""

# 添加公钥到授权密钥
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 生成主机密钥
mkdir -p ~/.ssh/hostkeys
ssh-keygen -t rsa -f ~/.ssh/hostkeys/ssh_host_rsa_key -N ""
ssh-keygen -t ed25519 -f ~/.ssh/hostkeys/ssh_host_ed25519_key -N ""
```

### 步骤 2: 启动 SSH 守护进程

```bash
# 在 Termux 中
sshd -p 8022 -h ~/.ssh/hostkeys

# 或者使用启动脚本
bash ~/start-sshd.sh
```

### 步骤 3: 从 U22 连接

```bash
# 在 U22 中
ssh -p 8022 -o StrictHostKeyChecking=no localhost

# 测试命令
ssh -p 8022 localhost "echo '连接成功'"
```

---

## 验证连接

```bash
# 在 U22 中执行

# 1. 测试端口连通性
timeout 2 bash -c "echo > /dev/tcp/localhost/8022" && echo "✅ 端口开放"

# 2. SSH 连接测试
ssh -p 8022 -o BatchMode=yes localhost "echo ✅ SSH 成功"

# 3. 执行 Termux 命令
ssh -p 8022 localhost "sv start ssh-gate"
```

---

## 自动化方案

### 方案 A: Termux 常驻 SSH

在 Termux 中创建自启动脚本：

```bash
# ~/.termux/boot/start-sshd.sh
#!/data/data/com.termux/files/usr/bin/bash
sleep 5
sshd -p 8022 -h ~/.ssh/hostkeys
```

需要安装 Termux:Boot 应用。

### 方案 B: U22 触发 Termux 启动

使用 `am` 命令通过 Intent 启动 Termux：

```bash
# 在 U22 中创建脚本
cat > /root/bin/termux-ssh-start << 'EOF'
#!/bin/bash
# 通过 Android Intent 启动 Termux SSH
am startservice --user 0 -n com.termux/com.termux.app.TermuxBootService
sleep 3
am broadcast --user 0 -a com.termux.RUN_COMMAND -n com.termux/.app.RunCommandService \
    --es command "sshd -p 8022"
EOF
chmod +x /root/bin/termux-ssh-start
```

### 方案 C: 共享存储同步

通过 `/sdcard` 共享目录传递命令：

```bash
# U22 写入命令
echo "sv start ssh-gate" > /sdcard/termux-command.txt

# Termux 监控并执行（需要后台服务）
```

---

## 当前限制

| 限制 | 说明 | 解决方案 |
|------|------|----------|
| U22 无法执行 Termux 二进制 | 架构隔离 | SSH 连接 |
| /proc 访问受限 | 容器权限 | 使用 Termux |
| 无法直接 `ps` 查看进程 | 权限限制 | SSH 到 Termux 查询 |
| Termux SSH 需手动启动 | 无守护进程 | Termux:Boot |

---

## 推荐工作流

```
┌─────────────────────────────────────────┐
│  1. 在 Termux 中启动 SSH 守护进程        │
│     sshd -p 8022                         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  2. 在 U22 中 SSH 连接到 Termux          │
│     ssh -p 8022 localhost               │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  3. 在 Termux 中执行 sv 服务管理         │
│     sv start ssh-gate                   │
└─────────────────────────────────────────┘
```

---

## 一键连接脚本

创建 U22 连接脚本：

```bash
# /root/bin/termux-connect
#!/bin/bash
ssh -p 8022 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -o LogLevel=ERROR localhost "$@"
```

使用：
```bash
termux-connect "sv status"
termux-connect "pkg list-installed"
```

---

## 故障排查

### SSH 连接失败

```bash
# 检查 Termux SSH 是否运行
# 需要在 Termux 中执行
pgrep -f sshd

# 检查端口监听
# 在 Termux 中执行
netstat -tlnp | grep 8022
```

### 权限问题

```bash
# 在 Termux 中修复权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/hostkeys/*
```

### 端口占用

```bash
# 在 Termux 中
pkill sshd
sshd -p 8022
```

---

## 安全注意事项

1. **限制监听地址**: `sshd -p 8022 -i` (仅监听 localhost)
2. **使用密钥认证**: 禁用密码登录
3. **定期更新密钥**: `ssh-keygen -f ~/.ssh/id_rsa -N ""`
4. **监控日志**: `tail -f ~/.ssh/sshd.log`
