---
name: security-threat-defense
description: Use when assessing, triaging, or hardening threats against external package registries and artifact sources (public or private package indexes, container registries, model hubs) that an organization consumes from or publishes to, including typosquatting, dependency confusion, malicious releases, compromised maintainer accounts, and tampered artifacts.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Security Threat Defense

## Purpose and boundaries

This skill guides an analyst through detecting, assessing, and mitigating threats that originate from or pass through external registries: npm, PyPI, Maven, NuGet, RubyGems, crates.io, OCI container registries, Helm chart repositories, and ML model hubs. It covers both consumption (pulling dependencies into builds) and publication (releasing packages under the organization's namespace).

In scope: source-of-truth verification, namespace and resolution-order risks, provenance and signature checks, malicious-package indicators, maintainer-account risk, and the containment steps that follow a confirmed threat.

Out of scope: general application vulnerability scanning, network intrusion response, and legal or compliance attestations. This skill does not certify that any artifact is safe. It produces evidence-backed risk decisions.

## Inputs and assumptions

Collect before acting:

- Dependency manifest and lockfiles, with the exact resolved versions and hashes.
- Registry configuration: which indexes are consulted, in what order, and whether private indexes proxy public ones.
- Artifact identifiers: name, version, digest, publisher account, and publish timestamp.
- Build provenance records or attestations, if the ecosystem produces them.
- Incident context: alert source, affected build IDs, and time window.

Assumptions to state explicitly in every report: the registry API and metadata reflect the state at query time; publisher identity claims are unverified unless backed by an attestation; absence of a known-malicious advisory does not establish safety. Registry features, attestation formats, and CLI behavior change between versions. Verify every version-sensitive detail against the current official documentation for that registry before relying on it.

## Operating workflow

1. **Scope the artifact set.** Enumerate every external artifact referenced by the affected build, including transitive and build-time dependencies. Record a digest for each. Artifacts without a lockfile digest are flagged as unpinned.
2. **Check resolution integrity.** Confirm that each name resolves to the intended index. For internal package names, verify that no public index serves a package with the same name at a higher version. Record the resolution path.
3. **Compare against the baseline.** Diff the current artifact digest and metadata against the last known-good release. Flag new install-time scripts, new network calls in install hooks, new binary blobs, changed maintainers, and publish timestamps that break the project's normal cadence.
4. **Assess the publisher.** Check account age, prior publishing history under the name, ownership changes, and whether the release is linked to a source commit or verifiable build attestation.
5. **Inspect the content.** Review install and build hooks, obfuscated strings, encoded payloads, unexpected executables, and credentials-access patterns. Treat automated scanner output as leads, not verdicts.
6. **Classify.** Assign one of: confirmed malicious, suspected compromise, suspicious-unverified, unpinned-exposure, or clear-with-evidence.
7. **Contain or record.** Apply the decision gate below.

## Decision gates

- **Gate A, containment (requires explicit approval):** Blocking an index entry, revoking a token, pinning or rolling back a production dependency, or removing a published version. Present the evidence, blast radius, and rollback path. Do not proceed without named approval.
- **Gate B, external reporting (requires explicit approval):** Reporting to a registry security team, notifying a maintainer, or publishing an advisory. Outbound communication is irreversible and must be approved.
- **Gate C, destructive operations (requires explicit approval):** Deleting artifacts, purging caches, force-rewriting lockfiles across branches, or unpublishing. Never perform these as part of triage.
- **Gate D, sensitive data:** If evidence contains secrets, tokens, or personal data, redact before sharing and report the exposure through the credential-rotation process. Do not paste live credentials into tickets.
- **Proceed without approval:** Read-only metadata queries, local digest computation, and writing the internal analysis record.

Escalate immediately when a confirmed malicious artifact has been installed in a production or release build.

## Verification and evidence

Each finding must include:

- The artifact identifier and digest, and the method used to compute or retrieve it.
- At least two independent indicators, such as an unexpected maintainer change plus an install-hook network call, before a classification above "suspicious-unverified."
- Timestamps in UTC with the source of each timestamp.
- The exact query or command used, with the registry version or API version noted as unverified until checked against current documentation.

Quality checks before closing:

- 100% of external artifacts in scope have a recorded digest or an explicit unpinned flag.
- Every classification cites at least one primary artifact, not only a third-party summary.
- Containment actions have a named approver and a tested rollback.
- Re-scan after remediation shows the affected digest no longer resolves in the build.

## Failure handling

- **Registry unreachable or rate-limited:** Record the gap, do not infer safety, retry with backoff, and mark affected artifacts as unverified.
- **Digest mismatch against lockfile:** Treat as a potential tampering event. Halt the build promotion and escalate. Do not regenerate the lockfile to make the mismatch disappear.
- **Conflicting indicators:** Keep the stricter classification until resolved, and document the conflict.
- **Scanner false positive:** Document the reasoning with line-level evidence. Do not suppress rules org-wide based on one case.
- **Evidence incomplete:** State what is missing and what decision it blocks.

## Deliverable contract

Produce a single report containing:

1. Summary: artifacts reviewed, classifications, and highest-severity finding.
2. Artifact table: name, version, digest, source index, publisher, classification.
3. Findings: each with indicators, evidence links or query outputs, and confidence level (high, medium, low).
4. Pending gates: each action awaiting approval, with the approver required.
5. Recommended actions ordered by risk reduction, each marked reversible or irreversible.
6. Assumptions and unverified items, including version-sensitive details to check against official documentation.

## What not to do

- Do not execute unknown packages or install-time scripts to observe their behavior outside an isolated sandbox with approval.
- Do not declare an artifact safe based on absence of advisories.
- Do not delete, unpublish, or overwrite artifacts during triage.
- Do not contact maintainers or registries without Gate B approval.
- Do not invent registry features, flags, or attestation formats. Verify them.
- Do not paste secrets or tokens into reports.