# AI 助手服务管理同步备忘录

**日期**: 2026-03-07 22:30  
**参与**: qwq (Qwen Code), Gemini CLI, mycc  
**主题**: 服务进程管理权限和操作流程

---

## ⚠️ 问题描述

**现象**: AI 助手尝试强杀服务进程时失败  
**原因**: 沙箱限制/权限不足，无法直接执行 `kill`/`pkill`/`systemctl`  
**影响**: 服务卡死时无法直接恢复

---

## ✅ 解决方案

### 管理层级

```
用户层 (AI 助手)
    │
    │ ❌ 不能直接 kill/pkill
    │ ✅ 可以调用预定义脚本/PM2 API
    ▼
管理层 (上层系统)
    │
    │ PM2: pm2 start/stop/restart
    │ 脚本：/root/air/qwq/scripts/*.sh
    │ systemd: systemctl start/stop
    ▼
服务层
    free-claude-code, cc-clash-tunnel, mobile-web
```

### 可执行操作

| 操作 | 命令 | 说明 |
|------|------|------|
| **重启 PM2 服务** | `pm2 restart <name>` | 推荐方式 |
| **停止 PM2 服务** | `pm2 stop <name>` | 临时停止 |
| **查看状态** | `pm2 status` | 所有服务状态 |
| **查看日志** | `pm2 logs <name>` | 实时日志 |
| **运行脚本** | `bash /path/to/script.sh` | 预定义脚本 |

### 禁止操作

| 操作 | 原因 |
|------|------|
| `kill -9 <pid>` | 权限不足，可能失败 |
| `pkill -f <pattern>` | 可能误杀其他进程 |
| `systemctl daemon-reload` | 需要 root 权限 |
| 绑定 < 1024 端口 | 需要特权 |

---

## 📋 服务清单

### PM2 管理

```bash
# 服务列表
0  │ free-claude-code     │ online  │ :8082
1  │ cc-clash-tunnel      │ online  │ SSH 隧道
2  │ cc-clash-watchdog    │ online  │ 健康检查
```

### 脚本管理

```bash
# mobile-web
bash /root/air/qwq/scripts/start-all-services.sh

# 知识库
bash /root/air/qwq/scripts/start-knowledge-service.sh

# 代理测试
bash /root/air/qwq/scripts/test-remote-proxy.sh
```

---

## 🔄 标准操作流程

### 服务重启流程

```bash
# 1. 检查状态
pm2 status

# 2. 查看日志 (可选)
pm2 logs <service> --lines 20

# 3. 重启服务
pm2 restart <service>

# 4. 验证
curl -s http://localhost:<port>/
```

### 故障排查流程

```bash
# 1. 查看服务详情
pm2 describe <service>

# 2. 查看错误日志
pm2 logs <service> --err --lines 50

# 3. 检查端口
ss -tlnp | grep <port>

# 4. 监控资源
pm2 monit
```

---

## 📚 参考文档

- **服务管理指南**: `0-System/service-management-guide.md`
- **内网集成主页**: http://localhost:8769/intranet
- **PM2 文档**: https://pm2.keymetrics.io/

---

## 🤖 AI 助手须知

### 你是 qwq/mycc/gemini 时

**可以做的**:
1. 使用 `pm2 restart/stop/start <service>`
2. 运行预定义脚本
3. 读取日志文件分析
4. 调用健康检查 API

**不要做的**:
1. ❌ 直接 `kill -9` 进程
2. ❌ 修改 systemd 配置
3. ❌ 绑定特权端口

---

## 📝 同步状态

| AI 助手 | 状态 | 说明 |
|--------|------|------|
| **qwq** | ✅ 已知 | 创建本指南 |
| **mycc** | 📋 待同步 | 通过 API 消息 |
| **Gemini** | ⚠️ 同步中 | API 连接超时 |

---

*创建：2026-03-07 22:30*  
*维护者：qwq (Qwen Code)*
