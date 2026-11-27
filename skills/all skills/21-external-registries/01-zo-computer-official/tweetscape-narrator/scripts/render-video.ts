#!/usr/bin/env bun
/**
 * Step 4: Render final video with Remotion
 * 
 * Usage:
 *   bun run scripts/render-video.ts --project-dir <dir>                    # Full 1080p render
 *   bun run scripts/render-video.ts --project-dir <dir> --preview          # 5s preview from start
 *   bun run scripts/render-video.ts --project-dir <dir> --preview --start=30s  # 5s preview from 30s
 */

import { parseArgs } from "util";
import { spawn } from "child_process";
import { copyFile, mkdir, readdir } from "fs/promises";
import { existsSync } from "fs";
import { getVersionedPath } from "./lib/versioning";

const videoDir = "/home/workspace/Skills/tweetscape-narrator/video";
const bundlePath = `${videoDir}/.remotion-bundle`;

// Parse time string like "30s", "1m30s", "90" into seconds
function parseTime(input: string): number {
  const minSecMatch = input.match(/^(\d+)m(\d+)s?$/);
  if (minSecMatch) {
    return parseInt(minSecMatch[1]) * 60 + parseInt(minSecMatch[2]);
  }
  const secMatch = input.match(/^(\d+)s?$/);
  if (secMatch) {
    return parseInt(secMatch[1]);
  }
  const num = parseFloat(input);
  if (!isNaN(num)) return num;
  return 0;
}

interface SceneTimestamp {
  sceneId: string;
  start: number;
  end: number;
}

interface AudioManifest {
  audioPath: string;
  duration: number;
  scenes: SceneTimestamp[];
}

interface Manifest {
  handle: string;
  profile: { displayName?: string };
  posts: Array<{ screenshotPath?: string; text: string; author: { handle: string }; likeCount: number; replyCount: number; isReply: boolean }>;
}

interface RenderConfig {
  width: number;
  height: number;
  crf: number;
  fps: number;
  concurrency: number;
  frames?: [number, number];
}

interface Scene {
  id: string;
  relatedPostIndices?: number[];
  postFocusPoints?: string[];
}

interface Script {
  scenes: Scene[];
}

async function runCommand(cmd: string, args: string[], cwd: string): Promise<void> {
  console.log(`$ ${cmd} ${args.join(" ").slice(0, 100)}${args.join(" ").length > 100 ? "..." : ""}`);
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, { cwd, stdio: "inherit" });
    proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Command failed with code ${code}`));
    });
    proc.on("error", reject);
  });
}

async function ensureBundle(): Promise<void> {
  // Always rebuild bundle to ensure new assets in public/ are included
  if (existsSync(bundlePath)) {
    await runCommand("rm", ["-rf", bundlePath], videoDir);
  }
  
  console.log("📦 Building Remotion bundle...");
  await runCommand(
    "npx",
    ["remotion", "bundle", "src/index.tsx", "--out-dir", bundlePath],
    videoDir
  );
}

async function render(outputPath: string, propsPath: string, config: RenderConfig): Promise<void> {
  // Ensure absolute paths since cwd is videoDir
  const absOutputPath = outputPath.startsWith("/") ? outputPath : `${process.cwd()}/${outputPath}`;
  
  const args = [
    "remotion",
    "render",
    bundlePath,           // Use pre-built bundle, not src/index.tsx
    "TweetscapeDoc",
    absOutputPath,
    `--props=${propsPath}`,
    `--width=${config.width}`,
    `--height=${config.height}`,
    `--crf=${config.crf}`,
    `--fps=${config.fps}`,
    `--concurrency=${config.concurrency}`,
    `--codec=h264`,
    "--image-format=jpeg",
    "--jpeg-quality=80",
    "--muted",            // We add audio separately, faster to skip during render
    "--disable-web-security",
    "--enable-multiprocess-on-linux",
    "-y",                 // Overwrite without asking
  ];

  if (config.frames) {
    args.push(`--frames=${config.frames[0]}-${config.frames[1]}`);
  }

  await runCommand("npx", args, videoDir);

  // Mux audio back in with ffmpeg (much faster than Remotion audio handling)
  const audioPath = `${videoDir}/public/narration.mp3`;
  if (existsSync(audioPath)) {
    const tempPath = absOutputPath.replace(".mp4", "_noaudio.mp4");
    await runCommand("mv", [absOutputPath, tempPath], videoDir);
    await runCommand(
      "ffmpeg",
      [
        "-i", tempPath,
        "-i", audioPath,
        "-c:v", "copy",     // Don't re-encode video
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-y",
        absOutputPath,
      ],
      videoDir
    );
    await runCommand("rm", [tempPath], videoDir);
  }
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      "project-dir": { type: "string", short: "p" },
      output: { type: "string", short: "o" },
      preview: { type: "boolean", default: false },
      draft: { type: "boolean", default: false },
      start: { type: "string" },
    },
    allowPositionals: true,
  });

  const projectDir = values["project-dir"] || positionals[0];
  if (!projectDir) {
    console.error(`
Usage: bun run scripts/render-video.ts --project-dir <dir> [--preview] [--start=30s]

Options:
  --project-dir, -p  Project directory with manifest.json, script.json, etc.
  --output, -o       Output path (default: <project-dir>/video.mp4)
  --preview          Fast preview: 5s, 640x360, low quality
  --start            Start time for preview (e.g. 30s, 1m30s, 90)
`);
    process.exit(1);
  }

  const manifestPath = `${projectDir}/manifest.json`;
  const scriptPath = `${projectDir}/script.json`;
  const audioManifestPath = `${projectDir}/narration-timestamps.json`;
  const screenshotDir = `${projectDir}/screenshots`;
  const publicDir = `${videoDir}/public`;

  if (!existsSync(manifestPath) || !existsSync(audioManifestPath)) {
    console.error("Missing required files. Run the full pipeline first.");
    process.exit(1);
  }

  console.log("📦 Loading project...");
  const manifest: Manifest = await Bun.file(manifestPath).json();
  const script: Script = await Bun.file(scriptPath).json();
  const audioManifest: AudioManifest = await Bun.file(audioManifestPath).json();

  // Copy assets to public/
  await mkdir(publicDir, { recursive: true });

  const audioSrc = `${projectDir}/narration.mp3`;
  if (existsSync(audioSrc)) {
    await copyFile(audioSrc, `${publicDir}/narration.mp3`);
  }

  if (existsSync(screenshotDir)) {
    const files = await readdir(screenshotDir);
    await Promise.all(
      files
        .filter((f) => f.endsWith(".png"))
        .map((f) => copyFile(`${screenshotDir}/${f}`, `${publicDir}/${f}`))
    );
    console.log(`📸 ${files.length} screenshots ready`);
  }

  // Build props
  const relatedPostsByScene: Record<string, number[]> = {};
  const focusPointsByScene: Record<string, string[]> = {};
  for (const scene of script.scenes) {
    relatedPostsByScene[scene.id] = scene.relatedPostIndices || [];
    focusPointsByScene[scene.id] = scene.postFocusPoints || [];
  }

  const props = {
    audioPath: "narration.mp3",
    scenes: audioManifest.scenes,
    posts: manifest.posts.map((p, i) => ({
      ...p,
      screenshotPath: existsSync(`${screenshotDir}/post_${i.toString().padStart(3, "0")}.png`)
        ? `post_${i.toString().padStart(3, "0")}.png`
        : undefined,
    })),
    profileScreenshot: existsSync(`${screenshotDir}/profile.png`) ? "profile.png" : "",
    profileName: manifest.profile.displayName || manifest.handle,
    handle: manifest.handle,
    duration: audioManifest.duration,
    relatedPostsByScene,
    focusPointsByScene,
  };

  const propsPath = `${videoDir}/render-props.json`;
  await Bun.write(propsPath, JSON.stringify(props, null, 2));

  await ensureBundle();

  const isPreview = values.preview;
  const isDraft = values.draft;
  const totalFrames = Math.ceil(audioManifest.duration * 30);

  if (isPreview) {
    // Preview: 5 seconds, 640x360, high CRF (low quality)
    const startSec = values.start ? parseTime(values.start) : 0;
    const startFrame = Math.floor(startSec * 30);
    const endFrame = Math.min(startFrame + 150, totalFrames); // 5s at 30fps
    const actualStart = startFrame / 30;
    const actualEnd = endFrame / 30;
    
    const outputPath = getVersionedPath(`${projectDir}/preview.mp4`);

    console.log(`\n⚡ Preview: ${actualStart.toFixed(1)}s → ${actualEnd.toFixed(1)}s at 640x360`);

    await render(outputPath, propsPath, {
      width: 640,
      height: 360,
      crf: 35,
      fps: 30,
      concurrency: 4,
      frames: [startFrame, endFrame],
    });

    console.log(`\n✅ Preview: ${outputPath}`);
  } else if (isDraft) {
    // Draft render: 720p, high CRF for speed
    const outputPath = getVersionedPath(values.output || `${projectDir}/video_draft.mp4`);

    console.log(`\n🎬 Draft render: ${audioManifest.duration.toFixed(1)}s at 720p (Fast)`);

    await render(outputPath, propsPath, {
      width: 1280,
      height: 720,
      crf: 30, // Lower quality for speed
      fps: 30,
      concurrency: 4,
    });

    console.log(`\n✅ Draft Video: ${outputPath}`);
  } else {
    // Full render: 1080p, decent quality
    const outputPath = getVersionedPath(values.output || `${projectDir}/video.mp4`);

    console.log(`\n🎬 Full render: ${audioManifest.duration.toFixed(1)}s (${totalFrames} frames) at 1080p`);

    await render(outputPath, propsPath, {
      width: 1920,
      height: 1080,
      crf: 23,
      fps: 30,
      concurrency: 4,
    });

    console.log(`\n✅ Video: ${outputPath}`);
  }

  // Clean up bundle after render to avoid stale cache issues
  if (existsSync(bundlePath)) {
    await runCommand("rm", ["-rf", bundlePath], videoDir);
    console.log("🧹 Cleaned up Remotion bundle");
  }
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
