---
name: swiftui-uikit-interface-development
description: Use when building, migrating, or debugging iOS/iPadOS/visionOS screens that mix SwiftUI and UIKit, including embedding UIHostingController or UIViewRepresentable, bridging navigation, state, or gestures, or deciding which framework owns a given view.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SwiftUI and UIKit Interface Development

## Purpose and boundaries

This skill guides the design, implementation, and review of interfaces where SwiftUI and UIKit coexist in one app. It covers hosting SwiftUI inside UIKit containers, wrapping UIKit views for SwiftUI, sharing state and navigation across the boundary, and migrating individual screens incrementally.

It does not cover pure SwiftUI greenfield apps with no UIKit, backend design, App Store submission, or non-Apple UI toolkits. Use it when the question is "where does this view live and how do the two frameworks talk."

## Inputs and assumptions

Before acting, confirm:

- Deployment target and minimum OS version. Bridging behavior, navigation APIs, and property wrapper semantics differ across iOS releases.
- Xcode and Swift language version in use.
- The current owner of navigation: UINavigationController, a coordinator, a SwiftUI NavigationStack, or a mix.
- Whether the screen is being migrated, newly added, or repaired.
- Any UIKit-only dependencies (custom gesture recognizers, UIKit delegates, third-party views).
- Performance constraints and whether the screen is a list, a scrolling collection, or a high-frequency animation.

If any of these are unknown, state the assumption explicitly in the deliverable.

## Operating workflow

1. **Map the current hierarchy.** List each container (UIViewController, UIHostingController, UIViewRepresentable) and its owner. Note which object holds the source of truth.
2. **Choose the boundary direction.** Host SwiftUI in UIKit when the surrounding navigation or lifecycle is UIKit-controlled. Wrap UIKit in SwiftUI when a specific control has no SwiftUI equivalent. Avoid nesting bridges more than two levels deep.
3. **Define state ownership.** One observable model owns each piece of state. Pass values down; send events up through closures or a small coordinator. Never duplicate the same mutable state in both frameworks.
4. **Implement the bridge.** For UIViewRepresentable, implement `makeUIView`, `updateUIView`, and a `Coordinator` for delegate callbacks. Keep `updateUIView` idempotent: compare before assigning to avoid feedback loops.
5. **Route navigation through one owner.** Present SwiftUI screens from UIKit via the hosting controller's navigation controller, or from SwiftUI via a single path binding. Do not push the same destination from both sides.
6. **Verify on device and simulator** across the target OS range (see Verification).

## Decision gates

- **Gate A: Framework ownership.** If the screen needs UIKit-only features (UICollectionView compositional layouts with custom behavior, UIDocumentPickerViewController, AVFoundation preview layers), keep the container in UIKit and host SwiftUI subviews. Otherwise, default to SwiftUI for the new content.
- **Gate B: Bridge necessity.** Wrap a UIKit view only after confirming no native SwiftUI API meets the requirement on the minimum deployment target. Check current official documentation for availability.
- **Gate C: Lifecycle sensitivity.** If the bridged view owns a session, camera, or media resource, require explicit teardown in `dismantleUIView` or the coordinator's deinit path. Escalate for review before shipping.
- **Gate D: Destructive or external changes.** Replacing a navigation root, altering persisted state keys, or changing analytics events requires explicit approval from the project owner before implementation.

## Verification and evidence

- Build with warnings treated as review items; zero new warnings in touched files.
- Run the affected flow on the minimum supported OS and the current release. Record device model and OS build.
- Confirm no retain cycles: profile with Instruments (Leaks, Allocations) across push, pop, and dismiss of the bridged screen. Expect hosting controllers and coordinators to deallocate after dismissal.
- Confirm state consistency: change a value on each side and verify the other side updates once, with no loops (log update counts in `updateUIView`).
- Confirm accessibility: VoiceOver reads the bridged control with the same label, traits, and focus order as the native equivalent.
- Measure frame stability during scroll or animation on a representative device. Compare against the pre-change baseline; a regression beyond a noticeable dropped-frame threshold blocks merge.
- Attach screenshots or screen recordings for both light and dark appearance and the largest Dynamic Type size.

## Failure handling

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

## Deliverable contract

Provide:

1. A short hierarchy diagram (text) showing containers, owners, and bridge points.
2. The changed files with complete code for each touched type.
3. A decision record listing which gates were applied and their outcomes.
4. A verification table: check, environment (device, OS, Xcode), result, evidence link or attachment.
5. A list of assumptions and any version-sensitive APIs flagged for documentation verification.
6. Explicit approval requests for any destructive, irreversible, external-impacting, or sensitive change, marked as pending until approved.