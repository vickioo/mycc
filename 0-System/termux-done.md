# Termux + U22 架构完成报告

**日期**: 2026-03-05  
**状态**: ✅ 完成

---

## 完成的工作

### 1. Termux SSH 守护进程 ✅

- Termux sshd 已启动（端口 8022）
- 可从 U22 SSH 连接到 Termux
- 命令：`ssh -p 8022 localhost`

### 2. U22 sv-style 服务管理 ✅

- ssh-gate 服务：端口转发中（8045-CC, 8006-PVE 等）
- watchdog 服务：健康检查运行中
- 管理命令：`sv status`, `sv start/stop`

### 3. Termux 服务脚本 ✅

已创建在 Termux 中：
- `~/.local/sv/ssh-gate/run` - ssh-gate 服务脚本
- `~/.local/sv/watchdog/run` - watchdog 服务脚本
- `~/bin/sv` - 服务管理命令
- `~/.ssh/config` - SSH 配置
- `~/.ssh/id_ed25519_vi` - SSH 密钥

### 4. 文档完成 ✅

| 文档 | 位置 |
|------|------|
| 架构指南 | `0-System/termux-architecture.md` |
| SSH 连接指南 | `0-System/termux-ssh-guide.md` |
| 服务管理文档 | `0-System/sv-service-manager.md` |
| 解耦方案 | `0-System/architecture-decoupling.md` |

---

## 当前状态

### U22 服务

```
ssh-gate: ✅ 运行中 (端口转发正常)
  - 8045 (CC) ✅
  - 8006 (PVE) ✅
  - 8821 (SJLL SSH) ✅
  - 3390-3396 (内网服务) ✅

watchdog: ✅ 运行中
```

### Termux 服务

```
SSH 守护进程：✅ 运行中 (端口 8022)
sv 服务脚本：✅ 已创建
SSH 配置：✅ 已配置
```

---

## 连接测试

### U22 → Termux

```bash
# ✅ 成功
ssh -p 8022 localhost "echo OK"
```

### U22 → gate (通过 Termux)

```bash
# ❌ 暂时失败 - databasei 公网连接不可用
ssh -p 8022 localhost "ssh gate 'echo OK'"
```

### U22 → gate (直接)

```bash
# ✅ 通过 U22 的 ssh-gate 服务
ssh CC "echo OK"
```

---

## 网络状况

| 连接 | 状态 | 说明 |
|------|------|------|
| U22 → Termux (8022) | ✅ | SSH 守护进程运行中 |
| U22 → gate (8822) | ⚠️ | 公网连接暂时不可用 |
| U22 → CC (通过 gate) | ✅ | 端口转发正常 |
| U22 → PVE (8006) | ✅ | 端口转发正常 |

---

## 使用方法

### 在 U22 中管理服务

```bash
# 查看状态
sv status

# 重启 ssh-gate
sv restart ssh-gate

# 查看日志
sv log ssh-gate 100
```

### 在 Termux 中管理服务

```bash
# 查看状态
ssh -p 8022 localhost "sv status"

# 启动服务
ssh -p 8022 localhost "bash ~/.local/sv/ssh-gate/run start"

# 直接 SSH 到 Termux 执行
ssh -p 8022 localhost
```

---

## 架构优势

| 特性 | U22 方案 | Termux 方案 |
|------|---------|------------|
| 网络权限 | ⚠️ 受限 | ✅ 完整 |
| /proc 访问 | ❌ 失败 | ✅ 正常 |
| 执行权限 | ✅ root | ⚠️ 应用沙盒 |
| 保活能力 | ⚠️ 依赖系统 | ✅ Tasker |
| 当前状态 | ✅ 运行中 | ✅ 就绪 |

---

## 下一步建议

### 如果 databasei 恢复连接

1. 在 Termux 中启动 ssh-gate：
```bash
ssh -p 8022 localhost "bash ~/.local/sv/ssh-gate/run start"
```

2. 验证 Termux 端口转发：
```bash
ssh -p 8022 localhost "timeout 2 bash -c 'echo > /dev/tcp/localhost/8045'"
```

3. 切换 U22 使用 Termux 转发（可选）

### 如果 databasei 持续不可用

- 继续使用 U22 的 ssh-gate 服务（当前运行正常）
- Termux 作为备用方案就绪

---

## 文件清单

### U22 文件

```
/root/
├── .local/sv/
│   ├── ssh-gate/
│   │   ├── run
│   │   ├── conf
│   │   └── log/current
│   └── watchdog/
│       └── run
├── bin/sv/
│   └── sv
└── air/qwq/0-System/
    ├── termux-architecture.md
    ├── termux-ssh-guide.md
    ├── termux-setup.sh
    ├── enable-termux-ssh.sh
    ├── sv-service-manager.md
    └── termux-ssh-config
```

### Termux 文件

```
~/.ssh/
├── config
├── id_ed25519_vi
├── id_ed25519_vi.pub
└── authorized_keys

~/.local/sv/
├── ssh-gate/
│   └── run
└── watchdog/
    └── run

~/bin/
└── sv

~/start-sshd.sh
```

---

## 快速参考

```bash
# U22 服务管理
sv status
sv start ssh-gate
sv restart ssh-gate

# Termux SSH 连接
ssh -p 8022 localhost

# Termux 服务管理（远程）
ssh -p 8022 localhost "sv status"
ssh -p 8022 localhost "bash ~/.local/sv/ssh-gate/run start"

# 端口转发验证
timeout 2 bash -c "echo > /dev/tcp/localhost/8045" && echo OK
```
