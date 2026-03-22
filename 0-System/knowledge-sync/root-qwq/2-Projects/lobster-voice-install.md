# 🦞 语音交互安装指南

**来源**: 微信文章 - 逛逛 GitHub  
**日期**: 2026-03-07  
**状态**: 📋 待安装

---

## 📋 项目信息

- **开源项目**: NoizAI/skills
- **GitHub**: https://github.com/NoizAI/skills
- **功能**: 让 OpenClaw 小龙虾具备语音能力
- **支持**: 音色克隆、多平台、Agent Teams

---

## 🚀 安装步骤

### Step 1: 在 Surface 龙虾上执行

在 Surface 的 Cherry Studio / OpenClaw 中输入：

```
帮我装这个 Skill：https://github.com/NoizAI/skills
```

或者手动安装：

```bash
# 查看可安装技能
npx skills add NoizAI/skills --list --full-depth

# 安装语音技能
npx skills add NoizAI/skills --full-depth --skill tts -y
```

### Step 2: 配置 Noiz API Key

1. 访问 Noiz AI 官网注册账号
2. 获取 API Key
3. 在 OpenClaw 配置中设置

### Step 3: 音色克隆（可选）

1. 准备一段参考音频（如川普的音频）
2. 丢给小龙虾进行克隆
3. 告诉它："记住这个音色就是你的音色"

### Step 4: 测试语音

对小龙虾说：
```
用你的音色跟我打个招呼
```

---

## 📦 技能列表

| 技能 | 说明 |
|------|------|
| **文本转语音** | Kokoro / Noiz 两种模式 |
| **声音对话** | 自动寻找并克隆音色 |
| **特色语音** | 情绪化、人格化表达 |
| **视频翻译** | 翻译视频并配音 |
| **语音克隆** | 克隆参考音频音色 |

---

## 🔧 配置模式

### Kokoro 模式（本地）
- ✅ 纯本地运行
- ⚠️ 需要下载模型
- ❌ 不支持音色克隆

### Noiz 云端模式（推荐）
- ✅ 大额免费额度
- ✅ 支持音色克隆
- ✅ 高质量语音
- ⚠️ 需要 API Key

---

## 🎯 使用场景

1. **开车/做家务** - 不便看屏幕时语音交互
2. **多 Agent Teams** - 不同角色不同音色
3. **情感陪伴** - 语音传递人设和情感
4. **高辨识度** - 听声音就知道是哪个 AI

---

## 📞 需要支持

### API Key
- **Noiz API Key** - 需要注册获取
- **注册链接**: 需访问 Noiz AI 官网

### 设备要求
- **Surface 龙虾** - Windows 环境
- **OpenClaw** - 已安装
- **网络** - 可访问 GitHub 和 Noiz API

---

## ✅ 安装检查清单

- [ ] Surface 龙虾可访问 GitHub
- [ ] 已安装 OpenClaw
- [ ] 已注册 Noiz AI 账号
- [ ] 已获取 API Key
- [ ] 已安装 Skill
- [ ] 已配置 API Key
- [ ] 已测试语音输出
- [ ] 已克隆音色（可选）

---

## 🔗 相关链接

- GitHub: https://github.com/NoizAI/skills
- Noiz AI: （待补充）
- 原文：https://mp.weixin.qq.com/s/jXAljkAtbvrQY3zByglBNA

---

*等待 Surface 龙虾安装确认*
