---
name: app-frameworks
description: Use when choosing, scaffolding, structuring, or migrating a frontend application framework (React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit, Remix, Astro, and similar), or when diagnosing framework-level architecture problems in a web or hybrid app.
author: Luo Kai
provenance: original
version: 1.1.0
---

# App Frameworks

## Purpose and boundaries

This skill guides framework-level decisions for frontend applications: selecting a framework and meta-framework, establishing project structure, defining rendering strategy (client, server, static, hybrid), organizing routing and data loading, and planning framework upgrades or migrations.

In scope: framework selection rationale, project layout, routing and data-fetching patterns, rendering modes, build and deployment integration at the framework level, upgrade and migration plans.

Out of scope: visual design, backend API design, CSS methodology beyond framework integration, infrastructure provisioning, and non-web native mobile internals (advise only on framework boundaries).

## Inputs and assumptions

Collect before recommending anything:

1. Product type: content-heavy, authenticated dashboard, real-time, e-commerce, embedded widget.
2. Constraints: SEO requirements, time-to-interactive targets, browser support, offline needs, team languages and experience.
3. Existing stack: current framework and version, build tool, deployment target, test tooling.
4. Scale: expected team size, number of routes, number of contributors per area.
5. Hosting: static host, Node server, edge runtime, or container.

If any of items 1, 2, or 3 is missing, ask. Do not assume a framework version is current; state the version you reasoned about and mark it for verification against official documentation.

## Operating workflow

1. Restate the product type and the two or three requirements that most constrain the choice.
2. Enumerate candidate frameworks (maximum four). Include the existing one if this is not greenfield.
3. Score each candidate against the criteria in Decision gates.
4. Recommend one option with the reason it wins and the main tradeoff accepted.
5. Define the project skeleton: top-level directories, route layout, data-loading boundary, and where shared state lives.
6. Specify the rendering mode per route group (for example: marketing pages static, account area client-rendered behind auth).
7. Produce a migration or adoption sequence with reversible steps.
8. Attach the verification plan from Verification and evidence.

## Decision gates

Proceed only when each gate is satisfied:

- **Gate A, Requirement fit:** The framework supports the required rendering modes (SSR, SSG, or SPA) natively or through its official meta-framework. Reject candidates requiring unofficial plugins for core needs.
- **Gate B, Team fit:** At least one team member can maintain the framework; learning cost is estimated in weeks, not quarters, for the stated timeline.
- **Gate C, Ecosystem health:** Active maintenance, a documented upgrade path, and a stable release channel. Check release notes and deprecation policy at decision time.
- **Gate D, Exit cost:** Routing, data loading, and component code can be isolated so a future move is bounded. Avoid framework-specific logic leaking into domain modules.
- **Gate E, Migration risk:** For existing apps, a strangler approach (migrating route groups incrementally) is preferred over full rewrites unless the current code is unmaintainable and the team has agreed to that cost.

Require explicit user approval before: replacing a framework in a production codebase, changing the deployment runtime, deleting legacy modules, altering authentication or data-handling flows, or performing any migration that cannot be rolled back within one release.

## Verification and evidence

- Build succeeds with production configuration and the output size is recorded before and after any change.
- Route smoke test: every route in the new layout returns the expected status and renders the primary heading in a headless run.
- Rendering check: for SSR or SSG routes, confirm the server-delivered HTML contains primary content without client JavaScript executing.
- Performance baseline: record a Largest Contentful Paint and Interaction to Next Paint measurement on a representative device profile before and after. Report the figures; do not state improvements without them.
- Bundle diff: list the largest chunks added or removed.
- Upgrade checks: run the framework's official codemods or migration guide steps, and list every deprecation warning that remains.

Mark any framework option, command, or config key you cite as "verify against current official docs" unless you have confirmed it for the exact version in use.

## Failure handling

- **Build fails after scaffolding:** Revert to the last green commit, isolate the failing module, and fix in a separate change. Do not proceed to route work on a broken build.
- **Hydration or client/server mismatch:** Identify non-deterministic values (dates, random IDs, locale, browser-only APIs) rendered during server pass; move them behind a client-only boundary or stabilize them.
- **Performance regression beyond baseline:** Roll back the rendering mode change for the affected route group and profile before retrying.
- **Team resists chosen framework:** Re-run Gate B with the actual team; do not override with a preference.
- **Conflicting requirements (for example, full SSR plus fully offline):** Surface the conflict, propose route-level splits, and request a decision.

## Deliverable contract

Produce a single document containing, in order:

1. Context summary (product type, constraints, version assumptions).
2. Candidate table with gate scores and a one-line rationale per candidate.
3. Recommendation with accepted tradeoffs.
4. Project skeleton as a directory tree with a one-line purpose per top-level directory.
5. Rendering mode map by route group.
6. Ordered migration or adoption steps, each with a rollback action.
7. Verification plan with the metrics listed above and empty result fields to be filled.
8. Open items list, each with an owner and a verification source.

Do not claim performance gains, compatibility, or security properties that have not been measured or confirmed against official documentation. Do not present a recommendation as final without user approval for any gated action.\n\n## Ultron routing contract

**Choose this skill when:** the task is deciding which frontend framework or meta-framework to use, defining application-level rendering and routing architecture, choosing the data-loading model, or planning a framework adoption or migration.

**Do not use it as the primary implementation guide when:** the framework is already selected and the work is a component-level rendering, reactivity, hydration, accessibility, or framework-idiomatic code change. Route that work to `web-frontend-frameworks`.

**Handoff to the implementation skill:** provide the selected framework and verified version, product constraints, rendering mode by route group, routing and data-loading boundaries, hosting assumptions, and any migration constraints. If implementation evidence shows the chosen architecture cannot satisfy a requirement, return the evidence here for an architectural decision rather than accumulating framework-specific workarounds.

**Why the boundary exists:** framework selection and application implementation are related but different decisions. Keeping them separate prevents a component bug from triggering an unnecessary framework redesign and prevents architectural choices from being made by whichever implementation detail was encountered first.
