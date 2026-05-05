#!/usr/bin/env bun

/**
 * Skill Validator for Zo Skills Registry
 * 
 * Scans a skill for safety issues, validates structure,
 * and provides guidance for contribution.
 */

import { existsSync, readFileSync, readdirSync, statSync } from "fs";
import { join, relative, basename } from "path";

// Exit codes
const EXIT_CLEAN = 0;
const EXIT_WARNINGS = 1;
const EXIT_BLOCKING = 2;
const EXIT_ERROR = 3;

// Patterns that are BLOCKING issues
const SECRET_PATTERNS = [
  // API keys and tokens (common formats)
  /['"]?(?:api[_-]?key|apikey|api_token|api_secret)['"]?\s*[:=]\s*['"][a-zA-Z0-9_\-]{16,}['"]/i,
  /['"]?[a-zA-Z0-9_]*(?:secret|token|key|password|pwd|passwd)['"]?\s*[:=]\s*['"][^'"\s]{8,}['"]/i,
  // AWS credentials
  /AKIA[0-9A-Z]{16}/,
  // GitHub tokens
  /gh[pousr]_[A-Za-z0-9_]{36,}/,
  // Generic high-entropy strings that look like secrets
  /['"][a-zA-Z0-9]{32,}['"]/g,
  // Private keys
  /-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----/,
  // Bearer tokens
  /Bearer\s+[a-zA-Z0-9_\-\.]{20,}/i,
  // Connection strings with passwords
  /(?:mongodb|postgres|mysql|redis):\/\/[^:\s]+:[^@\s]+@/i,
];

// Dangerous patterns - only match actual usage, not documentation
const DANGEROUS_PATTERNS = [
  // Code execution risks (actual function calls, not strings)
  /\beval\s*\([^)]*\)/,
  /\bexec\s*\(/,
  /\bFunction\s*\(\s*["'`]/,
  /\bsetTimeout\s*\(\s*["'`][^"'`]*["'`]/,
  /\bsetInterval\s*\(\s*["'`][^"'`]*["'`]/,
  // Shell injection (actual imports, not comments)
  /^(?!\s*\/\/)(?!\s*\*).*\bchild_process\b/,
  /\.exec\s*\([^)]*\+/,
  /\.execSync\s*\([^)]*\+/,
  /spawn\s*\([^)]*\+/,
];

const PRIVATE_FILE_PATTERNS = [
  /^\.env/,
  /^\.env\./,
  /\.local$/,
  /\.cache$/,
  /config\.json$/,
  /secrets?\./i,
  /credentials?/i,
  /private/i,
  /personal/i,
  /^\./,  // Hidden files generally
];

const BINARY_EXTENSIONS = new Set([
  ".exe", ".dll", ".so", ".dylib", ".bin",
  ".zip", ".tar", ".gz", ".bz2", ".xz",
  ".jpg", ".jpeg", ".png", ".gif", ".webp", ".ico",
  ".mp3", ".mp4", ".mov", ".avi",
  ".woff", ".woff2", ".ttf", ".otf",
]);

interface Finding {
  type: "BLOCKING" | "WARNING" | "INFO";
  file: string;
  message: string;
  line?: number;
}

interface ValidationResult {
  skillPath: string;
  skillName: string;
  findings: Finding[];
  hasBlocking: boolean;
  hasWarnings: boolean;
  stats: {
    filesChecked: number;
    codeFiles: number;
    linesOfCode: number;
  };
}

function printBanner() {
  console.log("\n🔍 Zo Skill Validator\n");
  console.log("This tool checks your skill for safety issues and registry compliance.\n");
}

function getAllFiles(dir: string, basePath: string = dir): string[] {
  const files: string[] = [];
  
  if (!existsSync(dir)) return files;
  
  const entries = readdirSync(dir);
  
  for (const entry of entries) {
    // Skip common non-skill directories
    if (["node_modules", ".git", "dist", "build", "output", "cache", "Trash"].includes(entry)) {
      continue;
    }
    
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);
    
    if (stat.isDirectory()) {
      files.push(...getAllFiles(fullPath, basePath));
    } else {
      files.push(fullPath);
    }
  }
  
  return files;
}

function isTextFile(filePath: string): boolean {
  const ext = filePath.slice(filePath.lastIndexOf(".")).toLowerCase();
  if (BINARY_EXTENSIONS.has(ext)) return false;
  
  // Check for common binary markers
  try {
    const buffer = readFileSync(filePath);
    // If file contains null bytes, likely binary
    if (buffer.includes(0)) return false;
    return true;
  } catch {
    return false;
  }
}

function scanFileForSecrets(filePath: string, content: string): Finding[] {
  const findings: Finding[] = [];
  const lines = content.split("\n");
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // Skip comments and documentation
    if (line.trim().startsWith("//") || 
        line.trim().startsWith("#") || 
        line.trim().startsWith("*") ||
        line.trim().startsWith("/*") ||
        line.trim().startsWith("*/")) {
      continue;
    }
    
    for (const pattern of SECRET_PATTERNS) {
      if (pattern.test(line)) {
        // Double-check it's not a placeholder or env var reference
        if (/\bprocess\.env\./.test(line) || 
            /\$\{?\w+_KEY\}?/.test(line) ||
            /YOUR_|EXAMPLE_|PLACEHOLDER|demo|example|test/i.test(line)) {
          continue;
        }
        
        findings.push({
          type: "BLOCKING",
          file: filePath,
          message: `Potential secret/key detected`,
          line: lineNum,
        });
        break;
      }
    }
  }
  
  return findings;
}

function scanFileForDangerousPatterns(filePath: string, content: string): Finding[] {
  const findings: Finding[] = [];
  const lines = content.split("\n");
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;
    
    // Skip comments and documentation
    if (line.trim().startsWith("//") || 
        line.trim().startsWith("#") || 
        line.trim().startsWith("*") ||
        line.trim().startsWith("/*") ||
        line.trim().startsWith("*/")) {
      continue;
    }
    
    for (const pattern of DANGEROUS_PATTERNS) {
      if (pattern.test(line)) {
        findings.push({
          type: "WARNING",
          file: filePath,
          message: `Potentially dangerous pattern: ${pattern.source.slice(0, 50)}...`,
          line: lineNum,
        });
      }
    }
  }
  
  return findings;
}

function isPrivateFile(filePath: string): boolean {
  const fileName = basename(filePath);
  return PRIVATE_FILE_PATTERNS.some(pattern => pattern.test(fileName));
}

function validateSkillMd(skillPath: string, content: string): Finding[] {
  const findings: Finding[] = [];
  
  // Check for frontmatter
  if (!content.startsWith("---")) {
    findings.push({
      type: "BLOCKING",
      file: "SKILL.md",
      message: "Missing frontmatter (must start with ---)",
    });
    return findings;
  }
  
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    findings.push({
      type: "BLOCKING",
      file: "SKILL.md",
      message: "Invalid frontmatter format",
    });
    return findings;
  }
  
  const frontmatter = frontmatterMatch[1];
  
  // Required fields
  const requiredFields = ["name", "description", "compatibility"];
  for (const field of requiredFields) {
    const pattern = new RegExp(`^${field}:\s*(.+)$`, "m");
    if (!pattern.test(frontmatter)) {
      findings.push({
        type: "BLOCKING",
        file: "SKILL.md",
        message: `Missing required field: ${field}`,
      });
    }
  }
  
  // Validate name format
  const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
  if (nameMatch) {
    const name = nameMatch[1].trim();
    const expectedName = basename(skillPath);
    
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) {
      findings.push({
        type: "BLOCKING",
        file: "SKILL.md",
        message: `Invalid skill name "${name}". Must be lowercase, alphanumeric, hyphen-separated.`,
      });
    }
    
    if (name !== expectedName) {
      findings.push({
        type: "WARNING",
        file: "SKILL.md",
        message: `Skill name "${name}" doesn't match folder name "${expectedName}"`,
      });
    }
  }
  
  // Check description length
  const descMatch = frontmatter.match(/^description:\s*(.+)$/m);
  if (descMatch) {
    const desc = descMatch[1].trim();
    if (desc.length > 1024) {
      findings.push({
        type: "BLOCKING",
        file: "SKILL.md",
        message: `Description too long (${desc.length} chars, max 1024)`,
      });
    }
    if (desc.length < 10) {
      findings.push({
        type: "WARNING",
        file: "SKILL.md",
        message: `Description seems short (${desc.length} chars)`,
      });
    }
  }
  
  // Check for usage instructions in body
  if (!/##?\s*(?:Usage|Getting Started|How to use)/i.test(content)) {
    findings.push({
      type: "WARNING",
      file: "SKILL.md",
      message: "No usage instructions found in SKILL.md",
    });
  }
  
  return findings;
}

async function validateSkill(skillPath: string): Promise<ValidationResult> {
  const findings: Finding[] = [];
  let filesChecked = 0;
  let codeFiles = 0;
  let linesOfCode = 0;
  
  const skillName = basename(skillPath);
  
  // Check skill exists
  if (!existsSync(skillPath)) {
    return {
      skillPath,
      skillName,
      findings: [{ type: "BLOCKING", file: "", message: `Skill path does not exist: ${skillPath}` }],
      hasBlocking: true,
      hasWarnings: false,
      stats: { filesChecked: 0, codeFiles: 0, linesOfCode: 0 },
    };
  }
  
  // Get all files
  const allFiles = getAllFiles(skillPath);
  
  // Check for SKILL.md
  const skillMdPath = join(skillPath, "SKILL.md");
  if (!existsSync(skillMdPath)) {
    findings.push({
      type: "BLOCKING",
      file: "",
      message: "Missing SKILL.md file (required for all skills)",
    });
  } else {
    const skillMdContent = readFileSync(skillMdPath, "utf-8");
    findings.push(...validateSkillMd(skillPath, skillMdContent));
    filesChecked++;
  }
  
  // Scan all files
  for (const filePath of allFiles) {
    const relativePath = relative(skillPath, filePath);
    
    // Skip the SKILL.md we already checked
    if (relativePath === "SKILL.md") continue;
    
    filesChecked++;
    
    // Check for private files
    if (isPrivateFile(filePath)) {
      findings.push({
        type: "BLOCKING",
        file: relativePath,
        message: "Private/config file detected (should not be shared)",
      });
      continue;
    }
    
    // Skip binary files
    if (!isTextFile(filePath)) continue;
    
    // Read and scan code files
    const content = readFileSync(filePath, "utf-8");
    const lines = content.split("\n").length;
    linesOfCode += lines;
    codeFiles++;
    
    // Scan for secrets
    findings.push(...scanFileForSecrets(relativePath, content));
    
    // Scan for dangerous patterns
    findings.push(...scanFileForDangerousPatterns(relativePath, content));
  }
  
  // Check folder structure
  const hasScripts = existsSync(join(skillPath, "scripts"));
  const hasReferences = existsSync(join(skillPath, "references"));
  const hasAssets = existsSync(join(skillPath, "assets"));
  
  if (!hasScripts && !hasReferences && !hasAssets) {
    findings.push({
      type: "INFO",
      file: "",
      message: "No scripts/, references/, or assets/ folders found (simple skill)",
    });
  }
  
  const hasBlocking = findings.some(f => f.type === "BLOCKING");
  const hasWarnings = findings.some(f => f.type === "WARNING");
  
  return {
    skillPath,
    skillName,
    findings,
    hasBlocking,
    hasWarnings,
    stats: { filesChecked, codeFiles, linesOfCode },
  };
}

function printResults(result: ValidationResult) {
  console.log(`\n📁 Skill: ${result.skillName}`);
  console.log(`   Path: ${result.skillPath}`);
  console.log(`   Files: ${result.stats.filesChecked} (${result.stats.codeFiles} code files, ${result.stats.linesOfCode} lines)\n`);
  
  if (result.findings.length === 0) {
    console.log("✅ All checks passed!\n");
    return;
  }
  
  // Group by type
  const blocking = result.findings.filter(f => f.type === "BLOCKING");
  const warnings = result.findings.filter(f => f.type === "WARNING");
  const info = result.findings.filter(f => f.type === "INFO");
  
  if (blocking.length > 0) {
    console.log("\n❌ BLOCKING ISSUES (must fix before sharing):\n");
    for (const finding of blocking) {
      const line = finding.line ? `:${finding.line}` : "";
      console.log(`   • ${finding.file}${line}`);
      console.log(`     ${finding.message}\n`);
    }
  }
  
  if (warnings.length > 0) {
    console.log("\n⚠️  WARNINGS (review before proceeding):\n");
    for (const finding of warnings) {
      const line = finding.line ? `:${finding.line}` : "";
      console.log(`   • ${finding.file}${line}`);
      console.log(`     ${finding.message}\n`);
    }
  }
  
  if (info.length > 0) {
    console.log("\nℹ️  NOTES:\n");
    for (const finding of info) {
      console.log(`   • ${finding.message}\n`);
    }
  }
}

function printNextSteps(result: ValidationResult) {
  console.log("\n" + "=".repeat(60));
  console.log("NEXT STEPS");
  console.log("=".repeat(60) + "\n");
  
  if (result.hasBlocking) {
    console.log("❌ Fix the BLOCKING issues above before proceeding.\n");
    console.log("Common fixes:");
    console.log("   • Replace hardcoded secrets with process.env.VAR_NAME");
    console.log("   • Remove .env files and personal data files");
    console.log("   • Add required fields to SKILL.md frontmatter");
    console.log("   • Rename skill folder to match 'name' in SKILL.md\n");
    return;
  }
  
  console.log("✅ Your skill passed validation!\n");
  console.log("To share this skill to the Zo Registry:\n");
  console.log("1. Fork https://github.com/zocomputer/skills");
  console.log("2. Copy your skill to the Community/ folder:");
  console.log(`   cp -r ${result.skillPath} /path/to/fork/Community/${result.skillName}`);
  console.log("3. From the fork root, run validation:");
  console.log("   bun validate");
  console.log("4. Commit and push:");
  console.log("   git add Community/" + result.skillName);
  console.log(`   git commit -m "Add ${result.skillName} skill"`);
  console.log("   git push origin main");
  console.log("5. Open a Pull Request with this description:\n");
  console.log("-".repeat(40));
  console.log(`## Skill Submission: ${result.skillName}`);
  console.log("");
  console.log("**Author:** @YOUR_GITHUB_USERNAME");
  console.log("**Category:** <automation|integration|utility|media|other>");
  console.log("");
  console.log("### What it does");
  console.log("<2-3 sentence description>");
  console.log("");
  console.log("### Requirements");
  console.log("- <any external services/APIs needed>");
  console.log("- <any API keys required (stored in env vars)>");
  console.log("");
  console.log("### Usage Example");
  console.log("\`\`\`bash");
  console.log(`bun /home/workspace/Skills/${result.skillName}/scripts/SCRIPT.ts ARGS`);
  console.log("\`\`\`");
  console.log("-".repeat(40) + "\n");
  
  if (result.hasWarnings) {
    console.log("⚠️  You have warnings above. Review them before submitting.\n");
  }
}

async function main() {
  printBanner();
  
  const skillPath = process.argv[2];
  
  if (!skillPath) {
    console.error("Usage: bun validate.ts <path-to-skill>");
    console.error("");
    console.error("Example:");
    console.error("  bun validate.ts /home/workspace/Skills/my-skill");
    process.exit(EXIT_ERROR);
  }
  
  const resolvedPath = skillPath.startsWith("/") 
    ? skillPath 
    : join(process.cwd(), skillPath);
  
  const result = await validateSkill(resolvedPath);
  printResults(result);
  printNextSteps(result);
  
  if (result.hasBlocking) {
    process.exit(EXIT_BLOCKING);
  } else if (result.hasWarnings) {
    process.exit(EXIT_WARNINGS);
  } else {
    process.exit(EXIT_CLEAN);
  }
}

main().catch(err => {
  console.error("Error:", err);
  process.exit(EXIT_ERROR);
});
