---
name: web-performance
description: Use when diagnosing, measuring, or improving frontend page load, rendering, interactivity, or runtime responsiveness in a web application, including Core Web Vitals triage, bundle size reduction, caching and asset delivery review, and performance regression checks.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Web Performance

## Purpose and boundaries

This skill covers client-side and delivery-layer performance of web frontends: how fast content becomes visible, how quickly the page responds to input, how visually stable it is, and how much data and script it ships. It produces measured findings and ranked, reversible changes.

In scope: field and lab metric analysis, network waterfall review, JavaScript bundle and main-thread analysis, image and font loading, rendering and layout stability, HTTP caching and compression configuration review, and performance budgets in CI.

Out of scope: backend query tuning, capacity planning, CDN contract decisions, and redesigns unrelated to measured bottlenecks. Route those to the appropriate owner and say so.

## Inputs and assumptions

Required before analysis:
- The target URL or route list, and the user journeys that matter (landing, checkout, dashboard interaction).
- Access to at least one measurement source: field data (RUM or CrUX-style reporting), a lab profiler, or a reproducible local build.
- The framework and build tooling in use. Treat framework-specific APIs as version-sensitive; verify against current official documentation before recommending them.
- Target device and network profile. Do not assume desktop fast-network results represent users.

Assumptions to state explicitly in the report: test device class, throttling profile, cache state (cold or warm), and whether results are lab or field.

## Operating workflow

1. **Baseline.** Record Largest Contentful Paint, Interaction to Next Paint, and Cumulative Layout Shift for each key route, along with Time to First Byte. Run at least five lab runs per route and report the median and spread. Record the exact build hash and environment.
2. **Classify the bottleneck.** Map each failing metric to a phase:
   - Slow TTFB: server response, redirects, or uncached HTML.
   - Slow LCP: render-blocking resources, late-discovered hero image, client-rendered content, or slow resource priority.
   - Poor INP: long tasks on the main thread, heavy event handlers, or large re-renders.
   - Poor CLS: images or embeds without dimensions, late-injected content, web font swap shifts.
3. **Inspect the waterfall.** Identify the critical request chain. Look for sequential dependencies that could be parallel, such as CSS-imported fonts or scripts that load other scripts.
4. **Audit the bundle.** Measure transferred (compressed) size per entry point and per route. Identify modules contributing most to size using a bundle visualizer. Flag duplicated dependencies and libraries imported for a single helper.
5. **Profile interaction.** Record a trace during the slowest real interaction. Find tasks over 50 ms and the functions responsible.
6. **Rank candidate changes.** Score each by expected impact on the failing metric, implementation risk, and reversibility.
7. **Implement one change per branch or commit,** re-measure under the same conditions, and keep only changes that improve the target metric without regressing others.

## Decision gates

- **Proceed to code changes only if** the bottleneck is reproduced in lab data and the baseline variance is smaller than the expected improvement. If variance is larger, collect more runs first.
- **Lazy-load or code-split** only for content below the fold or behind user action. Never defer the LCP element or above-the-fold critical styles.
- **Add preload or fetchpriority hints** only for resources the browser discovers late and that are verified as LCP candidates. Excessive hints degrade performance.
- **Adopt a caching change** only after confirming the asset is content-hashed or the cache key is explicitly versioned. Unversioned long-lived caching of mutable URLs is a defect.
- **Remove a dependency** only after confirming replacement behavior parity in tests.
- **Stop and request approval** before changing production CDN rules, cache purge operations, third-party tag removal (analytics, ads, consent tools), or any change affecting legal consent or tracking behavior.

## Verification and evidence

Each claimed improvement requires:
- Before and after medians from matching conditions (device, throttling, cache state, build mode).
- Confirmation that no other tracked metric regressed beyond noise.
- Bundle size deltas in compressed bytes for changed entry points.
- A passing functional test for any altered rendering or loading path, including behavior with JavaScript disabled where content is server-rendered.

Quality checks to report:
- LCP under 2.5 s, INP under 200 ms, CLS under 0.1 at the 75th percentile of field data, where field data exists.
- Initial JavaScript for key routes within the team's documented budget.
- Every image above the fold has explicit intrinsic dimensions.

Do not state a percentage improvement without the raw numbers behind it. Do not cite benchmark results from memory.

## Failure handling

- **Metrics conflict** (lab improves, field does not): report the discrepancy, check device and network mix of field users, and do not ship on lab data alone.
- **Change regresses another metric:** revert, record the trade-off, and propose a narrower alternative.
- **Measurement noise dominates:** increase run count, pin environment, and report the uncertainty instead of forcing a conclusion.
- **Missing tooling or access:** state which measurement is unavailable and what conclusions are therefore withheld.
- **Version uncertainty** about a framework or browser API: mark it unverified and direct the user to the current official documentation rather than guessing.

## What not to do

- Do not add performance hints, inline critical CSS, or caching headers by habit without a measured failing metric behind them.
- Do not minify or obfuscate as a substitute for removing unused code.
- Do not remove third-party scripts or change consent logic without explicit approval.
- Do not disable features, lazy-load the LCP element, or hide content to win a score.
- Do not present synthetic scores as user experience evidence.

## Deliverable contract

Produce a report containing:
1. Scope, environment, device and network profile, and cache state.
2. Baseline table: route, metric, median, spread, field status.
3. Ranked bottleneck list with phase classification and evidence links or trace references.
4. Proposed changes with expected impact, risk, and reversal path.
5. Verification results with before and after data for each implemented change.
6. Open items, unverified version-sensitive details, and approval requests.