---
name: twitter-api
description: Post, quote, reply to, and delete X (Twitter) tweets via the local X CLI script using API keys. Use when the user asks to tweet, quote tweet, reply, or delete on X/Twitter.
metadata:
  author: 0.zo.computer
  category: Community
  display-name: Post to X (Twitter)
  emoji: 🐦
---

# X (Twitter) API CLI

Post, quote, reply to, and delete tweets using the local X CLI script in `Community/twitter-api/scripts/`.

## Setup

The USER must complete these steps in the X Developer Portal:

1. Sign in with their X account.
2. Create a new project (or use the default).
3. Create a new app under the project.
4. Change the app permissions to **Read & Write** before generating keys.
5. Go to the app's "Keys and Tokens" tab and generate:
   - API Key and Secret (Consumer Keys)
   - Access Token and Secret (User Context)

Then the USER must set secrets in [Settings > Developers](/settings#developers) or export them locally:
- `X_API_KEY`
- `X_API_KEY_SECRET` (or `X_API_SECRET`)
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET` (or `X_ACCESS_SECRET`)

Optional local setup: copy `scripts/.env.example` to `scripts/.env` and fill in values.

If required keys are missing, stop and ask the user to configure them before posting.

## Commands

Run from `Community/twitter-api/scripts/`:

```bash
bun x.ts post "Your tweet text here"
bun x.ts quote https://x.com/user/status/123 "Your commentary"
bun x.ts reply https://x.com/user/status/123 "Your reply text"
bun x.ts delete https://x.com/user/status/123
```

### Media

Attach media by repeating `--media`:

```bash
bun x.ts post --media /path/to/image.png "Caption"
bun x.ts quote https://x.com/user/status/123 --media /path/to/image.png "Commentary"
```

## Notes

- Max length is 280 characters. If over, trim before posting.
- Use actual line breaks in the shell for multi-paragraph tweets.
- Tweet IDs or full URLs are accepted for quote/reply/delete.
