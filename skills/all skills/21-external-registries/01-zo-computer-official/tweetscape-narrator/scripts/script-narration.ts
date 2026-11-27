#!/usr/bin/env bun
/**
 * Step 2: Generate narration script with scene markers
 * Takes a manifest from ingest, produces structured narration with post references
 */

import { parseArgs } from "util";
import { safeWriteJson } from "./lib/versioning";

interface Post {
  uri: string;
  text: string;
  createdAt: string;
  author: { handle: string; displayName?: string };
  likeCount: number;
  replyCount: number;
  repostCount: number;
  isReply: boolean;
  replyTo?: string;
  screenshotPath?: string;
}

interface Profile {
  handle: string;
  displayName?: string;
  description?: string;
  followersCount?: number;
  postsCount?: number;
}

interface IngestManifest {
  handle: string;
  profile: Profile;
  posts: Post[];
  outputDir: string;
}

interface NarrationScene {
  id: string;
  type: "intro" | "observation" | "specimen" | "interaction" | "conclusion";
  narrationText: string;
  relatedPostIndices: number[];
  visualDirection: string;
  postFocusPoints?: string[]; // New: list of keywords or phrases to zoom into
}

interface NarrationScript {
  title: string;
  handle: string;
  totalDurationEstimate: number;
  scenes: NarrationScene[];
  fullNarration: string;
}

function analyzeForNarration(posts: Post[], profile: Profile) {
  const topics = new Map<string, number>();
  const interactions = new Map<string, number>();
  let replyCount = 0;
  let originalCount = 0;

  for (const post of posts) {
    if (post.isReply) {
      replyCount++;
      if (post.replyTo) {
        interactions.set(post.replyTo, (interactions.get(post.replyTo) || 0) + 1);
      }
    } else {
      originalCount++;
    }

    const words = post.text.toLowerCase().split(/\s+/);
    for (const word of words) {
      if (word.length > 5 && !word.startsWith("http") && !word.startsWith("@")) {
        topics.set(word, (topics.get(word) || 0) + 1);
      }
    }
  }

  return {
    postCount: posts.length,
    originalPosts: originalCount,
    replies: replyCount,
    replyRatio: replyCount / posts.length,
    topInteractions: [...interactions.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5),
    topTopics: [...topics.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([w]) => w),
    interestingPosts: posts
      .map((p, i) => ({ ...p, index: i }))
      // .filter((p) => p.text.length > 50 && !p.text.startsWith("@")) // Remove this filter or make it smarter
      .slice(0, 5), // We might want to pass MORE posts to the LLM to give it options, or select smarter ones
  };
}

async function generateStructuredNarration(
  manifest: IngestManifest
): Promise<NarrationScript> {
  const analysis = analyzeForNarration(manifest.posts, manifest.profile);
  
  // Format posts for LLM context - STRICTLY FILTER REPOSTS
  // We only want to narrate original content to avoid "identity confusion"
  const formattedPosts = manifest.posts
    .slice(0, 15)
    .map((p, i) => {
      // Skip if it's a pure repost (no text, or starts with RT logic if we had it)
      // For now, rely on the fact that we can label them for the LLM
      const isRepost = p.repostCount > 0 && p.text.length === 0; // Rough heuristic, or if author != handle
      const isAuthor = p.author.handle === manifest.handle;
      
      let prefix = `[${i}]`;
      if (!isAuthor) prefix += ` [REPOST/REPLY from @${p.author.handle}]`;
      else if (p.isReply) prefix += ` [REPLY]`;
      else prefix += ` [ORIGINAL POST]`;

      return `${prefix}\n"${p.text.replace(/\n/g, " ").slice(0, 200)}${p.text.length > 200 ? "..." : ""}"\n`;
    })
    .join("\n");

  const prompt = `
You are David Attenborough narrating a nature documentary about a digital creature.
The creature is the user "@${manifest.handle}" (${manifest.profile.displayName || manifest.handle}).

Here are the "specimens" (posts) we have captured from their feed. 
IMPORTANT: 
- Pay close attention to the [TAGS]. 
- [ORIGINAL POST] are the user's own thoughts. Focus on these.
- [REPOST/REPLY from @...] are OTHER PEOPLE. Do NOT attribute these words to our subject.
- If you discuss a [REPOST], describe it as "the creature observing another" or "mimicking a peer", do not say the user wrote it.

${formattedPosts}

Write a documentary script with 4-5 scenes. Output ONLY valid JSON in this exact format:
{
  "title": "The Digital Habitat of ${manifest.handle}",
  "handle": "${manifest.handle}",
  "totalDurationEstimate": 60,
  "scenes": [
    {
      "id": "intro",
      "type": "intro",
      "narrationText": "The opening narration (2-3 sentences establishing the habitat)",
      "relatedPostIndices": [], 
      "visualDirection": "Wide shot of profile",
      "postFocusPoints": []
    },
    ...
  ]
}

RULES:
- "relatedPostIndices": An array of integers matching the [i] index above.
- **CRITICAL**: For "intro" and "conclusion" scenes, LEAVE "relatedPostIndices" EMPTY []. This ensures we show the user's profile, not a random tweet.
- Only include indices if that SPECIFIC tweet is being discussed.
- Use "visualDirection" to describe what we see (e.g. "Zoom in on the engagement count").
- "postFocusPoints": A list of short strings (1-3 words) found in the post text that the camera should pan/zoom to. e.g. ["my new project", "100 likes"].
- Tone: Attenborough. Scientific, curious, slightly whispered.
- Do not use the word "tweet" or "post" or "bluesky" - use nature metaphors (call, signal, display, territory).
- Write ONLY the JSON, no other text.
`;

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY || "",
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 2048,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  if (!response.ok) {
    throw new Error(`Anthropic API error: ${await response.text()}`);
  }

  const data = (await response.json()) as { content: Array<{ text: string }> };
  const jsonText = data.content[0].text;
  
  // Parse the JSON (handle potential markdown code blocks)
  const cleanJson = jsonText.replace(/```json\n?|\n?```/g, "").trim();
  const parsed = JSON.parse(cleanJson) as { scenes: NarrationScene[] };

  const fullNarration = parsed.scenes.map((s) => s.narrationText).join("\n\n");
  const wordCount = fullNarration.split(/\s+/).length;
  const estimatedDuration = Math.ceil(wordCount / 2.5); // ~150 words per minute

  return {
    title: `The Digital Habitat of ${manifest.profile.displayName || manifest.handle}`,
    handle: manifest.handle,
    totalDurationEstimate: estimatedDuration,
    scenes: parsed.scenes,
    fullNarration,
  };
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      manifest: { type: "string", short: "m" },
      output: { type: "string", short: "o" },
    },
    allowPositionals: true,
  });

  const manifestPath = values.manifest || positionals[0];
  if (!manifestPath) {
    console.error("Usage: bun run script-narration.ts --manifest <manifest.json>");
    process.exit(1);
  }

  console.log(`📖 Loading manifest from ${manifestPath}...`);
  const manifest = (await Bun.file(manifestPath).json()) as IngestManifest;

  console.log(`✍️  Generating structured narration script...`);
  const script = await generateStructuredNarration(manifest);

  console.log(`\n${"─".repeat(60)}`);
  console.log(`📽️  ${script.title}`);
  console.log(`⏱️  Estimated duration: ~${script.totalDurationEstimate} seconds`);
  console.log(`🎬 Scenes: ${script.scenes.length}`);
  console.log("─".repeat(60));
  
  for (const scene of script.scenes) {
    console.log(`\n[${scene.type.toUpperCase()}] ${scene.id}`);
    console.log(`  "${scene.narrationText}"`);
    console.log(`  📸 Posts: ${scene.relatedPostIndices.length > 0 ? scene.relatedPostIndices.join(", ") : "none"}`);
    console.log(`  🎥 Visual: ${scene.visualDirection}`);
  }
  
  console.log("\n" + "─".repeat(60));

  const outputPath = values.output || manifestPath.replace("manifest.json", "script.json");
  const { backup } = await safeWriteJson(outputPath, script);
  if (backup) {
    console.log(`📦 Previous version backed up to: ${backup}`);
  }
  console.log(`\n✅ Script saved to: ${outputPath}`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
