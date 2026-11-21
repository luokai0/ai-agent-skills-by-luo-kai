---
name: productivity-agent-workflows
description: Use when an agent must plan, execute, or audit multi-step productivity work across external registries (package indexes, container registries, model hubs, plugin marketplaces, template galleries) and needs a controlled, verifiable workflow for discovery, selection, publishing, and maintenance.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Productivity Agent Workflows

## Purpose and boundaries

This skill governs how an agent finds, evaluates, consumes, and publishes artifacts through external registries as part of professional productivity work: dependency updates, template reuse, shared asset maintenance, and routine registry housekeeping.

In scope:
- Searching registries and shortlisting candidates against written requirements.
- Reading metadata (maintainer, license, release history, deprecation notices, checksums, signatures) before use.
- Staging installs or pulls in an isolated location and verifying them.
- Preparing publish or update operations as drafts, with dry runs where the registry supports them.

Out of scope:
- Publishing, deleting, yanking, transferring ownership, or changing access policies without explicit approval (see Decision gates).
- Authoring malware analysis, credential harvesting, or evasion of registry rate limits or access controls.
- Legal or compliance determinations. Report license and policy facts; do not certify compliance.

## Inputs and assumptions

Before acting, confirm or record:
1. The goal in one sentence and the success condition.
2. Registry name, base URL, and the account or token context. Tokens are used only if the user supplied them for this task; never echo them.
3. Target environment (OS, runtime, language version) and any pinned constraints.
4. Allowed actions: read-only, stage-only, or publish.
5. Whether the artifact is internal, public, or contains sensitive data.

Assumptions must be stated in the output. Registry behavior, flags, and API endpoints change. Any command syntax, endpoint path, or version number you cite must be checked against the registry's current official documentation before it is presented as fact. Mark unverified items as `[verify]`.

## Operating workflow

1. **Define requirements.** Write a short checklist: functional need, minimum version, license class acceptable to the user, maximum age of last release, required platforms.
2. **Discover.** Run at least two search angles (by name, by keyword/tag, by maintainer). Record candidate identifiers exactly as shown by the registry.
3. **Screen.** Eliminate candidates failing hard requirements. Record the reason for each elimination.
4. **Inspect metadata.** For each remaining candidate capture: publisher identity, last release date, release frequency, open deprecation or security notices, declared license, dependency count, download or usage signals (labelled as signals, not quality proof), and checksum or signature availability.
5. **Stage.** Install or fetch into a scratch directory or disposable environment. Never into the production tree first.
6. **Verify.** Apply the checks in "Verification and evidence."
7. **Integrate or draft publish.** Make the minimal change to the project. For publishing, prepare the artifact, metadata, and a dry-run report, then stop at the decision gate.
8. **Record.** Write the evidence log and the rollback path.

Example: Updating a shared internal template package. Discover the current published version, compare changelog entries between pinned and latest, stage the new version in a scratch project, run the template test suite, and produce a diff of generated output. Publishing the new version waits for approval.

Example: Choosing a base container image. Compare image digests and build provenance statements where the registry exposes them; prefer images whose publisher and build source are documented; pin by digest rather than mutable tag.

## Decision gates

Stop and request explicit, specific approval before any of the following:
- Publishing, overwriting, or re-tagging an artifact. Overwriting a published version is never allowed; a new version is required.
- Deleting, yanking, deprecating, or unpublishing any artifact.
- Changing ownership, collaborators, visibility, tokens, or access policy.
- Any action that sends data outside the environment, including uploading logs, source, or datasets.
- Installing packages that run install-time scripts on a machine that holds credentials.
- Anything involving personal data, secrets, regulated data, or customer material.
- Actions that would consume paid quota or incur cost.

Proceed without asking only for read-only discovery, metadata inspection, and staged installs into scratch locations.

Choose "reject" over "proceed with warning" when: the publisher is unidentifiable, the artifact has an unresolved security advisory affecting the required version, the license conflicts with the stated usage class, or checksums do not match the registry's published values.

## Verification and evidence

Quality checks that must pass before integration:
- Checksum or digest of the staged artifact matches the registry-published value. Record both.
- Signature or attestation verified where offered, using the registry's documented tooling `[verify]`.
- Test suite of the consuming project passes on the target runtime, with the pinned version.
- Dependency tree diff shows only the expected additions and removals; no unexpected transitive upgrades.
- Generated output or behavior diff reviewed; differences listed and each explained.
- Advisory check performed against the registry's or a recognized vulnerability database's data for the exact version.

Evidence log format (one line per item): `check | command or source | timestamp | result | artifact identifier`. Do not record secrets in logs.

Measurable targets: zero unexplained transitive changes; 100% of artifacts pinned to an exact version or digest; every rejected candidate has a stated reason.

## Failure handling

- **Checksum mismatch:** Discard the staged artifact. Do not retry with the same source more than once. Report the mismatch with both values and recommend escalation.
- **Registry unavailable or rate-limited:** Back off, record the time, and resume later. Do not switch to unofficial mirrors without approval.
- **Test failure after upgrade:** Revert to the pinned version in the scratch environment, confirm the baseline passes, then determine whether the failure is caused by the new artifact before changing the project.
- **Ambiguous metadata:** Mark the field as unknown. Do not infer a license or maintainer from partial data.
- **Partial publish:** Stop immediately, report the state of every published object, and wait for a decision. Do not attempt cleanup deletions without approval.

## Deliverable contract

Every run ends with a report containing, in order:
1. Goal and outcome (met, partially met, blocked).
2. Candidates considered, with elimination reasons.
3. Chosen artifact with exact identifier, version, and digest.
4. Evidence log per the format above.
5. Changes made, with file paths, and confirmation that no publish or destructive action occurred unless approved.
6. Open items, including every `[verify]` marker and the source used to check it.
7. Rollback steps: the exact pinned version or previous digest to restore.

Do not state that an artifact is secure, compliant, or production-ready. State the checks performed and their results instead.