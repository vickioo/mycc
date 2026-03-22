# 🖥️ SJLL (sj-liuliang) 主机深度检查报告

**检查时间**: 2026-03-10 08:30  
**检查者**: qwq (本地监控系统)  
**连接方式**: SSH port 8822 (vicki@113.57.105.174)

---

## 📊 系统概览

| 项目 | 状态 | 详情 |
|------|------|------|
| **主机名** | DatabaseI | - |
| **运行时间** | ✅ 64 天 3 小时 | 稳定运行 |
| **负载** | 1.43 / 1.32 / 1.27 | 正常 |
| **外网 IP** | 113.57.105.174 | 与 CC-Server 相同出口 |
| **Tailscale** | ❌ 未安装 CLI | 无法通过 Tailscale 直连 |

---

## 🔍 AI 服务检测结果

### ❌ 未找到 AI 相关进程

**搜索范围**:
- `qwen`, `openclaw`, `cherry`, `lobster`, `claude`, `yolo`, `oc-`

**结果**: 无匹配进程

### ❌ 未找到 AI 配置文件

**检查位置**:
- `/home/vicki/.qwen` - 未找到
- `/home/vicki/.openclaw` - 未找到
- `/home/vicki/.cherry*` - 未找到
- `/root/.qwen`, `/root/.openclaw` - 未找到
- `/home/work/*`, `/home/admin/*` - 未找到

### ❌ 未找到 AI 相关命令

```bash
which qwen openclaw cherry  # 全部 not found
```

---

## 🌐 网络服务

### 开放端口

| 端口 | 服务 | 状态 |
|------|------|------|
| **8080** | HTTP (AngularJS) | ✅ 监听中 |

**8080 服务详情**:
- 检测到 AngularJS 应用
- 似乎是音乐相关网站 (musickid.org) 的登录页面
- **非 AI 相关服务**

### Docker 状态

```bash
Docker 容器：无运行中容器
```

---

## 💾 系统资源

### 内存使用

| 项目 | 大小 |
|------|------|
| 总内存 | 16 GB |
| 已用 | 5.6 GB |
| 可用 | 9.9 GB |
| 交换 | 16 GB (已用 3.5 GB) |

### 磁盘使用

| 挂载点 | 大小 | 已用 | 可用 |
|--------|------|------|------|
| `/` (sda6) | 47 GB | 32 GB (72%) | 13 GB |
| `/home` (sda7) | 57 GB | 8.6 GB (15%) | 45 GB |
| `/mnt/0009DC270007488C` (sdb5) | 501 GB | 309 GB (62%) | 192 GB |
| `/mnt/0007DDB000055A64` (sdb6) | 432 GB | 171 GB (40%) | 261 GB |

### GPU

**状态**: 未检测到 NVIDIA GPU (或驱动未安装)

---

## ⚙️ 系统服务

### 关键服务

| 服务 | 状态 |
|------|------|
| containerd | ✅ 运行中 |
| docker | ✅ 运行中 |
| fail2ban | ✅ 运行中 |
| grafana-server | ❌ 失败 |

### 定时任务

```bash
# 用户 crontab
0 3 * * * /home/jobs/backup2vi.sh  # 每日 3 点备份

# Root crontab
* * * * * /opt/hfish/hfish  # 每分钟运行 HFish (蜜罐)
```

---

## 🔎 后台任务检查

### screen/tmux 会话

- **screen**: 无会话
- **tmux**: 无会话

### nohup 后台任务

- **结果**: 无

### Python/Node 进程

| 进程 | 用户 | 用途 |
|------|------|------|
| mount.ntfs | root | NTFS 挂载 |
| networkd-dispatcher | root | 网络调度 |
| gnome-terminal | vicki | 终端 |
| update-manager | vicki | 系统更新 |
| fail2ban-server | root | 入侵防护 |

**结论**: 无 AI 相关进程

---

## 📋 关于 QwenCLI YOLO 模式和 OpenClaw 修复

### 用户提到的功能

根据描述，SJLL 上应该有：
1. **QwenCLI YOLO 模式** - 未检测到
2. **OpenClaw 修复任务** - 未检测到
3. **其他 AI 服务** - 未检测到

### 可能原因

1. **服务未启动** - AI 服务可能已安装但未运行
2. **不同用户目录** - 可能安装在其他用户下
3. **不同位置** - 配置文件可能在非标准位置
4. **已卸载/移除** - AI 服务可能已被移除

---

## 🎯 建议操作

### 确认 AI 服务位置

```bash
# 1. 全面搜索 AI 相关文件
ssh -p 8822 vicki@113.57.105.174 "
  find / -name '*qwen*' -o -name '*openclaw*' -o -name '*cherry*' 2>/dev/null | head -50
"

# 2. 检查所有用户的 bashrc/alias
ssh -p 8822 vicki@113.57.105.174 "
  for user in vicki root work admin jack whyh888; do
    echo \"=== \$user ===\"
    cat /home/\$user/.bashrc 2>/dev/null | grep -iE 'qwen|openclaw|cherry'
  done
"

# 3. 检查环境变量
ssh -p 8822 vicki@113.57.105.174 "
  env | grep -iE 'qwen|openclaw|cherry|yolo'
"
```

### 如需安装/启动 AI 服务

```bash
# 安装 Qwen CLI (如未安装)
npm install -g @anthropic-ai/qwen-cli

# 安装 OpenClaw
npm install -g @qingchencloud/openclaw-zh

# 启动服务
openclaw gateway
```

---

## 📊 与 CC-Server 对比

| 项目 | CC-Server | SJLL |
|------|-----------|------|
| OpenClaw | ✅ 运行中 (2 网关) | ❌ 未检测到 |
| Qwen CLI | ✅ 可用 | ❌ 未找到 |
| Tailscale | ✅ 已安装 | ❌ 未安装 |
| Docker | ✅ 运行中 | ✅ 运行中 |
| 外网出口 | 113.57.105.174 | 113.57.105.174 (相同) |

---

## 📝 结论

**SJLL (sj-liuliang) 主机状态**:
- ✅ 系统运行正常 (64 天 uptime)
- ✅ Docker/Containerd 运行正常
- ❌ **未检测到任何 AI 相关服务**
- ❌ **未找到 QwenCLI YOLO 模式**
- ❌ **未找到 OpenClaw 修复任务**

**建议**:
1. 确认 AI 服务是否已安装
2. 检查是否在其他用户目录
3. 如需部署 AI 服务，可参考 CC-Server 配置

---

*检查完成时间：2026-03-10 08:30*  
*检查者：qwq (本地 Qwen Code 监控系统)*
