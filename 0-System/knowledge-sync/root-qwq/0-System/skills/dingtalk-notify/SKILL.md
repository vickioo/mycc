# 🛠️ Skill: dingtalk-notify

**版本**: v1.0.0  
**描述**: 钉钉群通知发送工具  
**触发词**: `/notify`, `发送通知`, `钉钉消息`

---

## 功能

1. **钉钉机器人** — 支持 Webhook + 加签安全验证
2. **多通道** — 主备机器人自动切换
3. **Markdown 格式** — 支持富文本消息
4. **错误诊断** — 详细的发送状态反馈

---

## 配置

### 环境变量 (`/root/air/mycc/.env`)

```bash
# 主通道 (cc-mi15)
DINGTALK_WEBHOOK_PRIMARY="https://oapi.dingtalk.com/robot/send?access_token=xxx"
DINGTALK_SECRET_PRIMARY="SECxxx"

# 备用通道 (ccBot)
DINGTALK_WEBHOOK_SECONDARY="https://oapi.dingtalk.com/robot/send?access_token=yyy"
DINGTALK_SECRET_SECONDARY="SECyyy"
```

---

## 用法

### 命令行

```bash
# 发送通知
node /root/air/qwq/scripts/dingtalk-notify.js "标题" "内容" [级别]

# 示例
node /root/air/qwq/scripts/dingtalk-notify.js "📋 测试通知" "这是测试内容" info
node /root/air/qwq/scripts/dingtalk-notify.js "⚠️ 告警" "服务异常" error
```

### 集成到脚本

```bash
#!/bin/bash
# 在脚本中调用
node /root/air/qwq/scripts/dingtalk-notify.js "汇报标题" "汇报内容" success
```

---

## 文件位置

| 文件 | 路径 |
|------|------|
| **主程序** | `/root/air/qwq/scripts/dingtalk-notify.js` |
| **配置** | `/root/air/mycc/.env` |

---

## 加签算法

```javascript
function signDingTalk(secret) {
  const timestamp = Date.now();
  const stringToSign = `${timestamp}\n${secret}`;
  const sign = crypto.createHmac('sha256', secret)
    .update(stringToSign)
    .digest('base64');
  return { timestamp, sign: encodeURIComponent(sign) };
}
```

---

## 消息格式

```markdown
## 📋 标题

**内容**

- 项目 1
- 项目 2

> 🕐 时间戳
```

---

## 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 310000 | 签名不匹配 | 检查密钥和时间戳 |
| 400 | 请求错误 | 检查 Webhook URL |
| 401 | 未授权 | 检查 access_token |

---

*创建*: 2026-03-10  
*维护者*: qwq
