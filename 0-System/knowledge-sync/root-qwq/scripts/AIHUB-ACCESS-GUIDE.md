# AIHub 系统访问指南

**更新日期**: 2026-03-13

---

## 📱 系统访问入口总览

AIHub 系统共有 **4 种访问方式**，分为 **2 大类**：

```
┌─────────────────────────────────────────────────────────┐
│                    AIHub 系统                            │
├─────────────────────────────────────────────────────────┤
│  📖 知识管理 (Obsidian)                                  │
│     └── 本地编辑、知识图谱、双向链接                     │
│                                                         │
│  🌐 Web 访问 (HTTP 服务)                                  │
│     ├── 8766 端口 - AIHub 移动端界面                      │
│     └── 8082 端口 - free-claude-code API                 │
│                                                         │
│  📁 文件系统                                             │
│     └── 直接访问 Markdown 文件                            │
└─────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Obsidian 访问方式

### 适用场景
- 知识编辑和管理
- 查看双向链接
- 使用知识图谱
- 日记和模板

### 访问方法

#### 方法 A: 桌面端 Obsidian
```
1. 安装 Obsidian (https://obsidian.md)
2. 打开 Obsidian → "打开文件夹作为 Vault"
3. 选择：/root/Obsidian/AIHub
4. 完成！
```

#### 方法 B: Obsidian Mobile (手机)
```
1. 安装 Obsidian App (iOS/Android)
2. 通过 USB/网络同步文件夹
3. 或使用 Obsidian Sync (付费)
```

### 特点
| 优点 | 缺点 |
|------|------|
| ✅ 强大的双向链接 | ❌ 需要安装软件 |
| ✅ 知识图谱可视化 | ❌ 移动端同步复杂 |
| ✅ 丰富的插件生态 | ❌ 无法直接 HTTP 访问 |
| ✅ 离线可用 | |

---

## 2️⃣ Web 浏览器访问 (HTTP 服务)

### 2.1 AIHub 移动端界面 (8766 端口)

**服务**: FastAPI + Docsify

#### 本地访问
```
http://localhost:8766/
```

#### 局域网访问 (需配置)
```
http://<服务器 IP>:8766/
例如：http://192.168.100.228:8766/
```

#### Termux 访问
```
# 在 Termux 浏览器中打开
http://localhost:8766/

# 或通过 SSH 隧道
ssh -L 8766:localhost:8766 user@server
然后在手机浏览器访问 http://localhost:8766/
```

**功能**:
- 📱 移动端优化界面
- 💬 AI 对话
- 📚 知识库浏览
- 📊 项目看板

---

### 2.2 free-claude-code API (8082 端口)

**服务**: Claude Code 代理

#### 访问地址
```
http://localhost:8082/
```

**功能**:
- 🔌 Claude API 代理
- 🔄 多模型路由
- 📡 WebSocket 支持

---

## 3️⃣ 文件系统直接访问

### 路径
```
/root/Obsidian/AIHub/
```

### 访问方法
- SSH/SFTP 连接
- 文件管理器
- VS Code Remote

---

## 📡 外部访问配置

### 从 Termux 访问

#### 方法 1: SSH 隧道 (推荐)
```bash
# 在 Termux 中执行
ssh -L 8766:localhost:8766 -L 8082:localhost:8082 root@your-server

# 然后在手机浏览器访问
http://localhost:8766/
http://localhost:8082/
```

#### 方法 2: 修改监听地址
```bash
# 修改 aihub/app.py
uvicorn.run(app, host="0.0.0.0", port=8766)

# 重启服务
pkill -f "python3 app.py"
cd /root/air/aihub && python3 app.py &

# 在 Termux 访问服务器 IP
http://<server-IP>:8766/
```

### 从手机浏览器访问

#### 前提条件
1. 服务器和手机在同一局域网
2. 或配置了端口转发/隧道

#### 步骤
```
1. 获取服务器 IP
   ip addr show | grep inet

2. 确保防火墙允许
   iptables -A INPUT -p tcp --dport 8766 -j ACCEPT

3. 在手机浏览器访问
   http://<服务器 IP>:8766/
```

---

## 🔐 安全配置

### 当前状态
| 服务 | 监听地址 | 外部访问 |
|------|---------|---------|
| aihub (8766) | 0.0.0.0 | ⚠️ 需防火墙配置 |
| free-claude (8082) | 0.0.0.0 | ⚠️ 需防火墙配置 |
| Obsidian | 本地文件 | ✅ 无需网络 |

### 推荐配置
```bash
# 仅允许本地访问 (安全)
# 在 app.py 中修改
uvicorn.run(app, host="127.0.0.1", port=8766)

# 或通过防火墙限制
ufw allow from 192.168.100.0/24 to any port 8766
```

---

## 📊 访问方式对比

| 访问方式 | 适用设备 | 功能 | 难度 |
|---------|---------|------|------|
| **Obsidian 桌面** | PC/Mac | 完整编辑、知识图谱 | ⭐ |
| **Obsidian Mobile** | 手机/平板 | 查看、简单编辑 | ⭐⭐ |
| **Web (8766)** | 任意浏览器 | 移动端界面、AI 对话 | ⭐ |
| **Web (8082)** | 开发者 | API 调试 | ⭐⭐⭐ |
| **文件系统** | 任意 | 原始文件访问 | ⭐⭐ |

---

## 🚀 快速开始

### 场景 1: 在 PC 上管理知识
```
1. 安装 Obsidian
2. 打开 /root/Obsidian/AIHub
3. 开始编辑
```

### 场景 2: 在手机上查看
```
选项 A: 安装 Obsidian Mobile + 同步
选项 B: 浏览器访问 http://服务器 IP:8766/
```

### 场景 3: 在 Termux 中访问
```bash
# SSH 隧道
ssh -L 8766:localhost:8766 root@server

# 浏览器打开
http://localhost:8766/
```

---

## 🛠️ 服务管理

### 启动所有服务
```bash
# AIHub Web
cd /root/air/aihub && python3 app.py &

# free-claude-code
pm2 start free-claude-code

# 检查状态
curl http://localhost:8766/
curl http://localhost:8082/
```

### 停止服务
```bash
pkill -f "python3 app.py"
pm2 stop free-claude-code
```

---

## 📋 总结

### 当前系统能力

**访问入口总数**: **4 个**

| # | 入口 | 类型 | 地址 |
|---|------|------|------|
| 1 | Obsidian Vault | 本地文件 | `/root/Obsidian/AIHub` |
| 2 | AIHub Web | HTTP | `http://localhost:8766/` |
| 3 | free-claude API | HTTP | `http://localhost:8082/` |
| 4 | 文件系统 | SFTP/SSH | `/root/Obsidian/AIHub/` |

### 推荐组合

**日常使用**:
- 📖 Obsidian (知识管理)
- 🌐 Web 8766 (快速查看、AI 对话)

**开发调试**:
- 🔌 Web 8082 (API 测试)
- 📁 文件系统 (直接编辑)

**移动访问**:
- 📱 Obsidian Mobile (离线编辑)
- 🌐 SSH 隧道 + Web (在线访问)

---

*Last updated: 2026-03-13*
