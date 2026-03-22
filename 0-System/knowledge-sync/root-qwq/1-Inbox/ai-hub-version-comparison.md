# AI Hub 项目版本对比报告

**生成时间**: 2026-03-11 19:55  
**对比对象**: CC 服务器 vs 本地 (qwq)

---

## 📊 版本信息

| 位置 | Git Commit | 版本说明 |
|------|------------|----------|
| **CC 服务器** | `fbb543e` | feat: add cc-switch (OneAPI) + dingtalk Stream bot skill |
| **本地** | `e17cf34` | feat(feishu): streaming card + CHANNEL_WEB switch + schema 2.0 |
| **远程 origin** | `e17cf34` | 与本地同步 |

**结论**: 本地版本 **领先** CC 服务器 4 个 commit

---

## 🔄 CC 服务器最近变更 (过去 5 个 commit)

### 新增功能
1. **cc-switch 技能** - OneAPI 自动切换
2. **钉钉 Stream 机器人** - 流式通知
3. **安全加固** - `/pair` 端点速率限制

### 文件变更统计
```
18 files changed, 3059 insertions(+), 143 deletions(-)
```

### 主要新增文件
| 文件 | 说明 |
|------|------|
| `.claude/skills/cc-switch/` | OneAPI 自动切换技能 |
| `.claude/skills/dingtalk/` | 钉钉机器人通知 |
| `.claude/skills/skill-creator/SKILL.md` | 技能创建指南 (510 行) |

---

## 📦 本地版本优势

| 功能 | 说明 |
|------|------|
| **飞书集成** | 流式卡片 + schema 2.0 |
| **桌面技能** | macOS OCR + 鼠标键盘控制 |
| **多源情报** | 每日情报收集管道 |
| **Agent Teams** | 多 Agent 协同后端 |

---

## 🎯 同步建议

### 方案 A: CC 服务器同步到最新版本 (推荐)
```bash
# 在 CC 服务器上执行
cd /data/mycc
git pull origin main
```

**优点**:
- 获得最新功能
- 保持多端一致

**风险**:
- 需要测试 OneAPI 兼容性

### 方案 B: 本地回退到 CC 版本
```bash
# 在本地执行
cd /root/air/mycc
git reset --hard fbb543e
```

**优点**:
- 稳定性高

**缺点**:
- 丢失新功能

---

## 📋 待同步到 CC 的新功能

1. **飞书流式卡片** - 需要测试 CC 环境
2. **桌面技能** - macOS 专属，CC 可能不需要
3. **情报收集** - 可部署到 CC

---

## 🚀 下一步行动

1. **同步 CC 到最新版本**
2. **测试 OneAPI + 飞书集成**
3. **部署情报收集技能**
4. **统一 Surface 版本**

---

*报告生成：2026-03-11 19:55*
