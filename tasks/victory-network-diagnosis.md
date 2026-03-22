# Victory本地网络可达性诊断与修复

**优先级**: P1 (中期关键基础设施)
**状态**: pending
**依赖**: Victory可达性确认 (当前通过Tailscale公网跳板)

---

## 📋 问题描述

Victory服务器（172.16.2.97）在本地多路由器局域网隔离环境中**无法通过192.168.1.3路由器中转访问RDP 3389端口**。

- ✅ **历史状态**: 以前可以正常跨路由器访问
- ❌ **当前状态**: 直连被防火墙阻止
- 🔄 **临时方案**: 通过公网跳板访问（配置文件: victory-SJLL）
- 🎯 **目标**: 恢复本地直接访问能力（192.168.1.3 → Victory:3389）

---

## 🔍 背景信息

### 网络拓扑
```
本地网络:
  192.168.1.3 (路由器A) ──中转──> Victory (172.16.2.97:3389)
  192.168.100.x (CC/其他设备) ──内网──> Victory

当前可连通路径:
  U22/Surface ──Tailscale──> Victory (100.100.1.8) 延迟180ms
```

### 历史诊断记录
见 `0-System/knowledge-sync/root-qwq/1-Inbox/victory-port-scan-2026-03-10.md`:
- Tailscale Ping: ✅ 在线 (180ms via DERP hkg)
- ICMP Ping: ❌ 100% 丢包
- 所有端口(22,80,443,3000,3389等): ❌ 关闭/被阻止
- **结论**: 防火墙阻止了所有直连端口

---

## 🎯 任务目标

1. **诊断根本原因**: 确定为什么192.168.1.3中转失效
2. **修复配置**: 调整防火墙/网络设置，恢复本地直连
3. **验证连通**: 从本地设备成功RDP/SSH到Victory
4. **文档更新**: 在PHASE1_SYNC_PLAN.md中记录网络配置

---

## 📝 详细步骤

### 步骤1: 检查Victory Windows防火墙配置

**通过Tailscale SSH登录Victory**:
```bash
tailscale ssh vicki@victory  # 或使用公网跳板
```

**检查入站规则**:
```powershell
# 查看RDP相关规则
Get-NetFirewallRule -DisplayName "*RDP*" | Format-Table -AutoSize

# 检查3389端口规则
Get-NetFirewallRule -Direction Inbound -LocalPort 3389 | Format-Table

# 查看当前网络配置文件
Get-NetConnectionProfile
```

**可能的修复**:
```powershell
# 允许RDP在所有网络配置文件
Set-NetFirewallRule -Name "RemoteDesktop-UserMode-In-TCP" -Enabled True

# 或创建新规则允许特定子网
New-NetFirewallRule -DisplayName "Allow LAN RDP" -Direction Inbound `
  -LocalPort 3389 -Protocol TCP -Action Allow `
  -RemoteAddress 192.168.1.0/24,192.168.100.0/24
```

---

### 步骤2: 检查本地路由器中转配置

**登录192.168.1.3路由器管理界面**:

**检查项目**:
- 端口转发规则: 是否有将外部端口3389转发到Victory的172.16.2.97:3389?
- 防火墙/NAT规则: 是否允许来自内网的流量转发?
- VLAN/接口配置: 192.168.1.x和172.16.2.x网段之间是否有隔离?
- DMZ设置: Victory是否在DMZ中?

**常见问题**:
- 路由器固件更新重置了端口转发规则
- ISP/上游设备修改了策略
- 误启用了AP隔离（Client Isolation）

---

### 步骤3: 网络配置文件差异检查

**Victory上检查网络位置**:
```powershell
# 查看当前网络配置文件（专用/公用）
Get-NetConnectionProfile

# 检查网络类别设置
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction
```

**典型差异**:
| 配置文件 | 入站默认 | 文件共享 | RDP |
|----------|----------|----------|-----|
| 专用网络 | 允许 | ✅ | ✅ |
| 公用网络 | 阻止 | ❌ | ❌ |

**修复**: 将网络配置文件设为"专用"或调整公用网络防火墙为允许。

---

### 步骤4: 本地探测验证

**从Surface/U22/CC进行探测**:

```bash
# 测试3389端口连通性 (需要telnet或nc)
telnet 192.168.1.3 3389  # 如果192.168.1.3是路由器，应该是telnet到路由器

# 或尝试直接连接Victory
nmap -p 3389 172.16.2.97

# 检查路由路径
traceroute 172.16.2.97
```

---

### 步骤5: 验证与收尾

**验收条件**:
- [ ] 从本地至少一个设备（U22/Surface）可直接RDP到Victory
- [ ] `telnet 172.16.2.97 3389` 成功连接
- [ ] Tailscale SSH 作为备用方案仍然可用
- [ ] 文档更新: PHASE1_SYNC_PLAN.md 中补充网络配置说明

---

## ⚠️ 风险与注意事项

- 修改防火墙规则可能暂时中断现有连接（如Tailscale）
- 路由器配置不当可能导致整个网络不可用
- 优先使用最小权限原则，仅允许可信子网访问
- 记录所有配置变更，便于回滚

---

## 📊 关联文档

- `0-System/knowledge-sync/root-qwq/1-Inbox/victory-port-scan-2026-03-10.md`
- `0-System/knowledge-sync/root-gem/PHASE1_SYNC_PLAN.md`
- `0-System/knowledge-sync/root-gem/fix_victory_ssh.ps1`
- `0-System/knowledge-sync/root-gem/check_victory.ps1`

---

*创建时间: 2026-03-21*
*创建者: cc (Claude Code)*
