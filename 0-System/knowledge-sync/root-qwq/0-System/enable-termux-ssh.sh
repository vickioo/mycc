#!/bin/bash
#
# enable-termux-ssh.sh - 在 Termux 中启动 SSH 守护进程
# 用法：将此脚本复制到 Termux 并执行
#

echo "╔════════════════════════════════════════════════╗"
echo "║     Termux SSH 守护进程启动脚本                ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "请在 Termux 应用中执行以下命令："
echo ""
echo "  bash ~/air/qwq/0-System/enable-termux-ssh.sh"
echo ""
echo "或者手动执行："
echo "  1. 在 Termux 中：sshd"
echo "  2. 在 U22 中：ssh -p 8022 localhost"
echo ""

# 创建 Termux 执行脚本
cat > /data/data/com.termux/files/home/start-sshd.sh << 'EOFSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
# Termux SSH 守护进程启动脚本

echo "正在启动 Termux SSH 守护进程..."

# 生成 SSH 密钥（如果没有）
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -f ~/.ssh/id_rsa -N "" -q
fi

# 添加公钥到 authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 停止旧的 sshd
pkill sshd 2>/dev/null || true

# 生成主机密钥
mkdir -p ~/.ssh/hostkeys
ssh-keygen -t rsa -f ~/.ssh/hostkeys/ssh_host_rsa_key -N "" -q
ssh-keygen -t ecdsa -f ~/.ssh/hostkeys/ssh_host_ecdsa_key -N "" -q
ssh-keygen -t ed25519 -f ~/.ssh/hostkeys/ssh_host_ed25519_key -N "" -q

# 启动 sshd
export SSHD_PORT=8022
/data/data/com.termux/files/usr/bin/sshd -p 8022 -h ~/.ssh/hostkeys

sleep 2

# 验证
if pgrep -f "sshd.*8022" >/dev/null 2>&1; then
    echo "✅ Termux SSH 守护进程已启动 (端口 8022)"
    echo ""
    echo "从 U22 连接："
    echo "  ssh -p 8022 localhost"
else
    echo "❌ 启动失败，请检查错误"
fi
EOFSCRIPT

chmod +x /data/data/com.termux/files/home/start-sshd.sh
echo "✅ 脚本已创建：/data/data/com.termux/files/home/start-sshd.sh"
echo ""
echo "现在请在 Termux 中执行："
echo "  bash ~/start-sshd.sh"
