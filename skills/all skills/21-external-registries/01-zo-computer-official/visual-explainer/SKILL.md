---
name: visual-explainer
description: Build polished visual explainers as zo.space pages. Creates public routes at /explain/[slug] and keeps each explainer shareable at a stable URL.
compatibility: Created for Zo Computer
metadata:
  author: skeletorjs
---

# Visual Explainer (Zo)

Use this skill when the user asks for a visual explanation, architecture breakdown, implementation walkthrough, roadmap, comparison, or technical explainer page.

This Zo-native version publishes explainers to zo.space route paths:
- `/explain/<slug>` for each explainer page
- optional `/explain` index page that links to all explainers

## Required Behavior

1. Always publish explainers as zo.space page routes via `update_space_route`.
2. Route path format is always `/explain/<slug>`.
3. Default to `public=True` unless the user explicitly asks for private visibility.
4. After each publish/update, run `get_space_errors` and fix issues before proceeding.
5. Respond with the live URL: `https://<handle>.zo.space/explain/<slug>`.

## Workflow

1. Convert the requested title/topic into a URL-safe slug.
2. Create or update route `/explain/<slug>` with a self-contained React page.
3. Use a clear visual system:
- Distinctive typography (avoid default stacks)
- Strong color direction with CSS variables
- At least one meaningful visual (diagram section, timeline, system map, or comparison grid)
- Mobile-responsive layout
4. If this is part of a series, also update `/explain` with links to recent explainers.
5. Validate with `get_space_errors`.

## Route Template

Start from `assets/explainer-page.tsx` and adapt content per topic.

## Fast Slug Helper

Use `scripts/slugify.sh`:

```bash
bash Skills/visual-explainer/scripts/slugify.sh "My Explainer Title"
```
