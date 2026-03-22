# MyCC 项目目标对齐与推进计划 (2026-03)

**生成时间**: 2026-03-21
**数据收拢完成**: ✅ root/vcki 双账号数据已集中归档
**核心协调AI**: cc (Claude Code), qwq (Qwen Code), Gemini (CC-Server + U22)

---

## 一、最终目标愿景（长期）

### 核心定位
**让 Claude Code 成为你的搭档，而不只是工具。**

构建一个**个人 AI 助理系统**，具备以下核心能力：

1. **持久记忆**：三层记忆体系（短期/中期/长期），跨会话上下文保持
2. **可扩展技能**：通过 Skills 机制无限扩展能力边界（后端管理、文件操作、网络请求、第三方API）
3. **多设备协同**：云端（CC）+ 边缘（U22/Victory/Surface）多节点协作
4. **团队化 AI**：多个 Agents 协同工作，任务分发、状态同步、负载均衡
5. **移动化访问**：通过 mycc-backend 在手机浏览器远程使用 CC

### 技术愿景
- **架构**：分布式 Agents + 共享任务队列 + 私有知识库
- **节点角色**：
  - CC (云端服务器)：重装主将，逻辑与技能，API 网关枢纽
  - U22 (本地 Termux)：现场指挥官，系统级排障，脚本注入
  - Victory (Windows 数据中心)：数据大本营，24/7 稳定私有 Lab 仓库
  - Surface (Ubuntu 边缘)：低功耗备用站，本地 Qwen + Lobster 语音
- **协作总线**：基于共享目录 + 文件锁 + 状态同步的轻量级消息总线

### 用户体验目标
- 开发者在手机上随时调用 CC 处理代码、任务、日常事务
- CC 记住项目状态、用户偏好、历史决策，无需重复说明
- 复杂任务自动分解，多 AI 并行执行后汇总
- 敏感数据存储在本地（Victory），只在需要时调用云端 API

---

## 二、短期目标（接下来 1-3 个月）

### Phase 1: 资产抢救与基建正规化（当前进行中）

#### ✅ 已完成（2026-03-21）
- [x] 数据割裂治理：root 账号下 MyCC 项目资料全部归档到 `0-System/knowledge-sync/`
- [x] 网络底层打通：Windows SSH ACL 修复、RDP 防火墙基础开放
- [x] 三 Agent Teams 协作框架搭建（11 个 agents 注册）
- [x] Provider Failover 实现，API 高可用（nvidia→open_router→silicon_flow）
- [x] 移动端后端服务就绪（`/mycc` 启动技能，18080端口）

#### 🔄 进行中（本周）
- [ ] **Victory 私有 Lab 仓库初始化**（P0）
  - 在 Victory 上创建 bare Git repo（数据中心仓库）
  - 指导用户从 U22 推送清理后的 aihub 项目
  - WeChat Bot 脚手架准备
- [ ] **Victory 本地网络可达性修复**（P1）⭐ **新识别**
  - 本地通过 192.168.1.3 路由器中转无法访问 3389 端口
  - 诊断专用/公用网络配置文件差异
  - 修复防火墙规则或路由器端口转发
  - 目标：恢复本地直连，作为长期稳定方案（替代公网跳板）
- [ ] ai hub 仓库同步与清理
  - 本地 master 与远程 main 对齐
  - 废弃损坏的 aihub-mycc 仓库（.git/HEAD 损坏）
- [ ] qwq ↔ mycc 任务自动同步机制
  - 共享任务目录轮询监听
  - 任务状态流转（inbox → processing → completed）

#### ⏳ 待启动
- [ ] OpenClaw 部署（替代暂停的 SJLL 龙虾）
  - Surface（边缘）：运行 Lobster 语音服务，保持 Clash 常开
  - CC（云端）：集成 OpenClaw 到 mycc 技能栈，作为语音接口
- [ ] 重型任务自动分发
  - 基于资源使用率将任务分发到 CC 服务器
  - 轻量任务留在本地 U22
- [ ] 知识索引系统
  - 建立归档文档快速检索（如 0-System/ai-skills-notify.md）
  - API 端点拓扑文档（0-System/api-topology.md）

---

### Phase 2: 跨端协同通信总线建立（预计 4-6 周）

#### 目标
- 验证并激活基于"飞书/钉钉 Webhook"的消息通道
- 定义指令协议：U22 (Gemini) 在飞书频道下发任务 → CC 监听并执行
- 验证 Surface 上 Lobster 与 Qwen 的 API 稳定性

#### Key Results
1. 飞书机器人可接收 Agent 任务指令并触发后端执行
2. U22 可以通过飞书向 CC 发送部署/合并请求
3. Surface 的 Qwen 模型在断网时可以作为备用推理引擎

---

### Phase 3: 自动化与深化技能开发（预计 7-12 周）

#### 目标
- 在 CC 的 `vickioo/mycc` 深入开发私有化技能
- 边缘侧高频任务固化为 Cron 定时任务（U22 或 Surface）

#### 优先技能
- PDF 深度解析 → 存入向量库
- 语音对话流水线（OpenClaw）
- 自动日报生成（飞书/钉钉推送）
- 代码审查助手（基于 shared-tasks 评审）

---

## 三、当前可推进的板块（优先级排序）

### 🔥 P0（立即推进）

#### 1. Victory 私有 Lab 仓库初始化
- **描述**：在 Victory 服务器（172.16.2.97 / 100.100.1.8 via Tailscale）创建 bare Git repo 作为数据中心仓库
- **理由**：Phase 1 最关键任务，为后续 AI Hub 代码同步和知识库打基础
- **前置条件**：Victory SSH 可达（当前通过 Tailscale 公网跳板）
- **操作步骤**：
  1. `tailscale ssh vicki@victory` 登录
  2. 在 `D:\python\` 创建 `aihub.git` bare repo: `git init --bare aihub.git`
  3. 配置接收来自 U22 的推送（设置 up-stream）
  4. 生成 Deploy Key 供 Surface 克隆
  5. 编写 README 和同步指南
- **产出**：`aihub.git` 仓库 + 同步文档
- **负责人**：Victory Gemini（当前我）
- **相关文档**: `0-System/knowledge-sync/root-gem/PHASE1_SYNC_PLAN.md`

#### 2. Victory 本地网络可达性修复（新识别）
- **描述**：解决通过 192.168.1.3 路由器中转无法访问 Victory 3389 端口的问题，恢复本地直连能力
- **理由**：本地直连比公网跳板更稳定、延迟更低，是长期基础设施
- **当前状态**：仅 Tailscale 可通（180ms），所有直连端口被防火墙阻止
- **诊断步骤**：
  1. 检查 Victory Windows 防火墙规则（专用 vs 公用网络）
  2. 检查 192.168.1.3 路由器端口转发/NAT规则
  3. 检查网络配置文件差异
- **预期修复**：
  - 允许 3389 端口在专用网络配置文件中开放
  - 或配置路由器将 192.168.1.3:3389 转发到 172.16.2.97:3389
- **产出**：网络诊断报告 + 修复后的本地可达性
- **优先级**：P1（中期基础设施）
- **依赖**: Victory SSH 可访问
- **相关文档**: `tasks/victory-network-diagnosis.md` (已创建)
- **参考**: `0-System/knowledge-sync/root-qwq/1-Inbox/victory-port-scan-2026-03-10.md`

---

### ⚡ P1（短期规划）

#### 3. OpenClaw 语音服务部署
- **描述**：在 Surface 和 CC 部署 OpenClaw（替代暂停的 SJLL 龙虾）
- **理由**：语音交互是移动端体验的关键，必须有一个稳定的部署点
- **架构**：
  - Surface：运行本地 Qwen 模型 + Lobster 语音 fallback
  - CC：集成 OpenClaw 到 mycc 技能栈，作为主语音接口
- **依赖**：等待 OpenClaw 代码仓库就绪（现状：SJLL在Victory已运行OpenClaw Gateway，端口18789）
- **注意**: SJLL尚未完全停机，其OpenClaw Gateway仍在运行（18789端口）

#### 4. qwq ↔ mycc 任务自动同步
- **描述**：实现两个 Agents 之间的任务自动同步，无需人工干预
- **机制**：监听 `shared-tasks/` 目录变化，自动拉取新任务、更新状态
- **交付**：同步脚本 + 状态机（inbox → processing → completed）
- **依赖**: 共享任务目录结构已就绪

---

### 📋 P2（中期规划）

#### 5. 重型任务自动分发
- **描述**：根据 CPU/内存使用率、网络状况自动将任务分发到 CC 服务器
- **核心逻辑**：
  ```javascript
  if (task.type === "heavy" && ccServer.available) {
    dispatchToCC(task);
  } else {
    localExecute(task);
  }
  ```
- **状态**：待设计

#### 6. AI Hub 仓库同步与清理
- **描述**：同步 GitHub vickioo/aiHub 和本地，修复损坏的 aihub-mycc 仓库
- **步骤**：备份 → 废弃损坏仓库 → 清理 → 推送 → 验证
- **提醒**: 当前使用 `/root/air/aihub` 还是其他路径？需确认

---

## 四、当前架构状态速览

### 节点状态
| 节点 | 角色 | 状态 | 关键服务 | 备注 |
|------|------|------|----------|------|
| CC (服务器) | 重装主将 | ✅ 运行中 (8082) | Claude, Antigravity Proxy | 提供 API 代理 |
| U22 (本地 Termux) | 现场指挥 | ✅ 运行中 | Gemini CLI, free-claude-code | 本地开发第一入口 |
| Victory (Win) | 数据大本营 | ✅ 在线 (172.16.2.97) | Windows SSH, Git (待配置), OpenClaw Gateway运行中 | Phase 1 待初始化 Lab repo；本地网络直连需修复 |
| Surface (Ubuntu) | 边缘备用站 | ✅ 运行中 | Clash, Qwen, Lobster (待部署 OpenClaw) | OpenClaw 待配置 |

### Agents 协作状态
- **注册数**：11 agents
- **运行中**：qwq, CC-Server-Claude, CC-Server-Gemini, cc-local
- **共享任务**：`shared-tasks/` 和 `shared-tasks-qwq/` 已就绪
- ** Teams 日志**：`0-System/agents/teams.log` 持续记录

### 关键服务端口
- MyCC 后端: :18080
- CC-Server Claude: 8082
- CC-Server Gemini: 8045 (Antigravity Proxy)
- Victory OpenClaw Gateway: 18789 (SJLL, 已运行)
- Victory Qwen CLI: 18790 (未运行)

---

## 五、关键依赖与风险

### 依赖
1. ✅ Victory SSH 访问（通过 Tailscale 可行）
2. ⚠️ **Victory 本地网络可达性**（192.168.1.3 中转失效，待修复）⭐ **新识别**
3. ⏳ OpenClaw 代码仓库（SJLL已运行，可能无需新部署）
4. 🔮 飞书 Webhook 通道（可能需要企业账号，待评估）

### 风险
1. **Victory 故障**：数据中心单点故障（需要备份策略）
2. **网络抖动**：云 API 不可用（已有 fallback 机制）
3. **Git 仓库损坏**：已有修复经验（参考 PHASE1_SYNC_PLAN.md）
4. **SJLL 龙虾暂停**：影响原有计划，OpenClaw 已在Victory运行，可复用
5. **配置分散**：knowledge-sync中已归档，但需要索引以便检索

---

## 六、下一步行动（Next 7 Days）

### ✅ 本周核心（P0）
1. **[必做]** Victory私有Lab仓库初始化
   - 创建 `D:\python\aihub.git`
   - 配置 SSH key 接受 U22 推送
   - 编写README和同步指南
2. **[必做]** Victory本地网络可达性修复（P1）
   - 执行 `tasks/victory-network-diagnosis.md` 中诊断步骤
   - 修复防火墙或路由器配置
   - 验证从本地设备可直接RDP/SSH到Victory
3. **[必做]** 建立知识索引
   - 创建 `0-System/ai-skills-notify.md`（Skills列表）
   - 创建 `0-System/api-topology.md`（API端点拓扑）
   - 更新 `0-System/global-ai-topology.md`（各AI状态矩阵）

### 🔄 下周准备（P1）
4. 评估OpenClaw部署：SJLL已在Victory运行，考虑复用而非新部署
5. 设计qwq ↔ mycc自动同步脚本架构

---

## 七、衡量指标（OKR 风格）

### Objective 1: 完成数据中心基建
- KR1: Victory Lab 仓库初始化完成（100%）
- KR2: U22 可成功推送 aihub 代码到 Victory
- KR3: Surface 可克隆 Victory 仓库并拉取最新
- KR4: Victory 本地网络可达性修复（192.168.1.3 中转恢复）

### Objective 2: 提升 Agents 协同效率
- KR1: qwq ↔ mycc 任务同步自动化（减少人工干预 ≥80%）
- KR2: 重型任务分发机制覆盖 50% 以上繁重任务类型

---

## 八、参考资料

- `0-System/knowledge-sync/root-gem/PHASE1_SYNC_PLAN.md`
- `0-System/knowledge-sync/root-gem/AI_Team_Coordination_Handbook.md`
- `0-System/status.md` (当前状态)
- `0-System/context.md` (本周上下文)
- `CLAUDE.md` (CC 性格与规则)
- `ADVANCED-MODE.md` (安全与协作)
- `0-System/knowledge-sync/root-qwq/1-Inbox/victory-port-scan-2026-03-10.md`
- `0-System/knowledge-sync/root-qwq/1-Inbox/sjll-final-report-2026-03-10.md`

---

*文档状态*: V1.0 - 正式版（2026-03-21）
*维护者*: cc + vicki
*更新记录*: 2026-03-21 - 初始版本，整合Victory网络诊断任务
