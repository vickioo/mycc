# 任务：Vercel 云部署准备就绪

**状态**: 🟡 准备就绪 (需要手动登录)  
**优先级**: 高  
**创建**: 2026-03-06

---

## ✅ 已完成

- [x] V3 聊天窗口版开发完成
- [x] Hooks 配置优化完成
- [x] 文档体系完善
- [x] Node.js 检查 (v22.22.0 ✅)
- [x] npm 检查 (10.9.4 ✅)

---

## 📋 待完成 (需要手动操作)

### 1. 注册 Vercel 账号 (5 分钟)

访问：https://vercel.com/signup

选择登录方式:
- GitHub (推荐)
- GitLab
- Bitbucket
- 邮箱

### 2. 安装 Vercel CLI (10 分钟)

```bash
npm install -g vercel
```

### 3. 登录 Vercel (2 分钟)

```bash
vercel login
```

选择登录方式 (与注册时相同)

### 4. 首次部署 (5 分钟)

```bash
cd /root/air/qwq/mobile-web
vercel --prod
```

按提示操作:
- Set up and deploy? **Y**
- Which scope? **选择你的账号**
- Link to existing project? **N**
- Project name? **ai-team-mobile**
- Directory? **./**
- Want to override settings? **N**

### 5. 测试访问

部署完成后会显示:
```
🔍  Inspecting Project…
🚀  Production: https://ai-team-mobile-xxx.vercel.app
```

访问上面的 URL 测试。

---

## 🎯 部署后配置

### 自定义域名 (可选)

1. 访问 Vercel Dashboard
2. 选择项目
3. Settings → Domains
4. 添加域名

### 环境变量

如果需要 Firebase 等:
1. Settings → Environment Variables
2. 添加变量
3. Redeploy

---

## 📊 免费额度

- ✅ 100GB 带宽/月
- ✅ 100GB-Hours Serverless/月
- ✅ 自动 HTTPS
- ✅ 全球 CDN

---

## 🔗 相关文档

- `/root/air/qwq/0-System/quick-start-cloud.md`
- `/root/air/qwq/0-System/cloud-deployment-plan.md`

---

*Created: 2026-03-06*
