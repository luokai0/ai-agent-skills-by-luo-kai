---
name: product-design-app-development
description: Use when designing, building, or preparing a product app for distribution through an external registry, such as an app store, plugin marketplace, or public package registry, including metadata, packaging, submission readiness, and listing review.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Product Design App Development

## Purpose and boundaries

This skill guides the design and development of an app whose primary distribution channel is an external registry that a third party operates and reviews. It covers product definition for registry constraints, packaging and metadata, pre-submission verification, and response to review outcomes.

In scope: registry-specific design constraints, manifest and listing metadata, build and packaging layout, version and changelog discipline, submission checklists, and review feedback triage.

Out of scope: general application architecture unrelated to distribution, marketing copy strategy, legal drafting, and any act of publishing, submitting, or changing a live listing.

## Inputs and assumptions

Before work begins, collect and confirm:

1. The target registry and the specific policy and guideline documents in force. Record the date you read them.
2. The app's core user task, supported platforms, and minimum runtime versions.
3. Data the app collects, stores, or transmits, including third-party SDKs.
4. Existing publisher account, signing identities, and who holds them. Do not assume access.
5. Current release branch, build tooling, and the last approved version.

Assume nothing about registry rules from memory. Registry policies, manifest fields, and size or permission limits change. Mark every version-sensitive detail as "verify against current official documentation" in your working notes and in the deliverable.

## Operating workflow

1. **Map registry constraints to product decisions.** List each mandatory rule (permissions, content, age rating, data disclosure, required assets, review guidelines). For each, assign an owner and a design response. Example: if the registry requires a privacy declaration, the design must have a data inventory before any UI copy is written.
2. **Define the listing contract.** Draft name, short description, long description, category, keywords, screenshot set, and support URL in one document. Check each against character limits and prohibited claims in the current guidelines.
3. **Design for reviewability.** Each feature that needs elevated permissions gets a one-paragraph justification tied to a user-visible action. Hidden or deferred functionality must be disclosed, or removed.
4. **Build and package.** Produce a reproducible build from a tagged commit. Confirm the artifact's identifier, version string, and signing match the listing. Record artifact size and checksum.
5. **Run the pre-submission checklist** (see Verification).
6. **Prepare the submission packet** with the changelog, reviewer notes, test account credentials stored in an approved secret channel (never in the packet body), and known limitations.
7. **Stop at the submission gate.** Hand the packet to the approver.

## Decision gates

Stop and obtain explicit human approval before:

- Submitting, publishing, promoting, or updating any live listing.
- Changing signing keys, publisher identity, or package name. These are irreversible for existing users.
- Adding permissions, data collection, or third-party SDKs that alter the privacy disclosure.
- Using a feature flag or remote configuration to change behavior after review.
- Deleting or unpublishing a version that users may have installed.
- Sharing credentials, user data, or crash logs containing personal data with any external party.

Proceed without approval only for local builds, local tests, drafts, and internal documents.

Decision criteria for scope cuts: if a feature cannot be justified against a guideline within the release window, remove it from the submission build rather than requesting an exception.

## Verification and evidence

Each claim in the packet needs evidence:

- Build reproducibility: two clean builds from the same commit produce matching checksums, or the difference is explained.
- Metadata: every field validated against the current registry schema and length limits, with the source document cited.
- Permissions: a table mapping each permission to the code path and user action that requires it. Any permission without a mapping fails.
- Privacy: data inventory matches the disclosure text, including SDK-level collection. Mismatch is a blocker.
- Functional testing: a clean-install test on the minimum supported runtime and one current runtime, with results recorded.
- Assets: screenshots generated from the release build, with dimensions checked against registry requirements.

Quality threshold: zero open blockers, and no warnings without a written disposition by the owner.

## Failure handling

- **Rejected review:** Quote the cited guideline verbatim, identify the responsible feature or metadata field, and classify the fix as metadata-only, code change, or policy dispute. Metadata-only fixes can proceed to the approval gate. Code changes require a new build and full checklist rerun. Disputes go to the approver with evidence; do not argue with reviewers in the response without approval.
- **Failed build or signing:** Halt. Do not re-sign with alternate identities to get past an error.
- **Discovered privacy or security defect after approval:** Escalate immediately. Do not patch the live build without the approval gate.
- **Ambiguous guideline:** Record the ambiguity, choose the more conservative interpretation, and flag it for the approver.

## Deliverable contract

The final output is a submission packet containing:

1. Release summary: version, commit, artifact identifier, checksum, and target platforms.
2. Registry constraint map with source documents and retrieval dates.
3. Listing contract with validated metadata and character counts.
4. Permission and data-collection tables with evidence links.
5. Pre-submission checklist with pass, fail, or waived status per item and named owners.
6. Known limitations and reviewer notes.
7. Explicit statement of which approval gates remain open.

Do not state that the app is "compliant" or "approved." State only what was verified and against which document version.