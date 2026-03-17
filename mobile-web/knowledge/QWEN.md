# Qwen Code - Global Memory & Capabilities

## 🧠 Global Memory

### User Information
- **Name**: vicki
- **Working Directory**: `/root/air/qwq`

### Multi-AI-Agent System Architecture

**Local Agents**:
- **qwq**: Qwen Code at `/root/air/qwq`
- **mycc**: Claude Code template at `/root/air/mycc`
- **free-claude-code**: Proxy at `/root/free-claude-code` (port 8083 via PM2)

**CC Server (CC 服务器)**:
- SSH alias: `CC`
- Running Claude and One-API services
- Has Clash VPN service for internet access
- Exit IP: 113.57.105.174

**CC Clash Tunnel** ⏸ 已停止:
- Script: `/root/cc-clash-tunnel.sh`
- PM2: `cc-clash-tunnel`, `cc-clash-watchdog` (health check every 30s)
- Forwards CC server's Clash SOCKS5 (port 7890) to localhost:7890
- Auto-proxy: `/root/auto-proxy.sh` in `.bashrc` - transparent proxy detection
- Usage: `export ALL_PROXY=socks5h://localhost:7890` (or auto-detected)
- **状态**: 2026-03-16 手动停止，可通过 `pm2 start cc-clash-tunnel` 重启

**通知系统**:
- 钉钉: `node /root/air/qwq/scripts/dingtalk-notify.js "标题" "内容" "info"`
- 5min-report: PM2 服务 `/root/air/qwq/scripts/5min-report.sh`
- 定期同步: 参考 [ai-skills-notify.md](./0-System/ai-skills-notify.md)

**Agent Communication**:
- qwq ↔ mycc: Local file sync via `shared-tasks/`
- Task Router: `router.sh` (distributes to CC, SJLL, local)
- Tracker: `tracker.sh` (task status monitoring)
- Health Check: `healthcheck.sh` (network connectivity)

### User Preferences
- **Language**: English (for explanations and responses)
- **Code/Technical**: Preserve verbatim (no translation)
- **Output Style**: Concise, minimal scrolling, avoid verbose output
- **Screen Optimization**: Compact responses, reduce line count

---

## 🚀 Core Capabilities

### File Operations
- `read_file` - Read file contents (text, images, PDFs)
- `write_file` - Create/write files
- `edit` - Precise text replacement with context
- `list_directory` - List directory contents
- `glob` - Fast file pattern matching
- `grep_search` - Regex-based content search

### Code Execution
- `run_shell_command` - Execute shell commands (foreground/background)
- Support for long-running processes (servers, watchers)

### Web & External
- `web_search` - Search for current information
- `web_fetch` - Fetch and process URL content

### Task Management
- `todo_write` - Track multi-step tasks
- `task` - Delegate to specialized subagents
- `skill` - Execute specialized skills

### Memory
- `save_memory` - Store user preferences and facts

---

## 📋 Best Practices

1. **Conventions**: Match existing project style
2. **Verification**: Run build/lint/test after changes
3. **Security**: Explain critical commands before execution
4. **Efficiency**: Parallel independent operations
5. **Tracking**: Use todo list for complex tasks

---

## 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Display help information |
| `/bug` | Report a bug or provide feedback |

---

*Last updated: 2026-03-05*

## Qwen Added Memories
- User's name is vicki
- SSH 密钥统一配置：U22 和 Termux 必须使用相同的 SSH 密钥（/root/.ssh/id_ed25519，指纹 SHA256:lV5Xuhsy8/YW2mE/39+KyBOPuhrbNEtVNeLxNnelxd0）连接 gate 服务器 (113.57.105.174:8822)。Termux 配置：~/.ssh/id_ed25519，~/.ssh/config 中 Host gate 指定 IdentityFile ~/.ssh/id_ed25519。服务器 authorized_keys 必须包含对应公钥。避免反复重试被 ban。
