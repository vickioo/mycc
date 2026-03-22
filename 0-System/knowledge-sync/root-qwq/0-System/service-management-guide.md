# 服务管理指南

**版本**: V1.0  
**日期**: 2026-03-07 22:30  
**适用**: Gemini CLI, mycc, 所有 AI 助手

---

## ⚠️ 重要提示

**问题**: AI 助手无法直接强杀本地服务进程  
**原因**: 沙箱限制/权限不足  
**解决方案**: 通过上层管理系统 (PM2/systemd/脚本) 间接管理

---

## 🎯 服务管理层次

```
┌─────────────────────────────────────────────────────────┐
│                    用户层                                │
│                   (AI 助手)                              │
│                                                          │
│   ❌ 不能直接执行：kill/pkill/systemctl                  │
│   ✅ 可以执行：预定义脚本/PM2 API                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  管理层 (上层)                           │
│                                                          │
│   ✅ PM2: pm2 start/stop/restart                        │
│   ✅ 脚本：/root/air/qwq/scripts/*.sh                   │
│   ✅ systemd: systemctl start/stop                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  服务层                                  │
│                                                          │
│   free-claude-code, cc-clash-tunnel, mobile-web         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 服务清单

### PM2 管理服务

| 服务名 | PM2 ID | 端口 | 说明 |
|--------|--------|------|------|
| **free-claude-code** | 0 | 8082 | Claude API 代理 |
| **cc-clash-tunnel** | 1 | - | CC Clash 隧道 |
| **cc-clash-watchdog** | 2 | - | 健康检查 |

### 独立服务

| 服务 | 管理方式 | 说明 |
|------|---------|------|
| **mobile-web** | 脚本 | AI Team Mobile V8 |
| **knowledge-base** | 脚本 | Docsify 知识库 |

---

## 🔧 管理命令

### PM2 服务管理

```bash
# 查看所有服务状态
pm2 status

# 查看详细信息
pm2 describe <id|name>

# 重启服务
pm2 restart <id|name>

# 停止服务
pm2 stop <id|name>

# 启动服务
pm2 start <id|name>

# 查看日志
pm2 logs <id|name> --lines 50

# 监控资源
pm2 monit
```

### 脚本管理

```bash
# 重启 mobile-web
bash /root/air/qwq/scripts/start-all-services.sh

# 重启知识库
bash /root/air/qwq/scripts/start-knowledge-service.sh
```

### systemd 管理

```bash
# 查看状态
systemctl status clash-for-linux

# 重启服务
systemctl restart clash-for-linux

# 停止服务
systemctl stop clash-for-linux
```

---

## 🤖 AI 助手操作指南

### ✅ 可以执行的操作

1. **调用预定义脚本**
   ```bash
   bash /root/air/qwq/scripts/restart-service.sh <service-name>
   ```

2. **使用 PM2 命令** (如果权限允许)
   ```bash
   pm2 restart free-claude-code
   ```

3. **读取日志分析**
   ```bash
   tail -50 /root/free-claude-code/pm2-out.log
   ```

4. **健康检查**
   ```bash
   curl -s http://localhost:8082/health
   ```

### ❌ 不能执行的操作

1. **直接杀进程**
   ```bash
   ❌ kill -9 <pid>
   ❌ pkill -f <pattern>
   ```

2. **修改系统配置**
   ```bash
   ❌ systemctl daemon-reload
   ❌ 编辑 /etc/systemd/ 下的文件
   ```

3. **绑定特权端口**
   ```bash
   ❌ 绑定 < 1024 的端口
   ```

---

## 📝 标准操作流程

### 流程 1: 服务重启

```bash
# 1. 检查当前状态
pm2 status

# 2. 查看日志 (可选)
pm2 logs <service> --lines 20

# 3. 重启服务
pm2 restart <service>

# 4. 验证
curl -s http://localhost:<port>/health
```

### 流程 2: 故障排查

```bash
# 1. 检查服务状态
pm2 describe <service>

# 2. 查看错误日志
pm2 logs <service> --err --lines 50

# 3. 检查端口占用
lsof -i :<port> 2>/dev/null || ss -tlnp | grep <port>

# 4. 检查资源
pm2 monit
```

### 流程 3: 服务恢复

```bash
# 1. 停止旧服务
pm2 stop <service>

# 2. 清理 (可选)
pm2 delete <service>

# 3. 重新启动
pm2 start <service>

# 4. 设置开机自启
pm2 save
pm2 startup
```

---

## 🚨 常见问题

### Q1: 服务无法停止

**现象**: `pm2 stop` 无响应

**解决**:
```bash
# 强制删除
pm2 delete <service>

# 如果还不行，重启 PM2
pm2 kill
pm2 resurrect
```

### Q2: 端口被占用

**现象**: `Address already in use`

**解决**:
```bash
# 查找占用进程
lsof -i :<port>

# 通过 PM2 停止相关服务
pm2 stop <service-name>

# 如果还不行，重启 PM2
pm2 kill
sleep 2
pm2 resurrect
```

### Q3: AI 助手权限不足

**现象**: `Permission denied`

**解决**:
- 使用预定义脚本
- 通过 PM2 API (如果可用)
- 请求用户手动执行

---

## 📚 相关文件

| 文件 | 说明 |
|------|------|
| `/root/air/qwq/scripts/` | 管理脚本目录 |
| `/root/free-claude-code/` | free-claude-code 配置 |
| `/opt/clash-for-linux/` | Clash 配置 |
| `~/.pm2/` | PM2 配置和日志 |

---

## 🔗 快速链接

- **PM2 文档**: https://pm2.keymetrics.io/docs/usage/quick-start/
- **systemd 文档**: https://www.freedesktop.org/software/systemd/man/systemctl.html
- **内网集成主页**: http://localhost:8769/intranet

---

*创建：2026-03-07 22:30*  
*维护者：qwq (Qwen Code)*  
*同步给：Gemini CLI, mycc*
