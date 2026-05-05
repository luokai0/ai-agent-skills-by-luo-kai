#!/usr/bin/env bun

import { parseArgs } from "util";

const BLUESKY_API = "https://public.api.bsky.app/xrpc";

interface Post {
  text: string;
  createdAt: string;
  author: {
    handle: string;
    displayName?: string;
  };
  likeCount?: number;
  replyCount?: number;
  repostCount?: number;
  isReply?: boolean;
  replyTo?: string;
}

interface FeedItem {
  post: {
    uri: string;
    cid: string;
    author: {
      did: string;
      handle: string;
      displayName?: string;
    };
    record: {
      text: string;
      createdAt: string;
      reply?: {
        parent: { uri: string };
        root: { uri: string };
      };
    };
    likeCount?: number;
    replyCount?: number;
    repostCount?: number;
  };
  reply?: {
    parent?: {
      author?: {
        handle: string;
        displayName?: string;
      };
    };
  };
}

interface ElevenLabsVoice {
  voice_id: string;
  name: string;
  labels?: {
    accent?: string;
    description?: string;
    age?: string;
    gender?: string;
    use_case?: string;
  };
}

async function fetchBlueskyFeed(handle: string, limit: number = 50): Promise<Post[]> {
  const url = `${BLUESKY_API}/app.bsky.feed.getAuthorFeed?actor=${handle}&limit=${limit}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch feed: ${response.status} ${response.statusText}`);
  }
  
  const data = await response.json() as { feed: FeedItem[] };
  
  return data.feed.map((item: FeedItem) => ({
    text: item.post.record.text,
    createdAt: item.post.record.createdAt,
    author: {
      handle: item.post.author.handle,
      displayName: item.post.author.displayName,
    },
    likeCount: item.post.likeCount || 0,
    replyCount: item.post.replyCount || 0,
    repostCount: item.post.repostCount || 0,
    isReply: !!item.post.record.reply,
    replyTo: item.reply?.parent?.author?.handle,
  }));
}

function analyzeFeed(posts: Post[], handle: string): string {
  const topics = new Map<string, number>();
  const interactions = new Map<string, number>();
  let totalEngagement = 0;
  let replyCount = 0;
  let originalCount = 0;
  
  for (const post of posts) {
    totalEngagement += (post.likeCount || 0) + (post.replyCount || 0) + (post.repostCount || 0);
    
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
      if (word.length > 5 && !word.startsWith('http') && !word.startsWith('@')) {
        topics.set(word, (topics.get(word) || 0) + 1);
      }
    }
  }
  
  const topInteractions = [...interactions.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);
  
  const topTopics = [...topics.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word]) => word);
  
  const timeRange = posts.length > 0 
    ? `${new Date(posts[posts.length - 1].createdAt).toLocaleDateString()} to ${new Date(posts[0].createdAt).toLocaleDateString()}`
    : 'unknown';
  
  return JSON.stringify({
    handle,
    postCount: posts.length,
    timeRange,
    originalPosts: originalCount,
    replies: replyCount,
    avgEngagement: Math.round(totalEngagement / posts.length),
    frequentInterlocutors: topInteractions.map(([h, c]) => ({ handle: h, count: c })),
    recurringThemes: topTopics,
    samplePosts: posts.slice(0, 10).map(p => ({
      text: p.text.slice(0, 200),
      likes: p.likeCount,
      isReply: p.isReply,
    })),
  }, null, 2);
}

async function generateNarration(analysis: string, posts: Post[]): Promise<string> {
  const postsContext = posts.slice(0, 20).map(p => 
    `[${p.isReply ? 'Reply' : 'Post'}] ${p.text}`
  ).join('\n\n');

  const prompt = `You are David Attenborough narrating a nature documentary, but instead of wildlife, you're observing the digital ecosystem of a social media user's timeline.

Here is the analysis of their "tweetscape":
${analysis}

And here are some of their recent posts:
${postsContext}

Write a 2-3 paragraph nature documentary narration (about 200-300 words) observing this user's digital habitat. Treat their posts as behavioral patterns, their interactions as symbiotic relationships, their topics as the terrain they traverse. Use Attenborough's signature style:
- Warm, contemplative tone
- Scientific observation mixed with gentle wonder
- Occasional dry wit
- Treating mundane digital behavior as fascinating natural phenomena
- Zooming in on specific "specimens" (posts) and zooming out to see the larger ecosystem

IMPORTANT RULES:
- Do NOT use the word "tweetscape" - find more evocative nature metaphors.
- Do NOT break the fourth wall or acknowledge this is a parody.
- Do NOT include any stage directions, asterisks, or meta-commentary like "*In a calm voice*" or "(pause)"
- Write ONLY the narration text itself, as it would be spoken aloud.
- Write as if this is a genuine documentary about the natural world of online discourse.`;

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY || "",
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to generate narration: ${error}`);
  }

  const data = await response.json() as { content: Array<{ text: string }> };
  let narration = data.content[0].text;
  
  // Clean up any stage directions that might have slipped through
  narration = narration.replace(/^\*[^*]+\*\n*/gm, '');
  narration = narration.replace(/\([^)]+\)/g, '');
  narration = narration.trim();
  
  return narration;
}

async function findDocumentaryVoice(apiKey: string): Promise<{ id: string; name: string }> {
  // Preferred voices for documentary narration (British, warm, narrator-style)
  const preferredVoices = [
    { id: "JBFqnCBsd6RMkjVDRZzb", name: "George" },      // Warm British narrator
    { id: "TxGEqnHWrfWFTfGW9XjX", name: "Josh" },        // Deep narrator
    { id: "pNInz6obpgDQGcFmaJgB", name: "Adam" },        // Deep narration
    { id: "ErXwobaYiN019PkySvjV", name: "Antoni" },      // Well-rounded narrator
  ];
  
  // Try to verify the first preferred voice exists
  try {
    const response = await fetch("https://api.elevenlabs.io/v1/voices", {
      headers: { "xi-api-key": apiKey },
    });
    
    if (response.ok) {
      const data = await response.json() as { voices: ElevenLabsVoice[] };
      
      // Look for documentary/narrator voices
      for (const preferred of preferredVoices) {
        const found = data.voices.find((v: ElevenLabsVoice) => v.voice_id === preferred.id);
        if (found) {
          return { id: found.voice_id, name: found.name };
        }
      }
      
      // Fallback: find any voice with "narrator" or "documentary" in description
      const narratorVoice = data.voices.find((v: ElevenLabsVoice) => {
        const desc = (v.labels?.description || v.labels?.use_case || '').toLowerCase();
        return desc.includes('narrator') || desc.includes('documentary');
      });
      
      if (narratorVoice) {
        return { id: narratorVoice.voice_id, name: narratorVoice.name };
      }
      
      // Last resort: use first available voice
      if (data.voices.length > 0) {
        return { id: data.voices[0].voice_id, name: data.voices[0].name };
      }
    }
  } catch (e) {
    console.warn("Could not fetch voice list, using default");
  }
  
  return preferredVoices[0];
}

async function synthesizeVoice(text: string, outputPath: string): Promise<void> {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) {
    throw new Error("ELEVENLABS_API_KEY not set. Add it in Settings > Developers.");
  }

  const voice = await findDocumentaryVoice(apiKey);
  console.log(`🎭 Using voice: ${voice.name}`);
  
  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice.id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": apiKey,
    },
    body: JSON.stringify({
      text,
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.65,
        similarity_boost: 0.75,
        style: 0.35,
        use_speaker_boost: true,
      },
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`ElevenLabs API error: ${error}`);
  }

  const audioBuffer = await response.arrayBuffer();
  await Bun.write(outputPath, audioBuffer);
}

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      handle: { type: "string", short: "h" },
      count: { type: "string", short: "c", default: "50" },
      "text-only": { type: "boolean", default: false },
      output: { type: "string", short: "o" },
    },
    allowPositionals: true,
  });

  const handle = values.handle;
  if (!handle) {
    console.error("Usage: bun run narrate.ts --handle <bluesky-handle>");
    console.error("Example: bun run narrate.ts --handle norvid-studies.bsky.social");
    process.exit(1);
  }

  const count = parseInt(values.count || "50");
  const textOnly = values["text-only"] || false;
  
  console.log(`🔭 Observing the digital wilderness of @${handle}...`);
  
  const posts = await fetchBlueskyFeed(handle, count);
  console.log(`📊 Collected ${posts.length} specimens for analysis`);
  
  const analysis = analyzeFeed(posts, handle);
  console.log(`🧬 Behavioral patterns mapped`);
  
  console.log(`✍️  Composing documentary narration...`);
  const narration = await generateNarration(analysis, posts);
  
  console.log(`\n${"─".repeat(60)}`);
  console.log(narration);
  console.log("─".repeat(60) + "\n");
  
  if (!textOnly) {
    const outputDir = "/home/workspace/Skills/tweetscape-narrator/output";
    await Bun.write(`${outputDir}/.gitkeep`, "");
    
    const safeHandle = handle.replace(/[^a-zA-Z0-9]/g, "_");
    const timestamp = new Date().toISOString().slice(0, 10);
    const outputPath = values.output || `${outputDir}/${safeHandle}_${timestamp}.mp3`;
    
    console.log(`🎙️  Synthesizing voice narration...`);
    await synthesizeVoice(narration, outputPath);
    console.log(`✅ Audio saved to: ${outputPath}`);
  }
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
