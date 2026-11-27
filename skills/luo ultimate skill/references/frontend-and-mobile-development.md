# Frontend and Mobile Development

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## android-platform-development

**Use when:** Use when building, debugging, reviewing, or releasing native Android apps or platform-facing Android code (Kotlin/Java, Gradle, Jetpack, manifest, permissions, lifecycle, storage, background work, release signing) and a decision on architecture, API usage, or verification is needed.

### Purpose and boundaries

This skill guides engineering work on native Android applications: project configuration, component lifecycle, UI state handling, permissions, data persistence, background execution, build and signing, and Play-ready release preparation. It covers app-level code and build configuration, not Android OS internals, custom ROM work, kernel modules, or device firmware.

Stop and escalate when the task requires modifying system partitions, signing with keys you do not control, altering Play Console listings or policy declarations, or making claims about security, privacy compliance, or certification.

### Inputs and assumptions

Collect before acting:
- Target `minSdk`, `targetSdk`, and `compileSdk` from the existing Gradle files. Do not assume values.
- Build system state: Gradle wrapper version, AGP version, Kotlin version, and whether a version catalog exists.
- UI toolkit in use (Jetpack Compose, View system, or mixed) and the architecture pattern already present.
- Affected components: activities, services, workers, broadcast receivers, content providers.
- Required device or emulator matrix, and whether physical hardware is available.

If any of these are missing and cannot be read from the repository, state the assumption explicitly in your output.

### Operating workflow

1. Read `settings.gradle(.kts)`, the root and module `build.gradle(.kts)`, the version catalog, and `AndroidManifest.xml` for each module touched.
2. Map the change to lifecycle owners. Identify which state survives configuration change, process death, and task removal.
3. Choose the narrowest API that satisfies the requirement. Prefer framework or Jetpack components already in the project over new dependencies.
4. Implement in small, reviewable units. Keep UI state in observable holders; keep side effects in scoped coroutines or managed workers.
5. Update manifest declarations, permissions, and exported flags only when the change requires them, and document each addition.
6. Run the build, unit tests, lint, and instrumented tests on the agreed device matrix.
7. Produce the deliverable contract below.

### Decision gates

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

### Verification and evidence

Each change must show:
- `./gradlew assembleDebug` and `./gradlew test` completing with zero failures, plus the relevant `connectedAndroidTest` run where instrumentation applies.
- Lint report with no new errors compared to baseline. Record the baseline command and count.
- For lifecycle changes: a test or manual script covering rotation, backgrounding, and process death restoration, with the observed result.
- For permissions: a test on a device at the lowest supported API level where behavior differs, and the denial path exercised.
- For background work: confirmation that the work runs under Doze or battery-restricted conditions, or a documented limitation.
- Any version-specific behavior (permission rules, background limits, foreground service types, notification requirements, API deprecations) must be checked against current official Android developer documentation and cited by page title and access date. Do not rely on memory for these details.

Do not report performance numbers unless measured with a profiler or benchmark run you actually executed; include device model, API level, and build variant.

### Failure handling

- Build failure after dependency change: revert the change, rerun the build, then isolate by bisecting the dependency or plugin version. Do not upgrade unrelated libraries to resolve it.
- Crash on specific API level: reproduce on that level, check the stack trace for the failing call, and gate with a version check only if the framework documentation confirms the API is unavailable there.
- Flaky instrumentation tests: quarantine the test with an issue reference rather than retrying until green.
- Lint regressions: fix the cause; suppress only with a comment explaining why the suppression is correct.
- Unclear requirement or conflicting constraints: stop and list the conflict with the two options and their consequences.

### Deliverable contract

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

### Ultron routing contract

**Choose this skill when:** the application is native Android and the work concerns Android project structure, lifecycle, Jetpack/platform APIs, permissions, storage, background execution, native UI, Gradle/build configuration, signing, or Android release behavior.

**Choose `react-native-cross-platform-development` when:** the application is built primarily in React Native with a shared TypeScript/JavaScript codebase targeting both Android and iOS.

**Handoff contract:** when React Native requires Android-specific native modules, manifests, permissions, Gradle configuration, lifecycle integration, or platform debugging, the React Native skill supplies the cross-platform requirement and this skill handles the native Android boundary. Return the native API behavior, version constraints, required platform changes, and device-level verification.

**Why the boundary exists:** a React Native application may contain native Android code, but it is not the same architecture as a fully native Android application.


## app-frameworks

**Use when:** Use when choosing, scaffolding, structuring, or migrating a frontend application framework (React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit, Remix, Astro, and similar), or when diagnosing framework-level architecture problems in a web or hybrid app.

### Purpose and boundaries

This skill guides framework-level decisions for frontend applications: selecting a framework and meta-framework, establishing project structure, defining rendering strategy (client, server, static, hybrid), organizing routing and data loading, and planning framework upgrades or migrations.

In scope: framework selection rationale, project layout, routing and data-fetching patterns, rendering modes, build and deployment integration at the framework level, upgrade and migration plans.

Out of scope: visual design, backend API design, CSS methodology beyond framework integration, infrastructure provisioning, and non-web native mobile internals (advise only on framework boundaries).

### Inputs and assumptions

Collect before recommending anything:

1. Product type: content-heavy, authenticated dashboard, real-time, e-commerce, embedded widget.
2. Constraints: SEO requirements, time-to-interactive targets, browser support, offline needs, team languages and experience.
3. Existing stack: current framework and version, build tool, deployment target, test tooling.
4. Scale: expected team size, number of routes, number of contributors per area.
5. Hosting: static host, Node server, edge runtime, or container.

If any of items 1, 2, or 3 is missing, ask. Do not assume a framework version is current; state the version you reasoned about and mark it for verification against official documentation.

### Operating workflow

1. Restate the product type and the two or three requirements that most constrain the choice.
2. Enumerate candidate frameworks (maximum four). Include the existing one if this is not greenfield.
3. Score each candidate against the criteria in Decision gates.
4. Recommend one option with the reason it wins and the main tradeoff accepted.
5. Define the project skeleton: top-level directories, route layout, data-loading boundary, and where shared state lives.
6. Specify the rendering mode per route group (for example: marketing pages static, account area client-rendered behind auth).
7. Produce a migration or adoption sequence with reversible steps.
8. Attach the verification plan from Verification and evidence.

### Decision gates

Proceed only when each gate is satisfied:

- **Gate A, Requirement fit:** The framework supports the required rendering modes (SSR, SSG, or SPA) natively or through its official meta-framework. Reject candidates requiring unofficial plugins for core needs.
- **Gate B, Team fit:** At least one team member can maintain the framework; learning cost is estimated in weeks, not quarters, for the stated timeline.
- **Gate C, Ecosystem health:** Active maintenance, a documented upgrade path, and a stable release channel. Check release notes and deprecation policy at decision time.
- **Gate D, Exit cost:** Routing, data loading, and component code can be isolated so a future move is bounded. Avoid framework-specific logic leaking into domain modules.
- **Gate E, Migration risk:** For existing apps, a strangler approach (migrating route groups incrementally) is preferred over full rewrites unless the current code is unmaintainable and the team has agreed to that cost.

Require explicit user approval before: replacing a framework in a production codebase, changing the deployment runtime, deleting legacy modules, altering authentication or data-handling flows, or performing any migration that cannot be rolled back within one release.

### Verification and evidence

- Build succeeds with production configuration and the output size is recorded before and after any change.
- Route smoke test: every route in the new layout returns the expected status and renders the primary heading in a headless run.
- Rendering check: for SSR or SSG routes, confirm the server-delivered HTML contains primary content without client JavaScript executing.
- Performance baseline: record a Largest Contentful Paint and Interaction to Next Paint measurement on a representative device profile before and after. Report the figures; do not state improvements without them.
- Bundle diff: list the largest chunks added or removed.
- Upgrade checks: run the framework's official codemods or migration guide steps, and list every deprecation warning that remains.

Mark any framework option, command, or config key you cite as "verify against current official docs" unless you have confirmed it for the exact version in use.

### Failure handling

- **Build fails after scaffolding:** Revert to the last green commit, isolate the failing module, and fix in a separate change. Do not proceed to route work on a broken build.
- **Hydration or client/server mismatch:** Identify non-deterministic values (dates, random IDs, locale, browser-only APIs) rendered during server pass; move them behind a client-only boundary or stabilize them.
- **Performance regression beyond baseline:** Roll back the rendering mode change for the affected route group and profile before retrying.
- **Team resists chosen framework:** Re-run Gate B with the actual team; do not override with a preference.
- **Conflicting requirements (for example, full SSR plus fully offline):** Surface the conflict, propose route-level splits, and request a decision.

### Deliverable contract

Produce a single document containing, in order:

1. Context summary (product type, constraints, version assumptions).
2. Candidate table with gate scores and a one-line rationale per candidate.
3. Recommendation with accepted tradeoffs.
4. Project skeleton as a directory tree with a one-line purpose per top-level directory.
5. Rendering mode map by route group.
6. Ordered migration or adoption steps, each with a rollback action.
7. Verification plan with the metrics listed above and empty result fields to be filled.
8. Open items list, each with an owner and a verification source.

Do not claim performance gains, compatibility, or security properties that have not been measured or confirmed against official documentation. Do not present a recommendation as final without user approval for any gated action.

### Ultron routing contract

**Choose this skill when:** the task is deciding which frontend framework or meta-framework to use, defining application-level rendering and routing architecture, choosing the data-loading model, or planning a framework adoption or migration.

**Do not use it as the primary implementation guide when:** the framework is already selected and the work is a component-level rendering, reactivity, hydration, accessibility, or framework-idiomatic code change. Route that work to `web-frontend-frameworks`.

**Handoff to the implementation skill:** provide the selected framework and verified version, product constraints, rendering mode by route group, routing and data-loading boundaries, hosting assumptions, and any migration constraints. If implementation evidence shows the chosen architecture cannot satisfy a requirement, return the evidence here for an architectural decision rather than accumulating framework-specific workarounds.

**Why the boundary exists:** framework selection and application implementation are related but different decisions. Keeping them separate prevents a component bug from triggering an unnecessary framework redesign and prevents architectural choices from being made by whichever implementation detail was encountered first.


## apple-release-profiling-and-tooling

**Use when:** "Use when profiling, diagnosing performance, memory, energy, or launch-time regressions in iOS, iPadOS, macOS, watchOS, or tvOS release builds, or when selecting and validating Apple developer tooling (Instruments, Xcode Organizer, MetricKit, xctrace) for a release candidate."

### Purpose and boundaries

This skill guides profiling of Apple platform release candidates: choosing the right instrument, capturing comparable traces, interpreting results, and producing a regression verdict. It covers pre-release profiling, comparison against a baseline build, and interpretation of field telemetry that Apple provides.

It does not cover feature design, App Store submission mechanics, signing or provisioning changes, or rewriting app architecture beyond what a measured finding justifies.

### Inputs and assumptions

Collect before starting:

- Baseline build identifier (version, build number, commit) and candidate build identifier.
- Target OS versions and hardware classes (for example, oldest supported device and current flagship). Record the device model and OS build for every capture.
- Release-relevant user flows (cold launch, scroll-heavy list, media playback, background sync).
- Existing telemetry: crash and hang reports, MetricKit payloads, Organizer metrics, if available.
- Thresholds the team has agreed on. If none exist, record that and treat findings as observations, not gates.

Assumptions to state explicitly: tool menus, flags, and template names change between Xcode and OS releases. Verify every command, template name, and option against current Apple documentation for the toolchain in use before relying on it.

### Operating workflow

1. **Freeze the comparison.** Build baseline and candidate with the same toolchain, configuration, and signing mode (profiling-enabled configuration, not debug). Record the exact toolchain version.
2. **Standardize device state.** Use a clean-enough device: same OS build, similar free storage, low-power mode off, thermal state recorded. Reboot before a capture series.
3. **Define one scenario per trace.** Script the user action so start and end are repeatable. Repeat each scenario at least five times per build and keep all runs, not only the best one.
4. **Select the instrument by symptom:**
   - Slow launch or hitches: Time Profiler and Animation Hitches.
   - Memory growth or leaks: Allocations and Leaks, with generation marking.
   - Energy or background drain: Energy Log and CPU/network activity.
   - Disk or database stalls: File Activity and System Trace.
   - Unknown regression: start with a broad time profile, then narrow.
5. **Capture, export, and label.** Save traces with build, device, OS, scenario, and run number in the filename. Keep raw traces in the evidence store.
6. **Compare, do not eyeball.** Extract the same metric from each run (for example, time to first frame, hitch duration sum, peak resident memory after the scenario) and compare distributions, not single values.
7. **Attribute.** Map hot frames to code owners. Confirm the attributed change exists in the diff between builds before proposing a fix.
8. **Check field data.** Compare lab results against Organizer metrics or MetricKit payloads for the candidate, where available, and note sample size and time window.

### Decision gates

- **Gate A (proceed to fix):** Regression appears in at least 4 of 5 runs for both the same device and a second device class, and the attributed diff is identified.
- **Gate B (escalate before release):** Regression exceeds the agreed threshold, or crashes, hangs, or memory termination appear in candidate runs and not baseline runs. Requires release owner sign-off to ship.
- **Gate C (hold for more data):** Differences fall within run-to-run variance, or only one device class shows the change. Re-capture under controlled conditions before deciding.
- **Gate D (external action):** Any change to production telemetry configuration, submission to external services, or sharing traces outside the organization requires explicit approval from the named owner.

### Verification and evidence

Each verdict must include:

- Table of builds, devices, OS builds, toolchain version, scenario, and run count.
- Per-run metric values for baseline and candidate, plus median and spread.
- Trace file references and the frames or allocations that support the attribution.
- Telemetry sample size and window if field data is cited.
- Statement of what was not measured.

Quality checks: every metric has at least five runs per build; no trace is reported without device and OS metadata; no conclusion relies on a single run; thresholds are cited from the agreed source.

### Failure handling

- **Inconsistent runs (high variance):** Check thermal state, background load, and device storage. Re-run after reboot. If variance persists, report the metric as inconclusive.
- **Trace does not contain expected samples:** Confirm the target process was selected and the recording covered the scenario. Do not infer from partial data.
- **Tool version mismatch:** Stop, record the mismatch, and re-capture both builds with one toolchain.
- **Symbols missing or unresolved frames:** Verify dSYM availability for the exact build. Do not guess symbol names.
- **Conflicting lab and field data:** Report both; do not average them. Investigate device mix and OS distribution differences.

### Deliverable contract

Produce a single report containing: summary verdict (pass, hold, or escalate, with gate reference); comparison tables; attributed code locations with owners; recommended next action; list of approvals required; and evidence index. Do not claim performance improvements or compliance outcomes that the captured data does not directly show.

**Do not:** average away variance; profile debug builds and compare them to release builds; invent benchmark numbers, flag names, or version compatibility; change telemetry or ship builds without explicit approval; delete or overwrite baseline traces.


## flutter-cross-platform-development

**Use when:** Use when building, reviewing, or debugging a Flutter application targeting iOS, Android, web, or desktop, including state management, platform channels, responsive layouts, build configuration, and release readiness across platforms.

### Purpose and boundaries

This skill guides engineering work on a Flutter codebase that must run on more than one platform from a shared Dart code base. It covers widget architecture, state flow, navigation, platform-specific adaptation, native interop through platform channels, plugin selection, build flavors, and per-platform release readiness.

In scope: diagnosing layout and rendering defects, designing state and data boundaries, adding or reviewing platform channel code, evaluating plugins, configuring flavors and signing inputs, and preparing a verified release candidate.

Out of scope: native-only feature work with no Flutter surface, app store listing copy, legal or privacy compliance determinations, backend API design, and performance claims not backed by measurement on the target device.

### Inputs and assumptions

Collect before acting:
- Target platforms and minimum OS versions for each (set by product, not by assumption).
- Flutter and Dart SDK versions pinned in the repository, and the toolchain used in CI.
- Current state management approach and any existing architecture document.
- Failing symptom with reproduction steps, device or emulator model, and logs.
- Whether the task touches signing, store submission, or production configuration.

If the repository does not pin the SDK, stop and request the version. Treat all package versions and API signatures as version-sensitive: confirm against current official pub.dev and Flutter documentation before writing code that depends on them.

### Operating workflow

1. Reproduce. Run the app on the affected platform in the matching mode (debug for logic, profile for performance, release for signing or plugin issues). Record the exact platform and build mode.
2. Locate the boundary. Decide whether the defect lives in Dart widgets, state logic, a plugin, a platform channel, or native configuration. Read the plugin source for the failing platform before assuming a Dart fault.
3. Make the smallest change that fixes the boundary, keeping platform conditionals in one adapter layer rather than scattered through widgets.
4. Use `LayoutBuilder`, `MediaQuery`, and adaptive breakpoints rather than hard-coded pixel sizes. Respect safe areas, text scale factor, and keyboard insets on every screen you touch.
5. For platform channels, define the message contract (method name, argument types, error codes) in a single Dart file and mirror it in each native implementation. Return typed errors; never let a native exception escape as an untyped crash.
6. Add or update tests at the lowest layer that exposes the defect: unit tests for logic, widget tests for layout, integration tests on a real device for channels and permissions.
7. Verify on every targeted platform before declaring the change complete.

### Decision gates

- Plugin selection: prefer maintained plugins from verified publishers with a recent release, passing analysis on your target platforms, and a license compatible with your product. Reject a plugin that lacks support for a required platform rather than writing ad hoc native glue without review.
- State management: keep one approach per application. Do not mix providers, global singletons, and ad hoc streams for the same data.
- Platform conditionals: use `defaultTargetPlatform` or `kIsWeb` only inside adapters. If a widget branches on platform more than twice, extract it.
- Native code changes: require explicit owner approval before modifying Gradle signing, Xcode provisioning, entitlements, or manifest permissions.
- Release actions: any signing, store upload, tagging, or production configuration change requires explicit user approval and a named reviewer.

### Verification and evidence

Minimum evidence per change:
- `flutter analyze` with zero new warnings in changed files.
- `dart format --set-exit-if-changed` passes on touched files.
- Relevant unit and widget tests pass; new tests fail before the fix and pass after.
- Manual or integration check on each affected platform, with device model, OS version, and build mode recorded.
- For layout changes: screenshots at narrow phone width, tablet or desktop width, and largest system text scale.
- For release candidates: build artifacts produced from a clean checkout, with the exact commit hash and flavor recorded.

Performance statements require profile-mode measurements on a named device. Do not report frame times or startup durations from debug builds.

### Failure handling

- If reproduction fails on one platform only, record the divergence and check plugin implementation, platform version, and permissions before changing shared code.
- If a fix works on one platform and breaks another, revert the platform-specific branch and reconsider the abstraction rather than adding a further conditional.
- If a build fails in CI but not locally, compare SDK versions, Gradle or CocoaPods lockfiles, and environment variables before editing source.
- If a plugin behaves inconsistently with its documentation, pin the version, file an issue with a minimal reproduction, and use a documented workaround only with a removal note.
- Stop and escalate when the fix requires changing signing, permissions, or data handling.

### Deliverable contract

Each completed task delivers:
1. A summary of the root cause or design decision, in two to five sentences.
2. The list of changed files with a one-line reason per file.
3. The verification record: commands run, platforms tested, device and OS, build mode, and results.
4. Known limitations and any version-sensitive items flagged for confirmation against current official documentation.
5. Open approvals required before merge or release, if any.

Do not claim a platform is supported unless it was run. Do not present benchmark numbers, store acceptance, or compliance outcomes as guaranteed. Do not invent API names, flags, or package versions; quote only what has been checked in the current official documentation.

### Ultron routing contract

**Choose this skill when:** the project is Flutter and uses Dart with Flutter's widget/rendering model, plugin ecosystem, platform channels, and build flavors. It owns Flutter architecture, state/navigation, rendering defects, native interop, plugin evaluation, and platform release readiness.

**Choose `react-native-cross-platform-development` when:** the project is React Native and uses a shared JavaScript/TypeScript application with React Native's component and native-module model.

**Handoff contract:** when evaluating cross-platform architecture, compare the actual project constraints and team skills rather than assuming either framework is universally better. If a Flutter app needs native Android or iOS code, hand the platform-specific task to the relevant native skill and retain responsibility for the Flutter channel/plugin contract.

**Why the boundary exists:** Flutter and React Native solve similar product goals through different languages, rendering systems, plugin contracts, and debugging tools. Do not mix implementation guidance between them.


## javascript-typescript-runtimes

**Use when:** Use when choosing, configuring, debugging, or migrating JavaScript or TypeScript execution environments, including Node.js, Deno, Bun, browsers, and edge or serverless runtimes, or when resolving module format, TypeScript execution, or cross-runtime compatibility issues.

### Purpose and boundaries

This skill guides decisions about where JavaScript or TypeScript code executes and how it is loaded, resolved, and verified there. It covers:

- Runtime selection (server, edge, browser, CLI tooling).
- Module system behavior (CommonJS, ES modules, interop).
- How TypeScript is executed: type-stripping, transpilation, or compilation to JavaScript.
- Built-in API availability (fetch, streams, crypto, file system, timers).
- Process, environment, and package-resolution differences between runtimes.

It does not cover language syntax tutorials, bundler plugin internals, framework architecture, or infrastructure provisioning. Treat exact API names, CLI flags, and version-specific behavior as claims to confirm against current official documentation for the runtime version in use. Do not assert them from memory.

### Inputs and assumptions

Collect before recommending anything:

1. Target environment(s) and exact runtime versions in use or planned.
2. Entry point type: script, server, library, CLI, worker, or browser bundle.
3. Module format of the source and of published artifacts (`type` field, file extensions, export maps).
4. TypeScript configuration: target, module resolution mode, strictness, whether `tsc` emits or only type-checks.
5. Dependency constraints: native addons, Node-specific built-ins, or runtime-specific packages.
6. Deployment constraints: cold start limits, memory caps, filesystem access, outbound network rules.

If any item is missing and affects the answer, ask. Do not assume a runtime version is current.

### Operating workflow

1. Restate the goal in one sentence: run, ship, library-publish, migrate, or debug.
2. Identify the runtime's contract: module loader, global objects, supported standards, and I/O model.
3. Reproduce the issue with the smallest entry file that fails, in the target runtime, before changing configuration.
4. Classify the failure: module resolution, format mismatch, missing global, TypeScript emit mismatch, native dependency, or environment variable and path difference.
5. Apply the smallest change that addresses the classified cause. Prefer changing one variable per iteration.
6. Re-run in every target runtime, not only the one where the bug appeared.
7. Record the final configuration and the reasoning behind it.

### Decision gates

Proceed only when the relevant gate passes:

- **Runtime choice gate:** Required built-ins, native modules, and deployment limits are confirmed supported by the chosen runtime's current documentation. If a dependency needs a native addon, confirm prebuilt binaries exist for the target platform.
- **Module format gate:** Each published file has one unambiguous format. Mixed CJS/ESM output requires an explicit dual-package strategy and tests for both import paths.
- **TypeScript execution gate:** Confirm whether the runtime executes TypeScript natively, requires a build step, or only strips types. Native type-stripping rarely supports all TS features (for example, enums or namespaces may require transformation). Verify this against current docs.
- **Migration gate:** Migration proceeds only with a passing baseline test suite on the current runtime and a rollback path.
- **Approval gate (explicit human approval required):** Changing production runtime versions, altering deployment targets, modifying global Node or system installs, deleting lockfiles or build caches, rotating secrets used by runtime configuration, or any action that affects external users or data.

### Verification and evidence

Each conclusion needs evidence:

- Show the exact command and runtime version output used to reproduce the result.
- Compare behavior across at least two runtimes when portability is claimed.
- For module issues, demonstrate both `import` and `require` paths (where applicable) succeed.
- For TypeScript, show that type-checking and runtime execution both pass, since they verify different things.
- Measure startup time or memory only with a stated method and repeat runs. Do not report numbers without the method.
- Quality thresholds: zero unresolved import errors, zero runtime-only failures on target versions, and test pass rate unchanged or improved from baseline.

### Failure handling

- **Module not found:** Check export maps, file extensions required by the resolution mode, and `type` field. Do not add broad fallbacks that mask resolution.
- **Global not defined:** Confirm the API is standard in that runtime version. Provide a runtime-detection shim only with a documented reason.
- **Native addon failure:** Identify the platform and architecture mismatch. Recommend a pure-JS or WASM alternative only after confirming functional parity.
- **Behavior differs between runtimes:** Document the difference, isolate it in an adapter, and add a test that pins expected behavior.
- If root cause remains unknown after three bounded attempts, stop and report observations, hypotheses, and what evidence would discriminate between them.

### Deliverable contract

Every response in this domain delivers:

1. Summary of the decision or fix in no more than five sentences.
2. Runtime and version matrix tested, with the verification source for version-sensitive claims.
3. Exact configuration changes as a minimal diff or file excerpt.
4. Evidence: commands run and their observed results.
5. Open risks and items requiring human approval.

### What not to do

- Do not invent API names, flags, package versions, benchmark figures, or compatibility guarantees.
- Do not recommend global installs or system-wide changes as a fix for project-level problems.
- Do not disable type checking or strict mode to make code run.
- Do not suppress module errors with broad `any` casts, ignore comments, or catch-all wrappers.
- Do not perform destructive actions (deleting lockfiles, caches, or build outputs; overwriting configs in shared repositories) without explicit approval.
- Do not claim production readiness without evidence from the actual target runtime.


## mobile-sdk-integration

**Use when:** Use when integrating, upgrading, or auditing a third-party or in-house mobile SDK (iOS, Android, React Native, Flutter) in an app, including dependency setup, permissions, initialization, data-collection disclosures, and release verification.

### Purpose and boundaries

This skill guides an agent through adding, upgrading, removing, or reviewing a mobile SDK inside an existing native or cross-platform app. It covers dependency resolution, build configuration, permission and manifest/plist changes, initialization order, runtime wiring, privacy-manifest and data-disclosure alignment, and pre-release verification.

It does not cover: designing the SDK itself, server-side backend integration beyond the app's configuration endpoints, legal determinations about privacy compliance (route those to counsel or the privacy team), or store submission decisions.

### Inputs and assumptions

Collect before changing anything:

1. Platform targets and minimum OS versions, and the current app's build system (Gradle/Kotlin DSL, Xcode project or SwiftPM, CocoaPods, Flutter pubspec, npm/Yarn/Metro for React Native).
2. The SDK's name, the exact version requested, and the vendor's current official integration documentation. Treat any version, method name, flag, or configuration key from memory as unverified.
3. Existing SDKs that may conflict (transitive native dependencies, duplicate symbols, shared analytics or networking stacks).
4. Data the SDK collects or transmits: identifiers, location, device info, usage events, and whether any data leaves the device.
5. The target environment: staging, internal track, or production.

If any input is missing, stop and ask. Do not infer the SDK's data practices from its name.

### Operating workflow

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

### Decision gates

Pause the mobile integration and obtain release-owner approval when any of these conditions apply:

- The change adds a new permission, entitlement, background mode, or tracking capability.
- The SDK transmits personal data, device identifiers, precise location, or health/financial data off-device.
- The change requires a major version upgrade, a native toolchain change, or raising the minimum OS version.
- The change removes or replaces an existing SDK that other features depend on.
- Any step would modify production keys, signing material, store listings, or live remote configuration.
- The vendor documentation conflicts with the version in use, or the required version cannot be found.

Proceed without a gate for: local dependency resolution on a feature branch, interface wrapping, unit tests, and drafting (not submitting) disclosure text.

### Verification and evidence

Each claim of success requires evidence:

- Clean build for every configured platform and build variant, with the dependency lockfile diff reviewed and attached.
- Dependency graph shows exactly one version of the SDK and no unexpected new transitive native libraries; list any that were added.
- Merged manifest or Info.plist diff contains only the approved permission and key changes.
- Launch test on a physical device or supported emulator per minimum OS version: app starts, SDK initializes once, no crash within a 60-second idle session, and no initialization logs before consent state is set.
- Network capture (proxy or platform tooling) confirms no SDK traffic before consent and that payloads match the disclosed data categories.
- Binary size delta recorded against the baseline; flag increases above the team's agreed threshold.
- Unit tests for the wrapper cover the enabled, disabled, and not-yet-consented states.

Every version-specific fact used in the work must cite the vendor page or release note consulted, with its retrieval date.

### Failure handling

- **Build conflict:** revert the dependency change, record the conflicting artifacts, and report them. Do not force-resolve by excluding native libraries without approval.
- **Crash at startup:** remove the SDK initialization call first to isolate it. Check for missing required keys or capabilities before changing code.
- **Unexpected network traffic:** disable data collection in the wrapper, capture again, and escalate with the captured domains and timing.
- **Documentation mismatch:** halt and report the mismatch with both sources. Do not guess the correct API.
- **Repeated failure after two attempts on the same step:** stop and hand off with logs and the current diff.

### Deliverable contract

Return a single integration report containing:

1. SDK name, exact version, vendor documentation URLs with retrieval dates.
2. Changed file list, grouped by dependency, platform config, wrapper code, and tests.
3. Permissions and capabilities added or removed, with justification for each.
4. Data categories the SDK collects, the consent gate applied, and the drafted disclosure text marked as pending review.
5. Verification evidence per section above, with pass/fail status for each check.
6. Open items and approvals still required.

### What not to do

- Do not invent API names, configuration keys, flags, package versions, or minimum OS requirements. Mark any version-sensitive detail "verify against current official documentation" until confirmed.
- Do not claim compliance with any law, regulation, or store policy. Describe only what was checked.
- Do not submit store declarations, rotate keys, change signing configuration, or modify production remote configuration without explicit approval.
- Do not add permissions or background modes speculatively.
- Do not initialize the SDK from multiple entry points.
- Do not disable certificate validation or add broad network exceptions to get tests passing.


## react-native-cross-platform-development

**Use when:** Use when building, debugging, reviewing, or planning a React Native app for iOS and Android, including shared code architecture, native module bridging, platform-specific UI, performance tuning, and release preparation.

### Purpose and boundaries

This skill guides production work on React Native applications targeting iOS and Android from a shared TypeScript/JavaScript codebase. It covers:

- Project structure and shared-versus-platform code boundaries
- Navigation, state, and data-layer decisions that affect both platforms
- Platform-specific UI and behavior branching
- Native module integration and native code changes
- Performance diagnosis on device
- Build, signing, and store-submission readiness checks

It does not cover web targets (React Native Web), desktop, backend API design, or general React patterns unrelated to native rendering. It does not replace store policy review or legal/privacy review.

### Inputs and assumptions

Before acting, establish:

1. React Native version and whether the project uses the New Architecture (Fabric/TurboModules). Mark any statement about defaults, flags, or template structure for verification against the current official React Native documentation, as these change between releases.
2. Whether the project is bare React Native or uses a managed framework layer, and which tooling manages native builds.
3. Minimum supported iOS and Android versions, and target devices (low-memory Android tiers matter more than flagship benchmarks).
4. Existing native dependencies and whether each has been checked for New Architecture compatibility.
5. CI environment, signing setup, and who holds release credentials.

If any of these are unknown, state the assumption explicitly in your output rather than guessing.

### Operating workflow

1. **Reproduce on both platforms.** Run the failing flow on a real iOS device or simulator and a real Android device or emulator. Record OS version, device model, build type (debug/release), and app version. Bugs that appear on one platform only are the most common cross-platform defect class.
2. **Classify the issue.** Choose one: JS logic, rendering/layout, native module, platform API behavior, build/tooling, or performance.
3. **Locate the boundary.** Determine whether the fault lies in shared code, a platform file (`.ios.tsx` / `.android.tsx` resolution), or native code. Inspect the native logs (Xcode console, Logcat) in addition to the Metro output.
4. **Make the smallest change in the right layer.** Prefer fixing shared logic over duplicating platform forks. Introduce a platform branch only when the platform behavior genuinely differs.
5. **Verify on both platforms** (see Verification and evidence).
6. **Document the change**: affected platforms, native changes, and any new permissions or config.

### Decision gates

- **Platform split vs. shared code:** Split into platform files only when the difference is in native behavior, default styling conventions the design requires to differ, or an API that is platform-exclusive. Otherwise use `Platform.select` or a single component with a small conditional.
- **Native module vs. existing library:** Use an established, maintained library first. Write a custom native module only when no candidate supports required functionality, and then require native review from someone competent in Swift/Kotlin.
- **Dependency upgrade:** Upgrade only with a changelog review, a New Architecture compatibility check, and a rebuild of both native projects. Do not upgrade React Native and native libraries in the same change.
- **Performance work:** Proceed only after profiling on a release build on a low-tier Android device. Do not optimize from debug-mode timings.
- **Native configuration changes** (permissions, entitlements, signing, bundle identifiers, package names, app transport security, network exceptions): Stop and obtain explicit human approval before editing. These affect store review, user privacy, and existing installs.

### Verification and evidence

Each change must produce:

- Screenshots or recordings from both platforms for any UI change, showing at minimum the default and one edge state (long text, small screen, or dark mode if supported).
- Release-build test run on both platforms for any native or dependency change.
- Lint and type-check passes, and the project's unit tests green.
- For performance claims: before/after frame timing or startup measurement on the same device, with the method recorded. Do not report a percentage improvement without the raw numbers.
- For native module changes: a manual test of the failure path (permission denied, module unavailable, unsupported OS version).

Quality thresholds to check, where the project has defined them: cold start on the reference Android device within the team's agreed budget; no dropped frames during the primary scroll list on the reference device; no unhandled promise rejections in the release build.

### Failure handling

- **Works on iOS only:** Check Android-specific layout defaults (elevation, font padding, flex direction defaults are shared but text metrics differ), Android permissions, and back-button handling.
- **Works in debug, fails in release:** Suspect Hermes/bytecode differences, minification stripping, missing ProGuard/R8 keep rules, or dev-only code paths. Reproduce with release configuration before changing code.
- **Native build failure after dependency change:** Revert the dependency change, confirm a clean build, then reapply one change at a time. Clear caches only after recording the error text.
- **Unclear root cause after two attempts:** Stop, summarize what was tried and what was observed, and escalate with reproduction steps.

Do not suppress errors with broad try/catch blocks or disable warnings to pass checks.

### Deliverable contract

Every completed task returns:

1. Summary of the change and the layer it affected (shared, platform-specific, native, build).
2. List of files changed, marking any native or configuration files separately.
3. Platforms tested, OS versions, device or simulator identifiers, and build type.
4. Verification evidence per the section above, or an explicit statement of what was not tested and why.
5. Open risks and assumptions, including any version-sensitive details pending confirmation against official documentation.
6. Any approval still required before release (for example, permission changes or signing modifications).

Do not claim cross-platform parity without evidence from both platforms. Do not state benchmark numbers, package versions, or compliance outcomes that were not directly observed or confirmed in current documentation.

### Ultron routing contract

**Choose this skill when:** the project uses React Native and a shared TypeScript/JavaScript codebase to target iOS and Android. It owns shared-versus-platform code boundaries, navigation/state, native module integration, device performance, and cross-platform release readiness.

**Choose `android-platform-development` when:** the task is a native Android application or requires deep Android-specific implementation beyond the React Native integration seam.

**Handoff contract:** describe the React Native version, native module boundary, Android/iOS behavior expected, and the shared API contract. The Android skill returns platform-specific implementation and verification; this skill validates that the native change does not break the shared application or iOS behavior.

**Why the boundary exists:** shared application behavior and native platform behavior must be coordinated without pretending that one codebase removes platform-specific constraints.


## swift-language-and-concurrency

**Use when:** Use when writing, reviewing, or migrating Swift code that involves language semantics, value vs. reference types, optionals, generics, protocols, async/await, actors, Sendable checking, structured concurrency, or strict concurrency diagnostics in iOS, macOS, watchOS, or server-side Swift projects.

### Purpose and boundaries

This skill guides correct, reviewable Swift code covering core language semantics and the concurrency model (async/await, tasks, actors, isolation, Sendable). It applies to application code, library code, and migrations toward stricter concurrency checking.

In scope: diagnosing isolation and data-race errors, choosing between actors, locks, and main-actor isolation, converting callback APIs to async, reviewing value-type copy semantics, and explaining compiler diagnostics.

Out of scope: UI layout, SwiftUI view design beyond isolation questions, build-system or signing configuration, and performance claims without measurement.

### Inputs and assumptions

Collect before acting:
- Swift language version and toolchain (from `Package.swift` or project settings).
- Concurrency checking level (minimal, targeted, complete) and any language-mode flags.
- Deployment targets and whether APIs used are available on them.
- The exact compiler diagnostic text, or a minimal reproducing snippet.
- Whether the code crosses module boundaries (public API stability matters).

If any of these is missing, state the assumption explicitly in your output. Do not assume a specific Swift release has a particular feature. Mark any version-sensitive behavior as "verify against current Swift and Apple documentation."

### Operating workflow

1. Reproduce: obtain the diagnostic or write the smallest snippet that triggers the behavior.
2. Classify the problem: value semantics, optionality, generic constraint, isolation boundary, cancellation, or Sendable conformance.
3. Trace ownership: for each value crossing a suspension point or isolation boundary, identify who owns it and whether it is mutable and shared.
4. Choose the narrowest fix (see Decision gates).
5. Apply the change, keeping public signatures stable unless the user approves a breaking change.
6. Run the build with strict concurrency checking at the target level and the existing test suite.
7. Add or update a test covering the changed behavior, including cancellation paths where tasks are involved.

### Decision gates

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

### Verification and evidence

- The original diagnostic no longer appears, and no new warnings appear at the targeted checking level.
- Existing tests pass; new tests cover the changed path, including a cancelled task and an error thrown mid-await where relevant.
- For thread-safety claims, run tests under the Thread Sanitizer where the platform supports it, and report the run configuration.
- For public API changes, list each changed signature and each caller updated.
- Do not claim performance improvements from concurrency changes without a measurement. Report the benchmark method and numbers, or state that none was run.

### Failure handling

- If the fix requires a Sendable conformance you cannot justify, stop and report the specific type and the reason it is not safe to conform.
- If behavior differs across Swift versions, report both observed behaviors and flag for verification against official release notes. Do not pick one silently.
- If a fix changes a public API or actor isolation of a public type, pause and request approval before proceeding.
- If tests become flaky after a concurrency change, treat it as a race until shown otherwise. Do not add sleeps as a fix.

### Deliverable contract

Return:
1. The assumptions list (toolchain, checking level, targets).
2. The root cause in one or two sentences, naming the isolation boundary or ownership issue.
3. The minimal diff or code, with unchanged signatures called out.
4. The verification record: build configuration, test results, sanitizer runs, and anything not run.
5. Open risks and any items requiring approval.

Do not: suppress diagnostics with blanket attributes, weaken `Sendable` to make an error disappear, mark mutable shared state `nonisolated`, call `Task.detached` to escape isolation without explaining why, or describe concurrency as "fixed" when only the compiler warning changed.


## swift-networking-and-packages

**Use when:** Use when designing, reviewing, or debugging Swift networking layers (URLSession, async/await requests, decoding, auth, retries, caching) or managing Swift Package Manager dependencies for iOS, macOS, or server-side Swift projects.

### Purpose and boundaries

This skill covers two linked concerns in Swift mobile and Apple-platform work:

1. **Networking layer**: request construction, transport via URLSession, concurrency, error modeling, decoding, authentication handoff, retry and cancellation, and response caching.
2. **Package management**: adding, pinning, resolving, and reviewing Swift Package Manager (SwiftPM) dependencies, including the effect of third-party packages on binary size, build time, privacy manifests, and licensing.

Out of scope: backend API design, UI state management beyond the call boundary, push notification infrastructure, and CocoaPods or Carthage migrations (note them only as migration sources).

### Inputs and assumptions

Before acting, establish:

- Target platforms and minimum OS versions (these gate which URLSession and concurrency APIs are available).
- Swift language version and Xcode version in use.
- Whether the project uses a `Package.resolved` file and whether it is committed.
- Existing networking abstraction, if any, and its error type.
- Auth model (bearer token, cookie, mTLS, none) and where credentials are stored.
- Data sensitivity: personal, health, financial, or regulated data changes what may be logged or cached.

If any of these is unknown, ask. Do not assume a minimum OS version.

### Operating workflow

1. **Map the call path.** Trace one request from call site to wire: request builder, session configuration, delegate or interceptor, decoder, error mapping, caller.
2. **Classify the change.** Networking-only, dependency-only, or both. Dependency changes require the gates below.
3. **Define the contract.** Write the expected status codes, decodable shapes, error cases, and timeout values before editing code.
4. **Implement behind one seam.** Route all requests through a single client protocol so tests can substitute a fake transport. Prefer `async throws` functions over completion handlers in new code.
5. **Model errors explicitly.** Separate transport failure, HTTP status failure, decoding failure, and cancellation into distinct cases. Never collapse them into a generic string.
6. **Handle cancellation.** Propagate task cancellation to URLSession calls. Do not swallow `CancellationError`.
7. **Retry narrowly.** Retry only idempotent requests, only on transient failures (timeouts, 429 or 503 with backoff honoring `Retry-After`), with a bounded attempt count and jitter.
8. **For packages,** add the minimum product needed, pin via `Package.resolved`, and record the reason in the PR description.

### Decision gates

Stop and obtain explicit user approval before:

- Adding any new third-party package, or upgrading a major version of an existing one.
- Changing the committed `Package.resolved` other than through a normal resolve.
- Deleting, force-resetting, or rewriting caches, keychains, or stored tokens.
- Changing TLS settings, certificate pinning, or disabling ATS exceptions.
- Adding logging of request or response bodies, headers containing credentials, or personal data.
- Altering server-facing behavior: new endpoints, changed retry semantics on non-idempotent methods (POST, PATCH without idempotency keys), or changed rate of calls.
- Any change that alters a privacy manifest or data-collection declaration.

Proceed without a gate for: local refactors within the seam, adding unit tests, and fixing decoding errors against a documented contract.

### Verification and evidence

Each change must show:

- **Build**: clean build on the minimum supported OS target and the current toolchain.
- **Tests**: unit tests with a fake transport covering success, each HTTP error class, malformed JSON, cancellation mid-request, and retry exhaustion. Target all branches of the error mapper.
- **Dependency audit**: `swift package show-dependencies` output (or the Xcode equivalent) attached to dependency PRs, with each new package's license and privacy manifest status checked by reading its repository. Confirm the exact current command syntax against official SwiftPM documentation.
- **Binary impact**: for new packages, measured app-size delta from an archive, reported as measured, not estimated.
- **Concurrency check**: build with strict concurrency checking enabled at the level the project uses; report any new warnings.

Do not state performance improvements, benchmark numbers, or compliance status without a measurement or a document reference.

### Failure handling

- **Resolution conflict**: report the conflicting version requirements verbatim, identify the dependent package, and propose either a version range change or a fork. Do not force a version with overrides without approval.
- **Unexpected status codes**: map to a generic server error case, preserve status and a redacted body excerpt for debugging, and flag for contract review.
- **Decoding failure**: surface the decoding path (key path) to the developer; do not silently default missing fields unless the contract marks them optional.
- **Flaky retries or duplicate writes**: stop retry, check idempotency, and escalate.
- **Uncertain API availability**: if an API's availability or signature is unverified, mark it "verify against current Apple documentation" rather than guessing.

### Deliverable contract

Every deliverable includes:

1. A short statement of what changed and why, in two to four sentences.
2. The file list with each file's role.
3. The error model and call contract for any new endpoint, as a table: method, path, success type, error cases, retry policy.
4. For package changes: package name, requested version rule, products added, license, reason, and approval reference.
5. Test results and the verification items above, with unverified items explicitly labeled.
6. Open questions and any gated actions awaiting approval.

### What not to do

- Do not use `try!` or force-unwrap response data in production paths.
- Do not disable certificate validation for debugging and leave it in code.
- Do not store tokens in UserDefaults or plain files; use the platform keychain.
- Do not retry POST requests without an idempotency mechanism agreed with the server.
- Do not add a package to solve a problem the standard library or URLSession already solves.
- Do not invent API names, flags, or package versions; verify against current official documentation.


## swiftui-uikit-interface-development

**Use when:** Use when building, migrating, or debugging iOS/iPadOS/visionOS screens that mix SwiftUI and UIKit, including embedding UIHostingController or UIViewRepresentable, bridging navigation, state, or gestures, or deciding which framework owns a given view.

### Purpose and boundaries

This skill guides the design, implementation, and review of interfaces where SwiftUI and UIKit coexist in one app. It covers hosting SwiftUI inside UIKit containers, wrapping UIKit views for SwiftUI, sharing state and navigation across the boundary, and migrating individual screens incrementally.

It does not cover pure SwiftUI greenfield apps with no UIKit, backend design, App Store submission, or non-Apple UI toolkits. Use it when the question is "where does this view live and how do the two frameworks talk."

### Inputs and assumptions

Before acting, confirm:

- Deployment target and minimum OS version. Bridging behavior, navigation APIs, and property wrapper semantics differ across iOS releases.
- Xcode and Swift language version in use.
- The current owner of navigation: UINavigationController, a coordinator, a SwiftUI NavigationStack, or a mix.
- Whether the screen is being migrated, newly added, or repaired.
- Any UIKit-only dependencies (custom gesture recognizers, UIKit delegates, third-party views).
- Performance constraints and whether the screen is a list, a scrolling collection, or a high-frequency animation.

If any of these are unknown, state the assumption explicitly in the deliverable.

### Operating workflow

1. **Map the current hierarchy.** List each container (UIViewController, UIHostingController, UIViewRepresentable) and its owner. Note which object holds the source of truth.
2. **Choose the boundary direction.** Host SwiftUI in UIKit when the surrounding navigation or lifecycle is UIKit-controlled. Wrap UIKit in SwiftUI when a specific control has no SwiftUI equivalent. Avoid nesting bridges more than two levels deep.
3. **Define state ownership.** One observable model owns each piece of state. Pass values down; send events up through closures or a small coordinator. Never duplicate the same mutable state in both frameworks.
4. **Implement the bridge.** For UIViewRepresentable, implement `makeUIView`, `updateUIView`, and a `Coordinator` for delegate callbacks. Keep `updateUIView` idempotent: compare before assigning to avoid feedback loops.
5. **Route navigation through one owner.** Present SwiftUI screens from UIKit via the hosting controller's navigation controller, or from SwiftUI via a single path binding. Do not push the same destination from both sides.
6. **Verify on device and simulator** across the target OS range (see Verification).

### Decision gates

- **Gate A: Framework ownership.** If the screen needs UIKit-only features (UICollectionView compositional layouts with custom behavior, UIDocumentPickerViewController, AVFoundation preview layers), keep the container in UIKit and host SwiftUI subviews. Otherwise, default to SwiftUI for the new content.
- **Gate B: Bridge necessity.** Wrap a UIKit view only after confirming no native SwiftUI API meets the requirement on the minimum deployment target. Check current official documentation for availability.
- **Gate C: Lifecycle sensitivity.** If the bridged view owns a session, camera, or media resource, require explicit teardown in `dismantleUIView` or the coordinator's deinit path. Escalate for review before shipping.
- **Gate D: Destructive or external changes.** Replacing a navigation root, altering persisted state keys, or changing analytics events requires explicit approval from the project owner before implementation.

### Verification and evidence

- Build with warnings treated as review items; zero new warnings in touched files.
- Run the affected flow on the minimum supported OS and the current release. Record device model and OS build.
- Confirm no retain cycles: profile with Instruments (Leaks, Allocations) across push, pop, and dismiss of the bridged screen. Expect hosting controllers and coordinators to deallocate after dismissal.
- Confirm state consistency: change a value on each side and verify the other side updates once, with no loops (log update counts in `updateUIView`).
- Confirm accessibility: VoiceOver reads the bridged control with the same label, traits, and focus order as the native equivalent.
- Measure frame stability during scroll or animation on a representative device. Compare against the pre-change baseline; a regression beyond a noticeable dropped-frame threshold blocks merge.
- Attach screenshots or screen recordings for both light and dark appearance and the largest Dynamic Type size.

### Failure handling

- **Blank or zero-size bridged view:** Check that the representable has a defined intrinsic size or that the parent applies a frame. Verify Auto Layout constraints on the hosting view.
- **Update loops or stale UI:** Remove side-effecting code from `updateUIView`. Move event handling to the coordinator and publish changes through the single owner.
- **Navigation stack corruption:** Stop and map the current stack. Do not attempt to fix by pushing duplicates. Revert to the last known-good owner.
- **Memory growth:** Isolate by removing the bridge and comparing. Escalate with Instruments traces rather than guessing.
- **Unknown API behavior or availability:** Do not infer. Mark the detail as version-sensitive and verify against current official Apple documentation before committing code.

Do not:
- Mutate SwiftUI state from UIKit delegate callbacks on background threads; dispatch to the main actor.
- Store UIViewController references inside SwiftUI views.
- Mix two navigation systems for the same screen stack without a written ownership decision.
- Claim performance or compliance improvements without measured evidence.

### Deliverable contract

Provide:

1. A short hierarchy diagram (text) showing containers, owners, and bridge points.
2. The changed files with complete code for each touched type.
3. A decision record listing which gates were applied and their outcomes.
4. A verification table: check, environment (device, OS, Xcode), result, evidence link or attachment.
5. A list of assumptions and any version-sensitive APIs flagged for documentation verification.
6. Explicit approval requests for any destructive, irreversible, external-impacting, or sensitive change, marked as pending until approved.


## web-frontend-frameworks

**Use when:** Use when choosing, structuring, debugging, migrating, or reviewing a browser-based UI built with a component framework or meta-framework (React, Vue, Svelte, Angular, Solid, Next.js, Nuxt, SvelteKit, Remix, Astro), including rendering-mode, state, routing, and build-tooling decisions.

### Purpose and boundaries

This skill guides professional work on component-based browser UIs: selecting a framework or rendering strategy, organizing components and state, wiring routing and data loading, diagnosing rendering or hydration faults, planning version migrations, and reviewing framework-specific code.

In scope: component models, reactivity and state flow, rendering modes (client-side, server-side, static, streaming, islands), hydration, routing and data fetching conventions, build integration, bundle size, accessibility of rendered output, and framework-level testing.

Out of scope: backend API design, visual design systems, native mobile frameworks, general JavaScript language questions unrelated to UI, and infrastructure provisioning beyond the frontend build and deploy step.

### Inputs and assumptions

Collect before recommending anything:

1. Target framework and exact version, read from the lockfile, not from memory.
2. Rendering requirements: SEO needs, personalization, offline use, first-load budget.
3. Runtime targets: browsers and devices, including minimum supported versions.
4. Existing constraints: team skill, monorepo, design system, hosting platform.
5. Data sources and whether they are authenticated or user-scoped.

Assumptions must be stated explicitly. If the version is unknown, say so and treat every API detail as provisional.

### Operating workflow

1. Restate the goal and the constraint that matters most (usually first-load performance, SEO, or interactivity).
2. Inspect the project: framework version, router type, rendering config, state library, test runner, build tool.
3. Map the component tree and identify where state lives. Keep server state, URL state, and transient UI state in separate homes.
4. Choose the smallest change that resolves the problem. Prefer local fixes over architectural rewrites unless the request is explicitly architectural.
5. Implement or recommend the change with the framework's idiomatic primitives for the verified version.
6. Run verification (below) and report results with evidence.

### Decision gates

Proceed only when the gate is passed; otherwise stop and ask.

- **Framework switch or major migration:** requires an inventory of dependencies, a written rollback path, and explicit approval from the owner.
- **Rendering mode change (e.g., client-only to server-rendered):** requires confirming hosting supports it and that data fetched on the server does not leak per-user secrets to cached responses.
- **Adding a global state library:** justify only if at least two distant components share mutable state that cannot live in server cache or URL.
- **Client-side fetching on initial render:** prefer framework data-loading primitives or server rendering when the data is needed for first paint.
- **Dependency upgrades:** pin, read the official migration guide for that exact version, and run the full test suite before and after.

### Verification and evidence

Report each check as pass, fail, or not run, with the command or observation behind it.

- Type check and linter pass with no newly suppressed diagnostics.
- Unit and component tests cover changed components; tests assert user-visible behavior, not internal state.
- No hydration mismatch warnings in the browser console for affected routes.
- Lighthouse or equivalent run on affected pages: compare before and after on the same machine and throttling profile. Report numbers only if measured.
- Production build succeeds; bundle diff for changed routes is reported in kilobytes gzipped.
- Keyboard navigation and focus order checked on changed interactive components; ARIA roles match native semantics where available.
- Effects and subscriptions have cleanup; list any that do not and why.

Do not claim performance improvements without before-and-after measurements.

### Failure handling

- **Hydration mismatch:** search for non-deterministic output (dates, random IDs, locale-dependent formatting, browser-only globals) in the render path. Move such values into effects or pass them from the server consistently.
- **Stale data after mutation:** check that the cache invalidation or revalidation mechanism the framework provides is called with the correct key. Do not add a polling workaround first.
- **Infinite render or update loops:** inspect dependency arrays, reactive computations that write to their own inputs, and unstable object or function identities passed as props.
- **Build failure after upgrade:** read the release notes for breaking changes, fix one category at a time, and re-run the build after each.
- **Unclear root cause after two attempts:** stop, summarize what was tried and observed, and ask for the reproduction steps or a minimal reproduction.

### Deliverable contract

Every deliverable contains:

1. Framework and version verified, with the source used (lockfile, config file, or user statement).
2. A short summary of the decision or fix, with the constraint that drove it.
3. Code changes as complete, runnable files or precise diffs, not fragments with ellipses.
4. A verification table listing each check from the previous section with status and evidence.
5. A list of open risks and any API details flagged for confirmation against current official documentation.

### What not to do

- Do not invent API names, hook signatures, configuration keys, CLI flags, or package versions. If unsure, say "verify in the official docs for version X."
- Do not state benchmark numbers, compliance outcomes, or security guarantees that were not measured or documented.
- Do not add a state library, animation library, or UI kit without a stated need.
- Do not disable lint rules, type checks, or accessibility warnings to get a build passing.
- Do not store tokens or secrets in client-accessible state, local storage, or rendered HTML.
- Do not run destructive or external-impacting actions without explicit approval: deleting branches or build caches, force-pushing, publishing packages, changing production DNS, deploying to production, or altering shared CI configuration. Describe the command and its effect, then wait for confirmation.

### Ultron routing contract

**Choose this skill when:** a frontend framework is already selected and the task concerns components, state ownership, rendering, hydration, routing implementation, framework-specific debugging, accessibility of rendered UI, bundle behavior, or a targeted migration within that framework.

**Do not use it as the primary decision guide when:** the unresolved question is which framework or meta-framework the application should adopt, which rendering architecture should govern the whole product, or whether to migrate the application. Route those decisions to `app-frameworks`.

**Handoff to the architecture skill:** when an implementation limitation reveals a genuine architectural mismatch, return the verified framework/version, affected routes, measured behavior, constraints that cannot be met, and the smallest viable alternatives. Do not turn a local defect into a framework replacement proposal without evidence.

**Why the boundary exists:** this skill owns correct implementation within a chosen frontend stack; the architecture skill owns selection and application-wide tradeoffs.


## web-performance

**Use when:** Use when diagnosing, measuring, or improving frontend page load, rendering, interactivity, or runtime responsiveness in a web application, including Core Web Vitals triage, bundle size reduction, caching and asset delivery review, and performance regression checks.

### Purpose and boundaries

This skill covers client-side and delivery-layer performance of web frontends: how fast content becomes visible, how quickly the page responds to input, how visually stable it is, and how much data and script it ships. It produces measured findings and ranked, reversible changes.

In scope: field and lab metric analysis, network waterfall review, JavaScript bundle and main-thread analysis, image and font loading, rendering and layout stability, HTTP caching and compression configuration review, and performance budgets in CI.

Out of scope: backend query tuning, capacity planning, CDN contract decisions, and redesigns unrelated to measured bottlenecks. Route those to the appropriate owner and say so.

### Inputs and assumptions

Required before analysis:
- The target URL or route list, and the user journeys that matter (landing, checkout, dashboard interaction).
- Access to at least one measurement source: field data (RUM or CrUX-style reporting), a lab profiler, or a reproducible local build.
- The framework and build tooling in use. Treat framework-specific APIs as version-sensitive; verify against current official documentation before recommending them.
- Target device and network profile. Do not assume desktop fast-network results represent users.

Assumptions to state explicitly in the report: test device class, throttling profile, cache state (cold or warm), and whether results are lab or field.

### Operating workflow

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

### Decision gates

- **Proceed to code changes only if** the bottleneck is reproduced in lab data and the baseline variance is smaller than the expected improvement. If variance is larger, collect more runs first.
- **Lazy-load or code-split** only for content below the fold or behind user action. Never defer the LCP element or above-the-fold critical styles.
- **Add preload or fetchpriority hints** only for resources the browser discovers late and that are verified as LCP candidates. Excessive hints degrade performance.
- **Adopt a caching change** only after confirming the asset is content-hashed or the cache key is explicitly versioned. Unversioned long-lived caching of mutable URLs is a defect.
- **Remove a dependency** only after confirming replacement behavior parity in tests.
- **Stop and request approval** before changing production CDN rules, cache purge operations, third-party tag removal (analytics, ads, consent tools), or any change affecting legal consent or tracking behavior.

### Verification and evidence

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

### Failure handling

- **Metrics conflict** (lab improves, field does not): report the discrepancy, check device and network mix of field users, and do not ship on lab data alone.
- **Change regresses another metric:** revert, record the trade-off, and propose a narrower alternative.
- **Measurement noise dominates:** increase run count, pin environment, and report the uncertainty instead of forcing a conclusion.
- **Missing tooling or access:** state which measurement is unavailable and what conclusions are therefore withheld.
- **Version uncertainty** about a framework or browser API: mark it unverified and direct the user to the current official documentation rather than guessing.

### What not to do

- Do not add performance hints, inline critical CSS, or caching headers by habit without a measured failing metric behind them.
- Do not minify or obfuscate as a substitute for removing unused code.
- Do not remove third-party scripts or change consent logic without explicit approval.
- Do not disable features, lazy-load the LCP element, or hide content to win a score.
- Do not present synthetic scores as user experience evidence.

### Deliverable contract

Produce a report containing:
1. Scope, environment, device and network profile, and cache state.
2. Baseline table: route, metric, median, spread, field status.
3. Ranked bottleneck list with phase classification and evidence links or trace references.
4. Proposed changes with expected impact, risk, and reversal path.
5. Verification results with before and after data for each implemented change.
6. Open items, unverified version-sensitive details, and approval requests.

