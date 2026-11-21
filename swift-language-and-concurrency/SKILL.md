---
name: swift-language-and-concurrency
description: Use when writing, reviewing, or migrating Swift code that involves language semantics, value vs. reference types, optionals, generics, protocols, async/await, actors, Sendable checking, structured concurrency, or strict concurrency diagnostics in iOS, macOS, watchOS, or server-side Swift projects.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Swift Language And Concurrency

## Purpose and boundaries

This skill guides correct, reviewable Swift code covering core language semantics and the concurrency model (async/await, tasks, actors, isolation, Sendable). It applies to application code, library code, and migrations toward stricter concurrency checking.

In scope: diagnosing isolation and data-race errors, choosing between actors, locks, and main-actor isolation, converting callback APIs to async, reviewing value-type copy semantics, and explaining compiler diagnostics.

Out of scope: UI layout, SwiftUI view design beyond isolation questions, build-system or signing configuration, and performance claims without measurement.

## Inputs and assumptions

Collect before acting:
- Swift language version and toolchain (from `Package.swift` or project settings).
- Concurrency checking level (minimal, targeted, complete) and any language-mode flags.
- Deployment targets and whether APIs used are available on them.
- The exact compiler diagnostic text, or a minimal reproducing snippet.
- Whether the code crosses module boundaries (public API stability matters).

If any of these is missing, state the assumption explicitly in your output. Do not assume a specific Swift release has a particular feature. Mark any version-sensitive behavior as "verify against current Swift and Apple documentation."

## Operating workflow

1. Reproduce: obtain the diagnostic or write the smallest snippet that triggers the behavior.
2. Classify the problem: value semantics, optionality, generic constraint, isolation boundary, cancellation, or Sendable conformance.
3. Trace ownership: for each value crossing a suspension point or isolation boundary, identify who owns it and whether it is mutable and shared.
4. Choose the narrowest fix (see Decision gates).
5. Apply the change, keeping public signatures stable unless the user approves a breaking change.
6. Run the build with strict concurrency checking at the target level and the existing test suite.
7. Add or update a test covering the changed behavior, including cancellation paths where tasks are involved.

## Decision gates

- Value type vs. class: prefer structs and enums for data with no identity. Use a class only when identity, shared mutable state, or Objective-C interop requires it. If a class must be shared across concurrency domains, it must be `final`, immutable, and `Sendable`, or be isolated.
- Isolation choice:
  - UI state and framework callbacks: `@MainActor`.
  - Mutable state shared by background work with no UI relation: an `actor`.
  - Synchronous hot paths with tiny critical sections: a lock, but never hold it across an `await`.
- `@unchecked Sendable`: allowed only when a documented synchronization mechanism guards all access and the user has accepted the risk. Each use requires a comment naming the guard.
- `nonisolated`: use only for immutable or inherently thread-safe members. Do not use it to silence an error on mutable state.
- Callback-to-async conversion: use `withCheckedThrowingContinuation` (or the non-throwing variant) only when the callback is called exactly once. If it may be called zero or multiple times, redesign rather than wrap.
- Unstructured `Task {}`: justify it. Prefer structured `async let` or task groups when child work is bounded by the caller's scope.
- Migrating to stricter checking: fix one module or target at a time. Do not mark broad regions `@preconcurrency` to hide new diagnostics without a tracked follow-up.

## Verification and evidence

- The original diagnostic no longer appears, and no new warnings appear at the targeted checking level.
- Existing tests pass; new tests cover the changed path, including a cancelled task and an error thrown mid-await where relevant.
- For thread-safety claims, run tests under the Thread Sanitizer where the platform supports it, and report the run configuration.
- For public API changes, list each changed signature and each caller updated.
- Do not claim performance improvements from concurrency changes without a measurement. Report the benchmark method and numbers, or state that none was run.

## Failure handling

- If the fix requires a Sendable conformance you cannot justify, stop and report the specific type and the reason it is not safe to conform.
- If behavior differs across Swift versions, report both observed behaviors and flag for verification against official release notes. Do not pick one silently.
- If a fix changes a public API or actor isolation of a public type, pause and request approval before proceeding.
- If tests become flaky after a concurrency change, treat it as a race until shown otherwise. Do not add sleeps as a fix.

## Deliverable contract

Return:
1. The assumptions list (toolchain, checking level, targets).
2. The root cause in one or two sentences, naming the isolation boundary or ownership issue.
3. The minimal diff or code, with unchanged signatures called out.
4. The verification record: build configuration, test results, sanitizer runs, and anything not run.
5. Open risks and any items requiring approval.

Do not: suppress diagnostics with blanket attributes, weaken `Sendable` to make an error disappear, mark mutable shared state `nonisolated`, call `Task.detached` to escape isolation without explaining why, or describe concurrency as "fixed" when only the compiler warning changed.