# mycc 高级模式配置

**启用时间**: 2026-03-09  
**协调方**: qwq (Qwen Code)

---

## 🚀 什么是高级模式

高级模式为 mycc 启用以下增强功能：

### 1. 开发安全审计
- Git 变更审查
- 敏感操作确认
- 代码质量检查

### 2. 现代化开发流程
- Pre-commit Hooks
- 自动化测试
- CI/CD 集成

### 3. 三方协作同步
- 与 qwq 的任务同步
- 与 CC-Server 的部署同步
- GitHub 远程协作

---

## 📋 启用步骤

### 步骤 1: 更新 CLAUDE.md

在 `CLAUDE.md` 中添加高级模式规则（见下方模板）。

### 步骤 2: 更新 permissions

修改 `.claude/settings.local.json`：

```json
{
  "permissions": {
    "allow": [...],
    "deny": [
      "Bash(rm -rf /*)",
      "Bash(curl *exe)",
      "Bash(wget *exe)",
      "Bash(mkfs:*)",
      "Bash(dd:*)",
      "Bash(*--force)",
      "Bash(*-y --no-confirm)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(git merge*)",
      "Bash(git rebase*)",
      "Bash(rm -rf*)",
      "Bash(docker rm*)",
      "Bash(kubectl delete*)"
    ]
  }
}
```

### 步骤 3: 启用 Pre-commit Hooks

```bash
cd /root/air/mycc
mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Pre-commit 安全审计

echo "🔍 运行 Pre-commit 审计..."

# 检查是否有敏感信息
if git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD|TOKEN)" | grep -v "^+#"; then
    echo "❌ 检测到敏感信息，请检查后再提交"
    exit 1
fi

# 检查是否有大文件 (>10MB)
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ] && [ $(stat -c%s "$file" 2>/dev/null || echo 0) -gt 10485760 ]; then
        echo "❌ 大文件警告：$file (>10MB)"
        exit 1
    fi
done

echo "✅ 审计通过"
exit 0
HOOK
chmod +x .git/hooks/pre-commit
```

---

## 🔒 安全审计规则

### 禁止的操作 (Deny)
- `rm -rf /*` - 删除根目录
- `curl *exe` / `wget *exe` - 下载可执行文件
- `mkfs:*` - 格式化磁盘
- `dd:*` - 底层磁盘操作
- `*--force` / `*-y --no-confirm` - 强制无确认操作

### 需要确认的操作 (Ask)
- `git push*` - 推送代码
- `git merge*` / `git rebase*` - 合并/变基
- `rm -rf*` - 递归删除
- `docker rm*` / `kubectl delete*` - 删除容器/资源

### 自动批准的操作 (Auto Approve)
- 文件读取/编辑
- Git 查看操作
- 常规构建/测试

---

## 🛠️ 开发工作流

### 1. 任务接收
```bash
# 读取 qwq 同步的任务
cat /root/air/mycc/shared-tasks/mobile-web-todo.md
```

### 2. 开发流程
```bash
# 创建功能分支
git checkout -b feat/xxx

# 开发完成后
git add .
git commit -m "feat: xxx

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>"

# Pre-commit hook 自动运行审计
# 审计通过后推送
git push origin feat/xxx
```

### 3. 代码审查
- qwq 负责审查
- CC-Server 负责部署测试
- 三方确认后合并

---

## 📊 状态检查

```bash
# 检查高级模式状态
cat /root/air/mycc/ADVANCED-MODE.md

# 检查安全审计
cat .git/hooks/pre-commit

# 检查 permissions
cat .claude/settings.local.json | jq '.permissions'
```

---

*高级模式已启用 - 安全、高效、现代化*
