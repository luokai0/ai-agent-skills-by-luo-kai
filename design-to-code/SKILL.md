---
name: design-to-code
description: Use when converting a design file, mockup, prototype, or design specification (Figma, Sketch, XD, screenshots, or design tokens) into production frontend UI code, or when reviewing an implementation for fidelity to its design.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Design To Code

## Purpose and boundaries

This skill turns approved visual designs into frontend components and pages that match the design's layout, typography, color, spacing, states, and responsive behavior, while fitting the target codebase's conventions. It covers translating designs into markup, styles, and component structure; mapping design tokens to the project's theme system; and reviewing an existing implementation against its design.

It does not cover: inventing product behavior the design does not specify, redesigning screens, backend data modeling, brand or copy decisions, accessibility sign-off (it flags issues; a human owns certification), or deploying changes.

## Inputs and assumptions

Before writing code, confirm you have:
- The design source (file link, export, or screenshots at 1x and 2x) and the specific frames or components in scope.
- Target framework, styling system, and component library already used in the repository. Inspect `package.json`, existing components, and the theme configuration. Do not introduce a new styling approach.
- Breakpoints the design covers. If only one viewport is provided, state that responsive behavior is unverified.
- Token source: whether the design uses named variables/styles or raw values.
- Interaction states provided (hover, focus, disabled, error, loading, empty). Missing states are listed as open questions, not invented.

Assume the design is the source of truth for visuals, and the existing codebase is the source of truth for conventions. When they conflict, prefer the codebase convention and report the deviation.

## Operating workflow

1. **Inventory.** List every frame and component in scope. Identify repeated patterns (buttons, cards, form fields) that already exist in the codebase.
2. **Map tokens.** Build a table: design variable to project token (color, spacing, radius, type scale, shadow). Reuse existing tokens. Only add a new token when no existing one fits, and flag it.
3. **Decompose.** Split the layout into components with clear props. Separate presentational components from data-fetching logic. A component should reflect one visual responsibility.
4. **Build structure first.** Write semantic markup (landmarks, headings in order, real buttons and links) before styling. Use flex or grid as the design's alignment implies.
5. **Apply styles.** Use token references only; no hardcoded hex values, pixel offsets, or font stacks where a token exists. Implement all provided states.
6. **Responsive pass.** Implement the provided breakpoints. Where none are given, use fluid widths and flag the gap.
7. **Verify** (see below), then report.

## Decision gates

- **Missing state or breakpoint:** Stop for that element, record it as an open question, and implement only a clearly labeled provisional version if the user approves.
- **Token conflict** (design value differs from nearest token by more than a visible step): ask whether to adopt the token or add a new one. Do not silently round.
- **New dependency** (icon set, animation library, layout primitive): require approval, state the reason, and check the project's existing packages first.
- **Design asset export** (images, SVG, fonts): confirm licensing and whether the asset should be checked into the repo or loaded from a CDN. Treat that choice as external-impacting.
- **Replacing existing components:** requires approval, since it affects other screens.

## Verification and evidence

Provide evidence, not assertions:
- Side-by-side screenshots at each provided breakpoint, compared against the design frame. Report the measured pixel differences for key elements (box size, gap, font size) using the design tool's inspect values.
- Spacing and typography checks: each margin, padding, gap, and font size on the design's spec sheet matches a token or the stated value.
- Keyboard walk-through: every interactive element reachable and visibly focused in logical order.
- Automated checks the project already runs (type checking, linting, unit and visual regression tests). Report the actual command output, not an expectation.
- Contrast: report measured ratios for text and essential UI colors against WCAG 2.2 thresholds, using a tool. Mark results as indicative; do not claim compliance.

Target a visual deviation of no more than 2 px on positioned elements and exact token usage for colors and type. Anything larger is listed explicitly.

## Failure handling

- If a screenshot comparison fails, identify the element, correct the cause, and re-run. Do not loosen the threshold to pass.
- If the design uses a value that cannot be expressed in the project's system, report the constraint and propose the closest option with its visual cost.
- If the codebase lacks a required primitive, stop and ask before building one.
- If verification tooling is unavailable, state which checks were not run. Never report a check as passed when it was not executed.

## Deliverable contract

Return:
1. Files changed or created, with paths.
2. Token mapping table, including any new tokens flagged for approval.
3. Component list with props and responsibilities.
4. Verification record: commands run, outcomes, screenshot comparisons, measured deviations.
5. Open questions: missing states, breakpoints, assets, and unresolved token conflicts.
6. Known deviations from the design, each with a reason.

Do not:
- Hardcode values where tokens exist.
- Add dependencies, global styles, or theme changes without approval.
- Modify shared components silently.
- Invent copy, data, or behavior not present in the design.
- Describe the implementation as matching the design without the verification record to support it.