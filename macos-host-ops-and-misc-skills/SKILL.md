---
name: macos-host-ops-and-misc-skills
description: Use when operating, diagnosing, or maintaining a macOS build host or developer workstation for mobile development, including Xcode toolchain selection, simulators and devices, signing identities in Keychain, DerivedData and cache cleanup, Homebrew-managed tools, and CI runner housekeeping.
author: Luo Kai
provenance: original
version: 1.0.0
---

# macOS Host Operations and Miscellaneous Mobile Build Tasks

## Purpose and boundaries

This skill covers the host-level work that surrounds iOS, iPadOS, macOS, and watchOS builds: selecting and verifying toolchains, managing simulators and attached devices, inspecting code-signing state, reclaiming disk space, keeping package-manager tools consistent, and keeping CI runner machines healthy.

It does not cover app architecture, UI code, store submission, or certificate issuance in the Apple Developer portal. Those require their own skills or explicit human ownership.

## Inputs and assumptions

Before acting, collect:

- Host identity: macOS version, hardware architecture, free disk space, and whether the machine is a personal workstation or a shared CI host.
- Required toolchain: Xcode version, SDK version, and any simulator runtimes the project pins. Read the project's version files or CI configuration rather than assuming the latest install.
- Current state, captured read-only: the active developer directory, installed Xcode bundles, simulator device list, and keychain identities.
- Owner of the host and who may approve changes to it.

Assume nothing about flags, subcommands, or output formats. Verify them against the installed tool's help output and current Apple developer documentation. Mark any detail you cannot verify as version-sensitive in your report.

## Operating workflow

1. Snapshot state read-only. Record the output of the active developer directory query, the installed Xcode list, the available simulator runtimes and devices, and free disk space. Save the snapshot to a file so changes can be compared later.
2. Identify the gap between the required and actual state. List each mismatch explicitly.
3. Plan the smallest change that closes each gap. Prefer switching the active developer directory over reinstalling Xcode. Prefer creating a new simulator over deleting an existing one.
4. Present the plan to the owner and wait for approval where a gate applies (see Decision gates).
5. Apply changes one at a time. After each change, re-run the relevant read-only check.
6. Run a representative build or test on the changed host, not just the version query.
7. Write the change log: what changed, why, the before and after snapshots, and any rollback step.

## Decision gates

Stop and request explicit approval before any of the following:

- Deleting or moving Xcode bundles, simulator runtimes, device support files, DerivedData for other projects, or Homebrew packages.
- Importing, exporting, deleting, or changing keychain items, private keys, or provisioning profiles.
- Changing system-wide settings, security policy, Gatekeeper behavior, or user accounts.
- Modifying a shared CI host that other pipelines depend on, or restarting a runner service during active jobs.
- Any action that sends data off the host, including uploading logs, symbol files, or crash reports.
- Any action on a physical device that wipes data, resets trust, or changes pairing.

Proceed without a gate only for read-only inspection and for cleaning caches that the project's own tooling regenerates, such as the current project's DerivedData, after confirming the project path.

## Verification and evidence

A change counts as done only when all of these hold:

- The active developer directory resolves to the intended Xcode, and the reported version matches the pin.
- A clean build of the target scheme succeeds on the host, with the log saved.
- The required simulator runtime boots and the test target launches on it.
- Free disk space is recorded before and after cleanup, with the reclaimed amount stated.
- Signing identities listed in the keychain are unchanged except for items the owner approved.

Evidence means saved command output and timestamps. Do not report success from memory or from exit codes alone when the output contradicts them.

## Failure handling

- Build fails after toolchain switch: revert the active developer directory to the previous path, record the error, and compare SDK versions before retrying.
- Simulator fails to boot: shut down all simulators, check the runtime status, and reboot the simulator service only if the owner has approved a restart. Do not delete the device to fix it without approval.
- Disk nearly full during build: stop, report the largest consumers, and request approval for specific deletions.
- Unexpected keychain prompt or access denial: stop automated steps, do not click through or bypass the prompt, and escalate to the owner.
- Conflicting Homebrew and Xcode-bundled tools: pin the project's tool path explicitly and record the discrepancy rather than uninstalling either.

## Deliverable contract

Every task ends with a report containing:

1. Summary of the requested outcome and whether it was met.
2. Before and after snapshots, referenced by file path.
3. Each change made, with the approval reference that authorized it.
4. Verification results, including the build and boot logs.
5. Open items, each marked as version-sensitive or unverified where applicable.
6. Rollback instructions for every change.

## What not to do

- Do not run cleanup commands with broad glob patterns against shared directories.
- Do not disable signing checks, security prompts, or sandboxing to make a build pass.
- Do not copy private keys or certificates between machines.
- Do not invent command options; check the installed tool's help first.
- Do not claim compliance or security guarantees for any configuration.
- Do not leave temporary files, debug logging, or background processes running after the task.