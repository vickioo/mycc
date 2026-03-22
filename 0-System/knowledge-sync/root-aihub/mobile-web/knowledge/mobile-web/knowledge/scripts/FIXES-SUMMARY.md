# 脚本修复总结

**日期**: 2026-03-07  
**状态**: ✅ 已完成

---

## 🔧 修复内容

### 1. Termux→U22 启动脚本阻塞问题

**问题**: `auto-proxy.sh` 使用后台任务 + disown，导致从 Termux 进入 U22 时需要回车才能继续

**修复**:
- 创建 `auto-proxy-fixed.sh`
- 移除后台任务，直接同步执行
- 检测逻辑保持不变（ss 命令优先）

**文件**:
- `/root/air/qwq/0-System/auto-proxy-fixed.sh` (新版本)
- `/root/auto-proxy.sh` (旧版本 - 待替换)

**替换命令**:
```bash
cp /root/air/qwq/0-System/auto-proxy-fixed.sh /root/auto-proxy.sh
chmod +x /root/auto-proxy.sh
```

---

### 2. 清理进程自杀问题

**问题**: `pkill -f "ssh -N.*gate"` 可能误杀自己（如果脚本本身匹配模式）

**修复**:
- 使用 `setsid` 启动 SSH 隧道，创建独立会话
- SSH 进程不再受父进程影响
- 避免 `pkill` 误杀

**文件**:
- `/root/air/qwq/0-System/termux-setup.sh` (已修复)

**关键改动**:
```bash
# 旧代码 (可能被误杀)
nohup ssh -N ... gate >> "$LOGFILE" 2>&1 &

# 新代码 (独立会话)
setsid ssh -N ... gate >> "$LOGFILE" 2>&1 &
```

---

### 3. 多 Agent 对话记录标准化导出

**功能**: 统一导出所有 AI Agent 的对话记录

**支持 Agent**:
- qwq (Qwen Code)
- mycc (Claude Code Local)
- cc (CC Server Claude)
- sjll (龙虾)

**输出格式**:
- Markdown (人类可读)
- JSON (机器处理)

**用法**:
```bash
# 导出所有 Agent (Markdown)
python3 /root/air/qwq/scripts/export-conversations.py

# 导出指定 Agent
python3 export-conversations.py --agents qwq,mycc

# JSON 格式
python3 export-conversations.py --format json

# 两种格式都导出
python3 export-conversations.py --format all
```

**输出位置**:
`/root/air/qwq/6-Diaries/conversations/`

---

## 📋 待处理事项

### U22 上替换 auto-proxy.sh
```bash
# 备份旧版本
cp /root/auto-proxy.sh /root/auto-proxy.sh.bak

# 替换为新版本
cp /root/air/qwq/0-System/auto-proxy-fixed.sh /root/auto-proxy.sh
chmod +x /root/auto-proxy.sh

# 验证
source ~/.bashrc
```

### 验证 ssh-gate 服务
```bash
# 重启服务
sv restart ssh-gate

# 检查状态
sv status ssh-gate
```

---

## 📊 对比

| 问题 | 旧行为 | 新行为 |
|------|--------|--------|
| Termux→U22 | 阻塞，需回车 | 直接进入 |
| pkill 清理 | 可能自杀 | 安全 |
| 对话导出 | 手动整理 | 自动标准化 |

---

*修复完成时间：2026-03-07*
