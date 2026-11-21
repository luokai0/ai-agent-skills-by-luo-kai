---
name: react-native-cross-platform-development
description: Use when building, debugging, reviewing, or planning a React Native app for iOS and Android, including shared code architecture, native module bridging, platform-specific UI, performance tuning, and release preparation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# React Native Cross Platform Development

## Purpose and boundaries

This skill guides production work on React Native applications targeting iOS and Android from a shared TypeScript/JavaScript codebase. It covers:

- Project structure and shared-versus-platform code boundaries
- Navigation, state, and data-layer decisions that affect both platforms
- Platform-specific UI and behavior branching
- Native module integration and native code changes
- Performance diagnosis on device
- Build, signing, and store-submission readiness checks

It does not cover web targets (React Native Web), desktop, backend API design, or general React patterns unrelated to native rendering. It does not replace store policy review or legal/privacy review.

## Inputs and assumptions

Before acting, establish:

1. React Native version and whether the project uses the New Architecture (Fabric/TurboModules). Mark any statement about defaults, flags, or template structure for verification against the current official React Native documentation, as these change between releases.
2. Whether the project is bare React Native or uses a managed framework layer, and which tooling manages native builds.
3. Minimum supported iOS and Android versions, and target devices (low-memory Android tiers matter more than flagship benchmarks).
4. Existing native dependencies and whether each has been checked for New Architecture compatibility.
5. CI environment, signing setup, and who holds release credentials.

If any of these are unknown, state the assumption explicitly in your output rather than guessing.

## Operating workflow

1. **Reproduce on both platforms.** Run the failing flow on a real iOS device or simulator and a real Android device or emulator. Record OS version, device model, build type (debug/release), and app version. Bugs that appear on one platform only are the most common cross-platform defect class.
2. **Classify the issue.** Choose one: JS logic, rendering/layout, native module, platform API behavior, build/tooling, or performance.
3. **Locate the boundary.** Determine whether the fault lies in shared code, a platform file (`.ios.tsx` / `.android.tsx` resolution), or native code. Inspect the native logs (Xcode console, Logcat) in addition to the Metro output.
4. **Make the smallest change in the right layer.** Prefer fixing shared logic over duplicating platform forks. Introduce a platform branch only when the platform behavior genuinely differs.
5. **Verify on both platforms** (see Verification and evidence).
6. **Document the change**: affected platforms, native changes, and any new permissions or config.

## Decision gates

- **Platform split vs. shared code:** Split into platform files only when the difference is in native behavior, default styling conventions the design requires to differ, or an API that is platform-exclusive. Otherwise use `Platform.select` or a single component with a small conditional.
- **Native module vs. existing library:** Use an established, maintained library first. Write a custom native module only when no candidate supports required functionality, and then require native review from someone competent in Swift/Kotlin.
- **Dependency upgrade:** Upgrade only with a changelog review, a New Architecture compatibility check, and a rebuild of both native projects. Do not upgrade React Native and native libraries in the same change.
- **Performance work:** Proceed only after profiling on a release build on a low-tier Android device. Do not optimize from debug-mode timings.
- **Native configuration changes** (permissions, entitlements, signing, bundle identifiers, package names, app transport security, network exceptions): Stop and obtain explicit human approval before editing. These affect store review, user privacy, and existing installs.

## Verification and evidence

Each change must produce:

- Screenshots or recordings from both platforms for any UI change, showing at minimum the default and one edge state (long text, small screen, or dark mode if supported).
- Release-build test run on both platforms for any native or dependency change.
- Lint and type-check passes, and the project's unit tests green.
- For performance claims: before/after frame timing or startup measurement on the same device, with the method recorded. Do not report a percentage improvement without the raw numbers.
- For native module changes: a manual test of the failure path (permission denied, module unavailable, unsupported OS version).

Quality thresholds to check, where the project has defined them: cold start on the reference Android device within the team's agreed budget; no dropped frames during the primary scroll list on the reference device; no unhandled promise rejections in the release build.

## Failure handling

- **Works on iOS only:** Check Android-specific layout defaults (elevation, font padding, flex direction defaults are shared but text metrics differ), Android permissions, and back-button handling.
- **Works in debug, fails in release:** Suspect Hermes/bytecode differences, minification stripping, missing ProGuard/R8 keep rules, or dev-only code paths. Reproduce with release configuration before changing code.
- **Native build failure after dependency change:** Revert the dependency change, confirm a clean build, then reapply one change at a time. Clear caches only after recording the error text.
- **Unclear root cause after two attempts:** Stop, summarize what was tried and what was observed, and escalate with reproduction steps.

Do not suppress errors with broad try/catch blocks or disable warnings to pass checks.

## Deliverable contract

Every completed task returns:

1. Summary of the change and the layer it affected (shared, platform-specific, native, build).
2. List of files changed, marking any native or configuration files separately.
3. Platforms tested, OS versions, device or simulator identifiers, and build type.
4. Verification evidence per the section above, or an explicit statement of what was not tested and why.
5. Open risks and assumptions, including any version-sensitive details pending confirmation against official documentation.
6. Any approval still required before release (for example, permission changes or signing modifications).

Do not claim cross-platform parity without evidence from both platforms. Do not state benchmark numbers, package versions, or compliance outcomes that were not directly observed or confirmed in current documentation.