/**
 * Agent Resolver - 解析和管理 Agent 目录
 * 用于 Agent Teams 功能
 */

import { join } from "path";
import { readdirSync, statSync } from "fs";

/**
 * 根据 agentId 解析 Agent 目录
 */
export function resolveAgentDir(agentId: string, agentsBaseDir: string): string | null {
  const agentDir = join(agentsBaseDir, agentId);
  try {
    if (statSync(agentDir).isDirectory()) {
      return agentDir;
    }
  } catch {
    // 目录不存在
  }
  return null;
}

/**
 * 列出所有可用的 Agent
 */
export function listAgents(agentsBaseDir: string): string[] {
  try {
    const entries = readdirSync(agentsBaseDir);
    return entries.filter(entry => {
      try {
        return statSync(join(agentsBaseDir, entry)).isDirectory();
      } catch {
        return false;
      }
    });
  } catch {
    return [];
  }
}