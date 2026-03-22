# Skills 目录

Claude Code 的可扩展能力模块。

## 来源说明

| 来源 | Skills |
|------|--------|
| **官方** (`anthropics/skills`) | `skill-creator`, `claude-api`, `mcp-builder`, `docx`, `xlsx`, `pdf`, `pptx` |
| **本地开发** | `mycc`, `dingtalk`, `tell-me`, `read-gzh`, `scheduler`, `setup`, `cc-usage`, `dashboard`, `cc-switch` |

## 官方 Skills

| Skill | 功能 | 触发场景 |
|-------|------|----------|
| `skill-creator` | 创建和优化 Skill | "创建一个 skill"、"把这个变成 skill" |
| `claude-api` | 使用 Claude API 构建 AI 应用 | 代码使用 `anthropic` SDK 或用户问 API 相关 |
| `mcp-builder` | 构建 MCP Server | "创建 MCP server"、"集成外部 API" |
| `docx` | Word 文档操作 | 涉及 .docx 文件 |
| `xlsx` | Excel 表格操作 | 涉及 .xlsx/.csv 文件 |
| `pdf` | PDF 操作 | 涉及 .pdf 文件 |
| `pptx` | PPT 演示文稿操作 | 涉及 .pptx 文件 |

## 本地 Skills

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `mycc` | 移动端访问后端 | `/mycc`、"启动 mycc" |
| `dingtalk` | 钉钉机器人（双向） | `/dingtalk`、"钉钉通知" |
| `tell-me` | 飞书通知 | `/tell-me`、"通知我" |
| `read-gzh` | 读取公众号文章 | `/read-gzh <链接>` |
| `scheduler` | 定时任务系统 | `/scheduler`、"定时任务" |
| `setup` | 首次使用引导 | `/setup`、"帮我配置" |
| `cc-usage` | Token 用量统计 | `/cc-usage`、"看看用量" |
| `dashboard` | 能力看板可视化 | `/dashboard` |
| `cc-switch` | 模型切换 | `/switch`、"切换模型" |

## 更新记录

- **2026-03-11**: SDK 升级到 2.1.72，从官方仓库同步 skill-creator 和其他实用 skills

## 更多资源

- [官方 Skill 仓库](https://github.com/anthropics/skills)
- [Claude Code 文档](https://code.claude.com/docs)
