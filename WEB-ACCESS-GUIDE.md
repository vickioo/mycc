# AIHub Web 访问指南

**更新日期**: 2026-03-14

---

## 🌐 访问地址

### 本地访问
```
http://localhost:8766/
```

### 局域网访问
```
http://<服务器 IP>:8766/
```

### Termux/手机访问
```bash
# SSH 隧道方式 (推荐)
ssh -L 8766:localhost:8766 root@服务器 IP

# 然后在浏览器访问
http://localhost:8766/
```

---

## 📱 功能说明

### 主页 (hub.html)
- 🤖 AI 对话
- 📊 项目看板
- 🔗 知识库入口

### 知识库 (index-docsify.html)
- 📚 文档浏览
- 🔍 全文搜索
- 📱 移动端优化

### AI 对话
- 多 Agent 切换
- 历史记录
- 实时响应

---

## 🔧 服务管理

### 启动服务
```bash
cd /root/Obsidian/AIHub
python3 app.py &
```

### 停止服务
```bash
pkill -f "python3 app.py"
```

### 查看日志
```bash
tail -f /tmp/aihub-web.log
```

---

## 📊 当前状态

| 服务 | 端口 | 状态 |
|------|------|------|
| AIHub Web | 8766 | ✅ 运行中 |
| free-claude | 8082 | ✅ 运行中 |

---

*Last updated: 2026-03-14*
