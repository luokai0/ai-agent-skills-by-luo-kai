---
name: machine-image-builds
description: Use when creating, updating, validating, or promoting golden machine images (VM images, AMIs, container base images, or similar OS images) through an automated build pipeline, including image hardening, provenance capture, and rollout to fleets.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Machine Image Builds

## Purpose and boundaries

This skill governs the lifecycle of reproducible machine images: defining the build, producing an artifact, verifying it, recording provenance, and promoting it to consumers. It applies to VM images (for example cloud AMIs or disk images built with a declarative image builder), immutable base images, and container base images built from a Dockerfile or equivalent.

In scope: build definitions, base OS selection, package and configuration layering, hardening steps, artifact tagging, smoke and compliance tests, promotion between channels, and deprecation of old images.

Out of scope: application code build, runtime configuration management for already-running hosts, and organization-wide cloud account setup. Redirect those to the relevant skill.

## Inputs and assumptions

Before acting, collect and confirm:

1. Target platform and format (cloud provider image catalog, hypervisor template, container registry).
2. Upstream base image identifier and the policy for accepting it (vendor-supported, internally mirrored, pinned digest).
3. Build tool and its version, read from the repository lockfile or pipeline definition. Do not assume a version.
4. Intended consumers, rollout channels (dev, staging, production), and the current production image identifier.
5. Required hardening baseline and its source (internal standard, CIS-style benchmark, or vendor guidance). Record the exact benchmark version used.
6. Retention and deprecation policy.

Assumptions must be stated in the work log. If any input is missing, stop and request it rather than guessing.

## Operating workflow

1. **Pin inputs.** Resolve the base image to an immutable digest or snapshot ID. Record package repository snapshot dates where the build tool supports them.
2. **Validate the definition.** Run the builder's syntax or validation mode. Confirm variables that carry secrets are injected at build time from the secret store, never written into the definition.
3. **Dry-run the layer order.** Confirm that changes are layered so that frequently changing components sit above stable ones, and that security updates are applied after base selection.
4. **Build in an isolated environment.** Use a dedicated build account or project with no production network routes. Tag the build with a unique ID, the git commit SHA, and the builder version.
5. **Harden and scan.** Apply the hardening baseline, then run a vulnerability scan and a configuration compliance check against the artifact. Save raw reports.
6. **Boot test.** Launch the artifact in a throwaway environment, confirm it boots, passes the health check, has the expected agent or service set, and has no leftover build credentials, shell history, or temporary keys.
7. **Generate provenance.** Record base digest, package snapshot, builder version, commit SHA, build timestamp, builder identity, and checksums or content digests of the final artifact.
8. **Promote.** Copy to the dev channel first. Promote to staging and production only after gates pass. Update channel pointers rather than overwriting artifact names.
9. **Deprecate.** Mark superseded images as deprecated with a date. Remove only after the retention period and confirmation that no running fleet references them.

## Decision gates

- **Base image gate:** Reject unpinned tags such as `latest` or floating major-version tags. Accept only digests, snapshot IDs, or versions explicitly listed in the approved base catalog.
- **Vulnerability gate:** Block promotion if any critical or high finding lacks an approved, dated exception. Medium and low findings are recorded with owner and target date.
- **Compliance gate:** Block promotion if mandatory hardening controls fail. Document any deviation with a risk owner and expiry date.
- **Boot and health gate:** Block if the instance fails to boot within the agreed timeout or the health check does not pass after the agreed warm-up period.
- **Secret scan gate:** Block if the artifact or its build logs contain credentials, tokens, or private keys. Treat any finding as an incident: stop, notify the security owner, and rotate the exposed material.
- **Promotion gate (requires explicit human approval):** Any promotion to production, any overwrite of a channel pointer, any deletion of an image, and any change that alters the default image for a fleet requires explicit approval from the named owner.

## Verification and evidence

Each build must produce these artifacts, stored with the build record:

- Build log with timestamps and the builder version.
- Provenance record in a machine-readable format.
- Vulnerability and compliance reports with tool name and version.
- Boot and health test output.
- Artifact checksum or content digest, and the list of channels it was promoted to.

Quality checks: the build is reproducible if rebuilt from the same inputs and yields an equivalent package set and configuration (exact byte identity is not required unless the tool guarantees it). Image size and boot time should be compared with the previous production image; a change beyond 20 percent in either requires a written explanation.

Do not claim compliance with any framework on the basis of these checks alone. Report the specific control results and the benchmark version that was run.

Version-sensitive details (builder flags, plugin names, cloud API parameters, scanner rule sets, benchmark revisions) must be checked against current official documentation before use and noted as verified with the date.

## Failure handling

- **Build failure:** Preserve logs, do not retry more than twice without a diagnosis, and do not change pinned inputs silently to get past the error.
- **Scan failure caused by tool error:** Re-run with the same tool version. If the tool itself is failing, treat the gate as not passed.
- **Boot failure:** Capture console output and cloud-init or equivalent logs. Do not promote a partially valid image.
- **Secret exposure:** Stop the pipeline, quarantine the artifact, and escalate to the security owner. Do not attempt to delete evidence.
- **Failed promotion:** Leave the channel pointer unchanged and record the reason.

## Deliverable contract

A completed run delivers:

1. Image identifier, channel status, and checksum or digest.
2. Pinned input list (base digest, snapshot dates, builder version, commit SHA).
3. Gate results table with pass, fail, or exception and evidence link for each gate.
4. Known risks, open exceptions with owners and expiry dates.
5. Explicit statement of any step not performed and why.
6. Rollback target: the previous approved image identifier.

What not to do:

- Do not use floating tags or `latest` in any definition or consumer reference.
- Do not embed credentials, keys, or tokens in build definitions, images, or logs.
- Do not overwrite an existing versioned artifact.
- Do not promote, delete, or repoint channels without explicit approval.
- Do not build directly against production networks or accounts.
- Do not state benchmark results, scan counts, or compliance status that were not actually measured in the run.