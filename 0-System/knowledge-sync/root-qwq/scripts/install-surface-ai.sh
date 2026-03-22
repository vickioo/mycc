#!/bin/bash
# Surface AI Agent 安装脚本

set -e

echo "🚀 Surface AI Agent 安装脚本"
echo "=============================="
echo ""

# 1. 配置 npm 全局目录
echo "📦 配置 npm 全局目录..."
export PATH="$HOME/.npm-global/bin:$PATH"
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
echo "✅ npm 全局目录配置完成"
echo ""

# 2. 安装 Codex CLI
echo "🤖 安装 Codex CLI..."
npm install -g @openai/codex
echo "✅ Codex CLI 安装完成"
echo ""

# 3. 验证安装
echo "🔍 验证安装..."
codex --version || echo "⚠️ Codex 版本检查失败，请手动验证"
node --version
npm --version
echo ""

# 4. 配置 mycc 环境变量
echo "📝 配置 mycc 环境变量..."
cat >> ~/.bash_aliases << 'EOF'

# mycc 环境变量
export MYCC_HOME="$HOME/air/mycc"
export PATH="$MYCC_HOME:$PATH"
EOF
source ~/.bash_aliases
echo "✅ mycc 环境变量配置完成"
echo ""

# 5. 安装 mycc 依赖
echo "📦 安装 mycc 依赖..."
cd ~/air/mycc
if [ -f "package.json" ]; then
    npm install || echo "⚠️ mycc 依赖安装失败，可手动执行 npm install"
else
    echo "⚠️ 未找到 package.json，mycc 可能不需要 npm 依赖"
fi
echo "✅ mycc 依赖安装完成"
echo ""

echo "=============================="
echo "🎉 安装完成!"
echo ""
echo "使用方式:"
echo "  codex exec \"你的提示词\"     # 使用 Codex"
echo "  cd ~/air/mycc               # 进入 mycc 项目"
echo "  ./start-mycc.sh             # 启动 mycc (如适用)"
echo ""
echo "请重新加载配置：source ~/.bashrc"
