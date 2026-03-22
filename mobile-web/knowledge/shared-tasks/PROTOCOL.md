# qwq ↔ mycc 共享协议

> Qwen Code (qwq) 与 Claude Code (mycc) 本地协同开发协议

---

## 共享目录

| 目录 | 用途 |
|------|------|
| `/root/air/mycc/shared-tasks-qwq/` | qwq 任务同步到 mycc |
| `/root/air/mycc/0-System/agents/qwq/` | qwq 状态文件 |

---

## 通信机制

### qwq → mycc
1. qwq 更新 `0-System/status.md`
2. 同步到 `mycc/0-System/agents/qwq/status.md`
3. mycc 通过 hooks 自动注入

### mycc → qwq
1. mycc 更新 `0-System/status.md`
2. qwq 定期读取 `mycc/0-System/status.md`

---

## 任务分发

```bash
# qwq 提交任务到 mycc
cp /root/air/qwq/shared-tasks/inbox/*.json /root/air/mycc/shared-tasks-qwq/inbox/

# mycc 处理完成后
mv /root/air/mycc/shared-tasks-qwq/inbox/*.json /root/air/mycc/shared-tasks-qwq/completed/
```

---

## 当前状态 (2026-03-05 12:20)

**qwq 完成**:
- ✅ 全局记忆系统激活
- ✅ CC 服务器连接验证
- ✅ One-API 渠道修复 (8 个正常)
- ✅ 任务分发机制验证

**mycc 完成**:
- ✅ One-API 修复：GLM5 可用
- ✅ SSH 预授权 + autoApprove
- ✅ 人类声纹日志
- ✅ 对话记录导出脚本

---

*Last updated: 2026-03-05 20:26*
