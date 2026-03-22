# 多端版本同步管理手册

**版本**: V1.0  
**更新日期**: 2026-03-09  
**维护者**: AI Team (Qwen Code)

---

## 📋 目录

1. [架构概述](#架构概述)
2. [多端定义](#多端定义)
3. [同步策略](#同步策略)
4. [操作指南](#操作指南)
5. [故障排查](#故障排查)
6. [最佳实践](#最佳实践)

---

## 架构概述

### 当前多端架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Team Hub 多端架构                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│   │   本地 U22   │     │  CC 服务器   │     │   Termux    │  │
│   │  (开发端)   │────▶│  (生产端)   │────▶│  (移动端)   │  │
│   └─────────────┘     └─────────────┘     └─────────────┘  │
│         │                   │                   │           │
│         │   Git Push        │   SSH Sync        │           │
│         │──────────────────▶│──────────────────▶│           │
│                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│   │   GitHub    │     │  Vercel     │     │  远程访问    │  │
│   │  (代码仓库)  │◀───▶│  (部署平台)  │◀───▶│  (用户端)   │  │
│   └─────────────┘     └─────────────┘     └─────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 版本同步层级

| 层级 | 位置 | 用途 | 同步频率 |
|------|------|------|----------|
| **L0** | 本地 U22 (`/root/air/qwq/`) | 开发、测试 | 实时 |
| **L1** | CC 服务器 (`/root/air/qwq/`) | 生产运行 | 按需 |
| **L2** | GitHub (`github.com/vicki/`) | 版本备份 | 每日 |
| **L3** | Vercel | 公开演示 | 自动 |
| **L4** | Termux | 移动访问 | 按需 |

---

## 多端定义

### 设备清单

| 代号 | 设备 | 位置 | 用途 |
|------|------|------|------|
| **U22** | Ubuntu 22.04 | 本地 | 主要开发环境 |
| **CC** | CC 服务器 | 云端 | 生产运行、AI 服务 |
| **SJLL** | 龙虾 Surface | 本地 | 语音交互 |
| **Termux** | 安卓手机 | 移动 | 移动访问 |
| **GitHub** | 云端仓库 | 云端 | 代码备份、版本控制 |
| **Vercel** | 部署平台 | 云端 | 公开演示 |

### 目录映射

| 目录 | U22 | CC | 用途 |
|------|-----|----|------|
| **项目根目录** | `/root/air/qwq/` | `/root/air/qwq/` | 主项目 |
| **mobile-web** | `/root/air/qwq/mobile-web/` | `/root/air/qwq/mobile-web/` | AI Hub |
| **knowledge** | `/root/air/qwq/mobile-web/knowledge/` | `/root/air/qwq/mobile-web/knowledge/` | 知识库 |
| **shared-tasks** | `/root/air/qwq/shared-tasks/` | `/data/mycc/shared-tasks-qwq/` | 任务同步 |

---

## 同步策略

### 文件分类同步

| 文件类型 | 同步方向 | 频率 | 方法 |
|----------|----------|------|------|
| **代码文件** (`*.py`, `*.html`, `*.js`) | U22 → CC | 修改后 | `scp` / `rsync` |
| **配置文件** (`*.json`, `*.md`) | U22 ↔ CC | 每日 | Git / rsync |
| **文档** (`*.md`) | U22 → GitHub | 每日 | Git push |
| **日志** (`*.log`) | 不同步 | - | 本地保留 |
| **敏感配置** (`*.env`, `*.key`) | 手动 | 按需 | 加密传输 |

### 同步优先级

```
P0 (紧急): app.py, 核心服务配置 → 立即同步
P1 (高):   HTML/CSS/JS → 1 小时内同步
P2 (中):   文档、配置 → 每日同步
P3 (低):   日志、临时文件 → 不同步
```

---

## 操作指南

### 1. 本地 → CC 服务器同步

#### 单文件同步
```bash
# 同步 app.py
scp /root/air/qwq/mobile-web/app.py CC:/root/air/qwq/mobile-web/

# 同步 HTML 文件
scp /root/air/qwq/mobile-web/*.html CC:/root/air/qwq/mobile-web/

# 同步知识库
scp -r /root/air/qwq/mobile-web/knowledge/ CC:/root/air/qwq/mobile-web/
```

#### 批量同步 (推荐)
```bash
# 使用同步脚本
/root/air/qwq/scripts/sync-to-cc-mycc.sh

# 或使用 rsync
rsync -avz --delete \
  /root/air/qwq/mobile-web/ \
  CC:/root/air/qwq/mobile-web/
```

#### 验证同步
```bash
# 检查文件 MD5
md5sum /root/air/qwq/mobile-web/app.py
ssh CC "md5sum /root/air/qwq/mobile-web/app.py"

# 检查服务状态
ssh CC "pgrep -f 'python3.*app.py' && echo '服务运行中'"
```

### 2. CC 服务器 → GitHub 同步

#### 配置 Git 远程仓库
```bash
# 在 CC 服务器上
cd /root/air/qwq/mobile-web

# 添加远程仓库 (替换为你的仓库)
git remote add origin https://github.com/vicki/ai-team-hub.git

# 或 SSH 方式
git remote add origin git@github.com:vicki/ai-team-hub.git
```

#### 提交并推送
```bash
# 查看变更
git status

# 添加文件
git add .

# 提交
git commit -m "sync: 多端版本同步 $(date +%Y-%m-%d)"

# 推送到 GitHub
git push -u origin master
```

### 3. 本地 → GitHub 同步

```bash
cd /root/air/qwq/mobile-web

# 配置远程 (首次)
git remote add origin git@github.com:vicki/ai-team-hub.git

# 日常同步
git add .
git commit -m "feat: 新增功能描述"
git push origin master
```

### 4. 自动化同步脚本

创建 `/root/air/qwq/scripts/sync-all.sh`:

```bash
#!/bin/bash
# 多端同步脚本

echo "=== 多端版本同步 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"

# 1. 同步到 CC
echo "[1/3] 同步到 CC 服务器..."
rsync -avz --delete \
  /root/air/qwq/mobile-web/ \
  CC:/root/air/qwq/mobile-web/

# 2. 验证 CC 服务
echo "[2/3] 验证 CC 服务..."
ssh CC "pgrep -f 'python3.*app.py' && echo '✅ AI Hub 运行中'"

# 3. 推送到 GitHub
echo "[3/3] 推送到 GitHub..."
cd /root/air/qwq/mobile-web
git add .
git commit -m "sync: 自动同步 $(date +%Y-%m-%d)" || echo "无变更"
git push origin master

echo "=== 同步完成 ==="
```

---

## 故障排查

### 问题 1: 文件不同步

**症状**: CC 服务器文件版本落后

**解决**:
```bash
# 检查 MD5
md5sum /root/air/qwq/mobile-web/app.py
ssh CC "md5sum /root/air/qwq/mobile-web/app.py"

# 强制同步
scp -f /root/air/qwq/mobile-web/app.py CC:/root/air/qwq/mobile-web/
```

### 问题 2: Git 冲突

**症状**: `git push` 失败，提示冲突

**解决**:
```bash
# 拉取远程变更
git pull origin master

# 解决冲突后
git add .
git commit -m "merge: 解决冲突"
git push origin master
```

### 问题 3: SSH 连接失败

**症状**: `scp` / `ssh CC` 失败

**解决**:
```bash
# 检查 SSH 配置
cat ~/.ssh/config

# 测试连接
ssh -v CC

# 如被 fail2ban 阻挡，等待后重试
```

### 问题 4: 服务启动失败

**症状**: CC 服务器 AI Hub 无法启动

**解决**:
```bash
# 查看日志
ssh CC "cat /tmp/hub.log"

# 检查依赖
ssh CC "pip3 list | grep -E 'fastapi|uvicorn|edge'"

# 重启服务
ssh CC "pkill -f 'python3.*app.py'; cd /root/air/qwq/mobile-web && python3 app.py &"
```

---

## 最佳实践

### 1. 提交规范

使用语义化提交信息：

```bash
# 新功能
git commit -m "feat: 添加 TTS 语音合成"

# 修复 bug
git commit -m "fix: 修复 chat.html 样式问题"

# 文档更新
git commit -m "docs: 更新多端同步手册"

# 配置变更
git commit -m "chore: 更新 GitHub 远程配置"

# 同步操作
git commit -m "sync: 多端版本同步 2026-03-09"
```

### 2. 分支策略

```
master      - 生产分支 (CC 服务器)
develop     - 开发分支 (本地 U22)
feature/*   - 功能分支
hotfix/*    - 紧急修复
```

### 3. 备份策略

```bash
# 每日备份到 GitHub
0 2 * * * cd /root/air/qwq/mobile-web && git add . && git commit -m "daily backup" && git push

# 每周备份到外部存储
0 3 * * 0 rsync -avz /root/air/qwq/ /backup/weekly/
```

### 4. 监控清单

每日检查：
- [ ] CC 服务运行状态
- [ ] GitHub 同步状态
- [ ] 文件 MD5 校验
- [ ] 日志文件大小

---

## 相关文档

| 文档 | 位置 | 说明 |
|------|------|------|
| [Git 版本控制](4-Assets/git-version-control.md) | 知识库 | Git 基础教程 |
| [GitHub 管理指引](github-management-guide.md) | 本目录 | GitHub 详细指南 |
| [SSH 统一配置](0-System/ssh-unified-config.md) | 0-System | SSH 配置说明 |
| [服务管理](0-System/sv-service-manager.md) | 0-System | 服务管理指南 |

---

*最后更新：2026-03-09*  
*维护者：AI Team*  
*版本：V1.0*
