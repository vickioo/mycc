# ☁️ 云部署快速指南

**目标**: 10 分钟内部署 AI Team Mobile 到云端

---

## 🚀 方案选择

### 最简单：Vercel (推荐)

**适合**: 快速部署，全球访问

**免费额度**:
- ✅ 100GB 带宽/月
- ✅ 自动 HTTPS
- ✅ 全球 CDN

**部署步骤**:

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录 (支持 GitHub/GitLab/Bitbucket)
vercel login

# 3. 进入项目目录
cd /root/air/qwq/mobile-web

# 4. 部署
vercel --prod
```

**输出示例**:
```
🔍  Inspecting Project…
🚀  Production: https://ai-team-mobile.vercel.app
```

**访问**: 打开浏览器访问上面的 URL

---

### 国内优化：Cloudflare Pages

**适合**: 国内用户访问

**免费额度**:
- ✅ 无限带宽
- ✅ 10 万请求/天

**部署步骤**:

```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录
wrangler login

# 3. 部署
cd /root/air/qwq/mobile-web
wrangler pages deploy . --project-name=ai-team
```

---

### 数据持久化：Firebase

**适合**: 保存对话历史

**免费额度**:
- ✅ 1GB Firestore 数据库
- ✅ 5 万读/天

**配置步骤**:

1. 访问 https://console.firebase.google.com
2. 创建新项目
3. 启用 Firestore Database
4. 下载 `serviceAccountKey.json`
5. 配置到 Vercel 环境变量

---

## 📊 对比表

| 方案 | 部署时间 | 国内速度 | 免费额度 | 推荐度 |
|------|----------|----------|----------|--------|
| Vercel | 5 分钟 | ⭐⭐⭐ | 100GB/月 | ⭐⭐⭐⭐⭐ |
| Cloudflare | 10 分钟 | ⭐⭐⭐⭐ | 无限 | ⭐⭐⭐⭐ |
| Firebase | 15 分钟 | ⭐⭐⭐ | 1GB+5 万读 | ⭐⭐⭐⭐ |
| 阿里云 | 30 分钟 | ⭐⭐⭐⭐⭐ | 9.9 元/月 | ⭐⭐⭐ |

---

## 🎯 推荐路径

**新手**: Vercel (最快，5 分钟上线)

**国内用户**: Cloudflare Pages + Firebase

**企业用户**: 阿里云 + 自定义域名

---

## 🔗 相关链接

- [Vercel 官网](https://vercel.com)
- [Cloudflare Pages](https://pages.cloudflare.com)
- [Firebase 官网](https://firebase.google.com)
- [阿里云学生机](https://developer.aliyun.com/plan/student)

---

*Last updated: 2026-03-06*
