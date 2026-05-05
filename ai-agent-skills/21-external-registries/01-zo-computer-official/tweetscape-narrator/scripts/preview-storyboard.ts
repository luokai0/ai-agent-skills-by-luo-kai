#!/usr/bin/env bun
/**
 * Preview Storyboard Generator
 * Generates a Markdown file visualizing the script scenes alongside their selected screenshots.
 * 
 * Usage:
 *   bun run scripts/preview-storyboard.ts --project-dir <dir>
 */

import { parseArgs } from "util";
import { existsSync } from "fs";

interface Scene {
  id: string;
  type: string;
  narrationText: string;
  relatedPostIndices: number[];
  visualDirection: string;
  postFocusPoints?: string[];
}

interface Script {
  title: string;
  handle: string;
  scenes: Scene[];
}

interface Manifest {
  posts: Array<{ 
    screenshotPath?: string; 
    text: string; 
    author: { handle: string; displayName?: string };
    createdAt: string;
  }>;
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      "project-dir": { type: "string", short: "p" },
    },
    allowPositionals: true,
  });

  const projectDir = values["project-dir"] || positionals[0];
  if (!projectDir) {
    console.error("Usage: bun run scripts/preview-storyboard.ts --project-dir <dir>");
    process.exit(1);
  }

  const scriptPath = `${projectDir}/script.json`;
  const manifestPath = `${projectDir}/manifest.json`;

  if (!existsSync(scriptPath) || !existsSync(manifestPath)) {
    console.error("Missing script.json or manifest.json in project directory.");
    process.exit(1);
  }

  const script: Script = await Bun.file(scriptPath).json();
  const manifest: Manifest = await Bun.file(manifestPath).json();

  let markdown = `# Storyboard: ${script.title}\n\n`;
  markdown += `**Handle**: ${script.handle}\n`;
  markdown += `**Project Dir**: \`${projectDir}\`\n\n`;
  markdown += `*Generated: ${new Date().toLocaleString()}*\n\n`;

  for (const scene of script.scenes) {
    markdown += `## Scene: ${scene.type.toUpperCase()} (${scene.id})\n\n`;
    markdown += `> **Narration**: "${scene.narrationText}"\n\n`;
    markdown += `**Visual Direction**: ${scene.visualDirection}\n\n`;
    
    if (scene.postFocusPoints && scene.postFocusPoints.length > 0) {
        markdown += `**Focus Points**: ${scene.postFocusPoints.join(", ")}\n\n`;
    }

    if (!scene.relatedPostIndices || scene.relatedPostIndices.length === 0) {
      markdown += `### Visual: Profile View\n`;
      markdown += `![Profile](./screenshots/profile.png)\n\n`;
    } else {
      markdown += `### Visuals (${scene.relatedPostIndices.length} posts)\n\n`;
      
      for (const index of scene.relatedPostIndices) {
        const post = manifest.posts[index];
        if (!post) {
          markdown += `**ERROR: Post index ${index} not found in manifest**\n\n`;
          continue;
        }

        const screenshotName = post.screenshotPath 
          ? post.screenshotPath.split("/").pop() 
          : "MISSING";
        
        markdown += `#### Post #${index} (@${post.author.handle})\n`;
        markdown += `*${post.text.replace(/\n/g, " ").substring(0, 100)}${post.text.length > 100 ? "..." : ""}*\n\n`;
        
        if (post.screenshotPath) {
            // Use relative path for Markdown preview if possible, or absolute
            // Here we use the relative path assuming the user views this MD file 
            // from the workspace root or handles paths intelligently.
            // But to be safe for "Preview Markdown", we should use the full path 
            // or the path relative to the MD file. 
            // If the MD file is in projectDir, then screenshots/image.png works.
            markdown += `![Post ${index}](./screenshots/${screenshotName})\n\n`;
        } else {
            markdown += `**[NO SCREENSHOT CAPTURED]**\n\n`;
        }
      }
    }
    
    markdown += "---\n\n";
  }

  const outputPath = `${projectDir}/STORYBOARD.md`;
  await Bun.write(outputPath, markdown);
  
  console.log(`✅ Storyboard generated at: ${outputPath}`);
}

main().catch(console.error);
