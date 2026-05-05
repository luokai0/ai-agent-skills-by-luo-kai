#!/usr/bin/env bun
/**
 * Full pipeline: ingest → script → record → render
 * One command to go from handle to finished video
 */

import { parseArgs } from "util";
import { spawn } from "child_process";

async function runScript(script: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn("bun", ["run", script, ...args], {
      cwd: "/home/workspace/Skills/tweetscape-narrator",
      stdio: "inherit",
    });
    proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${script} failed with code ${code}`));
    });
    proc.on("error", reject);
  });
}

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      handle: { type: "string", short: "h" },
      count: { type: "string", short: "c", default: "30" },
      "skip-screenshots": { type: "boolean", default: false },
      "audio-only": { type: "boolean", default: false },
      output: { type: "string", short: "o" },
      yes: { type: "boolean", default: false },
    },
    allowPositionals: true,
  });

  const handle = values.handle;
  if (!handle) {
    console.error(`
🎬 Tweetscape Narrator - Full Video Pipeline

Usage: bun run scripts/generate-video.ts --handle <bluesky-handle>

Options:
  --handle, -h        Bluesky handle to narrate (required)
  --count, -c         Number of posts to fetch (default: 30)
  --skip-screenshots  Skip screenshot capture (faster, text-only visuals)
  --audio-only        Stop after audio generation (skip video render)
  --output, -o        Output path for final video

Example:
  bun run scripts/generate-video.ts --handle norvid-studies.bsky.social
`);
    process.exit(1);
  }

  const safeHandle = handle.replace(/[^a-zA-Z0-9]/g, "_");
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
  const projectDir = `/home/workspace/Skills/tweetscape-narrator/output/${safeHandle}_${timestamp}`;

  console.log(`
╔═══════════════════════════════════════════════════════════╗
║  🎬 TWEETSCAPE NARRATOR - Documentary Video Generator     ║
╚═══════════════════════════════════════════════════════════╝
`);
  console.log(`📍 Target: @${handle}`);
  console.log(`📁 Project: ${projectDir}\n`);

  // Step 1: Ingest
  console.log("═══════════════════════════════════════════════════════════");
  console.log("STEP 1/4: INGESTION");
  console.log("═══════════════════════════════════════════════════════════\n");
  
  const ingestArgs = ["--handle", handle, "--count", values.count || "30", "--output", projectDir];
  if (values["skip-screenshots"]) ingestArgs.push("--skip-screenshots");
  
  await runScript("scripts/ingest.ts", ingestArgs);

  // Step 2: Script narration
  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("STEP 2/4: SCRIPTING");
  console.log("═══════════════════════════════════════════════════════════\n");
  
  await runScript("scripts/script-narration.ts", ["--manifest", `${projectDir}/manifest.json`]);

  // Step 2.5: Storyboard Preview
  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("STEP 2.5/4: STORYBOARD REVIEW");
  console.log("═══════════════════════════════════════════════════════════\n");
  
  await runScript("scripts/preview-storyboard.ts", ["--project-dir", projectDir]);

  if (!values.yes) {
    console.log(`
🛑 REVIEW REQUIRED
   A storyboard has been generated at: ${projectDir}/STORYBOARD.md
   Please review it to ensure screenshots and narration match.
   
   To continue, run:
   bun run scripts/record-audio.ts --script ${projectDir}/script.json
   bun run scripts/render-video.ts --project-dir ${projectDir}
    `);
    return;
  }

  // Step 3: Record audio
  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("STEP 3/4: RECORDING");
  console.log("═══════════════════════════════════════════════════════════\n");
  
  await runScript("scripts/record-audio.ts", ["--script", `${projectDir}/script.json`]);

  if (values["audio-only"]) {
    console.log("\n✅ Audio-only mode: stopping before video render");
    console.log(`   Audio: ${projectDir}/narration.mp3`);
    return;
  }

  // Step 4: Render video
  console.log("\n═══════════════════════════════════════════════════════════");
  console.log("STEP 4/4: RENDERING");
  console.log("═══════════════════════════════════════════════════════════\n");
  
  const outputPath = values.output || `${projectDir}/video.mp4`;
  await runScript("scripts/render-video.ts", ["--project-dir", projectDir, "--output", outputPath]);

  console.log(`
╔═══════════════════════════════════════════════════════════╗
║  ✅ COMPLETE!                                              ║
╚═══════════════════════════════════════════════════════════╝

📹 Video: ${outputPath}
🔊 Audio: ${projectDir}/narration.mp3
📝 Script: ${projectDir}/script.json
`);
}

main().catch((err) => {
  console.error("\n❌ Pipeline failed:", err.message);
  process.exit(1);
});
