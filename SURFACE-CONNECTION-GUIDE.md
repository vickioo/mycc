# Surface 主机连接指南

**更新日期**: 2026-03-14

---

## 🌐 当前状态

### 服务器端
- ✅ AIHub Web 服务运行中 (端口 8766)
- ✅ 授权码：`ceecee-super-team-8822`
- ⚠️ Tailscale 无法在容器中运行

### 访问方式

| 方式 | 可行性 | 说明 |
|------|--------|------|
| **Tailscale** | ❌ | 容器环境不支持 |
| **SSH 隧道** | ✅ | 推荐方式 |
| **局域网直连** | ✅ | 同一网络下 |
| **公网 IP** | ⚠️ | 需配置端口转发 |

---

## 🔧 方案 1: SSH 隧道 (推荐)

### 在 Surface 上操作

#### 1. 安装 OpenSSH 客户端
```powershell
# Windows PowerShell (管理员)
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

#### 2. 建立 SSH 隧道
```powershell
# 连接到服务器并创建隧道
ssh -L 8766:localhost:8766 -L 8082:localhost:8082 root@服务器 IP

# 输入密码后即可
```

#### 3. 在浏览器访问
```
http://localhost:8766/
```

#### 4. 输入授权码
```
ceecee-super-team-8822
```

---

## 🌐 方案 2: 局域网直连

### 前提条件
- Surface 和服务器在同一局域网
- 或服务器有公网 IP

### 步骤

#### 1. 获取服务器 IP
在服务器上执行：
```bash
hostname -I
# 或
ip addr show
```

#### 2. 在 Surface 浏览器访问
```
http://服务器 IP:8766/
```

#### 3. 输入授权码
```
ceecee-super-team-8822
```

---

## 🔐 方案 3: Tailscale (需在 Surface 安装)

### 在 Surface 上安装 Tailscale

#### 1. 下载安装
访问：https://tailscale.com/download

选择 Windows 版本下载并安装

#### 2. 登录授权
```
1. 打开 Tailscale
2. 登录你的账号
3. 记住 Surface 的 Tailscale IP (如 100.x.y.z)
```

### 在服务器上安装 Tailscale

**注意**: 当前容器环境不支持 Tailscale

**替代方案**:
- 在宿主机安装 Tailscale
- 配置端口转发到容器

```bash
# 在宿主机执行
tailscale up --advertise-exit-node

# 配置端口转发
iptables -t nat -A PREROUTING -i tailscale0 -p tcp --dport 8766 -j DNAT --to-destination 容器 IP:8766
```

### 访问方式
```
http://服务器 Tailscale IP:8766/
```

---

## 📱 授权码说明

当前 Web 服务需要授权码访问：

| 项目 | 值 |
|------|-----|
| **授权码** | `ceecee-super-team-8822` |
| **有效期** | 30 天 |
| **Cookie 名称** | `ai_hub_session` |

---

## 🔍 故障排查

### 问题 1: 无法连接
```
检查 SSH 服务是否正常
ssh root@服务器 IP
```

### 问题 2: 页面空白
```
检查服务是否运行
curl http://localhost:8766/
```

### 问题 3: 授权失败
```
清除浏览器 Cookie
重新输入授权码：ceecee-super-team-8822
```

---

## 📋 快速连接命令

### Surface PowerShell
```powershell
# SSH 隧道连接
ssh -L 8766:localhost:8766 root@服务器 IP

# 然后浏览器访问 http://localhost:8766/
# 授权码：ceecee-super-team-8822
```

---

*Last updated: 2026-03-14*
