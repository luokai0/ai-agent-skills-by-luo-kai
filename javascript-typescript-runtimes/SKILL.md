---
name: javascript-typescript-runtimes
description: Use when choosing, configuring, debugging, or migrating JavaScript or TypeScript execution environments, including Node.js, Deno, Bun, browsers, and edge or serverless runtimes, or when resolving module format, TypeScript execution, or cross-runtime compatibility issues.
author: Luo Kai
provenance: original
version: 1.0.0
---

# JavaScript and TypeScript Runtimes

## Purpose and boundaries

This skill guides decisions about where JavaScript or TypeScript code executes and how it is loaded, resolved, and verified there. It covers:

- Runtime selection (server, edge, browser, CLI tooling).
- Module system behavior (CommonJS, ES modules, interop).
- How TypeScript is executed: type-stripping, transpilation, or compilation to JavaScript.
- Built-in API availability (fetch, streams, crypto, file system, timers).
- Process, environment, and package-resolution differences between runtimes.

It does not cover language syntax tutorials, bundler plugin internals, framework architecture, or infrastructure provisioning. Treat exact API names, CLI flags, and version-specific behavior as claims to confirm against current official documentation for the runtime version in use. Do not assert them from memory.

## Inputs and assumptions

Collect before recommending anything:

1. Target environment(s) and exact runtime versions in use or planned.
2. Entry point type: script, server, library, CLI, worker, or browser bundle.
3. Module format of the source and of published artifacts (`type` field, file extensions, export maps).
4. TypeScript configuration: target, module resolution mode, strictness, whether `tsc` emits or only type-checks.
5. Dependency constraints: native addons, Node-specific built-ins, or runtime-specific packages.
6. Deployment constraints: cold start limits, memory caps, filesystem access, outbound network rules.

If any item is missing and affects the answer, ask. Do not assume a runtime version is current.

## Operating workflow

1. Restate the goal in one sentence: run, ship, library-publish, migrate, or debug.
2. Identify the runtime's contract: module loader, global objects, supported standards, and I/O model.
3. Reproduce the issue with the smallest entry file that fails, in the target runtime, before changing configuration.
4. Classify the failure: module resolution, format mismatch, missing global, TypeScript emit mismatch, native dependency, or environment variable and path difference.
5. Apply the smallest change that addresses the classified cause. Prefer changing one variable per iteration.
6. Re-run in every target runtime, not only the one where the bug appeared.
7. Record the final configuration and the reasoning behind it.

## Decision gates

Proceed only when the relevant gate passes:

- **Runtime choice gate:** Required built-ins, native modules, and deployment limits are confirmed supported by the chosen runtime's current documentation. If a dependency needs a native addon, confirm prebuilt binaries exist for the target platform.
- **Module format gate:** Each published file has one unambiguous format. Mixed CJS/ESM output requires an explicit dual-package strategy and tests for both import paths.
- **TypeScript execution gate:** Confirm whether the runtime executes TypeScript natively, requires a build step, or only strips types. Native type-stripping rarely supports all TS features (for example, enums or namespaces may require transformation). Verify this against current docs.
- **Migration gate:** Migration proceeds only with a passing baseline test suite on the current runtime and a rollback path.
- **Approval gate (explicit human approval required):** Changing production runtime versions, altering deployment targets, modifying global Node or system installs, deleting lockfiles or build caches, rotating secrets used by runtime configuration, or any action that affects external users or data.

## Verification and evidence

Each conclusion needs evidence:

- Show the exact command and runtime version output used to reproduce the result.
- Compare behavior across at least two runtimes when portability is claimed.
- For module issues, demonstrate both `import` and `require` paths (where applicable) succeed.
- For TypeScript, show that type-checking and runtime execution both pass, since they verify different things.
- Measure startup time or memory only with a stated method and repeat runs. Do not report numbers without the method.
- Quality thresholds: zero unresolved import errors, zero runtime-only failures on target versions, and test pass rate unchanged or improved from baseline.

## Failure handling

- **Module not found:** Check export maps, file extensions required by the resolution mode, and `type` field. Do not add broad fallbacks that mask resolution.
- **Global not defined:** Confirm the API is standard in that runtime version. Provide a runtime-detection shim only with a documented reason.
- **Native addon failure:** Identify the platform and architecture mismatch. Recommend a pure-JS or WASM alternative only after confirming functional parity.
- **Behavior differs between runtimes:** Document the difference, isolate it in an adapter, and add a test that pins expected behavior.
- If root cause remains unknown after three bounded attempts, stop and report observations, hypotheses, and what evidence would discriminate between them.

## Deliverable contract

Every response in this domain delivers:

1. Summary of the decision or fix in no more than five sentences.
2. Runtime and version matrix tested, with the verification source for version-sensitive claims.
3. Exact configuration changes as a minimal diff or file excerpt.
4. Evidence: commands run and their observed results.
5. Open risks and items requiring human approval.

## What not to do

- Do not invent API names, flags, package versions, benchmark figures, or compatibility guarantees.
- Do not recommend global installs or system-wide changes as a fix for project-level problems.
- Do not disable type checking or strict mode to make code run.
- Do not suppress module errors with broad `any` casts, ignore comments, or catch-all wrappers.
- Do not perform destructive actions (deleting lockfiles, caches, or build outputs; overwriting configs in shared repositories) without explicit approval.
- Do not claim production readiness without evidence from the actual target runtime.