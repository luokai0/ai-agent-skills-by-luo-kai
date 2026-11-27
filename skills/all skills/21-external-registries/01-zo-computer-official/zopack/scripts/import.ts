#!/usr/bin/env bun

import { parseArgs } from "util";

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    file: { type: "string", short: "f" },
    handle: { type: "string" },
    preview: { type: "boolean", short: "p" },
    help: { type: "boolean", short: "h" },
  },
});

if (values.help) {
  console.log(`zopack import -- Parse a .zopack.md file and output a deployment plan

Usage:
  bun import.ts --file <path> [options]

Options:
  -f, --file     Path to the .zopack.md file (required)
  --handle       Your zo.space handle for variable replacement
  -p, --preview  Preview the plan without outputting full code
  -h, --help     Show this help

The script outputs a JSON deployment plan. Zo reads this and deploys
each route using update_space_route.`);
  process.exit(0);
}

if (!values.file) {
  console.error("Error: --file is required. Use --help for usage.");
  process.exit(1);
}

interface ParsedRoute {
  path: string;
  route_type: "api" | "page";
  public: boolean;
  code: string;
}

interface ParsedPack {
  meta: Record<string, string>;
  routes: ParsedRoute[];
  npm_deps: string[];
  shadcn_components: string[];
  directories: string[];
  files: Array<{ path: string; content: string }>;
  secrets: string[];
  variables: Array<{ placeholder: string; description: string }>;
}

function parseFrontmatter(content: string): { meta: Record<string, string>; body: string } {
  const meta: Record<string, string> = {};
  if (!content.startsWith("---")) return { meta, body: content };

  const endIdx = content.indexOf("---", 3);
  if (endIdx === -1) return { meta, body: content };

  const frontmatter = content.slice(3, endIdx).trim();
  for (const line of frontmatter.split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let val = line.slice(colonIdx + 1).trim();
    // Strip surrounding quotes
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    meta[key] = val;
  }

  const body = content.slice(endIdx + 3).trim();
  return { meta, body };
}

function parseRoutes(body: string): ParsedRoute[] {
  const routes: ParsedRoute[] = [];

  // Match ### `path` (type, visibility)
  const routeHeaderRegex = /^###\s+`([^`]+)`\s+\((\w+),\s*(\w+)\)/gm;
  const headers: Array<{ path: string; type: string; visibility: string; index: number }> = [];

  let match: RegExpExecArray | null;
  while ((match = routeHeaderRegex.exec(body)) !== null) {
    headers.push({
      path: match[1],
      type: match[2],
      visibility: match[3],
      index: match.index,
    });
  }

  for (let i = 0; i < headers.length; i++) {
    const header = headers[i];
    const sectionStart = header.index;
    const sectionEnd = i < headers.length - 1 ? headers[i + 1].index : body.length;
    const section = body.slice(sectionStart, sectionEnd);

    // Extract the fenced code block
    const codeMatch = section.match(/```(?:typescript|tsx|ts)\n([\s\S]*?)```/);
    if (!codeMatch) continue;

    routes.push({
      path: header.path,
      route_type: header.type as "api" | "page",
      public: header.visibility === "public",
      code: codeMatch[1],
    });
  }

  return routes;
}

function parseDependencies(body: string): { npm: string[]; shadcn: string[] } {
  const npm: string[] = [];
  const shadcn: string[] = [];

  const depsSection = body.match(/## Dependencies\n\n([\s\S]*?)(?=\n## |\n---|$)/);
  if (!depsSection) return { npm, shadcn };

  const text = depsSection[1];

  // npm packages
  const npmMatch = text.match(/\*\*npm packages\*\*[^\n]*\n((?:- `[^`]+`\n?)*)/);
  if (npmMatch) {
    const lines = npmMatch[1].trim().split("\n");
    for (const line of lines) {
      const m = line.match(/- `([^`]+)`/);
      if (m) npm.push(m[1]);
    }
  }

  // shadcn/components
  const compMatch = text.match(/\*\*Components\*\*[^\n]*\n((?:- `[^`]+`\n?)*)/);
  if (compMatch) {
    const lines = compMatch[1].trim().split("\n");
    for (const line of lines) {
      const m = line.match(/- `([^`]+)`/);
      if (m) shadcn.push(m[1]);
    }
  }

  return { npm, shadcn };
}

function parseSetup(body: string): { directories: string[]; files: Array<{ path: string; content: string }>; secrets: string[] } {
  const directories: string[] = [];
  const files: Array<{ path: string; content: string }> = [];
  const secrets: string[] = [];

  const setupSection = body.match(/## Setup\n\n([\s\S]*?)(?=\n## |\n---|$)/);
  if (!setupSection) return { directories, files, secrets };

  const text = setupSection[1];

  // Directories
  const dirMatch = text.match(/\*\*Directories to create:\*\*\n((?:- `[^`]+`\n?)*)/);
  if (dirMatch) {
    for (const line of dirMatch[1].trim().split("\n")) {
      const m = line.match(/- `([^`]+)`/);
      if (m) directories.push(m[1]);
    }
  }

  // Files
  const fileMatch = text.match(/\*\*Files to initialize:\*\*\n((?:- `[^`]+`[^\n]*\n?)*)/);
  if (fileMatch) {
    for (const line of fileMatch[1].trim().split("\n")) {
      const m = line.match(/- `([^`]+)` with content: `([^`]*)`/);
      if (m) files.push({ path: m[1], content: m[2] });
    }
  }

  // Secrets
  const secretMatch = text.match(/\*\*Secrets required\*\*[^\n]*\n((?:- `[^`]+`\n?)*)/);
  if (secretMatch) {
    for (const line of secretMatch[1].trim().split("\n")) {
      const m = line.match(/- `([^`]+)`/);
      if (m) secrets.push(m[1]);
    }
  }

  return { directories, files, secrets };
}

function replaceVariables(code: string, handle?: string): string {
  if (handle) {
    code = code.replace(/\{\{HANDLE\}\}/g, handle);
  }
  return code;
}

async function main() {
  const filePath = values.file!.startsWith("/") ? values.file! : `/home/workspace/${values.file}`;
  const raw = await Bun.file(filePath).text();

  const { meta, body } = parseFrontmatter(raw);

  if (meta.format !== "zopack") {
    console.error("Error: This file does not appear to be a .zopack.md (missing format: zopack in frontmatter)");
    process.exit(1);
  }

  const routes = parseRoutes(body);
  const { npm, shadcn } = parseDependencies(body);
  const { directories, files, secrets } = parseSetup(body);

  // Apply handle replacement if provided
  const handle = values.handle;
  const processedRoutes = routes.map((r) => ({
    ...r,
    code: replaceVariables(r.code, handle),
  }));

  const plan: ParsedPack = {
    meta,
    routes: processedRoutes,
    npm_deps: npm,
    shadcn_components: shadcn,
    directories,
    files,
    secrets,
    variables: [],
  };

  // Check for unreplaced variables
  const unreplaced = new Set<string>();
  for (const r of processedRoutes) {
    const matches = r.code.match(/\{\{(\w+)\}\}/g);
    if (matches) for (const m of matches) unreplaced.add(m);
  }

  if (values.preview) {
    console.log(`Pack: ${meta.name || "unknown"}`);
    console.log(`Author: ${meta.author || "unknown"}`);
    console.log(`Description: ${meta.description || "none"}`);
    console.log(`\nRoutes (${routes.length}):`);
    for (const r of routes) {
      console.log(`  ${r.path} (${r.route_type}, ${r.public ? "public" : "private"}) -- ${r.code.split("\n").length} lines`);
    }
    if (npm.length > 0) console.log(`\nnpm deps: ${npm.join(", ")}`);
    if (shadcn.length > 0) console.log(`\nComponents: ${shadcn.join(", ")}`);
    if (directories.length > 0) console.log(`\nDirectories: ${directories.join(", ")}`);
    if (files.length > 0) console.log(`\nFiles: ${files.map((f) => f.path).join(", ")}`);
    if (secrets.length > 0) console.log(`\nSecrets needed: ${secrets.join(", ")}`);
    if (unreplaced.size > 0) console.log(`\nUnreplaced variables: ${[...unreplaced].join(", ")}`);
    if (!handle && unreplaced.has("{{HANDLE}}")) {
      console.log(`\nTip: Pass --handle <your-handle> to replace {{HANDLE}} automatically`);
    }
  } else {
    // Output full JSON plan for Zo to consume
    if (unreplaced.size > 0 && !handle) {
      console.error(`Warning: Unreplaced variables found: ${[...unreplaced].join(", ")}`);
      if (unreplaced.has("{{HANDLE}}")) {
        console.error(`Pass --handle <your-handle> to replace {{HANDLE}}`);
      }
    }
    console.log(JSON.stringify(plan, null, 2));
  }
}

main().catch((e) => {
  console.error("Import failed:", e.message);
  process.exit(1);
});
