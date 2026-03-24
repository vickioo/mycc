/**
 * 配置管理
 */

import { existsSync, readFileSync, unlinkSync, readdirSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import type { DeviceConfig } from "./types.js";
import { getRoot } from "./platform.js";

/**
 * 获取配置目录（统一逻辑）
 * 优先级：MYCC_SKILL_DIR > cwd/.claude/skills/mycc > cwd/../.claude/skills/mycc > ~/.mycc/
 *
 * 支持两种目录布局：
 * 1. cwd 是项目根目录：cwd/.claude/skills/mycc/current.json
 * 2. cwd 是 scripts/ 子目录：cwd/../.claude/skills/mycc/current.json
 */
export function getConfigDir(cwd: string): string {
  const envSkillDir = process.env.MYCC_SKILL_DIR;
  const homeDir = join(homedir(), ".mycc");
  const homeConfigPath = join(homeDir, "current.json");

  if (envSkillDir && existsSync(envSkillDir)) {
    return envSkillDir;
  }

  // 优先检查 cwd/.claude/skills/mycc（cwd 是项目根目录的情况）
  const cwdSkillDir = join(cwd, ".claude", "skills", "mycc");
  const cwdConfigPath = join(cwdSkillDir, "current.json");
  if (existsSync(cwdConfigPath)) {
    return cwdSkillDir;
  }

  // 检查 cwd/../.claude/skills/mycc（cwd 是 scripts/ 等子目录的情况）
  const parentSkillDir = join(cwd, "..", ".claude", "skills", "mycc");
  const parentConfigPath = join(parentSkillDir, "current.json");
  if (existsSync(parentConfigPath)) {
    return parentSkillDir;
  }

  if (existsSync(homeConfigPath)) {
    return homeDir;
  }

  // 两者都没有时，用 cwdSkillDir（persistPairToken 会自动创建目录）
  return cwdSkillDir;
}

/**
 * 加载设备配置（从 current.json）
 */
export function loadConfig(cwd: string): DeviceConfig | null {
  const configPath = join(getConfigDir(cwd), "current.json");
  try {
    if (existsSync(configPath)) {
      const content = readFileSync(configPath, "utf-8");
      const data = JSON.parse(content);
      // 只要有 deviceId 和 pairCode 就算有效配置
      if (data.deviceId && data.pairCode) {
        return data as DeviceConfig;
      }
    }
  } catch (err) {
    console.error("警告: 读取配置文件失败，将创建新配置");
  }
  return null;
}

/**
 * 删除设备配置（用于 --reset）
 */
export function deleteConfig(cwd: string): void {
  const configPath = join(getConfigDir(cwd), "current.json");
  try {
    if (existsSync(configPath)) {
      unlinkSync(configPath);
      console.log("已删除旧配置，将重新生成");
    }
  } catch {
    // 忽略
  }
}

/**
 * 自动查找项目根目录
 * 从当前目录向上查找，直到找到包含 .claude/ 或 claude.md (不区分大小写) 的目录
 *
 * 跳过 skill 内部的 .claude：即 .claude 位于 skills/ 目录下的情况（skill 自己的配置目录）
 */
export function findProjectRoot(startDir: string): string | null {
  let current = startDir;
  const root = getRoot(startDir);

  while (current !== root) {
    // 检查是否包含 .claude 目录
    if (existsSync(join(current, ".claude"))) {
      // 如果当前目录本身就是 skills/ 的子目录，跳过（这是 skill 自己的 .claude）
      const parent = join(current, "..");
      const parentName = parent.split("/").pop() || "";
      if (parentName === "skills") {
        current = parent;
        continue;
      }
      return current;
    }

    // 检查是否包含 claude.md（不区分大小写）
    try {
      const files = readdirSync(current);
      const hasClaudeMd = files.some(f => f.toLowerCase() === "claude.md");
      if (hasClaudeMd) {
        return current;
      }
    } catch {
      // 读取目录失败，跳过
    }

    // 向上一级
    const parent = join(current, "..");
    if (parent === current) break;
    current = parent;
  }

  return null;
}
