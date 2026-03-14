# Qwen Code Hooks 配置

**版本**: V3  
**更新**: 2026-03-06

---

## 🎯 目的

让 AI 在每次对话时自动获取：
- 当前时间
- 短期记忆 (status.md)
- 系统上下文

---

## 🔧 配置位置

`/root/.qwen/settings.json`

---

## 📋 当前配置

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "echo '<current-time>' && date '+%Y-%m-%d %H:%M %A' && echo '</current-time>' && echo '<short-term-memory>' && cat \"$CLAUDE_PROJECT_DIR/0-System/status.md\" 2>/dev/null && echo '</short-term-memory>'"
      }
    ]
  }
}
```

---

## 🔄 工作流程

```
用户发送消息
    ↓
Hooks 触发
    ↓
执行命令
    ↓
注入到 AI 上下文
    ↓
AI 回复 (带状态感知)
```

---

## 📊 注入内容

### 当前时间
```xml
<current-time>
2026-03-06 20:45 Friday
</current-time>
```

### 短期记忆
```xml
<short-term-memory>
# Status 内容...
</short-term-memory>
```

---

## 🧪 测试

发送任意消息，AI 应该：
1. 知道当前日期
2. 知道今日已完成事项
3. 知道待处理任务

---

## 🔗 相关文档

- `0-System/status.md` - 短期记忆
- `0-System/context.md` - 中期记忆
- `0-System/about-me/` - 长期记忆

---

*Last updated: 2026-03-06*
