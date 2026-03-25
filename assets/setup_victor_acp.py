#!/usr/bin/env python3
"""
Victor-CC ACP 身份配置脚本
创建 AID: victor-cc.agentid.pub
"""
import asyncio
import os
import json
from agentcp import AgentCP

async def main():
    # 配置
    agent_name = "victor-cc"
    seed_password = "victory2026"
    access_point = "agentid.pub"
    data_dir = "/home/vicki/air/mycc/data/acp"

    os.makedirs(data_dir, exist_ok=True)

    print(f"=== Victor-CC ACP 配置 ===")
    print(f"Agent Name: {agent_name}")
    print(f"Access Point: {access_point}")
    print(f"Data Dir: {data_dir}")
    print()

    # 创建 ACP 实例
    acp = AgentCP(
        agent_data_path=data_dir,
        seed_password=seed_password,
        debug=True
    )

    # 创建新身份 (参数顺序: ap, agent_name)
    print("正在创建 AID...")
    try:
        aid = acp.create_aid(access_point, agent_name)
        print(f"✅ AID 创建成功: {aid}")
    except Exception as e:
        print(f"❌ AID 创建失败: {e}")
        return

    # 保存配置
    config = {
        "aid": aid,
        "agent_name": agent_name,
        "seed_password": seed_password,
        "access_point": access_point,
        "data_dir": data_dir
    }

    config_file = "/home/vicki/air/mycc/data/acp/config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ 配置已保存到: {config_file}")
    print()
    print(f"=== Victor-CC ACP 身份 ===")
    print(f"AID: {aid}")
    print()
    print("现在可以通过 ACP 与其他 Agent 通信了！")

if __name__ == "__main__":
    asyncio.run(main())
