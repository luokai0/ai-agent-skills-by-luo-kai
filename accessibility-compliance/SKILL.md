---
name: accessibility-compliance
description: Use when auditing, remediating, or reviewing frontend web or app UI for WCAG conformance, keyboard and screen reader operability, color contrast, semantic markup, or accessible component behavior before release.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Accessibility Compliance

## Purpose and boundaries

This skill guides an agent through evaluating and fixing accessibility defects in frontend code and rendered UI against WCAG 2.1 or 2.2 success criteria (confirm the target version with the user). It covers automated scanning, manual keyboard and assistive technology checks, code-level remediation, and evidence reporting.

It does not certify legal compliance, issue conformance statements on behalf of an organization, or guarantee that a product is accessible. Those decisions belong to qualified auditors and the accountable team. Backend logic, content authoring policy, and non-web platforms are out of scope unless explicitly added.

## Inputs and assumptions

Before starting, establish:

- Target standard and level (for example WCAG 2.2 AA). Default to AA only if the user confirms it.
- Scope: specific routes, components, or user flows.
- Stack: framework, component library, and styling approach. Component libraries often have their own accessibility documentation; verify current versions against official docs.
- Runtime access: whether a browser can be run locally and whether test data is non-sensitive.
- Known constraints: design tokens that cannot change, legacy components, or third-party embeds.

Assume nothing about user environments. If a test cannot be run, record it as not verified rather than passing it.

## Operating workflow

1. **Map the scope.** List pages, states (empty, error, loading, modal open), and interactive flows. Identify each distinct component type.
2. **Run automated checks.** Use an established engine such as axe-core or an equivalent linter (confirm current version and rule set against its official documentation). Record rule IDs, counts, and affected selectors. Automated tools typically catch only a portion of defects; treat a clean run as incomplete evidence.
3. **Test keyboard operation.** Tab through each flow. Verify visible focus, logical order, no keyboard traps, operable custom widgets, and that Escape closes dismissible overlays with focus returned to the trigger.
4. **Test with assistive technology.** Use at least one screen reader on each major platform the user supports. Check accessible names, roles, states, live-region announcements, and form error association.
5. **Check visual properties.** Measure text and UI contrast with a tool; verify reflow at 320 CSS pixels wide, text resize, and that information is not conveyed by color alone.
6. **Review semantics in code.** Confirm native elements are used before ARIA, headings form a meaningful outline, landmarks exist, images have appropriate alternatives, and decorative content is hidden from assistive technology.
7. **Remediate in small commits.** Fix one defect class at a time, rerun the relevant checks, and note the before and after state.
8. **Produce the deliverable.** Follow the contract below.

## Decision gates

- **Gate A, before any change to shared design tokens or global styles:** stop and request approval. Changes can affect many components and other teams.
- **Gate B, before modifying third-party embeds or vendor components:** confirm ownership and whether a wrapper is acceptable. Do not fork vendor code without approval.
- **Gate C, before removing or altering existing tests, analytics hooks, or user-facing copy:** request approval. Copy changes can alter legal or brand commitments.
- **Gate D, before pushing, deploying, or publishing reports to external parties:** require explicit approval.
- **Contrast decisions:** if a fix would change brand colors, present two or three compliant alternatives with measured ratios and let the owner choose.
- **ARIA addition:** add ARIA only when no native element or attribute provides the semantics. Any added role must have all required states and properties.

## Verification and evidence

Each reported defect must include: WCAG criterion number and name, severity (blocker, serious, moderate, minor), reproduction steps, affected element selector or file path, and evidence (tool output excerpt or screen reader transcript summary).

A fix is verified only when:
- the originating automated rule no longer fires,
- the keyboard path works end to end,
- the screen reader announces the expected name, role, and state,
- contrast ratios meet the target threshold (4.5:1 normal text, 3:1 large text and non-text UI components under WCAG 2.x; confirm against the current specification),
- no new violations appear in the touched component.

Report unverified items separately. Never write "passes WCAG" as a blanket claim.

## Failure handling

- **Tool unavailable or crashes:** record the failure, fall back to manual checks, and mark the affected criteria as unverified.
- **Conflicting requirements** (for example, a design mandates a low-contrast style): escalate with the specific criterion and options.
- **Cannot reproduce a reported issue:** document the environment, browser, assistive technology version, and steps tried. Do not close it silently.
- **Fix introduces regression:** revert that change only, then re-analyze.

## Deliverable contract

Return a single report with these sections in order:

1. Scope and standard tested (with version of the criteria referenced).
2. Environment: browsers, assistive technologies, tool names and versions as observed.
3. Findings table: ID, criterion, severity, location, status (fixed, open, unverified).
4. Changes made: file paths and a summary of each change.
5. Verification results per finding, with evidence.
6. Open decisions requiring approval, from the decision gates.
7. Residual risk: areas not tested and why.

Do not state that the product is compliant. State only which criteria were checked, what passed, and what remains open. Version-sensitive details (tool rule IDs, criteria wording, browser support for specific features) must be marked for verification against current official documentation.