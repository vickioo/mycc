// Agent Resolver Stub
import { join } from "path";

export async function resolveAgentDir(): Promise<string> {
  return process.env.AGENT_DIR || join(process.cwd(), "agents");
}

export async function listAgents(): Promise<string[]> {
  return ["default"];
}
