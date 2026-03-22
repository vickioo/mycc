# AI Team 系统架构

**版本**: V3  
**更新时间**: 2026-03-06

---

## 📚 设计理念 (学习 mycc)

### 三层记忆系统

```
0-System/
├── status.md           # 短期记忆 (每日状态，Hooks 自动注入)
├── context.md          # 中期记忆 (本周上下文)
└── about-me/           # 长期记忆 (用户画像)
    └── profile.md
```

### PARA 知识管理

```
├── 1-Inbox/            # 收集 (创意/想法/待处理)
├── 2-Projects/         # 项目 (正在推进的任务)
├── 3-Thinking/         # 认知 (方法论/沉淀)
├── 4-Assets/           # 资产 (可复用资源)
└── 5-Archive/          # 归档 (历史记录)
```

### 任务追踪

```
tasks/
└── 任务名.md           # 跨会话任务追踪
```

---

## 🎯 工作流程

### 日常对话

1. 用户提问
2. Hooks 自动注入 `status.md`
3. AI 回答 (简洁直接)
4. 记录到对话历史

### 任务执行

1. 创建 `tasks/任务名.md`
2. 记录待办/进度/下一步
3. 完成后归档

### 每日睡前

1. 回顾今日完成
2. 更新 `status.md`
3. 追加到 `context.md`

### 周末回顾

1. 阅读本周 `context.md`
2. 归档到 `5-Archive/周记/`
3. 创建新的 `context.md`

---

## 🔧 Hooks 配置

### Qwen Code Hooks

位置：`/root/.qwen/settings.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "cat 0-System/status.md"
      }
    ]
  }
}
```

### 自动注入内容

每次对话自动注入：
- `0-System/status.md` - 当前状态
- `0-System/context.md` - 本周上下文
- `0-System/about-me/profile.md` - 用户画像

---

## 📊 文件归档规则

| 内容类型 | 去向 | 说明 |
|---------|------|------|
| 创意/想法 | `1-Inbox/` | 先收集，后整理 |
| 进行中项目 | `2-Projects/` | 追踪进度 |
| 认知沉淀 | `3-Thinking/` | 方法论 |
| 可复用资产 | `4-Assets/` | 模板/脚本 |
| 历史记录 | `5-Archive/` | 按日期归档 |

---

## 🚀 移动端架构

### V3 聊天窗口版

```
┌─────────────────────────────────┐
│  🤖 AI Team      [🦊 Qwen ▼]    │
├─────────────────────────────────┤
│  聊天记录 (最近 50 条)            │
│  • 用户消息 (右侧，蓝色)        │
│  • 助理消息 (左侧，白色)        │
├─────────────────────────────────┤
│  [📊] [📋] [📈] [👋]           │
├─────────────────────────────────┤
│  [输入框...]              [➤]   │
└─────────────────────────────────┘
```

### 后端 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 聊天界面 |
| `/api/chat` | POST | 发送消息 |
| `/api/history` | GET | 获取历史 |
| `/api/clear` | POST | 清空历史 |
| `/api/health` | GET | 健康检查 |

---

## ☁️ 云部署计划

### 阶段 1: 本地完善 (完成)

- ✅ V3 聊天窗口
- ✅ 对话历史 (50 条)
- ✅ 快捷操作
- ✅ 三层记忆系统

### 阶段 2: 云部署 (Week 1)

- [ ] 部署到 Vercel
- [ ] 配置自定义域名
- [ ] 测试手机访问

### 阶段 3: 数据持久化 (Week 2)

- [ ] Firebase Firestore
- [ ] 云端同步
- [ ] 离线缓存

### 阶段 4: 多端同步 (Week 3)

- [ ] 实时同步
- [ ] 冲突解决
- [ ] 多设备登录

---

## 📝 最佳实践

### 写作风格

- 简洁直接，不废话
- 搭档心态，不是客服
- 务实不纠结，先跑起来
- 带点幽默，但不硬凹

### 文件命名

- 日期：`YYYY-MM-DD-主题.md`
- 任务：`任务名.md`
- 周记：`week-YYYY-Www.md`

### Git 提交

```bash
git add .
git commit -m "feat: V3 聊天窗口版发布

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>"
git push origin main
```

---

## 🔗 相关链接

- [mycc GitHub](https://github.com/Aster110/mycc)
- [Vercel 文档](https://vercel.com/docs)
- [Firebase 文档](https://firebase.google.com/docs)

---

*Last updated: 2026-03-06*
