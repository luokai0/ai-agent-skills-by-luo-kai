---
name: ui-visual-design
description: Use when implementing or revising the visual layer of a user interface in code, including typography scales, spacing, color tokens, contrast, elevation, layout grids, responsive breakpoints, component states, and dark mode.
author: Luo Kai
provenance: original
version: 1.1.1
---

# UI Visual Design

## Purpose and boundaries

This skill turns approved visual intent into consistent, verifiable frontend styling. It covers design tokens, type, spacing, color, surfaces, layout, responsive behavior, and component visual states.

In scope: translating mockups or style rules into tokens and CSS or component styles; auditing existing UI for inconsistency and contrast failures; defining state styles (hover, focus, active, disabled, error, loading); adapting layouts across viewport widths.

Out of scope: brand strategy, creating new logos or illustrations, user research, information architecture, backend logic, and rewriting application behavior. If the request requires those, state the gap and stop at the visual boundary.

## Inputs and assumptions

Before editing, confirm:

1. The source of truth: a design file, a style guide, an existing token set, or a screenshot. If none exists, derive a minimal token set from the current code and label it as derived.
2. Target platforms and minimum browser or device support.
3. The styling stack in use (plain CSS, a preprocessor, utility classes, or CSS-in-JS). Do not assume one.
4. Whether dark mode, reduced motion, and text scaling must be supported.

Record assumptions explicitly in the work summary.

## Operating workflow

1. Inventory. List existing color values, font sizes, spacing values, radii, and shadows. Count distinct values. Values outnumbering the intended scale signal drift.
2. Define tokens. Map primitives (raw values) to semantic roles (for example, surface, text-primary, text-muted, border-subtle, accent, danger). Components reference semantic tokens only.
3. Type scale. Use a constrained ratio or explicit steps (for example, 12, 14, 16, 20, 24, 32, 40 px). Pair size with line height and weight as a unit. Keep body line length near 45 to 85 characters.
4. Spacing. Use one base unit (commonly 4 or 8 px) and derive all gaps and padding from it.
5. Color. Build neutral ramps plus a small number of accent ramps. Verify each text/background pair (see Verification).
6. Components. Implement all states: default, hover, focus-visible, active, disabled, error, loading, empty. Focus indicators must be visible and not removed.
7. Responsive. Adjust layout at a few breakpoints chosen from content, not device names. Test at narrow, medium, and wide widths, plus 200% text zoom.
8. Motion. Keep transitions short and purposeful. Respect the user's reduced-motion preference.
9. Migrate incrementally. Replace hard-coded values screen by screen rather than in one sweeping change.

## Decision gates

- Proceed to tokens only if the source of truth is identified or derived values are accepted by the requester.
- Do not introduce a new color, font, or radius outside the approved set without confirmation.
- Use a new breakpoint only when content breaks at the current set.
- Choose a fixed size only for non-text decoration; text sizes should be relative to user settings where the platform allows.
- Stop and request approval before: changing shared tokens that affect multiple products, deleting or renaming widely used component classes, altering brand assets, modifying production theme configuration, or merging or publishing changes to a shared branch. These are destructive or externally visible and require explicit approval.

## Verification and evidence

Measurable checks, all required before reporting completion:

- Contrast: normal text at least 4.5:1; large text (24 px regular or 18.66 px bold and above) and essential non-text UI boundaries and icons at least 3:1 against adjacent colors, per WCAG 2.2. Report the measured ratios for every changed pair, including dark mode.
- Hard-coded values: zero new raw hex, px, or font-size literals in components where a token exists. Report the count before and after.
- Focus: every interactive element shows a visible focus indicator with at least 3:1 contrast against adjacent colors.
- Layout: no horizontal scrolling at 320 CSS px width; no text clipping at 200% zoom.
- Visual regression: capture before and after screenshots for each changed screen at the chosen breakpoints, and list any intended differences.
- Tooling: run the project's existing linter, type checker, and visual or accessibility checks. Record the commands used. If a tool's current options or versions are uncertain, check its official documentation before relying on them.

Do not claim compliance with any standard or law. Report measured results only.

## Failure handling

- Contrast failure: adjust the semantic token's lightness within its ramp; do not special-case one component unless the exception is documented.
- Token conflicts: if two intents share one value, split the semantic token rather than overloading it.
- Visual regression beyond stated changes: revert the affected selector and isolate the cause.
- Missing design input: produce the derived token set, mark it as provisional, and request confirmation before shipping.

## Deliverable contract

Provide:

1. Changed files and a one-line purpose for each.
2. Token table: primitive, semantic role, value, and light and dark mappings.
3. Verification results: contrast ratios, hard-coded value counts before and after, screenshot comparisons, and commands run with outcomes.
4. Assumptions and open questions.
5. Any actions awaiting approval, listed explicitly, with none executed.

Do not: invent design values, present derived tokens as approved, remove focus styles for appearance, use color alone to convey state, or report unrun checks as passed.

## Ultron routing contract

**Choose this skill when:** the task requires creating, translating, or auditing a consistent visual language: design tokens, typography and spacing scales, color roles, surfaces, responsive composition, component states, contrast, or reduced-motion behavior.

**Choose `css-styling` when:** the visual specification is known and the problem is a concrete stylesheet implementation or browser-specific CSS defect, including cascade, specificity, layout, or responsive rule behavior.

**Handoff contract:** provide semantic tokens, component state definitions, approved breakpoints, reference dimensions, contrast requirements, and acceptance screenshots or measurements. The CSS skill returns implementation evidence and identifies any mismatch that needs a design decision rather than silently changing the visual system.

**Why the boundary exists:** the visual system defines what the interface should communicate; CSS implements that intent in a particular codebase. Mixing the two makes local fixes drift into inconsistent design decisions.
