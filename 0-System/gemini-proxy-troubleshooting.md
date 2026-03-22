# Gemini 代理故障诊断

**时间**: 2026-03-06 18:32  
**状态**: 🔴 需要协助

## 问题描述

Termux Clash 隧道已启动，但无法通过代理访问外网。

## 当前状态

### ✅ 正常

1. **U22 → gate**: SSH 连接正常
2. **Termux → gate**: SSH 连接正常  
3. **gate → CC**: SSH 跳转正常
4. **CC Clash**: 进程运行中 (PID: 4095557)
5. **Termux 隧道**: 已启动 (PID: 5484)

### ❌ 失败

1. **Termux curl 测试**: `curl --socks5 localhost:7891 https://api.ip.sb/ip` 超时
2. **U22 访问**: 无法访问 Termux 的 7891 端口

## 可能原因

1. **Clash 端口不匹配**
   - Termux 隧道连接 CC 的 7890 端口
   - 但 CC Clash 可能监听其他端口

2. **防火墙/路由问题**
   - CC 服务器可能阻止了来自 gate 的连接

3. **Clash 配置问题**
   - SOCKS5 代理可能未启用

## 需要 mycc 协助

请检查 CC 服务器 Clash 配置：

```bash
# 在 CC 服务器上执行
ssh CC "
  # 检查 Clash 监听端口
  netstat -tlnp | grep clash | grep -v grep
  
  # 或检查配置文件
  cat /opt/clash-for-linux/temp/config.yaml | grep -E 'port|socks-port' | head -5
  
  # 测试本地代理
  curl -s --socks5-hostname localhost:7890 https://api.ip.sb/ip
"
```

## 下一步

1. mycc 检查 CC 服务器 Clash 配置
2. 确认正确的 SOCKS5 端口
3. 更新 Termux 隧道配置
4. 测试完整链路
5. 测试 Gemini CLI

## 相关文件

- `shared-tasks/processing/gemini-proxy-status.md` - 状态文档
- `shared-tasks-qwq/processing/gemini-proxy-test.json` - 任务文件

## 最新诊断 (18:35)

### 问题根因

**Termux SSH 隧道端口绑定问题**

- SSH 隧道进程存在 (PID: 5484, 21745)
- 但本地 7891 端口无法连接 (`Connection refused`)
- 可能原因：IPv6/IPv4 绑定问题

### CC 服务器 Clash 状态 ✅

```
port: 7890 (HTTP)
socks-port: 7891 (SOCKS5)
监听：127.0.0.1:7891
```

### 需要排查

1. Termux SSH 隧道绑定到 IPv6 (::1) 但 curl 尝试 IPv4 (127.0.0.1)
2. 或者 SSH 隧道进程僵死

### 解决方案

在 Termux 中执行：
```bash
# 重启隧道，指定 IPv4
pkill -f 'ssh.*-D 7891'
nohup ssh -N -4 -D 127.0.0.1:7891 gate &
```

### 不需要 nginx

SSH 隧道已经提供 SOCKS5 代理，nginx 用于 HTTP 反向代理场景。
