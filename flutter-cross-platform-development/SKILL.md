---
name: flutter-cross-platform-development
description: Use when building, reviewing, or debugging a Flutter application targeting iOS, Android, web, or desktop, including state management, platform channels, responsive layouts, build configuration, and release readiness across platforms.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Flutter Cross Platform Development

## Purpose and boundaries

This skill guides engineering work on a Flutter codebase that must run on more than one platform from a shared Dart code base. It covers widget architecture, state flow, navigation, platform-specific adaptation, native interop through platform channels, plugin selection, build flavors, and per-platform release readiness.

In scope: diagnosing layout and rendering defects, designing state and data boundaries, adding or reviewing platform channel code, evaluating plugins, configuring flavors and signing inputs, and preparing a verified release candidate.

Out of scope: native-only feature work with no Flutter surface, app store listing copy, legal or privacy compliance determinations, backend API design, and performance claims not backed by measurement on the target device.

## Inputs and assumptions

Collect before acting:
- Target platforms and minimum OS versions for each (set by product, not by assumption).
- Flutter and Dart SDK versions pinned in the repository, and the toolchain used in CI.
- Current state management approach and any existing architecture document.
- Failing symptom with reproduction steps, device or emulator model, and logs.
- Whether the task touches signing, store submission, or production configuration.

If the repository does not pin the SDK, stop and request the version. Treat all package versions and API signatures as version-sensitive: confirm against current official pub.dev and Flutter documentation before writing code that depends on them.

## Operating workflow

1. Reproduce. Run the app on the affected platform in the matching mode (debug for logic, profile for performance, release for signing or plugin issues). Record the exact platform and build mode.
2. Locate the boundary. Decide whether the defect lives in Dart widgets, state logic, a plugin, a platform channel, or native configuration. Read the plugin source for the failing platform before assuming a Dart fault.
3. Make the smallest change that fixes the boundary, keeping platform conditionals in one adapter layer rather than scattered through widgets.
4. Use `LayoutBuilder`, `MediaQuery`, and adaptive breakpoints rather than hard-coded pixel sizes. Respect safe areas, text scale factor, and keyboard insets on every screen you touch.
5. For platform channels, define the message contract (method name, argument types, error codes) in a single Dart file and mirror it in each native implementation. Return typed errors; never let a native exception escape as an untyped crash.
6. Add or update tests at the lowest layer that exposes the defect: unit tests for logic, widget tests for layout, integration tests on a real device for channels and permissions.
7. Verify on every targeted platform before declaring the change complete.

## Decision gates

- Plugin selection: prefer maintained plugins from verified publishers with a recent release, passing analysis on your target platforms, and a license compatible with your product. Reject a plugin that lacks support for a required platform rather than writing ad hoc native glue without review.
- State management: keep one approach per application. Do not mix providers, global singletons, and ad hoc streams for the same data.
- Platform conditionals: use `defaultTargetPlatform` or `kIsWeb` only inside adapters. If a widget branches on platform more than twice, extract it.
- Native code changes: require explicit owner approval before modifying Gradle signing, Xcode provisioning, entitlements, or manifest permissions.
- Release actions: any signing, store upload, tagging, or production configuration change requires explicit user approval and a named reviewer.

## Verification and evidence

Minimum evidence per change:
- `flutter analyze` with zero new warnings in changed files.
- `dart format --set-exit-if-changed` passes on touched files.
- Relevant unit and widget tests pass; new tests fail before the fix and pass after.
- Manual or integration check on each affected platform, with device model, OS version, and build mode recorded.
- For layout changes: screenshots at narrow phone width, tablet or desktop width, and largest system text scale.
- For release candidates: build artifacts produced from a clean checkout, with the exact commit hash and flavor recorded.

Performance statements require profile-mode measurements on a named device. Do not report frame times or startup durations from debug builds.

## Failure handling

- If reproduction fails on one platform only, record the divergence and check plugin implementation, platform version, and permissions before changing shared code.
- If a fix works on one platform and breaks another, revert the platform-specific branch and reconsider the abstraction rather than adding a further conditional.
- If a build fails in CI but not locally, compare SDK versions, Gradle or CocoaPods lockfiles, and environment variables before editing source.
- If a plugin behaves inconsistently with its documentation, pin the version, file an issue with a minimal reproduction, and use a documented workaround only with a removal note.
- Stop and escalate when the fix requires changing signing, permissions, or data handling.

## Deliverable contract

Each completed task delivers:
1. A summary of the root cause or design decision, in two to five sentences.
2. The list of changed files with a one-line reason per file.
3. The verification record: commands run, platforms tested, device and OS, build mode, and results.
4. Known limitations and any version-sensitive items flagged for confirmation against current official documentation.
5. Open approvals required before merge or release, if any.

Do not claim a platform is supported unless it was run. Do not present benchmark numbers, store acceptance, or compliance outcomes as guaranteed. Do not invent API names, flags, or package versions; quote only what has been checked in the current official documentation.