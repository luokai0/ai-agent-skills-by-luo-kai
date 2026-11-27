#!/usr/bin/env bun

import OAuth from "oauth-1.0a";
import CryptoJS from "crypto-js";
import path from "path";

// --- Config ---

interface XConfig {
  apiKey: string;
  apiSecret: string;
  accessToken: string;
  accessSecret: string;
}

function getConfig(): XConfig {
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_KEY_SECRET || process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_TOKEN_SECRET || process.env.X_ACCESS_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error("Missing required environment variables:");
    if (!apiKey) console.error("  - X_API_KEY");
    if (!apiSecret) console.error("  - X_API_KEY_SECRET (or X_API_SECRET)");
    if (!accessToken) console.error("  - X_ACCESS_TOKEN");
    if (!accessSecret) console.error("  - X_ACCESS_TOKEN_SECRET (or X_ACCESS_SECRET)");
    console.error("\nSet them in .env or export them to your shell.");
    process.exit(1);
  }

  return { apiKey, apiSecret, accessToken, accessSecret };
}

function createOauth(config: XConfig) {
  return new OAuth({
    consumer: { key: config.apiKey, secret: config.apiSecret },
    signature_method: "HMAC-SHA1",
    hash_function: (baseString, key) =>
      CryptoJS.HmacSHA1(baseString, key).toString(CryptoJS.enc.Base64),
  });
}

// --- Helpers ---

function extractTweetId(input: string): string {
  const match = input.match(/\/status\/(\d+)/);
  return match ? match[1] : input;
}

function parseTextAndMedia(args: string[]) {
  const mediaPaths: string[] = [];
  let i = 0;
  while (i < args.length) {
    const token = args[i];

    if (token === "--media") {
      const pathArg = args[i + 1];
      if (!pathArg) {
        console.error("Usage error: --media must be followed by a file path.");
        process.exit(1);
      }
      mediaPaths.push(pathArg);
      i += 2;
      continue;
    }

    return {
      text: args.slice(i).join(" "),
      mediaPaths,
    };
  }

  return { text: "", mediaPaths };
}

async function uploadMediaPath(filePath: string, config: XConfig) {
  const resolved = path.isAbsolute(filePath) ? filePath : path.resolve(filePath);
  const arrayBuffer = await Bun.file(resolved).arrayBuffer();
  const mediaData = Buffer.from(arrayBuffer).toString("base64");

  const oauth = createOauth(config);
  const token = { key: config.accessToken, secret: config.accessSecret };
  const url = "https://upload.twitter.com/1.1/media/upload.json";
  const requestData = { url, method: "POST" as const, data: { media_data: mediaData } };
  const authHeader = oauth.toHeader(oauth.authorize(requestData, token));
  const body = new URLSearchParams({ media_data: mediaData });

  const response = await fetch(url, {
    method: "POST",
    headers: { ...authHeader, "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`X API Error (media upload): ${JSON.stringify(error, null, 2)}`);
  }

  const data = await response.json();
  return data.media_id_string;
}

async function uploadMediaPaths(paths: string[], config: XConfig) {
  const mediaIds: string[] = [];
  for (const mediaPath of paths) {
    mediaIds.push(await uploadMediaPath(mediaPath, config));
  }
  return mediaIds;
}

// --- API ---

interface TweetOptions {
  text: string;
  quoteTweetId?: string;
  replyToId?: string;
  mediaIds?: string[];
}

async function postTweet(options: TweetOptions, config: XConfig) {
  const oauth = createOauth(config);
  const token = { key: config.accessToken, secret: config.accessSecret };
  const url = "https://api.twitter.com/2/tweets";
  const requestData = { url, method: "POST" as const };
  const authHeader = oauth.toHeader(oauth.authorize(requestData, token));

  const body: Record<string, unknown> = { text: options.text };
  if (options.quoteTweetId) {
    body.quote_tweet_id = options.quoteTweetId;
  }
  if (options.replyToId) {
    body.reply = { in_reply_to_tweet_id: options.replyToId };
  }
  if (options.mediaIds && options.mediaIds.length) {
    body.media = { media_ids: options.mediaIds };
  }

  const response = await fetch(url, {
    method: "POST",
    headers: { ...authHeader, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`X API Error: ${JSON.stringify(error, null, 2)}`);
  }

  return response.json();
}

async function deleteTweet(tweetId: string, config: XConfig) {
  const oauth = createOauth(config);
  const token = { key: config.accessToken, secret: config.accessSecret };
  const url = `https://api.twitter.com/2/tweets/${tweetId}`;
  const requestData = { url, method: "DELETE" as const };
  const authHeader = oauth.toHeader(oauth.authorize(requestData, token));

  const response = await fetch(url, {
    method: "DELETE",
    headers: { ...authHeader },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`X API Error: ${JSON.stringify(error, null, 2)}`);
  }

  return response.json();
}

// --- CLI ---

const HELP = `
x-cli - Simple X (Twitter) posting CLI

Usage:
  x post [--media <path>] <text>                          Post a tweet (attach images by repeating --media)
  x quote <url> [--media <path>] <text>                    Quote tweet with commentary
  x reply <url> [--media <path>] <text>                    Reply to a tweet
  x delete <url>                                           Delete a tweet
  x help                                                   Show this help

Examples:
  x post "Hello from CLI"
  x post --media /home/workspace/Images/pegasus_crossroads.png "Zo Computer + art"
  x quote https://x.com/user/status/123 "Great point!"
  x reply https://x.com/user/status/123 "Thanks for sharing"
  x delete https://x.com/user/status/123

Note: Use actual line breaks in your text:
  x quote https://x.com/user/status/123 "First paragraph.

Second paragraph."

Max length: 280 characters
`;

const args = process.argv.slice(2);
const command = args[0];

if (!command || command === "help" || command === "-h") {
  console.log(HELP);
  process.exit(0);
}

const config = getConfig();

function assertText(text: string, usage: string) {
  if (!text) {
    console.error(usage);
    process.exit(1);
  }
  if (text.length > 280) {
    console.error(`Error: Tweet is ${text.length} chars (max 280)`);
    console.error(`You need to cut ${text.length - 280} characters.`);
    process.exit(1);
  }
}

async function run() {
  if (command === "post") {
    const { text, mediaPaths } = parseTextAndMedia(args.slice(1));
    assertText(text, 'Usage: x post "Your tweet here"');

    const mediaIds = mediaPaths.length ? await uploadMediaPaths(mediaPaths, config) : [];

    console.log(`Posting: "${text}"`);
    try {
      const result = await postTweet({ text, mediaIds }, config);
      console.log("✓ Posted!");
      console.log(`  https://x.com/i/status/${result.data.id}`);
    } catch (error) {
      console.error("✗ Failed:", error);
      process.exit(1);
    }
  } else if (command === "quote") {
    const tweetIdOrUrl = args[1];
    if (!tweetIdOrUrl) {
      console.error('Usage: x quote <tweet_id|url> "Your commentary here"');
      process.exit(1);
    }

    const { text, mediaPaths } = parseTextAndMedia(args.slice(2));
    assertText(text, 'Usage: x quote <tweet_id|url> "Your commentary here"');

    const quoteTweetId = extractTweetId(tweetIdOrUrl);
    const mediaIds = mediaPaths.length ? await uploadMediaPaths(mediaPaths, config) : [];

    console.log(`Quoting tweet ${quoteTweetId}: "${text}"`);
    try {
      const result = await postTweet({ text, quoteTweetId, mediaIds }, config);
      console.log("✓ Quote tweeted!");
      console.log(`  https://x.com/i/status/${result.data.id}`);
    } catch (error) {
      console.error("✗ Failed:", error);
      process.exit(1);
    }
  } else if (command === "reply") {
    const tweetIdOrUrl = args[1];
    if (!tweetIdOrUrl) {
      console.error('Usage: x reply <tweet_id|url> "Your reply here"');
      process.exit(1);
    }

    const { text, mediaPaths } = parseTextAndMedia(args.slice(2));
    assertText(text, 'Usage: x reply <tweet_id|url> "Your reply here"');

    const replyToId = extractTweetId(tweetIdOrUrl);
    const mediaIds = mediaPaths.length ? await uploadMediaPaths(mediaPaths, config) : [];

    console.log(`Replying to tweet ${replyToId}: "${text}"`);
    try {
      const result = await postTweet({ text, replyToId, mediaIds }, config);
      console.log("✓ Replied!");
      console.log(`  https://x.com/i/status/${result.data.id}`);
    } catch (error) {
      console.error("✗ Failed:", error);
      process.exit(1);
    }
  } else if (command === "delete") {
    const tweetIdOrUrl = args[1];

    if (!tweetIdOrUrl) {
      console.error("Usage: x delete <tweet_id|url>");
      process.exit(1);
    }

    const tweetId = extractTweetId(tweetIdOrUrl);

    console.log(`Deleting tweet ${tweetId}...`);

    try {
      const result = await deleteTweet(tweetId, config);
      if (result.data?.deleted) {
        console.log("✓ Deleted!");
      } else {
        console.log("✗ Tweet may not have been deleted:", result);
      }
    } catch (error) {
      console.error("✗ Failed:", error);
      process.exit(1);
    }
  } else {
    console.error(`Unknown command: ${command}`);
    process.exit(1);
  }
}

await run();

