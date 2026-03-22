# GitHub 仓库管理指引

**版本**: V1.0  
**更新日期**: 2026-03-09  
**维护者**: AI Team (Qwen Code)

---

## 📋 目录

1. [快速开始](#快速开始)
2. [仓库配置](#仓库配置)
3. [日常操作](#日常操作)
4. [分支管理](#分支管理)
5. [发布流程](#发布流程)
6. [自动化](#自动化)
7. [安全设置](#安全设置)

---

## 快速开始

### 1. 创建 GitHub 仓库

访问：https://github.com/new

**推荐设置**:
- **仓库名**: `ai-team-hub` 或 `qwq-mobile-web`
- **可见性**: Public (公开) 或 Private (私有)
- **初始化**: 
  - ✅ Add README
  - ✅ Add .gitignore (选择 `Python` + `Node`)
  - ✅ Add license (推荐 MIT)

### 2. 配置本地 Git

```bash
cd /root/air/qwq/mobile-web

# 初始化 Git (如未初始化)
git init

# 添加远程仓库
# 方式 A: HTTPS (需要输入密码)
git remote add origin https://github.com/vicki/ai-team-hub.git

# 方式 B: SSH (推荐，需配置 SSH Key)
git remote add origin git@github.com:vicki/ai-team-hub.git

# 验证配置
git remote -v
```

### 3. 首次推送

```bash
# 添加所有文件
git add .

# 提交
git commit -m "init: 初始提交 - AI Team Hub"

# 推送到 GitHub
git push -u origin master
```

---

## 仓库配置

### 推荐仓库设置

#### 1. 基本信息

进入 `Settings` → `General`:

| 设置项 | 推荐值 | 说明 |
|--------|--------|------|
| **About** | AI Team Hub - 多端协同系统 | 仓库描述 |
| **Website** | https://ai-team-hub.vercel.app | 项目网站 |
| **Topics** | `ai`, `multi-device`, `sync`, `python`, `fastapi` | 标签 |

#### 2. 功能启用

| 功能 | 状态 | 说明 |
|------|------|------|
| **Issues** | ✅ 启用 | 问题追踪 |
| **Projects** | ✅ 启用 | 项目管理 |
| **Wiki** | ⚪ 可选 | 文档 Wiki |
| **Discussions** | ✅ 启用 | 社区讨论 |
| **Sponsorships** | ⚪ 可选 | 赞助按钮 |

#### 3. 分支保护

进入 `Settings` → `Branches` → `Add branch protection rule`:

```
Branch name pattern: master

✅ Require a pull request before merging
✅ Require approvals (1)
✅ Require status checks to pass before merging
✅ Require branches to be up to date before merging
✅ Require conversation resolution before merging
```

---

## 日常操作

### 提交代码

```bash
cd /root/air/qwq/mobile-web

# 查看变更
git status
git diff

# 添加文件
git add <file>           # 单个文件
git add *.py            # 通配符
git add .               # 所有文件

# 提交
git commit -m "feat: 功能描述"

# 推送
git push origin master
```

### 查看历史

```bash
# 查看提交历史
git log --oneline -10

# 查看文件历史
git log --follow app.py

# 查看变更内容
git show <commit-hash>
```

### 回退操作

```bash
# 撤销工作区修改
git checkout -- <file>

# 撤销暂存区
git reset HEAD <file>

# 回退到上一个版本
git reset --hard HEAD~1

# ⚠️ 强制推送 (谨慎使用)
git push -f origin master
```

---

## 分支管理

### 分支策略

```
master          - 生产分支，随时可部署
├── develop     - 开发分支，日常开发
│   ├── feature/tts      - TTS 功能分支
│   ├── feature/sync     - 同步功能分支
│   └── hotfix/auth      - 认证修复分支
```

### 创建功能分支

```bash
# 从 develop 创建新分支
git checkout develop
git checkout -b feature/new-feature

# 开发完成后合并到 develop
git checkout develop
git merge feature/new-feature

# 删除功能分支
git branch -d feature/new-feature
```

### 发布到生产

```bash
# 从 develop 发布到 master
git checkout master
git merge develop
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin master --tags
```

---

## 发布流程

### 1. 准备发布

```bash
# 更新版本号
# 在相关文件更新版本 (如 package.json, setup.py)

# 更新 CHANGELOG.md
# 记录本次发布的变更

# 运行测试
python3 -m pytest  # 如有测试
```

### 2. 创建 Release

```bash
# 打标签
git tag -a v1.0.0 -m "Release v1.0.0 - TTS 语音合成"

# 推送标签
git push origin v1.0.0

# 或推送所有标签
git push origin --tags
```

### 3. GitHub Release

访问：https://github.com/vicki/ai-team-hub/releases/new

**Release 内容**:
```
Tag version: v1.0.0
Release title: v1.0.0 - TTS 语音合成

Description:
## ✨ 新功能
- 添加 TTS 语音合成 API
- 新增历史记录下载功能

## 🐛 Bug 修复
- 修复 chat.html 样式问题

## 📝 文档更新
- 新增多端同步手册
```

---

## 自动化

### GitHub Actions 配置

创建 `.github/workflows/sync.yml`:

```yaml
name: Auto Sync

on:
  push:
    branches: [master]
  schedule:
    - cron: '0 2 * * *'  # 每日 02:00 UTC

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
      
      - name: Notify
        run: |
          echo "Sync completed!"
```

### 配置 Secrets

进入 `Settings` → `Secrets and variables` → `Actions`:

| Secret Name | Value | 说明 |
|-------------|-------|------|
| `VERCEL_TOKEN` | `...` | Vercel 部署 Token |
| `VERCEL_ORG_ID` | `...` | Vercel 组织 ID |
| `VERCEL_PROJECT_ID` | `...` | Vercel 项目 ID |

---

## 安全设置

### 1. SSH Key 配置

```bash
# 生成 SSH Key (如没有)
ssh-keygen -t ed25519 -C "your-email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub
# Settings → SSH and GPG keys → New SSH key
```

### 2. 敏感信息保护

**不要提交到 Git 的文件**:

```bash
# .gitignore
*.env
*.key
*.pem
*.secret
history.jsonl
config.local.json
```

**创建 `.gitignore`**:

```gitignore
# Python
__pycache__/
*.py[cod]
*.env
.venv/

# Node
node_modules/
dist/
.next/

# Logs
*.log
hub.log
app_debug.log

# Sensitive
.env
.key
*.pem
history.jsonl

# OS
.DS_Store
Thumbs.db
```

### 3. 访问控制

进入 `Settings` → `Collaborators`:

| 用户 | 权限 | 说明 |
|------|------|------|
| `vicki` | Admin | 仓库所有者 |
| `mycc` | Write | 可推送代码 |
| `qwq` | Write | 可推送代码 |

---

## 与多端同步集成

### 同步脚本集成

创建 `/root/air/qwq/scripts/sync-to-github.sh`:

```bash
#!/bin/bash
# GitHub 同步脚本

cd /root/air/qwq/mobile-web

# 检查变更
git status --porcelain

if [ $? -eq 0 ]; then
    # 有变更则提交
    git add .
    git commit -m "sync: GitHub 自动同步 $(date +%Y-%m-%d %H:%M)"
    git push origin master
    echo "✅ 同步到 GitHub 成功"
else
    echo "ℹ️  无变更，跳过同步"
fi
```

### 定时同步

```bash
# 添加到 crontab
crontab -e

# 每日 02:00 同步到 GitHub
0 2 * * * /root/air/qwq/scripts/sync-to-github.sh >> /var/log/github-sync.log 2>&1
```

---

## 相关资源

| 资源 | 链接 |
|------|------|
| GitHub Docs | https://docs.github.com/ |
| Git 教程 | https://git-scm.com/book/zh/v2 |
| GitHub Flow | https://docs.github.com/en/get-started/quickstart/github-flow |
| Semantic Versioning | https://semver.org/ |
| Conventional Commits | https://www.conventionalcommits.org/ |

---

## 检查清单

### 首次配置
- [ ] 创建 GitHub 仓库
- [ ] 配置 Git 远程
- [ ] 配置 SSH Key
- [ ] 创建 `.gitignore`
- [ ] 首次推送代码

### 日常操作
- [ ] 提交前检查变更
- [ ] 使用语义化提交信息
- [ ] 推送到 GitHub
- [ ] 验证 GitHub 页面更新

### 发布流程
- [ ] 更新版本号
- [ ] 更新 CHANGELOG
- [ ] 创建 Git Tag
- [ ] 创建 GitHub Release
- [ ] 通知用户

---

*最后更新：2026-03-09*  
*维护者：AI Team*  
*版本：V1.0*
