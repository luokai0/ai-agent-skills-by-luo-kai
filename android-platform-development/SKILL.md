---
name: android-platform-development
description: Use when building, debugging, reviewing, or releasing native Android apps or platform-facing Android code (Kotlin/Java, Gradle, Jetpack, manifest, permissions, lifecycle, storage, background work, release signing) and a decision on architecture, API usage, or verification is needed.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Android Platform Development

## Purpose and boundaries

This skill guides engineering work on native Android applications: project configuration, component lifecycle, UI state handling, permissions, data persistence, background execution, build and signing, and Play-ready release preparation. It covers app-level code and build configuration, not Android OS internals, custom ROM work, kernel modules, or device firmware.

Stop and escalate when the task requires modifying system partitions, signing with keys you do not control, altering Play Console listings or policy declarations, or making claims about security, privacy compliance, or certification.

## Inputs and assumptions

Collect before acting:
- Target `minSdk`, `targetSdk`, and `compileSdk` from the existing Gradle files. Do not assume values.
- Build system state: Gradle wrapper version, AGP version, Kotlin version, and whether a version catalog exists.
- UI toolkit in use (Jetpack Compose, View system, or mixed) and the architecture pattern already present.
- Affected components: activities, services, workers, broadcast receivers, content providers.
- Required device or emulator matrix, and whether physical hardware is available.

If any of these are missing and cannot be read from the repository, state the assumption explicitly in your output.

## Operating workflow

1. Read `settings.gradle(.kts)`, the root and module `build.gradle(.kts)`, the version catalog, and `AndroidManifest.xml` for each module touched.
2. Map the change to lifecycle owners. Identify which state survives configuration change, process death, and task removal.
3. Choose the narrowest API that satisfies the requirement. Prefer framework or Jetpack components already in the project over new dependencies.
4. Implement in small, reviewable units. Keep UI state in observable holders; keep side effects in scoped coroutines or managed workers.
5. Update manifest declarations, permissions, and exported flags only when the change requires them, and document each addition.
6. Run the build, unit tests, lint, and instrumented tests on the agreed device matrix.
7. Produce the deliverable contract below.

## Decision gates

Pause and request explicit approval before:
- Changing `targetSdk`, `compileSdk`, signing configuration, `applicationId`, or keystore references.
- Adding permissions, exported components, or intent filters that expose app functionality.
- Deleting data, migrating a database schema destructively, or removing `fallbackToDestructiveMigration`-style behavior.
- Adding network endpoints, analytics, or third-party SDKs that transmit user data.
- Publishing, uploading to a track, or changing store metadata.

Choose background work by execution need:
- Deferrable, guaranteed work that survives restarts: WorkManager.
- User-initiated, long-running work with visible notification: foreground service with a declared type, only when the foreground-service rules for the target SDK are verified.
- Work tied to UI lifetime: lifecycle-scoped coroutines. Never launch unscoped `GlobalScope` work.

Choose storage by data shape: preferences for small key-value settings, Room for relational or queried data, app-specific files for blobs. Use scoped storage APIs for shared media; do not request broad storage access without a documented need.

## Verification and evidence

Each change must show:
- `./gradlew assembleDebug` and `./gradlew test` completing with zero failures, plus the relevant `connectedAndroidTest` run where instrumentation applies.
- Lint report with no new errors compared to baseline. Record the baseline command and count.
- For lifecycle changes: a test or manual script covering rotation, backgrounding, and process death restoration, with the observed result.
- For permissions: a test on a device at the lowest supported API level where behavior differs, and the denial path exercised.
- For background work: confirmation that the work runs under Doze or battery-restricted conditions, or a documented limitation.
- Any version-specific behavior (permission rules, background limits, foreground service types, notification requirements, API deprecations) must be checked against current official Android developer documentation and cited by page title and access date. Do not rely on memory for these details.

Do not report performance numbers unless measured with a profiler or benchmark run you actually executed; include device model, API level, and build variant.

## Failure handling

- Build failure after dependency change: revert the change, rerun the build, then isolate by bisecting the dependency or plugin version. Do not upgrade unrelated libraries to resolve it.
- Crash on specific API level: reproduce on that level, check the stack trace for the failing call, and gate with a version check only if the framework documentation confirms the API is unavailable there.
- Flaky instrumentation tests: quarantine the test with an issue reference rather than retrying until green.
- Lint regressions: fix the cause; suppress only with a comment explaining why the suppression is correct.
- Unclear requirement or conflicting constraints: stop and list the conflict with the two options and their consequences.

## Deliverable contract

Return:
1. Summary of changes, grouped by module, with file paths.
2. Assumptions list, including unverified SDK-version details flagged for documentation check.
3. Commands run and their outcomes (pass/fail counts, lint delta).
4. Manifest, permission, and exported-component changes, each marked as approved or pending approval.
5. Known limitations and untested device configurations.
6. Next actions requiring human approval, stated as explicit questions.

Do not:
- Invent API names, Gradle plugin IDs, library versions, or flags. Confirm each against the project or official docs.
- Claim Play policy, privacy, or accessibility compliance.
- Disable security features, certificate checks, or `android:allowBackup` decisions without approval and rationale.
- Commit signing keys, credentials, or `local.properties` contents.
- Suppress lint or test failures to achieve a green build.

## Ultron routing contract

**Choose this skill when:** the application is native Android and the work concerns Android project structure, lifecycle, Jetpack/platform APIs, permissions, storage, background execution, native UI, Gradle/build configuration, signing, or Android release behavior.

**Choose `react-native-cross-platform-development` when:** the application is built primarily in React Native with a shared TypeScript/JavaScript codebase targeting both Android and iOS.

**Handoff contract:** when React Native requires Android-specific native modules, manifests, permissions, Gradle configuration, lifecycle integration, or platform debugging, the React Native skill supplies the cross-platform requirement and this skill handles the native Android boundary. Return the native API behavior, version constraints, required platform changes, and device-level verification.

**Why the boundary exists:** a React Native application may contain native Android code, but it is not the same architecture as a fully native Android application.
