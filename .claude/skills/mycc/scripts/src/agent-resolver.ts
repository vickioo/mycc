import { readdirSync, statSync } from "fs";
import { join } from "path";

export interface Agent {
  id: string;
  name: string;
  path: string;
}

export function resolveAgentDir(agentId: string, agentsDir: string): string | null {
  try {
    const entries = readdirSync(agentsDir);
    for (const entry of entries) {
      const fullPath = join(agentsDir, entry);
      const stat = statSync(fullPath);
      if (stat.isDirectory() && entry === agentId) {
        return fullPath;
      }
    }
  } catch {
    // ignore
  }
  return null;
}

export function listAgents(agentsDir: string): Agent[] {
  try {
    const entries = readdirSync(agentsDir);
    return entries
      .map((entry) => {
        const fullPath = join(agentsDir, entry);
        try {
          if (statSync(fullPath).isDirectory()) {
            return { id: entry, name: entry, path: fullPath };
          }
        } catch {
          // ignore
        }
        return null;
      })
      .filter((a): a is Agent => a !== null);
  } catch {
    return [];
  }
}
