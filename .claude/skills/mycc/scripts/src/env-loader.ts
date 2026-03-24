/**
 * .env 文件加载 + PUBLIC_URL 检测
 *
 * 公网直连模式的核心：
 * - 读取 .env 文件中的 PUBLIC_URL
 * - 有 PUBLIC_URL → 公网模式（跳过 Tunnel）
 * - 没有 → 内网模式（启动 cloudflared）
 */

import { existsSync, readFileSync, watch } from "fs";
import { join, dirname } from "path";

/**
 * 解析 .env 文件内容为 key-value 对
 *
 * 支持：
 * - 注释行（# 开头）
 * - 空行
 * - 值的双引号 / 单引号
 * - 值中包含等号
 */
export function parseEnvFile(content: string): Record<string, string> {
  const env: Record<string, string> = {};

  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const eqIdx = trimmed.indexOf("=");
    if (eqIdx === -1) continue;

    const key = trimmed.slice(0, eqIdx).trim();
    const value = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, "");
    env[key] = value;
  }

  return env;
}

/**
 * 加载 PUBLIC_URL
 *
 * 优先级：
 *   1. process.env.PUBLIC_URL（环境变量直接传入）
 *   2. searchDirs 中的 .env 文件（按顺序查找，第一个找到即返回）
 *
 * 验证：
 *   - 必须 https:// 开头
 *   - 去除尾部斜杠
 *
 * @param searchDirs 搜索目录列表（按优先级排列）
 * @returns PUBLIC_URL 或 null
 */
export function loadPublicUrl(...searchDirs: string[]): string | null {
  // 环境变量优先
  if (process.env.PUBLIC_URL) {
    return validateUrl(process.env.PUBLIC_URL);
  }

  // 搜索 .env 文件
  for (const dir of searchDirs) {
    const envPath = join(dir, ".env");
    if (!existsSync(envPath)) continue;

    try {
      const content = readFileSync(envPath, "utf-8");
      const parsed = parseEnvFile(content);
      if (parsed.PUBLIC_URL) {
        return validateUrl(parsed.PUBLIC_URL);
      }
    } catch {
      // 读取失败，跳过
    }
  }

  return null;
}

/**
 * 加载 .env 文件到 process.env
 *
 * 优先级：
 *   1. searchDirs 中的 .env 文件（按顺序查找，第一个找到即加载）
 *   2. 不覆盖已存在的 process.env 变量（除非 overwrite=true）
 *
 * @param overwrite 是否覆盖已存在的环境变量（用于热重载）
 * @param searchDirs 搜索目录列表（按优先级排列）
 */
export function loadEnvFile(overwrite = false, ...searchDirs: string[]): void {
  for (const dir of searchDirs) {
    const envPath = join(dir, ".env");
    if (!existsSync(envPath)) continue;

    try {
      const content = readFileSync(envPath, "utf-8");
      const parsed = parseEnvFile(content);

      // 将解析的环境变量设置到 process.env
      for (const [key, value] of Object.entries(parsed)) {
        if (overwrite || process.env[key] === undefined) {
          process.env[key] = value;
        }
      }
    } catch {
      // 读取失败，跳过
    }
  }
}

/**
 * 监听 .env 文件变化，变化时触发回调
 *
 * @param callback 变化时的回调（传入被修改的 env 键列表）
 * @param searchDirs 搜索目录列表
 * @returns 停止监听的函数
 */
export function watchEnvFile(
  callback: (changedKeys: string[]) => void,
  ...searchDirs: string[]
): () => void {
  const watchers: Array<{ close?: () => void }> = [];

  const envPaths = searchDirs.map(dir => join(dir, ".env")).filter(p => existsSync(p));
  if (envPaths.length === 0) {
    console.warn("[EnvWatcher] 未找到 .env 文件，跳过监听");
    return () => {};
  }

  // 保存当前的 env 快照，用于对比
  let lastKeys = new Set(Object.keys(process.env));

  const reload = () => {
    loadEnvFile(true, ...searchDirs);

    const currentKeys = new Set(Object.keys(process.env));
    const changedKeys: string[] = [];

    for (const key of currentKeys) {
      if (!lastKeys.has(key)) {
        changedKeys.push(key);
      }
    }
    lastKeys = currentKeys;

    if (changedKeys.length > 0) {
      console.log(`[EnvWatcher] .env 变化: ${changedKeys.join(", ")}`);
      callback(changedKeys);
    }
  };

  for (const envPath of envPaths) {
    const w = watch(envPath, { persistent: false }, (eventType: string) => {
      if (eventType === "change") {
        // 防抖：延迟 300ms 避免短时间内多次触发
        clearTimeout((w as any)._debounce);
        (w as any)._debounce = setTimeout(reload, 300);
      }
    });
    watchers.push(w);
  }

  console.log(`[EnvWatcher] 已监听 ${envPaths.length} 个 .env 文件`);
  return () => {
    for (const w of watchers) {
      try { w.close?.(); } catch {}
    }
    console.log("[EnvWatcher] 已停止监听");
  };
}

/**
 * 验证并清理 URL
 * - 必须 https:// 开头
 * - 去除尾部斜杠和空格
 */
function validateUrl(raw: string): string | null {
  const url = raw.trim().replace(/\/+$/, "");
  if (!url.startsWith("https://")) {
    return null;
  }
  return url;
}
