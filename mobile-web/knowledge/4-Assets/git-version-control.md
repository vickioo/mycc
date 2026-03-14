# Git 版本控制指南

**版本**: V4  
**更新**: 2026-03-06

---

## 📚 已启用功能

### 1. Git 版本控制

- ✅ 本地 Git 仓库
- ✅ 自动提交记录
- ✅ 随时回滚
- ✅ 分支管理

### 2. 流式返回

- ✅ 打字机效果
- ✅ 实时反馈
- ✅ 长消息支持
- ✅ 无需 WebSocket

---

## 🎯 Git 工作流

### 日常使用

```bash
# 查看状态
git status

# 查看变更
git diff

# 提交变更
git add -A
git commit -m "feat: 描述你的改动

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>"

# 查看历史
git log --oneline -10
```

### 回滚操作

```bash
# 撤销工作区修改
git checkout -- 文件名

# 撤销暂存
git reset HEAD 文件名

# 回退到上一个版本
git reset --hard HEAD~1

# 查看特定版本
git show 666d594
```

### 分支管理

```bash
# 创建分支
git branch feature-name

# 切换分支
git checkout feature-name

# 合并分支
git checkout master
git merge feature-name
```

---

## 📊 当前状态

```bash
cd /root/air/qwq
git status
```

**首次提交**: `666d594` - V3 聊天窗口版 + 三层记忆系统

---

## 🔧 自动提交脚本

创建 `scripts/auto-commit.sh`:

```bash
#!/bin/bash
cd /root/air/qwq
git add -A
git commit -m "chore: 自动提交 $(date '+%Y-%m-%d %H:%M')"
```

---

## 📝 提交规范

### Commit Message 格式

```
<type>: <subject>

<body>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `chore`: 构建/工具
- `perf`: 性能优化
- `test`: 测试相关

### 示例

```
feat: V4 流式返回 + Git 版控

- ✨ 添加流式返回支持
- 📊 初始化 Git 仓库
- 📝 创建版控文档
- 🔧 优化长消息显示
```

---

## 🚀 推送远程 (可选)

### GitHub

```bash
# 添加远程仓库
git remote add origin https://github.com/yourname/ai-team.git

# 推送
git push -u origin master
```

### Gitee (国内)

```bash
# 添加远程仓库
git remote add origin https://gitee.com/yourname/ai-team.git

# 推送
git push -u origin master
```

---

## 🔗 相关 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/git/status` | GET | 查看 Git 状态 |
| `/api/git/commit` | POST | 提交变更 |
| `/api/chat/stream` | POST | 流式聊天 |

---

*Last updated: 2026-03-06*
