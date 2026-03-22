# 全局系统检查报告

**日期**: 2026-03-07 09:50  
**检查范围**: 全系统组件  
**状态**: ⚠️ 发现关键问题

---

## 📊 检查结果汇总

| 类别 | 检查项 | 状态 | 说明 |
|------|--------|------|------|
| **服务** | 知识库 (8772) | ✅ | 正常运行 |
| **服务** | free-claude-code (8083) | ✅ | 正常运行 |
| **服务** | CC SSH | ✅ | 连接正常 |
| **服务** | CC Clash Watchdog | ✅ | 运行 60m |
| **服务** | CC Clash Tunnel | ⚠️ | PM2 waiting 状态 (重启 168 次) |
| **服务** | mycc 后端 (8082) | ❌ | 未运行 |
| **服务** | U22 sv 服务 | ❌ | ssh-gate 和 watchdog 都未运行 |
| **资源** | 磁盘空间 | ⚠️ | 93% 使用 (37G 可用) |
| **资源** | 内存 | ✅ | 可用 5.8G |
| **资源** | Swap | ⚠️ | 使用 5.9G/15G |
| **数据** | Git 仓库 | ✅ | 存在 |
| **数据** | 知识库 | ✅ | 120+ 文档 |
| **数据** | 日记系统 | ✅ | 正常运行 |

---

## 🔴 关键问题

### 1. U22 sv 服务未运行

**影响**: 
- 无法通过 SSH 隧道访问内网服务
- 无法连接 database.local、sj-liuliang.local 等

**原因**: 
- 可能是容器重启后服务未自启动

**修复**:
```bash
/root/bin/sv/sv start ssh-gate
/root/bin/sv/sv start watchdog
```

---

### 2. 磁盘空间紧张 (93%)

**影响**:
- 系统可能无法写入新数据
- 服务可能崩溃

**修复**:
```bash
# 清理 PM2 日志
pm2 flush

# 清理临时文件
rm -rf /tmp/*.log /tmp/*-pm2*.log

# 清理旧的内核 (如果有)
# apt autoremove --purge

# 检查大文件
du -ah /root | sort -rh | head -20
```

---

### 3. CC Clash Tunnel 异常

**影响**:
- 外网访问可能受限
- Gemini 代理可能不可用

**状态**: PM2 重启 168 次，watchdog 正常运行

**修复**:
```bash
# 手动测试隧道
ssh -L 7890:localhost:7890 CC "echo OK"

# 重启隧道
pm2 restart cc-clash-tunnel

# 查看日志
pm2 logs cc-clash-tunnel --lines 50
```

---

### 4. mycc 后端未运行

**影响**:
- 本地 Claude Code 无法使用

**修复**:
```bash
cd /root/air/mycc
./start-mycc.sh
```

---

## 🟡 潜在风险

### 1. Swap 使用过高 (5.9G/15G)

**原因**: 内存压力大

**建议**:
- 监控内存使用
- 考虑关闭不必要的服务

### 2. 服务自启动缺失

**问题**: U22 容器重启后服务不会自动恢复

**建议**:
- 添加开机自启动脚本
- 使用 PM2 管理所有服务

---

## ✅ 正常运行

| 服务 | 端口 | 状态 |
|------|------|------|
| 知识库网页版 | 8772 | ✅ |
| free-claude-code | 8083 | ✅ |
| CC Clash Watchdog | - | ✅ (60m) |
| CC SSH | - | ✅ |
| Git 版本控制 | - | ✅ |
| 日记系统 | - | ✅ |

---

## 📋 修复优先级

### P0 - 立即修复
1. [ ] 启动 U22 sv 服务
2. [ ] 清理磁盘空间

### P1 - 今天完成
3. [ ] 修复 CC Clash Tunnel
4. [ ] 启动 mycc 后端

### P2 - 本周完成
5. [ ] 配置服务自启动
6. [ ] 优化内存使用
7. [ ] 建立监控告警

---

## 🔧 一键修复脚本

```bash
#!/bin/bash
# 系统修复脚本

echo "=== 修复 U22 sv 服务 ==="
/root/bin/sv/sv start ssh-gate
/root/bin/sv/sv start watchdog

echo "=== 清理磁盘空间 ==="
pm2 flush
rm -rf /tmp/*.log /tmp/*-pm2*.log 2>/dev/null

echo "=== 重启 CC Clash Tunnel ==="
pm2 restart cc-clash-tunnel

echo "=== 检查服务状态 ==="
sleep 3
/root/bin/sv/sv status
pm2 status
curl -s http://localhost:8772/api/health
curl -s http://localhost:8083/

echo "=== 修复完成 ==="
```

---

*报告生成：2026-03-07 09:50*  
*下次检查：2026-03-07 15:00*
