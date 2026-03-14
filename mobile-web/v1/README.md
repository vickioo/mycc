# AI Team Mobile Web Interface

**轻量级手机 Web 界面 - 随时随地访问 AI 助理团队**

---

## 🚀 快速启动

### 方式 1: 直接启动

```bash
cd /root/air/qwq/mobile-web
python3 app.py
```

### 方式 2: 使用启动脚本

```bash
/root/air/qwq/mobile-web/start.sh
```

### 方式 3: 后台运行

```bash
nohup python3 /root/air/qwq/mobile-web/app.py > /tmp/mobile-web.log 2>&1 &
```

---

## 📱 访问方式

### 本机访问
```
http://localhost:8765
```

### 手机访问 (同一 WiFi)

1. 查看电脑 IP 地址：
   ```bash
   hostname -I
   ```

2. 手机浏览器访问：
   ```
   http://<电脑 IP>:8765
   ```

### 远程访问 (需要端口转发)

```bash
# 通过 gate 服务器转发
ssh -R 8765:localhost:8765 gate
```

---

## 🎯 功能特性

### ✅ 已实现

1. **助理切换**
   - Qwen Code (当前会话)
   - Claude Code (CC 服务器)
   - Gemini CLI (Google)

2. **快捷命令**
   - 📊 服务状态
   - 📋 任务队列
   - 🌐 代理状态
   - 📈 用量统计

3. **自由对话**
   - 支持任意 shell 命令
   - 支持自然语言查询

4. **响应式界面**
   - 手机端优化
   - 渐变背景
   - 卡片式布局
   - 实时反馈

### ⏳ 计划中

- [ ] 历史记录查看
- [ ] 任务创建界面
- [ ] 实时日志查看
- [ ] 文件上传/下载
- [ ] WebSocket 实时推送

---

## 🔧 配置

### 修改助理列表

编辑 `app.py`:

```python
AI_AGENTS = {
    "qwq": {"name": "Qwen Code", "desc": "当前会话", "status": "online"},
    "mycc": {"name": "Claude Code", "desc": "CC 服务器", "status": "online"},
    "gemini": {"name": "Gemini CLI", "desc": "Google", "status": "standby"},
    # 添加更多助理...
}
```

### 修改端口

启动时指定：

```python
uvicorn.run(app, host="0.0.0.0", port=8765)  # 修改这里的端口
```

---

## 📊 API 接口

### 主页
```
GET /
```
返回 HTML 界面

### 发送消息
```
POST /api/chat
Content-Type: application/json

{
  "agent": "qwq",
  "message": "sv status"
}
```

### 列出助理
```
GET /api/agents
```

### 健康检查
```
GET /api/health
```

---

## 🔒 安全说明

### 当前状态
⚠️ **仅限内网使用**，无身份验证

### 建议措施

1. **内网隔离**
   - 仅在同一 WiFi 使用
   - 不开放到公网

2. **添加密码** (可选)
   在 `app.py` 中添加：
   ```python
   from fastapi.security import HTTPBasic, HTTPBasicCredentials
   security = HTTPBasic()
   
   @app.get("/")
   async def index(credentials: HTTPBasicCredentials = Depends(security)):
       # 验证用户名密码
   ```

3. **HTTPS** (可选)
   使用反向代理 (nginx/caddy) 配置 HTTPS

---

## 🐛 故障排查

### 无法访问

1. 检查服务是否运行：
   ```bash
   ps aux | grep mobile-web
   ```

2. 检查防火墙：
   ```bash
   ufw allow 8765/tcp
   ```

3. 检查端口占用：
   ```bash
   netstat -tlnp | grep 8765
   ```

### 命令执行失败

检查权限和路径，确保可以执行 shell 命令。

---

## 📝 使用示例

### 查看服务状态

1. 选择 "Qwen Code"
2. 点击 "📊 服务状态"
3. 或输入：`sv status`

### 查看任务队列

1. 选择 "Claude Code"
2. 点击 "📋 任务队列"
3. 或输入：`查看任务队列`

### 检查代理

1. 选择任意助理
2. 点击 "🌐 代理状态"
3. 等待响应

### 自定义命令

```
# 查看用量
python3 /root/air/qwq/.qwen/skills/qwq-usage/scripts/analyzer.py --days 7

# 重启服务
/root/bin/sv/sv restart ssh-gate

# 查看日志
tail -20 /root/.local/sv/ssh-gate/log/current
```

---

## 🎨 界面预览

```
┌─────────────────────────────────┐
│     🤖 AI Team                  │
│     你的 AI 助理团队              │
├─────────────────────────────────┤
│  ┌───────┐ ┌───────┐ ┌───────┐ │
│  │ 🦊    │ │ 🎯    │ │ ✨    │ │
│  │Qwen   │ │Claude │ │Gemini │ │
│  │在线   │ │在线   │ │待机   │ │
│  └───────┘ └───────┘ └───────┘ │
├─────────────────────────────────┤
│  [输入消息或命令...]            │
│                                 │
│  [📊 服务状态] [📋 任务队列]    │
│  [🌐 代理状态] [📈 用量统计]    │
│                                 │
│  [        发送        ]         │
├─────────────────────────────────┤
│  响应：                         │
│  ssh-gate: ✅ 运行中 - 健康     │
│  watchdog: ✅ 运行中            │
└─────────────────────────────────┘
```

---

## 📄 文件结构

```
/root/air/qwq/mobile-web/
├── app.py          # 主程序
├── start.sh        # 启动脚本
└── README.md       # 本文档
```

---

*版本：v1.0 | 创建时间：2026-03-06*
