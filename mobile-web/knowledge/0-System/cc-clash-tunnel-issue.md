# CC Clash Tunnel 系统故障报告

**日期**: 2026-03-05  
**状态**: 🔴 严重 - 隧道无法启动

---

## 问题现象

- PM2 进程不断重启 (`cc-clash-tunnel`, `cc-clash-watchdog`)
- 日志显示 "隧道启动失败" 循环
- 几分钟内连续发生多次重启

---

## 根本原因

**容器权限限制** - 当前运行环境对网络命名空间的访问受限：

```
Cannot open netlink socket: Permission denied
cat: /proc/net/tcp: Permission denied
Error: /proc must be mounted
stdfd_devnull: open /dev/null: Function not implemented
```

### 具体限制

1. **无法访问 /proc 文件系统** - `ss`, `ps` 等命令失效
2. **无法创建 netlink socket** - 网络状态查询失败
3. **SSH -f 后台模式失败** - `/dev/null` 访问受限

### 为什么有时能工作几天

容器环境可能在以下情况变化：
- 容器重启后权限重置
- 宿主机安全策略变更
- 资源限制动态调整

---

## 已尝试的修复

### ✅ 已完成
1. 修复隧道脚本 - 移除 SSH `-f` 标志，改用 `&` 后台运行
2. 添加 `ClearAllForwardings=yes` 清除 SSH 配置冲突
3. 增强错误检测和日志记录
4. 添加端口占用预检查

### ❌ 无效
- SSH 端口转发仍然失败（容器权限限制）
- `ss`, `netstat`, `/proc/net/tcp` 均无法使用

---

## 建议解决方案

### 方案 1: 在 CC 服务器上运行代理（推荐）
在 CC 服务器直接运行 Clash 客户端，通过 HTTP 代理访问：
```bash
# CC 服务器上
clash -d /etc/clash &

# 本地通过 SSH 隧道转发 HTTP 代理
ssh -N -L 7891:localhost:7891 CC
```

### 方案 2: 使用用户态网络工具
尝试使用 `proxychains` 或 `gost` 等用户态代理工具

### 方案 3: 容器权限提升
在容器启动时添加 `--cap-add=NET_ADMIN` 参数

### 临时方案：手动 SSH 隧道
```bash
# 手动建立隧道（不使用 PM2）
ssh -N -D 7890 -L 7891:localhost:7891 CC &
export ALL_PROXY=socks5h://localhost:7890
```

---

## 当前状态

| 组件 | 状态 |
|------|------|
| cc-clash-tunnel | 🔴 停止 (启动失败) |
| cc-clash-watchdog | 🟡 运行中 (无法修复隧道) |
| SSH 连接 (CC) | ✅ 正常 |
| 端口转发 | 🔴 失败 (容器限制) |
| 代理可用性 | 🔴 不可用 |

---

## 下一步行动

1. [ ] 确认容器是否可以重新配置权限
2. [ ] 测试方案 1（CC 服务器本地运行 Clash）
3. [ ] 或考虑使用云代理服务替代
