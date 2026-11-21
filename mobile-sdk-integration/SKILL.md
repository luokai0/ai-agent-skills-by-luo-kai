---
name: mobile-sdk-integration
description: Use when integrating, upgrading, or auditing a third-party or in-house mobile SDK (iOS, Android, React Native, Flutter) in an app, including dependency setup, permissions, initialization, data-collection disclosures, and release verification.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Mobile SDK Integration

## Purpose and boundaries

This skill guides an agent through adding, upgrading, removing, or reviewing a mobile SDK inside an existing native or cross-platform app. It covers dependency resolution, build configuration, permission and manifest/plist changes, initialization order, runtime wiring, privacy-manifest and data-disclosure alignment, and pre-release verification.

It does not cover: designing the SDK itself, server-side backend integration beyond the app's configuration endpoints, legal determinations about privacy compliance (route those to counsel or the privacy team), or store submission decisions.

## Inputs and assumptions

Collect before changing anything:

1. Platform targets and minimum OS versions, and the current app's build system (Gradle/Kotlin DSL, Xcode project or SwiftPM, CocoaPods, Flutter pubspec, npm/Yarn/Metro for React Native).
2. The SDK's name, the exact version requested, and the vendor's current official integration documentation. Treat any version, method name, flag, or configuration key from memory as unverified.
3. Existing SDKs that may conflict (transitive native dependencies, duplicate symbols, shared analytics or networking stacks).
4. Data the SDK collects or transmits: identifiers, location, device info, usage events, and whether any data leaves the device.
5. The target environment: staging, internal track, or production.

If any input is missing, stop and ask. Do not infer the SDK's data practices from its name.

## Operating workflow

1. **Baseline.** Record the current build status, dependency lockfile state, and app version. Create a branch or a clean working copy so the change is reviewable and revertible.
2. **Read the vendor documentation for the exact version.** Extract: minimum platform versions, required permissions, required entitlements or capabilities, initialization requirements, threading rules, and privacy disclosure requirements.
3. **Resolve dependencies.** Add the SDK using the project's native manager. Pin the version explicitly. Check the resulting dependency graph for version conflicts and duplicated native libraries. Commit the lockfile change.
4. **Configure platform files.** Make the minimum manifest, plist, or entitlement changes the vendor requires. Do not add broad permissions "in case" they are needed.
5. **Initialize once, early, and in the documented place.** Use the vendor-specified application or lifecycle entry point. Guard against repeated initialization and against calls before required consent or configuration is available.
6. **Wrap the SDK behind a thin internal interface.** Expose only the methods the app needs. This limits blast radius for future replacement and makes test doubles possible.
7. **Gate data collection.** Ensure the SDK does not collect or transmit data before the applicable consent state is known. Where the vendor provides a collection toggle, default it to the most restrictive value until consent is confirmed.
8. **Update disclosures.** Draft the changes to the platform privacy declarations (iOS privacy manifest and App Store data-collection answers; Google Play Data safety form) as proposals for human review. Do not submit them.
9. **Verify** (see the verification section).
10. **Document.** Produce the deliverable contract artifacts.

## Decision gates

Pause the mobile integration and obtain release-owner approval when any of these conditions apply:

- The change adds a new permission, entitlement, background mode, or tracking capability.
- The SDK transmits personal data, device identifiers, precise location, or health/financial data off-device.
- The change requires a major version upgrade, a native toolchain change, or raising the minimum OS version.
- The change removes or replaces an existing SDK that other features depend on.
- Any step would modify production keys, signing material, store listings, or live remote configuration.
- The vendor documentation conflicts with the version in use, or the required version cannot be found.

Proceed without a gate for: local dependency resolution on a feature branch, interface wrapping, unit tests, and drafting (not submitting) disclosure text.

## Verification and evidence

Each claim of success requires evidence:

- Clean build for every configured platform and build variant, with the dependency lockfile diff reviewed and attached.
- Dependency graph shows exactly one version of the SDK and no unexpected new transitive native libraries; list any that were added.
- Merged manifest or Info.plist diff contains only the approved permission and key changes.
- Launch test on a physical device or supported emulator per minimum OS version: app starts, SDK initializes once, no crash within a 60-second idle session, and no initialization logs before consent state is set.
- Network capture (proxy or platform tooling) confirms no SDK traffic before consent and that payloads match the disclosed data categories.
- Binary size delta recorded against the baseline; flag increases above the team's agreed threshold.
- Unit tests for the wrapper cover the enabled, disabled, and not-yet-consented states.

Every version-specific fact used in the work must cite the vendor page or release note consulted, with its retrieval date.

## Failure handling

- **Build conflict:** revert the dependency change, record the conflicting artifacts, and report them. Do not force-resolve by excluding native libraries without approval.
- **Crash at startup:** remove the SDK initialization call first to isolate it. Check for missing required keys or capabilities before changing code.
- **Unexpected network traffic:** disable data collection in the wrapper, capture again, and escalate with the captured domains and timing.
- **Documentation mismatch:** halt and report the mismatch with both sources. Do not guess the correct API.
- **Repeated failure after two attempts on the same step:** stop and hand off with logs and the current diff.

## Deliverable contract

Return a single integration report containing:

1. SDK name, exact version, vendor documentation URLs with retrieval dates.
2. Changed file list, grouped by dependency, platform config, wrapper code, and tests.
3. Permissions and capabilities added or removed, with justification for each.
4. Data categories the SDK collects, the consent gate applied, and the drafted disclosure text marked as pending review.
5. Verification evidence per section above, with pass/fail status for each check.
6. Open items and approvals still required.

## What not to do

- Do not invent API names, configuration keys, flags, package versions, or minimum OS requirements. Mark any version-sensitive detail "verify against current official documentation" until confirmed.
- Do not claim compliance with any law, regulation, or store policy. Describe only what was checked.
- Do not submit store declarations, rotate keys, change signing configuration, or modify production remote configuration without explicit approval.
- Do not add permissions or background modes speculatively.
- Do not initialize the SDK from multiple entry points.
- Do not disable certificate validation or add broad network exceptions to get tests passing.