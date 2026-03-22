# CC 服务器 AI Hub 服务状态报告

**生成时间**: 2026-03-09 12:30  
**执行者**: qwq (Qwen Code)

---

## ✅ 服务状态

### AI Hub (mobile-web)

| 项目 | 状态 | 说明 |
|------|------|------|
| **服务进程** | ✅ 运行中 | PID: 3719583 |
| **监听端口** | ✅ 8790 | `0.0.0.0:8790` |
| **SSH 隧道** | ✅ 运行中 | 8790 → 9090 (远程) |
| **Web 访问** | ✅ 正常 | HTTP 200 |
| **API 认证** | ✅ 正常 | Token 验证通过 |

### 访问方式

#### 本地访问 (CC 服务器)
```bash
http://localhost:8790/
```

#### 远程访问 (通过 SSH 隧道)
```bash
# 隧道已建立：localhost:8790 → databasei:9090
# 在远程服务器上访问 http://localhost:9090
```

#### 认证 Token
```
ceecee-super-team-8822
```

---

## 📁 文件位置

```
/root/air/qwq/mobile-web/
├── app.py                      # FastAPI 后端
├── hub.html                    # 主页面
├── intranet-hub.html           # 内网集成主页
├── INTRANET-HUB-RELEASE.md     # 发布说明
└── INTRANET-HUB-GUIDE.md       # 使用指南
```

---

## 🔧 服务配置

### 启动命令
```bash
cd /root/air/qwq/mobile-web
python3 app.py
```

### 依赖
- Python 3
- FastAPI
- Uvicorn
- Httpx
- Pydantic

### 环境变量
- `ONE_API_URL`: `http://127.0.0.1:3000/v1/chat/completions`
- `AI_TEAM_TOKEN`: `ceecee-super-team-8822`

---

## 📊 网络状态

### 本地监听
```
0.0.0.0:8790  - AI Hub 服务
```

### SSH 隧道
```bash
# 主隧道 (活跃)
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -N -R 9090:localhost:8790 vicki@113.57.105.174 -p 8822

# 备用隧道 (watchdog)
while true; do ssh -o ServerAliveInterval=30 -N -R 9090:localhost:8790 databasei; sleep 10; done
```

### 相关端口
| 端口 | 服务 | 状态 |
|------|------|------|
| 8790 | AI Hub | ✅ 监听 |
| 9090 | Clash 代理 | ✅ 监听 (隧道目标) |
| 8769 | 原 mobile-web 端口 | ⚠️ 已弃用 |
| 3000 | One-API | ✅ 运行中 |
| 8045 | Antigravity | ✅ 运行中 |

---

## 🎯 功能特性

### AI Hub 提供

1. **统一入口** - 所有 AI 服务的访问门户
2. **身份认证** - Token 验证机制
3. **API 网关** - 集成 One-API 推理服务
4. **系统监控** - 实时系统状态显示
5. **内网集成** - 侧边滑动导航菜单

### 集成服务

| 服务 | 状态 | 端口 |
|------|------|------|
| Qwen Code | ✅ | - |
| free-claude-code | ✅ | 8082 |
| Docsify 知识库 | ✅ | 8772 |
| CC Clash 隧道 | ✅ | 7890 |
| Antigravity | ✅ | 8045 |
| One-API | ✅ | 3000 |

---

## 🔍 故障排查

### 服务无法访问？

```bash
# 1. 检查进程
pgrep -f 'python3.*app.py'

# 2. 检查端口
ss -tlnp | grep 8790

# 3. 测试服务
curl http://localhost:8790/

# 4. 查看日志
cat /tmp/hub.log
```

### SSH 隧道断开？

```bash
# 手动重建隧道
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
    -N -R 9090:localhost:8790 vicki@113.57.105.174 -p 8822
```

### 依赖缺失？

```bash
pip3 install httpx fastapi uvicorn
```

---

## 📋 下一步建议

1. **PM2 托管** - 将 AI Hub 加入 PM2 进程管理
2. **开机自启** - 创建 systemd 服务
3. **日志轮转** - 配置日志管理
4. **监控告警** - 服务异常通知
5. **HTTPS 支持** - 添加 SSL 证书

---

## ✅ 验证清单

- [x] AI Hub 进程运行
- [x] 端口 8790 监听
- [x] SSH 隧道建立
- [x] Web 页面可访问
- [x] API 认证正常
- [x] 系统状态 API 可用

---

*报告生成：2026-03-09 12:30*  
*服务状态：✅ 正常运行*
