# AI Team 系统架构与云部署计划

**创建时间**: 2026-03-06  
**状态**: 规划中

---

## 📚 mycc 设计理念学习

### 核心架构

```
mycc/
├── CLAUDE.md              # AI 的"性格"定义
├── .claude/
│   ├── settings.local.json  # Hooks 配置
│   └── skills/              # 技能系统
├── 0-System/                # 三层记忆系统
│   ├── status.md            # 短期记忆 (每日状态)
│   ├── context.md           # 中期记忆 (本周上下文)
│   └── about-me/            # 长期记忆 (用户画像)
├── 1-Inbox/ ~ 5-Archive/    # PARA 知识管理
└── tasks/                   # 跨会话任务追踪
```

### 关键设计原则

1. **三层记忆系统**
   - 短期：自动注入 (Hooks)
   - 中期：每日睡前归档
   - 长期：深度理解用户

2. **PARA 文件组织**
   - Inbox → Projects → Thinking → Assets → Archive

3. **技能扩展系统**
   - 每个技能独立目录
   - SKILL.md 定义触发词和执行逻辑

4. **任务追踪**
   - 跨会话任务用 tasks/*.md 追踪
   - 完成后归档

---

## 🎯 当前系统拓扑

### 本地架构 (U22 + Termux)

```
┌─────────────────────────────────────────┐
│              U22 (Ubuntu 22.04)          │
│  ┌────────────────────────────────────┐ │
│  │  Qwen Code (qwq)                   │ │
│  │  ├─ .qwen/                         │ │
│  │  │   ├─ oauth_creds.json          │ │
│  │  │   ├─ settings.json             │ │
│  │  │   └── projects/                │ │
│  │  ├─ 0-System/                     │ │
│  │  │   ├─ status.md                 │ │
│  │  │   └── skills/                  │ │
│  │  └── mobile-web/ (V2 Lite)        │ │
│  │      └── app.py (对话历史)        │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  mycc (Claude Code Template)       │ │
│  │  ├─ CLAUDE.md                      │ │
│  │  ├─ .claude/                       │ │
│  │  │   ├─ skills/                    │ │
│  │  │   │   ├─ cc-usage/             │ │
│  │  │   │   └── dashboard/           │ │
│  │  │   └── settings.local.json      │ │
│  │  └── 0-System/                     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
           │
           │ SSH Tunnel (gate)
           ▼
┌─────────────────────────────────────────┐
│         CC 服务器 (192.168.100.228)      │
│  ┌────────────────────────────────────┐ │
│  │  free-claude-code Proxy :8082      │ │
│  │  ├─ UNICLOUD (Priority 1)         │ │
│  │  ├─ NVIDIA NIM (Priority 2)       │ │
│  │  └── One-API :3000                │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Clash VPN :7890                   │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 移动端访问

```
手机浏览器 → U22:8766 (V2 Lite)
            ├─ 对话历史 (最近 20 条)
            ├─ 快捷技能
            └── 助理切换
```

---

## ☁️ 免费云服务方案

### 推荐方案：Vercel + Firebase 混合

#### 方案 A: Vercel 静态托管 (推荐)

**适用**: AI Team Mobile V2 Lite 前端

**免费额度**:
- ✅ 100GB 带宽/月
- ✅ 100GB-Hours Serverless/月
- ✅ 自动 HTTPS + CDN
- ✅ 自定义域名

**部署步骤**:
```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录
vercel login

# 3. 部署
cd /root/air/qwq/mobile-web
vercel --prod
```

**优势**:
- 零配置部署
- 全球 CDN 加速
- 自动 HTTPS
- 支持自定义域名

**劣势**:
- 国内访问可能慢
- Serverless 有超时限制 (10s)

---

#### 方案 B: Cloudflare Pages (备选)

**适用**: 静态前端 + Workers 后端

**免费额度**:
- ✅ 无限带宽
- ✅ 10 万 Workers 请求/天
- ✅ 自动 HTTPS
- ✅ 全球 CDN

**部署步骤**:
```bash
# 1. 安装 Wrangler CLI
npm i -g wrangler

# 2. 登录
wrangler login

# 3. 部署
cd /root/air/qwq/mobile-web
wrangler pages deploy . --project-name=ai-team
```

**优势**:
- 无限带宽
- 国内访问较快 (有香港节点)
- Workers 支持后端逻辑

**劣势**:
- Workers 有并发限制
- 配置稍复杂

---

#### 方案 C: Firebase Hosting (国内优化)

**适用**: 需要国内快速访问

**免费额度**:
- ✅ 10GB 存储
- ✅ 360MB/天 流出
- ✅ 自动 HTTPS
- ✅ 全球 CDN

**部署步骤**:
```bash
# 1. 安装 Firebase CLI
npm i -g firebase-tools

# 2. 登录
firebase login

# 3. 初始化
firebase init hosting

# 4. 部署
firebase deploy --only hosting
```

**优势**:
- Google 背书，稳定
- 国内访问尚可
- 集成 Firestore 数据库

**劣势**:
- 带宽有限 (360MB/天)
- 配置复杂

---

### 国内云厂商优惠

#### 阿里云 (学生机)

**9.9 元/月**:
- ✅ 2 核 2G 云服务器
- ✅ 5GB OSS 存储
- ✅ 10GB 流出/月
- ✅ 100 万 函数计算 FC/月

#### 腾讯云 (云开发)

**免费额度**:
- ✅ 云托管：50 万 CBM/月
- ✅ 云数据库：256MB
- ✅ 云存储：5GB

---

## 🗺️ 实施路线图

### 阶段 1: 本地完善 (当前)

**目标**: 确保本地功能完备，可独立使用

**待办**:
- [x] V2 Lite 对话历史功能
- [ ] 本地数据持久化 (SQLite)
- [ ] 导出/导入对话记录
- [ ] 离线模式支持
- [ ] PWA 支持 (可安装到桌面)

**时间**: 1-2 天

---

### 阶段 2: 云部署测试 (Week 1)

**目标**: 部署到 Vercel，测试可访问性

**步骤**:
1. **Day 1**: Vercel 账号注册 + CLI 安装
2. **Day 2**: 部署 V2 Lite 静态版
3. **Day 3**: 配置自定义域名 (可选)
4. **Day 4**: 测试手机访问
5. **Day 5**: 性能优化

**交付**:
- ✅ V2 Lite 部署到 Vercel
- ✅ 手机可访问
- ✅ HTTPS 自动启用

---

### 阶段 3: 后端云化 (Week 2)

**目标**: 将对话历史同步到云端

**方案**:
```
U22 (本地)          Vercel (云端)
  │                    │
  │  POST /api/chat    │
  ├───────────────────>│
  │                    │  Firestore
  │                    ├──────────> 保存对话
  │                    │
  │  GET /api/history  │
  <────────────────────┤
  │                    │
```

**技术栈**:
- 前端：Vercel Hosting
- API: Vercel Serverless Functions
- 数据库：Firebase Firestore (免费 1GB)

**步骤**:
1. 创建 Firebase 项目
2. 配置 Firestore 数据库
3. 编写 Vercel Serverless Functions
4. 前端对接云 API
5. 本地数据迁移

---

### 阶段 4: mycc 经验借鉴 (Week 3)

**学习 mycc 的设计**:

1. **三层记忆系统**
   ```
   qwq/
   ├── 0-System/
   │   ├── status.md       # 每日状态 (短期)
   │   ├── context.md      # 每周上下文 (中期)
   │   └── about-me/       # 用户画像 (长期)
   └── tasks/              # 任务追踪
   ```

2. **技能扩展系统**
   ```
   .qwen/skills/
   ├── qwq-usage/          # 用量统计
   ├── dashboard/          # 状态看板
   └── mobile-web/         # 移动端技能
   ```

3. **Hooks 自动注入**
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

**实施**:
- Day 1: 重构 0-System 目录结构
- Day 2: 实现三层记忆自动归档
- Day 3: 创建任务追踪系统
- Day 4: 优化 Hooks 配置
- Day 5: 测试验证

---

### 阶段 5: 多端同步 (Week 4)

**目标**: 手机/平板/U22 数据实时同步

**架构**:
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  手机    │     │   平板   │     │   U22    │
│  V2 Lite │     │  V2 Lite │     │  V2 Lite │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └────────────────┼────────────────┘
                      │
                      ▼
             ┌────────────────┐
             │  Firebase      │
             │  Firestore     │
             │  (云端数据库)  │
             └────────────────┘
```

**功能**:
- ✅ 实时对话同步
- ✅ 离线缓存
- ✅ 冲突解决
- ✅ 多设备登录

---

## 📊 成本估算

### 免费方案 (推荐起步)

| 服务 | 免费额度 | 是否够用 |
|------|----------|----------|
| Vercel Hosting | 100GB/月 | ✅ 是 |
| Firebase Firestore | 1GB 存储 | ✅ 是 |
| Cloudflare CDN | 无限 | ✅ 是 |
| **总计** | **$0/月** | ✅ |

### 付费方案 (按需升级)

| 服务 | 价格 | 升级理由 |
|------|------|----------|
| Vercel Pro | $20/月/人 | 更多带宽 |
| Firebase Blaze | 按量付费 | 更多数据库 |
| 阿里云学生机 | 9.9 元/月 | 国内服务器 |
| **总计** | **~¥30/月** | - |

---

## 🎯 下一步行动

### 立即执行 (今天)

1. **完善本地功能**
   - [ ] 测试 V2 Lite 对话历史
   - [ ] 添加数据导出功能
   - [ ] 优化移动端 UI

2. **准备云部署**
   - [ ] 注册 Vercel 账号
   - [ ] 注册 Firebase 账号
   - [ ] 准备自定义域名 (可选)

### 本周内

1. **部署到 Vercel**
   - [ ] 安装 Vercel CLI
   - [ ] 首次部署测试
   - [ ] 配置环境变量

2. **集成 Firebase**
   - [ ] 创建 Firestore 数据库
   - [ ] 编写 Serverless Functions
   - [ ] 前端对接云 API

---

## 📝 学习笔记

### mycc 可借鉴的设计

1. **CLAUDE.md 定义 AI 性格**
   - qwq 也可以有自己的"性格"配置
   - 定义输出风格、介入方式等

2. **三层记忆系统**
   - 短期：status.md (每日)
   - 中期：context.md (每周)
   - 长期：about-me/ (永久)

3. **技能扩展系统**
   - 每个技能独立目录
   - SKILL.md 定义触发词
   - 可组合使用

4. **任务追踪**
   - tasks/*.md 跨会话追踪
   - 完成后自动归档

### mycc 的不同之处

1. **mycc 是 Claude Code 模板**
   - 需要用户 clone 后自己配置
   - 依赖 Claude Code 官方服务

2. **qwq 是 Qwen Code 实例**
   - 直接使用 OAuth 授权
   - 更轻量，开箱即用

3. **移动端策略**
   - mycc: 依赖 mycc.dev 官方服务
   - qwq: 自建 V2 Lite，完全可控

---

*Last updated: 2026-03-06*
