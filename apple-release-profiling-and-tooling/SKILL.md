---
name: apple-release-profiling-and-tooling
description: "Use when profiling, diagnosing performance, memory, energy, or launch-time regressions in iOS, iPadOS, macOS, watchOS, or tvOS release builds, or when selecting and validating Apple developer tooling (Instruments, Xcode Organizer, MetricKit, xctrace) for a release candidate."
author: Luo Kai
provenance: original
version: 1.0.0
---

# Apple Release Profiling And Tooling

## Purpose and boundaries

This skill guides profiling of Apple platform release candidates: choosing the right instrument, capturing comparable traces, interpreting results, and producing a regression verdict. It covers pre-release profiling, comparison against a baseline build, and interpretation of field telemetry that Apple provides.

It does not cover feature design, App Store submission mechanics, signing or provisioning changes, or rewriting app architecture beyond what a measured finding justifies.

## Inputs and assumptions

Collect before starting:

- Baseline build identifier (version, build number, commit) and candidate build identifier.
- Target OS versions and hardware classes (for example, oldest supported device and current flagship). Record the device model and OS build for every capture.
- Release-relevant user flows (cold launch, scroll-heavy list, media playback, background sync).
- Existing telemetry: crash and hang reports, MetricKit payloads, Organizer metrics, if available.
- Thresholds the team has agreed on. If none exist, record that and treat findings as observations, not gates.

Assumptions to state explicitly: tool menus, flags, and template names change between Xcode and OS releases. Verify every command, template name, and option against current Apple documentation for the toolchain in use before relying on it.

## Operating workflow

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

## Decision gates

- **Gate A (proceed to fix):** Regression appears in at least 4 of 5 runs for both the same device and a second device class, and the attributed diff is identified.
- **Gate B (escalate before release):** Regression exceeds the agreed threshold, or crashes, hangs, or memory termination appear in candidate runs and not baseline runs. Requires release owner sign-off to ship.
- **Gate C (hold for more data):** Differences fall within run-to-run variance, or only one device class shows the change. Re-capture under controlled conditions before deciding.
- **Gate D (external action):** Any change to production telemetry configuration, submission to external services, or sharing traces outside the organization requires explicit approval from the named owner.

## Verification and evidence

Each verdict must include:

- Table of builds, devices, OS builds, toolchain version, scenario, and run count.
- Per-run metric values for baseline and candidate, plus median and spread.
- Trace file references and the frames or allocations that support the attribution.
- Telemetry sample size and window if field data is cited.
- Statement of what was not measured.

Quality checks: every metric has at least five runs per build; no trace is reported without device and OS metadata; no conclusion relies on a single run; thresholds are cited from the agreed source.

## Failure handling

- **Inconsistent runs (high variance):** Check thermal state, background load, and device storage. Re-run after reboot. If variance persists, report the metric as inconclusive.
- **Trace does not contain expected samples:** Confirm the target process was selected and the recording covered the scenario. Do not infer from partial data.
- **Tool version mismatch:** Stop, record the mismatch, and re-capture both builds with one toolchain.
- **Symbols missing or unresolved frames:** Verify dSYM availability for the exact build. Do not guess symbol names.
- **Conflicting lab and field data:** Report both; do not average them. Investigate device mix and OS distribution differences.

## Deliverable contract

Produce a single report containing: summary verdict (pass, hold, or escalate, with gate reference); comparison tables; attributed code locations with owners; recommended next action; list of approvals required; and evidence index. Do not claim performance improvements or compliance outcomes that the captured data does not directly show.

**Do not:** average away variance; profile debug builds and compare them to release builds; invent benchmark numbers, flag names, or version compatibility; change telemetry or ship builds without explicit approval; delete or overwrite baseline traces.