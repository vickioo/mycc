# 知识库 V2.0 发布说明

**发布日期**: 2026-03-07  
**版本**: V2.0  
**状态**: ✅ 已上线

---

## 🎉 重大升级

### 采用 Docsify 专业框架

使用 **Docsify** 实现专业级知识库体验，无需构建，即开即用。

#### 核心优势
- ✅ **轻量级**: 仅 10KB 核心库
- ✅ **零构建**: 直接渲染 Markdown
- ✅ **可折叠**: 侧边栏目录支持折叠/展开
- ✅ **全文搜索**: 内置搜索引擎
- ✅ **响应式**: 完美支持移动端
- ✅ **可扩展**: 丰富插件生态

---

## 🌟 新增功能

### 1. 可折叠侧边栏

- 默认展开 2 级目录
- 点击文件夹可展开/折叠
- 支持最大 3 级嵌套

### 2. 全文搜索

- 实时搜索所有文档
- 高亮显示关键词
- 缓存 24 小时结果

### 3. 回到顶部

- 滚动 300px 后自动显示
- 平滑动画（600ms）
- 渐变按钮样式

### 4. 代码复制

- 一键复制代码块
- 成功/失败提示
- 支持多语言高亮

### 5. 图片缩放

- 点击图片放大查看
- 白色背景
- 平滑过渡

### 6. 分页导航

- 上一篇/下一篇按钮
- 跨章节导航
- 自动显示标题

---

## 📁 新增文件

### 模板文件
```
6-Diaries/templates/
├── daily-template.md    # 日更模板
└── weekly-template.md   # 周结模板
```

### 脚本文件
```
scripts/
├── daily-log.py         # 日记自动生成
└── start-knowledge-service.sh  # 知识库启动
```

### 文档文件
```
2-Projects/
└── project-board.md     # 项目看板（含 Mermaid 图表）
```

---

## 🚀 访问方式

### Docsify 专业版（推荐）
```
http://localhost:8772/kb-docs
```

### 旧版（保留兼容）
```
http://localhost:8772/kb
```

### 项目看板
```
http://localhost:8772/kb-files/2-Projects/project-board.md
```

---

## 📊 日更周结

### 创建今日日志
```bash
python3 /root/air/qwq/scripts/daily-log.py --daily
```

### 创建本周总结
```bash
python3 /root/air/qwq/scripts/daily-log.py --weekly
```

### 查看统计
```bash
python3 /root/air/qwq/scripts/daily-log.py --stats
```

### 自动化（推荐添加到 crontab）
```bash
# 每天 9:00 创建日志
0 9 * * * python3 /root/air/qwq/scripts/daily-log.py --daily

# 每周日 18:00 创建周总结
0 18 * * 0 python3 /root/air/qwq/scripts/daily-log.py --weekly
```

---

## 📈 项目看板

使用 Mermaid 图表展示：
- 项目总览（流程图）
- 任务分布（饼图）
- 进度追踪（燃尽图）
- 路线图（甘特图）

访问：`http://localhost:8772/kb-files/2-Projects/project-board.md`

---

## 🔧 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Docsify | 4.x | 核心框架 |
| PrismJS | 1.x | 代码高亮 |
| Mermaid | 9.x | 图表绘制 |
| Markdown | - | 文档格式 |

### CDN 资源
- Docsify: `cdn.jsdelivr.net/npm/docsify@4`
- PrismJS: `cdn.jsdelivr.net/npm/prismjs@1`
- Mermaid: 内置支持

---

## 📝 使用指南

### 浏览文档
1. 访问 http://localhost:8772/kb-docs
2. 点击左侧目录浏览
3. 使用搜索框查找内容

### 编写文档
1. 在对应目录创建 `.md` 文件
2. 使用标准 Markdown 语法
3. 支持 Mermaid 图表（```mermaid）

### 日更模板
```markdown
# 2026-03-07 工作日志

## 📋 今日重点
### P0 - 必须完成
- [ ] 核心任务

## 📝 工作记录
### 上午
### 下午
### 晚上

## ✅ 完成情况
## 🐛 问题与解决
## 💡 想法与灵感
## 📊 今日统计
## 🔄 明日计划
```

---

## 🆚 版本对比

| 功能 | V1.0 | V2.0 |
|------|------|------|
| 侧边栏 | ❌ | ✅ 可折叠 |
| 搜索 | ❌ | ✅ 全文 |
| 回到顶部 | ❌ | ✅ 自动 |
| 代码复制 | ❌ | ✅ 一键 |
| 图片缩放 | ❌ | ✅ 点击 |
| 分页导航 | ❌ | ✅ 自动 |
| 日更模板 | ❌ | ✅ 自动 |
| 周结模板 | ❌ | ✅ 自动 |
| 项目看板 | ❌ | ✅ Mermaid |

---

## ⏭️ 后续计划

### P1 - 近期（本周）
- [ ] 夜间模式切换
- [ ] 字体大小调节
- [ ] 阅读进度条
- [ ] 相关文章推荐

### P2 - 中期（本月）
- [ ] 评论系统
- [ ] 标签系统
- [ ] 版本对比
- [ ] 导出 PDF

### P3 - 长期（下季度）
- [ ] 多语言支持
- [ ] 协作编辑
- [ ] 版本历史
- [ ] API 文档生成

---

## 🐛 已知问题

1. **MyCC 未上线**: 需要手动启动
   ```bash
   cd /root/air/mycc
   ./start-mycc.sh
   ```

2. **部分 Mermaid 图表**: 可能需要刷新显示

3. **移动端搜索框**: 小屏幕可能遮挡内容

---

## 📞 反馈与支持

- 问题反馈：`shared-tasks/inbox/`
- 建议提交：`3-Thinking/`
- 文档更新：直接编辑对应 `.md` 文件

---

## 🎯 快速开始

```bash
# 1. 启动服务（如未运行）
/root/air/qwq/scripts/start-knowledge-service.sh

# 2. 访问知识库
# 浏览器打开：http://localhost:8772/kb-docs

# 3. 创建今日日志
python3 /root/air/qwq/scripts/daily-log.py --daily

# 4. 查看项目看板
# 浏览器打开：http://localhost:8772/kb-files/2-Projects/project-board.md
```

---

*发布说明版本：V2.0*  
*最后更新：2026-03-07 10:00*
