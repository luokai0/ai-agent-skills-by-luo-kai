---
name: tweetscape-narrator
description: |
  David Attenborough-style nature documentary narration of social media feeds.
  Fetches posts from Bluesky, analyzes the "digital ecosystem," generates narration,
  synthesizes voice with ElevenLabs, and renders a documentary-style video with Remotion.
compatibility: Created for Zo Computer
metadata:
  author: rc2.zo.computer
  category: Community
  display-name: Tweetscape Narrator
  emoji: 🎬
---
# Tweetscape Narrator

Creates nature documentary-style videos about social media users' feeds, narrated in the style of David Attenborough.

## Quick Start (Full Video)

```bash
cd Skills/tweetscape-narrator
bun run scripts/generate-video.ts --handle norvid-studies.bsky.social
```

This runs the full pipeline:
1. **Ingest** — Fetch posts, capture screenshots
2. **Script** — Generate structured narration with scene markers
3. **Record** — Synthesize voice with ElevenLabs (includes timestamps)
4. **Render** — Create documentary video with Remotion

## Interactive Workflow (Recommended)

For better results, run each step manually with review:

```bash
# 1. Ingest posts and screenshots
bun run scripts/ingest.ts --handle <handle> --count 30

# 2. Generate narration script
bun run scripts/script-narration.ts --manifest <dir>/manifest.json

# 3. ⭐ CREATE STORYBOARD FOR REVIEW (important!)
#    Write a storyboard.md file in the output directory with:
#    - Each scene's narration text as a blockquote
#    - Screenshots embedded as images using relative paths: ![](./screenshots/post_005.png)
#    - Scene metadata (visual direction, featured posts)
#    
#    This allows visual review of how narration aligns with screenshots
#    before spending time/money on audio synthesis.
#    
#    Review the storyboard.md, then revise script.json if needed
#    (especially intro/conclusion to avoid repetitive phrasing across videos)

# 4. Record audio with timestamps
bun run scripts/record-audio.ts --script <dir>/script.json

# 5. Render video
bun run scripts/render-video.ts --project-dir <dir>
```

### Storyboard Format

The storyboard.md should look like this:

```markdown
# 🎬 The Digital Habitat of <name>

**Subject:** @handle  
**Estimated Duration:** ~90 seconds  
**Scenes:** 5

---

## Scene 1: INTRO

**Visual Direction:** Wide shot of profile

![](./screenshots/profile.png)

> *"Narration text for intro scene..."*

---

## Scene 2: <behavior_name>

**Visual Direction:** Close-up on posts

![](./screenshots/post_005.png)

> *"Narration text for this scene..."*

**Featured Posts:**
1. *"Post text excerpt..."*
```

This lets you see exactly which screenshots will appear with which narration, and catch issues before audio/video generation.

## Audio Only (Original Mode)

```bash
bun run scripts/narrate.ts --handle someone.bsky.social
```

Add `--text-only` to skip voice synthesis.

## Options

| Flag | Description |
|------|-------------|
| `--handle, -h` | Bluesky handle (required) |
| `--count, -c` | Number of posts to fetch (default: 30) |
| `--skip-screenshots` | Skip screenshot capture |
| `--audio-only` | Stop after audio (skip video render) |
| `--output, -o` | Output path for final video |

## Requirements

- `ELEVENLABS_API_KEY` — For voice synthesis. Add in Settings > Developers.
- `ANTHROPIC_API_KEY` — For narration generation (already configured)

## Output Structure

```
output/<handle>_<timestamp>/
├── manifest.json          # Ingested posts + metadata
├── screenshots/           # Post screenshots
├── script.json           # Structured narration
├── storyboard.md         # Visual review document (create manually)
├── narration.mp3         # Voice audio
├── narration-timestamps.json  # Word-level timing
└── video.mp4             # Final documentary video
```

## Video Specs

- Resolution: 1920x1080 (16:9)
- Frame rate: 30fps
- Format: MP4 (H.264)
- Audio: AAC

## Tips for Good Results

1. **Vary intro/conclusion phrasing** — Check previous scripts to avoid repetitive openings like "In the vast digital ecosystem..." 
2. **Review storyboard before audio** — ElevenLabs costs money; catch script issues early
3. **Match screenshots to narration** — The `relatedPostIndices` in script.json control which posts appear during each scene

## Future Ideas

- [ ] X/Twitter support
- [ ] Custom voice selection
- [ ] Topic-based narration (narrate a hashtag, not a user)
- [ ] Multi-user "ecosystem" view
- [ ] Background music layer
- [ ] Auto-generate storyboard.md from script.json
