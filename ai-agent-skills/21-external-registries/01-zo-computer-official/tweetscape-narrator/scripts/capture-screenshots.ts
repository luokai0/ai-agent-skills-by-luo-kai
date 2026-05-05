#!/usr/bin/env bun
/**
 * Capture screenshots of Bluesky posts using puppeteer
 * Takes a manifest and captures the embed view of each post
 */

import { parseArgs } from "util";
import puppeteer from "puppeteer";
import { mkdir } from "fs/promises";
import { existsSync } from "fs";

interface Post {
  uri: string;
  text: string;
  embedUrl?: string;
  screenshotPath?: string;
}

interface Manifest {
  handle: string;
  posts: Post[];
  profile: {
    displayName?: string;
    avatar?: string;
    description?: string;
    followersCount?: number;
  };
}

async function capturePostScreenshot(
  page: puppeteer.Page,
  post: Post,
  outputPath: string,
  index: number
): Promise<string | null> {
  try {
    // Use the embed URL directly - Bluesky has nice embed views
    const embedUrl = post.embedUrl || `https://bsky.app/profile/${post.uri.split('/')[2]}/post/${post.uri.split('/').pop()}`;
    
    console.log(`   [${index + 1}] Capturing: ${post.text.slice(0, 50)}...`);
    
    await page.goto(embedUrl, { waitUntil: "networkidle2", timeout: 15000 });
    
    // Wait for post content to render
    await page.waitForSelector('[data-testid="postText"], [class*="Post"]', { timeout: 5000 }).catch(() => {});
    
    // Give images time to load
    await new Promise(r => setTimeout(r, 1000));
    
    // Find the main post element and screenshot it
    // Try to find the post container
    const postElement = await page.$('main article, [data-testid="post"], main > div > div');
    
    if (postElement) {
      await postElement.screenshot({ path: outputPath });
    } else {
      // Fallback: screenshot the viewport
      await page.screenshot({ path: outputPath, clip: { x: 0, y: 0, width: 600, height: 400 } });
    }
    
    return outputPath;
  } catch (error) {
    console.warn(`   ⚠️  Failed to capture post ${index}: ${error}`);
    return null;
  }
}

async function captureProfileScreenshot(
  page: puppeteer.Page,
  handle: string,
  outputPath: string
): Promise<string | null> {
  try {
    console.log(`   Capturing profile header...`);
    
    await page.goto(`https://bsky.app/profile/${handle}`, { waitUntil: "networkidle2", timeout: 15000 });
    
    // Wait for profile to load
    await page.waitForSelector('[data-testid="profileHeaderDisplayName"], img[alt*="avatar"]', { timeout: 5000 }).catch(() => {});
    await new Promise(r => setTimeout(r, 1500));
    
    // Screenshot the top portion (profile header)
    await page.screenshot({ 
      path: outputPath, 
      clip: { x: 0, y: 0, width: 1200, height: 500 } 
    });
    
    return outputPath;
  } catch (error) {
    console.warn(`   ⚠️  Failed to capture profile: ${error}`);
    return null;
  }
}

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      manifest: { type: "string", short: "m" },
      limit: { type: "string", short: "l", default: "10" },
    },
    allowPositionals: true,
  });

  if (!values.manifest) {
    console.error("Usage: bun run capture-screenshots.ts --manifest <path/to/manifest.json>");
    process.exit(1);
  }

  const manifestPath = values.manifest;
  const limit = parseInt(values.limit || "10");

  if (!existsSync(manifestPath)) {
    console.error(`Manifest not found: ${manifestPath}`);
    process.exit(1);
  }

  const manifest: Manifest = await Bun.file(manifestPath).json();
  const projectDir = manifestPath.replace("/manifest.json", "");
  const screenshotDir = `${projectDir}/screenshots`;
  
  await mkdir(screenshotDir, { recursive: true });

  console.log(`📸 Capturing screenshots for @${manifest.handle}`);
  console.log(`   Output: ${screenshotDir}`);
  console.log(`   Posts to capture: ${Math.min(limit, manifest.posts.length)}`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 800 });

  // Capture profile header
  const profilePath = `${screenshotDir}/profile.png`;
  await captureProfileScreenshot(page, manifest.handle, profilePath);

  // Capture individual posts
  const postsToCapture = manifest.posts.slice(0, limit);
  let capturedCount = 0;

  for (let i = 0; i < postsToCapture.length; i++) {
    const post = postsToCapture[i];
    const outputPath = `${screenshotDir}/post_${i.toString().padStart(3, "0")}.png`;
    
    const result = await capturePostScreenshot(page, post, outputPath, i);
    if (result) {
      manifest.posts[i].screenshotPath = outputPath;
      capturedCount++;
    }
    
    // Small delay between captures
    await new Promise(r => setTimeout(r, 500));
  }

  await browser.close();

  // Update manifest with screenshot paths
  await Bun.write(manifestPath, JSON.stringify(manifest, null, 2));

  console.log(`\n✅ Captured ${capturedCount}/${postsToCapture.length} screenshots`);
  console.log(`   Profile: ${profilePath}`);
  console.log(`   Manifest updated with screenshot paths`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
