/**
 * Versioning utilities - never overwrite, always version
 */

import { existsSync, readdirSync } from "fs";
import { copyFile, mkdir } from "fs/promises";
import { basename, dirname, join } from "path";

/**
 * Get the next version number for a file
 * e.g., script.json → script_v2.json if script.json exists
 */
export function getNextVersion(filePath: string): string {
  if (!existsSync(filePath)) {
    return filePath;
  }
  
  const dir = dirname(filePath);
  const base = basename(filePath);
  const ext = base.includes(".") ? "." + base.split(".").pop() : "";
  const name = ext ? base.slice(0, -ext.length) : base;
  
  // Check for existing versions
  let version = 2;
  while (existsSync(join(dir, `${name}_v${version}${ext}`))) {
    version++;
  }
  
  return join(dir, `${name}_v${version}${ext}`);
}

/**
 * Backup a file before overwriting
 * Returns the backup path, or null if file didn't exist
 */
export async function backupBeforeWrite(filePath: string): Promise<string | null> {
  if (!existsSync(filePath)) {
    return null;
  }
  
  const backupPath = getNextVersion(filePath.replace(/(\.[^.]+)$/, "_backup$1"));
  await copyFile(filePath, backupPath);
  return backupPath;
}

/**
 * Get versioned output path that won't overwrite existing files
 * For files, inserts _v2 before extension: video.mp4 → video_v2.mp4
 * For directories, appends _v2, _v3, etc.
 */
export function getVersionedPath(basePath: string): string {
  if (!existsSync(basePath)) {
    return basePath;
  }
  
  // Check if it's a file with extension
  const lastDot = basePath.lastIndexOf(".");
  const lastSlash = basePath.lastIndexOf("/");
  
  // Has extension if dot exists and is after the last slash
  const hasExtension = lastDot > lastSlash && lastDot !== -1;
  
  let version = 2;
  
  if (hasExtension) {
    const base = basePath.slice(0, lastDot);
    const ext = basePath.slice(lastDot);
    
    let versionedPath = `${base}_v${version}${ext}`;
    while (existsSync(versionedPath)) {
      version++;
      versionedPath = `${base}_v${version}${ext}`;
    }
    return versionedPath;
  } else {
    // Directory or extensionless file
    let versionedPath = `${basePath}_v${version}`;
    while (existsSync(versionedPath)) {
      version++;
      versionedPath = `${basePath}_v${version}`;
    }
    return versionedPath;
  }
}

/**
 * List all versions of a file
 */
export function listVersions(filePath: string): string[] {
  const dir = dirname(filePath);
  const base = basename(filePath);
  const ext = base.includes(".") ? "." + base.split(".").pop() : "";
  const name = ext ? base.slice(0, -ext.length) : base;
  
  if (!existsSync(dir)) return [];
  
  const files = readdirSync(dir);
  const versions = files.filter(f => {
    return f === base || f.match(new RegExp(`^${name}_v\\d+${ext.replace(".", "\\.")}$`));
  });
  
  return versions.map(f => join(dir, f)).sort();
}

/**
 * Safe write - backs up existing file first
 */
export async function safeWriteJson(filePath: string, data: unknown): Promise<{ path: string; backup: string | null }> {
  const backup = await backupBeforeWrite(filePath);
  await Bun.write(filePath, JSON.stringify(data, null, 2));
  return { path: filePath, backup };
}
