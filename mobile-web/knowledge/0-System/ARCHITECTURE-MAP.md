# AI Hub 全局架构共识

## 1. 中央集成仓库 (Primary)
- **Path**: /root/Obsidian/AIHub
- **Git**: git@github.com:vickioo/aiHub.git
- **Role**: 唯一权威知识归集地。

## 2. 智能体实验与备份 (Multi-Remote)
- **MyCC**: /home/vicki/air/mycc
  - **Origin**: git@github.com:vickioo/aiHub.git (私有备份/协同)
  - **Upstream**: git@github.com:Aster110/mycc.git (同步原版)
- **QWQ**: /home/vicki/air/qwq
  - **Origin**: git@github.com:vickioo/aiHub.git (千问专用分支/配置管理)
  - **Role**: 供应千问等第三方智能体的特殊扩展能力。
