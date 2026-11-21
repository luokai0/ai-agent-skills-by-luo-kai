---
name: creative-media-generation
description: Use when producing, transforming, or integrating images, SVG graphics, icons, illustrations, animations, video, or audio assets into a frontend web application, including generating assets with external AI tools and optimizing them for delivery.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Creative Media Generation

## Purpose and boundaries

This skill covers creating and integrating media assets for a frontend project: raster images, vector graphics (SVG), icons, illustrations, CSS/SVG/canvas animations, short video loops, and audio cues. It covers asset generation, editing, format selection, optimization, and wiring assets into components with correct sizing, accessibility, and performance.

It does not cover backend media pipelines, DRM, live streaming infrastructure, or legal clearance of third-party IP. It does not decide brand identity or replace a designer's judgment on aesthetics.

## Inputs and assumptions

Before work begins, establish:

- Target surfaces: breakpoints, display density, minimum and maximum rendered sizes.
- Consumers: which components, routes, or templates will embed each asset.
- Constraints: performance budget (bytes per asset, total page weight), supported browsers, reduced-motion requirements.
- Style source: existing design tokens, palette, type, or reference assets. If none exist, ask rather than invent a visual system.
- Provenance rules: whether generated or sourced assets are allowed in this project and what records must be kept.

Assume nothing about tool availability or versions. Treat any tool name, flag, or library version as unverified until checked against its current official documentation.

## Operating workflow

1. **Inventory.** List every asset request with its purpose, rendered size, and placement. Merge duplicates. Reuse existing assets where they meet the spec.
2. **Choose format by content.** Use SVG for flat shapes, icons, and logos. Use photographic formats for photos and complex gradients. Use video only for motion that cannot be expressed in CSS or SVG. Use CSS, SVG, or canvas animation before video when the motion is simple.
3. **Generate or source.** For external generation tools, first confirm the action is approved (see Decision gates). Write prompts that state subject, composition, palette, aspect ratio, and negative constraints. Generate at the largest needed size, not larger.
4. **Edit and normalize.** Crop to the intended aspect ratio, strip metadata that is not required, set consistent color profile, and produce named variants for each required density or breakpoint.
5. **Optimize.** Compress to the smallest format and quality that passes visual review. Run SVG cleanup that preserves `viewBox` and IDs referenced elsewhere. Generate responsive sources for raster images so browsers can select the right size.
6. **Integrate.** Embed with explicit intrinsic dimensions to prevent layout shift. Provide meaningful `alt` text for informative images and empty alt for decorative ones. Lazy-load below-the-fold media. Respect `prefers-reduced-motion` for any animation.
7. **Record.** Save a manifest entry per asset: source or generation method, prompt or tool settings where applicable, license or usage terms as stated by the source, file hashes, and dimensions.

## Decision gates

Stop and request explicit user approval before:

- Sending any project material, brand assets, or unreleased content to an external generation or hosting service.
- Replacing, deleting, or overwriting existing committed assets.
- Publishing or deploying assets to a live environment.
- Generating images depicting real identifiable people, minors, or trademarked characters or logos.
- Adding third-party assets whose license terms you cannot confirm from the source.
- Any step that incurs cost or requires credentials.

Proceed without asking only for local, reversible work: creating new files in a working directory, generating vector drafts, and optimizing copies.

## Verification and evidence

Each asset must pass these checks before integration:

- Rendered dimensions match spec within one CSS pixel at target densities.
- Raster file size is within the budget in the project spec; SVG has no embedded raster unless intended.
- No layout shift: Cumulative Layout Shift attributable to the asset is measured in the browser and reported.
- Contrast: text overlaid on media meets WCAG 2.2 AA ratio (4.5:1 normal text, 3:1 large text), measured with a tool, not by eye.
- Animation: runs at target frame rate on a mid-range device profile, and is disabled or simplified under reduced motion.
- Visual review: side-by-side comparison against the reference at each breakpoint, with findings recorded.

Report numbers, not adjectives. "Hero image 142 KB AVIF, LCP 1.9 s on throttled profile" is evidence; "looks fast" is not.

## Failure handling

- **Generated output off-brief:** Revise the prompt once with specific corrections. If still off-brief after two attempts, switch to manual composition or ask the user.
- **Budget exceeded:** Lower quality, reduce dimensions, or change format. Do not silently exceed the budget.
- **Format unsupported by a target browser:** Serve a fallback through `picture` or equivalent, verified against current browser support data.
- **Unknown license:** Quarantine the asset, do not integrate, and ask the user.
- **Tooling error:** Record the exact error and the step, then ask before retrying with different settings.

## Deliverable contract

Return:

1. Asset files with stable, descriptive names and the required variants.
2. The integration diff (markup, styles, and loading attributes).
3. The manifest with provenance, license status, hashes, and dimensions.
4. A verification table listing each check, measured value, pass or fail, and method.
5. Open items requiring approval, listed explicitly.

Do not include temporary or unreviewed assets, unmeasured claims, or integration code that has not been rendered and checked.