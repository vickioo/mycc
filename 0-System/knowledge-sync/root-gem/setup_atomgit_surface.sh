#!/bin/bash
# 在 Surface (OpenClaw) 上配置 AtomGit (surfclaw) 密钥

echo "开始为 Surface 的龙虾(OpenClaw) 配置 AtomGit 免费高速 API..."

# OpenClaw 的配置文件通常在 ~/.openclaw/settings.json 或环境变量中
# 我们将其注入到系统环境，因为 OpenClaw 和通用大模型工具都可以读环境变量
grep -q "ATOMGIT_API_KEY" ~/.bashrc || echo 'export ATOMGIT_API_KEY="Tzu8D4zyDRghWiqMTCGyFnM2"' >> ~/.bashrc
grep -q "OPENAI_API_KEY" ~/.bashrc || echo 'export OPENAI_API_KEY="Tzu8D4zyDRghWiqMTCGyFnM2"' >> ~/.bashrc
grep -q "OPENAI_BASE_URL" ~/.bashrc || echo 'export OPENAI_BASE_URL="https://api.gitcode.com/api/v1"' >> ~/.bashrc

echo "环境变量注入完毕。请确保您的 OpenClaw 或应用使用的是 openai 兼容模式，"
echo "并将 base_url 设置为 https://api.gitcode.com/api/v1 (或直接读取环境变量)。"
echo "您可以执行 source ~/.bashrc 然后重启您的代理/Agent服务。"
