# 钉钉通知配置完成

## ✅ 已完成配置

### 1. 钉钉 Webhook 配置

已配置两个钉钉机器人通道：

| 通道 | Webhook | 密钥 | 状态 |
|------|---------|------|------|
| 主通道 (cc-mi15) | `access_token=71bcdde...` | `SECcc86e370f...` | ⚠️ 签名需检查 |
| 备用通道 (ccBot) | `access_token=ae8d3ab...` | `SEC5a0e24964...` | ✅ 正常工作 |

配置文件：`/root/air/mycc/.env`

### 2. 通知脚本

**位置**: `/root/air/qwq/scripts/dingtalk-notify.js`

**用法**:
```bash
node /root/air/qwq/scripts/dingtalk-notify.js "标题" "内容" [级别]
# 级别：info, success, warning, error
```

**特性**:
- 支持钉钉加签安全验证
- 主通道失败自动切换备用通道
- Markdown 格式消息

### 3. 5 分钟汇报集成

**通知模式**: `dingtalk`

**触发条件**:
- 每 5 分钟定期汇报（心跳数 % 10 == 0 时发送）
- 服务异常时立即告警

**汇报内容**:
- 运行时长统计
- 服务状态检查
- 问题检测报告

## 📋 测试验证

```bash
# 测试通知
node /root/air/qwq/scripts/dingtalk-notify.js "📋 测试通知" "这是测试内容" info

# 查看汇报
pm2 logs 5min-report --lines 20

# 手动生成汇报
bash /root/air/qwq/scripts/5min-report.sh report
```

## 🔧 通知模式配置

编辑 `/root/air/qwq/scripts/pm2/monitor.config.js`:

```javascript
env: {
  NOTIFICATION_MODE: 'dingtalk'  // auto, dingtalk, silent
}
```

**模式说明**:
- `dingtalk` - 仅钉钉通知（当前使用）
- `auto` - 自动选择（默认）
- `silent` - 静默模式（只记录日志）

## 🛠️ 主通道修复

主通道 (cc-mi15) 报错 `310000 签名不匹配`，可能原因：

1. **密钥已更新** - 需要在钉钉开发者后台重新生成
2. **Webhook URL 变化** - 检查机器人配置

**修复步骤**:
1. 访问 https://open.dingtalk.com/document/
2. 进入机器人管理页面
3. 重新生成密钥（SEC 开头）
4. 更新 `/root/air/mycc/.env` 中的配置

当前使用备用通道 (ccBot) 正常工作。

## 📊 监控状态

```bash
# 查看 PM2 状态
pm2 status

# 查看监控日志
tail -f /tmp/qwq-monitor/monitor.log

# 快速状态检查
bash /root/air/qwq/scripts/quick-status.sh
```

## 🎯 下一步

1. **每 5 分钟自动汇报** - 已启动 ✅
2. **异常告警** - 检测到服务异常时自动通知 ✅
3. **主通道修复** - 可选，备用通道已可用

## 📝 历史配置来源

配置信息来自 Gemini 历史聊天记录：
- 主通道：cc-mi15（你和 cc 各自用一个）
- 备用通道：ccBot

配置已保存到 `/root/air/mycc/.env`，与飞书、Telegram 共用同一配置文件。
