# AI Team 实时状态

**更新时间**: 2026-03-07 14:15  
**健康度**: 85% ⚠️

---

## 📊 服务状态

### ✅ 运行中

| 服务 | 端口 | 状态 | 说明 |
|------|------|------|------|
| AI Team Hub | 8772 | ✅ | 统一入口 |
| AI 对话 | - | ✅ | 正常服务 |
| 系统监控 | - | ✅ | 实时监控 |
| 项目看板 | - | ✅ | Kanban |
| 龙虾语音 | - | ✅ | Surface |
| 知识库 | - | ✅ | Docsify |
| free-claude | 8083 | ✅ | API 代理 |
| CC Server | - | ✅ | SSH 连接 |
| Gate | - | ✅ | 跳板服务器 |

### ⚠️ 注意

| 服务 | 问题 | 处理中 |
|------|------|--------|
| Termux SSH | 重启后断开 | ✅ 配置中 |
| U22 ssh-gate | 健康检查失败 | ✅ 重启中 |
| SJLL 龙虾 | SSH 隧道未建立 | 📋 待处理 |

---

## 📈 进度追踪

### 已完成 (今日)

- ✅ 微信文章读取 (NoizAI 语音)
- ✅ Surface 语音 Skill 安装
- ✅ 导航优化 (所有页面)
- ✅ 进度追踪页面
- ✅ 架构文档 V7
- ✅ Termux 优化计划

### 进行中

- 🔄 Termux 服务配置 (80%)
- 🔄 U22 ssh-gate 修复 (50%)
- 🔄 SJLL 隧道重建 (0%)

### 待开始

- 📋 Termux:API 集成
- 📋 公司主机发现 (Qorder)
- 📋 Victory Windows 集成

---

## 🔧 当前任务

### Termux 优化

```bash
# 状态：服务目录已创建
# 下一步：安装 termux-services

pkg install termux-services
termux-services enable sshd
```

### U22 ssh-gate

```bash
# 状态：已重启
# 下一步：检查日志

tail -20 /root/.local/sv/ssh-gate/log/current
```

---

## 📞 快速链接

| 功能 | 地址 |
|------|------|
| 主页 | http://localhost:8772/ |
| 进度 | http://localhost:8772/progress |
| 监控 | http://localhost:8772/monitor |
| 对话 | http://localhost:8772/chat |
| 知识库 | http://localhost:8772/kb-docs |

---

*最后更新：2026-03-07 14:15*  
*下次同步：14:30*
