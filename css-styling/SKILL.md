---
name: css-styling
description: Use when writing, refactoring, or reviewing CSS for web interfaces, including layout, theming, responsive behavior, specificity conflicts, and visual regressions in frontend codebases.
author: Luo Kai
provenance: original
version: 1.0.0
---

# CSS Styling

## Purpose and boundaries

Produce maintainable, responsive, accessible CSS that matches the existing design system and browser support target. Covers layout (flow, flexbox, grid), typography, color and theming, spacing scales, responsive breakpoints, interaction states (hover, focus, disabled, error), motion, and stylesheet architecture.

Out of scope: JavaScript behavior, build configuration beyond what changes CSS output, markup restructuring, and brand or visual design decisions not already specified.

## Inputs and assumptions

Establish these before editing:
- Target browsers and minimum versions, taken from project configuration or the stakeholder. Do not assume.
- Styling method in use: plain CSS, CSS Modules, a preprocessor, a utility framework, or CSS-in-JS.
- Existing tokens, breakpoints, and naming conventions.
- Required component states and the design reference, if one exists.

If a missing item would change the output, ask. Otherwise state the assumption in the deliverable.

## Operating workflow

1. Read the surrounding stylesheet and locate existing tokens, utilities, and patterns. Reuse before creating.
2. Reproduce the issue or define the target: element, viewport width, and state.
3. Diagnose from computed styles, not guesses. Check cascade order, specificity, inherited properties, and containing blocks.
4. Make the smallest change at the correct layer: token, base element rule, component rule, or override. Change the source of a value rather than patching its symptom.
5. Verify across the viewport set and interaction states (see Verification and evidence).
6. Remove dead rules and duplicate declarations that the change introduced or exposed.

## Decision gates

- Use flexbox for one-dimensional alignment and grid for two-dimensional layout. Try intrinsic sizing (`min()`, `max()`, `clamp()`, `minmax()`, auto-fit) before adding media queries.
- Add a breakpoint only where content actually breaks at that width, not at a device size taken from a list.
- Keep specificity low. Use `!important` only to override third-party styles that cannot be changed, and document why.
- Use logical properties (inline and block axes) if the project supports right-to-left or vertical writing. Otherwise match the existing convention.
- Use custom properties for values that vary by theme or context. Use literal values for true constants.
- Ask for explicit approval before: renaming or deleting global selectors or tokens used elsewhere, changing shared design tokens that affect other products, altering published theme or public stylesheet exports, or making any change that alters brand appearance site-wide.

## Verification and evidence

Check every change against:
- Viewports: 320px, 768px, and 1280px at minimum, plus project-defined breakpoints.
- States: default, hover, focus-visible, active, disabled, and error where applicable.
- Keyboard focus remains visible. Focus indicators meet non-text contrast of 3:1 under WCAG 2.2; confirm this against current official guidance.
- Text contrast meets WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- Text does not clip or overflow at 200% zoom or with increased user font size.
- No unexpected layout shift in the affected region. Run visual regression tests if the project has them.
- Evidence: list the viewports and states checked, plus before and after screenshots or computed values for each changed property.

Before using any newer property, function, or pseudo-class, confirm support against current official compatibility data. Do not rely on memory.

## Failure handling

- If a fix works in one browser engine but not another, record the engine and version, then check for a fallback or progressive enhancement path.
- If specificity conflicts recur, stop patching. Map rule ownership and restructure the cascade.
- If a change causes a regression elsewhere, revert it and isolate the shared selector before retrying.
- If the request conflicts with accessibility requirements, do not implement the conflicting part. Report the conflict and propose alternatives.

## Deliverable contract

Return:
1. The changed CSS, limited to the files touched.
2. A short rationale naming the root cause and the layer changed.
3. A verification record: viewports, states, contrast results, and any unverified items stated explicitly.
4. Assumptions and open questions.
5. Version-sensitive properties or features flagged for verification against current official documentation.

Do not add unrelated restyling, introduce new frameworks, hard-code colors where tokens exist, set fixed pixel heights on text containers, or claim cross-browser support without testing.