# Claude Code Root Bypass 方案

## 背景
Claude Code 官方禁止 root 用户使用 `--dangerously-skip-permissions`。

## 解决方案：代理用户法
1. 创建普通用户 `vicki`。
2. 将项目迁移至 `/home/vicki/air/mycc`。
3. 配置 `vicki` 的 `~/.claude/settings.json` 为 `bypassPermissions`。
4. 在 root 下设置 Alias：
   `alias claude='cd /home/vicki/air/mycc && sudo -u vicki claude --dangerously-skip-permissions'`
