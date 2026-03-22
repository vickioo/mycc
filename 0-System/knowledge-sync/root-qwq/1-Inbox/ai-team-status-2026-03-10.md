# 🤖 AI 助理团队状态报告

**检查时间**: 2026-03-10 08:00  
**检查者**: qwq (本地监控系统)

---

## 📊 AI 助理分布

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent 团队状态                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  本地 (qwq)                                                 │
│  ├─ ✅ continuous-monitor (PM2) - 运行 13 小时               │
│  └─ ⏸️ 5min-report (PM2) - 已停止 (夜间静默)                │
│                                                              │
│  CC-Server (100.70.32.116)                                  │
│  ├─ ✅ openclaw-gateway (PID 3820017) - 运行中              │
│  ├─ ✅ openclaw (PID 4149608) - 运行中                      │
│  ├─ ✅ openclaw-gateway (PID 4149615) - 运行中              │
│  └─ ✅ task-scheduler (PID 4149629) - 任务调度              │
│                                                              │
│  SJLL (113.57.105.174:8822)                                 │
│  ├─ ❓ OpenClaw - 未检测到进程                              │
│  ├─ ❓ Cherry Studio - 未检测到进程                         │
│  └─ ❓ 龙虾服务 - 未检测到进程                              │
│                                                              │
│  Surface (192.168.3.200)                                    │
│  ├─ ❌ SSH 超时 - 可能睡眠/关机                             │
│  └─ ❓ OpenClaw - 无法检测                                   │
│                                                              │
│  Tailscale 网络                                             │
│  ├─ ✅ cc (Linux) - 在线                                    │
│  ├─ ✅ sj-liuliang (Windows) - 在线                         │
│  ├─ ⚠️  victory (Linux) - idle (防火墙阻止)                 │
│  ├─ ✅ xiaomi-phone (Android) - 在线                        │
│  └─ 🔴 vickimacbook-pro (macOS) - offline                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🟢 正在工作的 AI 助理

### 1. 本地 (qwq)

| 助理 | 状态 | 运行时长 | 职责 |
|------|------|----------|------|
| **continuous-monitor** | ✅ 运行中 | 13 小时 | 持续监控、自动恢复 |
| **5min-report** | ⏸️ 已停止 | - | 5 分钟汇报 (夜间静默) |

### 2. CC-Server

| 助理 | PID | 内存 | 职责 |
|------|-----|------|------|
| **openclaw-gateway** | 3820017 | 403MB | OpenClaw 网关 |
| **openclaw** | 4149608 | 57MB | OpenClaw CLI |
| **openclaw-gateway** | 4149615 | 339MB | OpenClaw 网关实例 2 |
| **task-scheduler** | 4149629 | 4MB | 任务调度器 |

**状态**: ✅ 正常运行，2 个网关实例 + 任务调度

---

## 🟡 可唤醒的 AI 助理

### 1. vickimacbook-pro (macOS)

**Tailscale IP**: 100.117.29.20  
**状态**: offline (关机/睡眠)  
**唤醒方式**: 
- 等待用户开机
- Wake-on-LAN (如果配置)

### 2. Surface-Pro5

**本地 IP**: 192.168.3.200  
**状态**: SSH 超时 (可能睡眠)  
**运行服务** (上次检测):
- OpenClaw Gateway (PID 491155)
- Qwen CLI (已登录)
- 龙虾保活 (PID 104151)

**唤醒方式**:
- 等待用户唤醒
- 网络唤醒 (WoL)

### 3. Victory (100.100.1.8)

**Tailscale IP**: 100.100.1.8  
**状态**: idle (防火墙阻止 SSH)  
**可运行**: OpenClaw、Qwen 等

**恢复方式**:
```bash
# 需要 vicki 执行
sudo ufw allow 22/tcp
tailscale set --ssh=true
```

---

## 🔴 无法连接的 AI 助理

### SJLL (113.57.105.174:8822)

**连接状态**: ✅ SSH 可连接  
**AI 服务**: ❌ 未检测到 OpenClaw/Cherry/龙虾进程

**可能原因**:
- AI 服务未启动
- 使用其他用户目录
- 配置在不同位置

**建议检查**:
```bash
# 检查所有用户的 AI 服务
ssh -p 8822 vicki@113.57.105.174 "
  ps aux | grep -E 'openclaw|cherry|qwen' | grep -v grep
  ls -la /home/*/ 2>/dev/null | grep -E 'openclaw|cherry'
"
```

---

## 📋 开发和运维进度

### CC-Server

**OpenClaw 状态**:
- ✅ Gateway 运行中 (2 实例)
- ✅ CLI 运行中
- ✅ 任务调度器运行中

**项目目录**:
```
/root/air/
└── qwq/        # Qwen Code 项目
```

**待确认**:
- [ ] OpenClaw 配置文件位置
- [ ] 任务调度器日志位置
- [ ] 当前进行中的任务

### 本地 (qwq)

**监控系统**:
- ✅ continuous-monitor 运行正常
- ⏸️ 5min-report 静默中 (08:00 恢复)

**定时任务**:
```
00 08 * * * bash /root/air/qwq/scripts/morning-report.sh  # 明早汇报
00 08 * * * bash /root/air/qwq/scripts/notify-surface-morning.sh  # Surface 通知
```

---

## 🎯 建议操作

### 立即执行

1. **检查 CC-Server 任务进度**:
   ```bash
   ssh CC "cat ~/.openclaw/tasks.md 2>/dev/null | head -20"
   ```

2. **检查 SJLL AI 配置**:
   ```bash
   ssh -p 8822 vicki@113.57.105.174 "
     find /home -name '.openclaw' -o -name '.cherry*' 2>/dev/null | head -10
   "
   ```

3. **恢复 5 分钟汇报** (08:00 后):
   ```bash
   pm2 start 5min-report
   ```

### 待用户确认

1. **Surface 唤醒** - 确认是否开机
2. **Victory 防火墙** - 开放 SSH 端口
3. **SJLL AI 配置** - 确认安装位置

---

*报告生成时间：2026-03-10 08:00*  
*生成者：qwq (本地 Qwen Code 监控系统)*
