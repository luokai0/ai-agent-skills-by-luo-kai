---
author: luo-kai
name: tweetclaw
description: "OpenClaw plugin for X/Twitter automation. Post tweets, reply, like, retweet, follow, DM, search, extract data, run giveaways, monitor accounts, automate flows via Xquik. 97 endpoints, 2 tools (explore + tweetclaw), 2 commands (/xstatus, /xtrends), background event poller."
homepage: https://xquik.com
read_when:
  - Posting, replying, liking, retweeting, or following on X/Twitter
  - Searching tweets or looking up X/Twitter users
  - Running giveaway draws from tweet replies
  - Monitoring X/Twitter accounts for new activity
  - Composing algorithm-optimized tweets
  - Extracting bulk data from X/Twitter (followers, replies, communities)
  - Downloading tweet media or uploading images
  - Sending DMs or updating X/Twitter profile
metadata: {"openclaw":{"emoji":"🐦","primaryEnv":"XQUIK_API_KEY","requires":{"env":["XQUIK_API_KEY"]},"tags":["twitter","x","automation","social-media","tweets","scraping","giveaway","monitoring","rest-api"]}}
---

# TweetClaw

OpenClaw plugin for X/Twitter automation powered by Xquik. Install via:

```bash
openclaw plugins install @xquik/tweetclaw
```

## When to Use

Use TweetClaw when the user wants to:

- Post tweets, reply to tweets, or delete tweets
- Like, retweet, or follow/unfollow users
- Send DMs on X/Twitter
- Update their X profile, avatar, or banner
- Upload media and tweet with images
- Search tweets or look up user profiles
- Extract bulk data (followers, replies, communities, spaces)
- Run giveaway draws from tweet replies
- Monitor X accounts for new activity
- Compose algorithm-optimized tweets
- Analyze a user's writing style
- Check trending topics on X
- Download tweet media (images, videos, GIFs)
- Set up Telegram alerts for monitor events
- Create and manage automation flows (triggers, steps, test runs)
- Open and manage support tickets
- Read X Articles (long-form posts)

Do NOT use TweetClaw for browsing X in a browser, analytics dashboards, scheduling future posts, or managing X ads.

## Configuration

### API key mode (full access)

```bash
openclaw config set plugins.entries.tweetclaw.config.apiKey 'xq_YOUR_KEY'
```

Get a key at [dashboard.xquik.com](https://dashboard.xquik.com/).

### MPP mode (no account, pay-per-use via Tempo/USDC)

```bash
npm i mppx viem
openclaw config set plugins.entries.tweetclaw.config.tempoPrivateKey '0xYOUR_KEY'
```

MPP gives agents access to 7 read-only X-API endpoints without any account or subscription. The mppx SDK handles HTTP 402 payment challenges automatically.

## Tools

TweetClaw registers 2 tools that cover the entire Xquik API (97 endpoints):

### `explore` (free, no network)

Search the API spec to find endpoints. No API calls are made.

Example: "What endpoints are available for tweet composition?"

The agent writes an async arrow function that filters the in-memory endpoint catalog:

```javascript
async () => spec.endpoints.filter(e => e.category === 'composition')
```

### `tweetclaw` (execute API calls)

Execute authenticated API calls. Auth is injected automatically.

Example: "Post a tweet saying 'Hello from TweetClaw!'"

```javascript
async () => {
  const { accounts } = await xquik.request('/api/v1/x/accounts');
  return xquik.request('/api/v1/x/tweets', {
    method: 'POST',
    body: { account: accounts[0].xUsername, text: 'Hello from TweetClaw!' }
  });
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/xstatus` | Account info, subscription status, usage |
| `/xtrends` | Trending topics from curated sources |
| `/xtrends tech` | Trending topics filtered by category |

## Event Notifications

When polling is enabled (default), TweetClaw checks for new events every 60 seconds:

- Monitor alerts: new tweets, replies, quotes, retweets from monitored accounts
- Follower changes: gained or lost followers on monitored accounts

## Common Workflows

### Post a tweet

```
You: "Post a tweet saying 'Hello from TweetClaw!'"
Agent uses tweetclaw -> finds connected account, posts tweet
```

### Reply to a tweet

```
You: "Reply 'Great thread!' to this tweet: https://x.com/user/status/123"
Agent uses tweetclaw -> posts reply with reply_to_tweet_id
```

### Like, retweet, follow

```
You: "Like and retweet this tweet, then follow the author"
Agent uses tweetclaw -> likes tweet, retweets, looks up user ID, follows
```

### Send a DM

```
You: "DM @username saying 'Hey, let's collaborate!'"
Agent uses tweetclaw -> looks up user ID, sends DM
```

### Update profile

```
You: "Change my bio to 'Building cool stuff' and update my avatar"
Agent uses tweetclaw -> PATCH /api/v1/x/profile, PATCH /api/v1/x/profile/avatar
```

### Upload media and tweet with image

```
You: "Tweet 'Check this out!' with this image: https://example.com/photo.jpg"
Agent uses tweetclaw -> uploads media, posts tweet with media_ids
```

### Search tweets

```
You: "Search tweets about AI agents"
Agent uses tweetclaw -> calls search endpoint with query
```

### Run a giveaway draw

```
You: "Pick 3 random winners from replies to this tweet: https://x.com/..."
Agent uses tweetclaw -> creates draw with filters
```

### Extract bulk data

```
You: "Extract the last 1000 followers of @elonmusk"
Agent uses tweetclaw -> estimates cost, creates extraction job
```

### Monitor an account

```
You: "Monitor @elonmusk for new tweets and follower changes"
Agent uses tweetclaw -> creates monitor with event types
```

### Download tweet media

```
You: "Download all media from this tweet"
Agent uses tweetclaw -> returns gallery URL with all media
```

### Compose an optimized tweet (free)

```
You: "Help me write a tweet about our product launch"
Agent uses tweetclaw -> 3-step compose/refine/score workflow
```

### Analyze writing style (free)

```
You: "Analyze @username's tweet style"
Agent uses tweetclaw -> returns style analysis with tone, patterns, metrics
```

### Browse trending topics (free)

```
You: "What's trending on X right now?"
Agent uses tweetclaw -> returns curated trending topics from 7 sources
```

### Create an automation flow (free)

```
You: "Create an automation that sends a DM when I get a new follower"
Agent uses tweetclaw -> creates flow with monitor_event trigger, adds send_dm step, tests it
```

### Read an X Article

```
You: "Get the full article from this tweet: https://x.com/user/status/123"
Agent uses tweetclaw -> calls /api/v1/x/articles/:tweetId, returns title, body, images
```

### Open a support ticket (free)

```
You: "Open a support ticket about my monitor not working"
Agent uses tweetclaw -> creates ticket with subject and description
```

## API Categories

| Category | Examples | Free |
|----------|---------|------|
| Write Actions | Post tweets, reply, like, retweet, follow, DM, update profile | No |
| Media | Upload media, download tweet media | No |
| Twitter | Search tweets, look up users, check follows | No |
| Composition | Compose, refine, score tweets; manage drafts | Yes |
| Styles | Analyze tweet styles, compare, performance | Mixed |
| Extraction | Reply/follower/community extraction (20 tools) | No |
| Draws | Giveaway draws, export results | No |
| Monitoring | Create monitors, view events, webhooks | No |
| Automations | Create flows, add steps, test runs, inbound webhooks | Yes |
| Account | API keys, subscription, connected X accounts | Yes |
| Trends | X trending topics, curated radar from 7 sources | Mixed |
| Support | Create tickets, reply, track status | Yes |

## Pricing

MPP pay-per-use (no account): 7 read-only X-API endpoints via Tempo (USDC) - tweet lookup ($0.0003), tweet search ($0.0003/tweet), user lookup ($0.00036), follower check ($0.002), article ($0.002), media download ($0.0003/media), trends ($0.0009).

Free tier (API key, no subscription): tweet composition, style analysis, drafts, curated radar, account management, integrations, automations (create/test), support tickets.

Subscription ($20/month): write actions, search, article lookup, media, extractions, draws, monitors, X trending, flow activation (2 free, 10 subscriber).

When a paid endpoint returns 402, TweetClaw provides a checkout URL.

## Tips

- Use `explore` first to discover endpoints before calling `tweetclaw` - saves tokens and avoids guessing
- Free endpoints (compose, styles, radar, drafts) work without a subscription - always try them first
- Never combine free and paid API calls in the same `Promise.all` - a 402 on one call kills all results
- For write actions (post, like, follow, DM), always pass the `account` parameter with the X username
- Follow/unfollow/DM require a numeric user ID - look up the user first via `/api/v1/x/users/:username`
- On 402 errors, call `POST /api/v1/subscribe` to get a checkout URL instead of giving up
- Use `/xstatus` to quickly check subscription and usage without invoking the AI agent
- The compose workflow (compose/refine/score) is free and helps draft high-engagement tweets
