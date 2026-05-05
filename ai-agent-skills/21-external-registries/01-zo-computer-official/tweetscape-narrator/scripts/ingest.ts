#!/usr/bin/env bun
/**
 * Step 1: Ingest posts and capture screenshots
 * Outputs a JSON manifest with posts and screenshot paths
 */

import { parseArgs } from "util";
import { mkdir } from "fs/promises";

const BLUESKY_API = "https://public.api.bsky.app/xrpc";

interface Post {
  uri: string;
  text: string;
  createdAt: string;
  author: {
    handle: string;
    displayName?: string;
    avatar?: string;
  };
  likeCount: number;
  replyCount: number;
  repostCount: number;
  isReply: boolean;
  replyTo?: string;
  embedUrl?: string;
  screenshotPath?: string;
}

interface FeedItem {
  post: {
    uri: string;
    cid: string;
    author: {
      did: string;
      handle: string;
      displayName?: string;
      avatar?: string;
    };
    record: {
      text: string;
      createdAt: string;
      reply?: { parent: { uri: string }; root: { uri: string } };
    };
    likeCount?: number;
    replyCount?: number;
    repostCount?: number;
    embed?: {
      images?: Array<{ thumb: string; fullsize: string; alt?: string }>;
      external?: { uri: string; title: string; description?: string };
    };
  };
  reply?: {
    parent?: { author?: { handle: string; displayName?: string } };
  };
}

interface Profile {
  did: string;
  handle: string;
  displayName?: string;
  description?: string;
  avatar?: string;
  banner?: string;
  followersCount?: number;
  followsCount?: number;
  postsCount?: number;
  screenshotPath?: string;
}

interface IngestManifest {
  handle: string;
  profile: Profile;
  ingestedAt: string;
  posts: Post[];
  outputDir: string;
}

function postToWebUrl(uri: string): string {
  // at://did:plc:xxx/app.bsky.feed.post/yyy -> https://bsky.app/profile/handle/post/yyy
  const match = uri.match(/at:\/\/([^/]+)\/app\.bsky\.feed\.post\/(.+)/);
  if (match) {
    return `https://bsky.app/profile/${match[1]}/post/${match[2]}`;
  }
  return uri;
}

async function fetchProfile(handle: string): Promise<Profile> {
  const url = `${BLUESKY_API}/app.bsky.actor.getProfile?actor=${handle}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch profile: ${response.status}`);
  }
  return response.json() as Promise<Profile>;
}

async function fetchBlueskyFeed(handle: string, limit: number = 50): Promise<Post[]> {
  const url = `${BLUESKY_API}/app.bsky.feed.getAuthorFeed?actor=${handle}&limit=${limit}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch feed: ${response.status} ${response.statusText}`);
  }

  const data = (await response.json()) as { feed: FeedItem[] };

  return data.feed.map((item: FeedItem) => ({
    uri: item.post.uri,
    text: item.post.record.text,
    createdAt: item.post.record.createdAt,
    author: {
      handle: item.post.author.handle,
      displayName: item.post.author.displayName,
      avatar: item.post.author.avatar,
    },
    likeCount: item.post.likeCount || 0,
    replyCount: item.post.replyCount || 0,
    repostCount: item.post.repostCount || 0,
    isReply: !!item.post.record.reply,
    replyTo: item.reply?.parent?.author?.handle,
    embedUrl: postToWebUrl(item.post.uri),
  }));
}

async function captureScreenshot(url: string, outputPath: string): Promise<boolean> {
  try {
    const proc = Bun.spawn([
      "agent-browser",
      "open",
      url,
    ]);
    await proc.exited;
    
    // Wait for page to render
    await new Promise((r) => setTimeout(r, 4000));
    
    const screenshot = Bun.spawn([
      "agent-browser",
      "screenshot",
      outputPath,
    ]);
    await screenshot.exited;
    
    // Verify file exists
    const file = Bun.file(outputPath);
    return await file.exists();
  } catch (e) {
    console.warn(`Failed to capture screenshot for ${url}: ${e}`);
    return false;
  }
}

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      handle: { type: "string", short: "h" },
      count: { type: "string", short: "c", default: "30" },
      output: { type: "string", short: "o" },
      "skip-screenshots": { type: "boolean", default: false },
    },
    allowPositionals: true,
  });

  const handle = values.handle;
  if (!handle) {
    console.error("Usage: bun run ingest.ts --handle <bluesky-handle>");
    process.exit(1);
  }

  const count = parseInt(values.count || "30");
  const skipScreenshots = values["skip-screenshots"] || false;
  
  const safeHandle = handle.replace(/[^a-zA-Z0-9]/g, "_");
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
  const outputDir = values.output || `/home/workspace/Skills/tweetscape-narrator/output/${safeHandle}_${timestamp}`;
  
  await mkdir(outputDir, { recursive: true });
  await mkdir(`${outputDir}/screenshots`, { recursive: true });

  console.log(`🔭 Ingesting feed from @${handle}...`);
  
  const profile = await fetchProfile(handle);
  console.log(`👤 Profile: ${profile.displayName || handle} (${profile.followersCount} followers)`);
  
  const posts = await fetchBlueskyFeed(handle, count);
  console.log(`📊 Fetched ${posts.length} posts`);

  if (!skipScreenshots) {
    console.log(`📸 Capturing screenshots...`);
    
    // Capture profile screenshot
    const profileUrl = `https://bsky.app/profile/${handle}`;
    const profileScreenshot = `${outputDir}/screenshots/profile.png`;
    await captureScreenshot(profileUrl, profileScreenshot);
    
    if (await Bun.file(profileScreenshot).exists()) {
       profile.avatar = profileScreenshot; // Hack to store it, or add a field
    }

    // Capture individual post screenshots (limit to avoid rate limiting)
    const postsToCapture = posts.slice(0, 15);
    for (let i = 0; i < postsToCapture.length; i++) {
      const post = postsToCapture[i];
      const screenshotPath = `${outputDir}/screenshots/post_${i.toString().padStart(3, "0")}.png`;
      
      process.stdout.write(`  [${i + 1}/${postsToCapture.length}] Capturing post...`);
      const success = await captureScreenshot(post.embedUrl!, screenshotPath);
      
      if (success) {
        post.screenshotPath = screenshotPath;
        console.log(` ✓`);
      } else {
        console.log(` ✗`);
      }
      
      // Small delay to be nice to the server
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  const manifest: IngestManifest = {
    handle,
    profile,
    ingestedAt: new Date().toISOString(),
    posts,
    outputDir,
  };

  const manifestPath = `${outputDir}/manifest.json`;
  await Bun.write(manifestPath, JSON.stringify(manifest, null, 2));
  
  console.log(`\n✅ Ingest complete!`);
  console.log(`   Manifest: ${manifestPath}`);
  console.log(`   Posts: ${posts.length}`);
  console.log(`   Screenshots: ${posts.filter(p => p.screenshotPath).length}`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
