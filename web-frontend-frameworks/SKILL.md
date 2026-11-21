---
name: web-frontend-frameworks
description: Use when choosing, structuring, debugging, migrating, or reviewing a browser-based UI built with a component framework or meta-framework (React, Vue, Svelte, Angular, Solid, Next.js, Nuxt, SvelteKit, Remix, Astro), including rendering-mode, state, routing, and build-tooling decisions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Web Frontend Frameworks

## Purpose and boundaries

This skill guides professional work on component-based browser UIs: selecting a framework or rendering strategy, organizing components and state, wiring routing and data loading, diagnosing rendering or hydration faults, planning version migrations, and reviewing framework-specific code.

In scope: component models, reactivity and state flow, rendering modes (client-side, server-side, static, streaming, islands), hydration, routing and data fetching conventions, build integration, bundle size, accessibility of rendered output, and framework-level testing.

Out of scope: backend API design, visual design systems, native mobile frameworks, general JavaScript language questions unrelated to UI, and infrastructure provisioning beyond the frontend build and deploy step.

## Inputs and assumptions

Collect before recommending anything:

1. Target framework and exact version, read from the lockfile, not from memory.
2. Rendering requirements: SEO needs, personalization, offline use, first-load budget.
3. Runtime targets: browsers and devices, including minimum supported versions.
4. Existing constraints: team skill, monorepo, design system, hosting platform.
5. Data sources and whether they are authenticated or user-scoped.

Assumptions must be stated explicitly. If the version is unknown, say so and treat every API detail as provisional.

## Operating workflow

1. Restate the goal and the constraint that matters most (usually first-load performance, SEO, or interactivity).
2. Inspect the project: framework version, router type, rendering config, state library, test runner, build tool.
3. Map the component tree and identify where state lives. Keep server state, URL state, and transient UI state in separate homes.
4. Choose the smallest change that resolves the problem. Prefer local fixes over architectural rewrites unless the request is explicitly architectural.
5. Implement or recommend the change with the framework's idiomatic primitives for the verified version.
6. Run verification (below) and report results with evidence.

## Decision gates

Proceed only when the gate is passed; otherwise stop and ask.

- **Framework switch or major migration:** requires an inventory of dependencies, a written rollback path, and explicit approval from the owner.
- **Rendering mode change (e.g., client-only to server-rendered):** requires confirming hosting supports it and that data fetched on the server does not leak per-user secrets to cached responses.
- **Adding a global state library:** justify only if at least two distant components share mutable state that cannot live in server cache or URL.
- **Client-side fetching on initial render:** prefer framework data-loading primitives or server rendering when the data is needed for first paint.
- **Dependency upgrades:** pin, read the official migration guide for that exact version, and run the full test suite before and after.

## Verification and evidence

Report each check as pass, fail, or not run, with the command or observation behind it.

- Type check and linter pass with no newly suppressed diagnostics.
- Unit and component tests cover changed components; tests assert user-visible behavior, not internal state.
- No hydration mismatch warnings in the browser console for affected routes.
- Lighthouse or equivalent run on affected pages: compare before and after on the same machine and throttling profile. Report numbers only if measured.
- Production build succeeds; bundle diff for changed routes is reported in kilobytes gzipped.
- Keyboard navigation and focus order checked on changed interactive components; ARIA roles match native semantics where available.
- Effects and subscriptions have cleanup; list any that do not and why.

Do not claim performance improvements without before-and-after measurements.

## Failure handling

- **Hydration mismatch:** search for non-deterministic output (dates, random IDs, locale-dependent formatting, browser-only globals) in the render path. Move such values into effects or pass them from the server consistently.
- **Stale data after mutation:** check that the cache invalidation or revalidation mechanism the framework provides is called with the correct key. Do not add a polling workaround first.
- **Infinite render or update loops:** inspect dependency arrays, reactive computations that write to their own inputs, and unstable object or function identities passed as props.
- **Build failure after upgrade:** read the release notes for breaking changes, fix one category at a time, and re-run the build after each.
- **Unclear root cause after two attempts:** stop, summarize what was tried and observed, and ask for the reproduction steps or a minimal reproduction.

## Deliverable contract

Every deliverable contains:

1. Framework and version verified, with the source used (lockfile, config file, or user statement).
2. A short summary of the decision or fix, with the constraint that drove it.
3. Code changes as complete, runnable files or precise diffs, not fragments with ellipses.
4. A verification table listing each check from the previous section with status and evidence.
5. A list of open risks and any API details flagged for confirmation against current official documentation.

## What not to do

- Do not invent API names, hook signatures, configuration keys, CLI flags, or package versions. If unsure, say "verify in the official docs for version X."
- Do not state benchmark numbers, compliance outcomes, or security guarantees that were not measured or documented.
- Do not add a state library, animation library, or UI kit without a stated need.
- Do not disable lint rules, type checks, or accessibility warnings to get a build passing.
- Do not store tokens or secrets in client-accessible state, local storage, or rendered HTML.
- Do not run destructive or external-impacting actions without explicit approval: deleting branches or build caches, force-pushing, publishing packages, changing production DNS, deploying to production, or altering shared CI configuration. Describe the command and its effect, then wait for confirmation.