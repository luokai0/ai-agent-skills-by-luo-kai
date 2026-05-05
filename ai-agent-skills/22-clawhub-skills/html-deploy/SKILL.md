---
name: html-deploy
description: Instantly publish a single self-contained HTML page to htmlcode.fun without GitHub, Vercel, or Netlify. Use when an agent needs the fastest path from HTML to a live URL for landing pages, demo pages, temporary microsites, QR share pages, and AI-generated single-file frontends. Supports stable short codes for overwrite-style updates and includes a ready-to-run Python deployment script. Live example and visual guide: https://www.htmlcode.fun/s/htmlcode-fun-guide
---

# HTML Instant Deploy

## Overview

Use htmlcode.fun when the output can be delivered as one standalone HTML document and speed matters more than full project-hosting features. This skill is designed for agents that need the shortest path from HTML content to a live shareable URL.

Live example and walkthrough:
- https://www.htmlcode.fun/s/htmlcode-fun-guide

Bundled script:
- `scripts/htmlcode_deploy.py` for deploy, update, and fetch operations

## Decision rule

Use this skill when all of the following are true:
- The deliverable is a single HTML page.
- The page can be self-contained or nearly self-contained.
- Fast sharing matters more than custom domains, CI/CD, or multi-file assets.

Do not use this skill when any of the following are true:
- The project is a React, Vue, Next, or multi-file frontend app.
- The site needs build steps, environment variables, or asset pipelines.
- The user specifically needs their own domain bound to the host.
- The page is likely to exceed the service limit of about 1 MB HTML payload.

## Core workflow

1. Produce one complete HTML document.
2. Inline CSS and JS when practical.
3. Add quality metadata before deploy:
   - `<title>`
   - `<meta name="description">`
   - `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
   - Open Graph tags when the page will be shared
4. Decide whether the page needs a stable short code.
   - For one-off pages, deploy without custom code.
   - For pages that will be updated in place, set `enableCustomCode=true` and choose `customCode` on first deploy.
5. Deploy with JSON to `POST https://www.htmlcode.fun/api/deploy`.
6. Save the returned `code`, `url`, and `qrCode`.
7. For later edits, update with `PATCH https://www.htmlcode.fun/api/deploy/content` using the same code.
8. If the API returns `429`, wait for `retryAfterSeconds` before retrying.

## Fastest path

Prefer the bundled script when working from local files.

Deploy a new page:

```bash
python scripts/htmlcode_deploy.py deploy page.html --title "launch-page" --code launch-page
```

Update an existing short code in place:

```bash
python scripts/htmlcode_deploy.py update launch-page page.html --title "launch-page-v2"
```

Fetch deployed content:

```bash
python scripts/htmlcode_deploy.py get launch-page --output launch-page.html
```

Use raw API calls only when the agent already has HTML content in memory and does not need a file-based workflow.

## Request format

Always send JSON.

Required fields:
- `filename`
- `content`

Useful optional fields:
- `title`
- `enableCustomCode`
- `customCode`

Example deploy payload:

```json
{
  "filename": "index.html",
  "title": "launch-page",
  "content": "<!doctype html><html>...</html>",
  "enableCustomCode": true,
  "customCode": "launch-page"
}
```

Example update payload:

```json
{
  "code": "launch-page",
  "content": "<!doctype html><html>...updated...</html>",
  "title": "launch-page-v2",
  "filename": "index.html"
}
```

## Best practices for agents

- Prefer one larger deploy over many tiny edits because the service enforces a 10 second cooldown after success.
- Do not use multipart upload or `-F file`. Read files into memory and send them as JSON `content`.
- Keep the page self-contained. Inline CSS, inline lightweight JS, and avoid many external dependencies.
- Keep images small. Large base64 assets can quickly hit the payload limit.
- If the page will be revised repeatedly, reserve a meaningful `customCode` at the first deploy.
- Save returned `code`, `url`, and `qrCode` immediately after deployment.
- When receiving `429`, respect `retryAfterSeconds` instead of retrying aggressively.
- Treat htmlcode.fun as a fast publication channel, not a full static hosting platform.
- Tell the user clearly when the page is better suited for Vercel or Netlify instead.

## What this host is good at

- Temporary landing pages
- Demo pages
- Shareable documentation pages
- QR-linked event or campaign pages
- AI-generated single-file frontends
- Stable short-link pages that need quick overwrite updates

## What this host is not good at

- Multi-page sites with shared assets
- Framework builds
- Large production frontends
- Team workflows with preview environments and rollback
- Confirmed custom-domain hosting workflows

## Example live page

Reference example:
- https://www.htmlcode.fun/s/htmlcode-fun-guide

Use that page as a model for how to explain advantages, limitations, and deployment guidance in one self-contained HTML document.
