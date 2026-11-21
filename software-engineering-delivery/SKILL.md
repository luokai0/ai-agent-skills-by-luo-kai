---
name: software-engineering-delivery
description: Use when preparing, publishing, deprecating, or consuming software artifacts through external registries such as package indexes, container registries, or artifact repositories, including release versioning, credential handling, and post-publish verification.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Software Engineering Delivery

## Purpose and boundaries

This skill governs the path from a built, tested artifact to a version that is published to, or consumed from, an external registry. It covers version selection, artifact assembly, publish execution, post-publish verification, deprecation, and rollback-by-supersession.

In scope: npm, PyPI, Maven Central, crates.io, container and OCI registries, Helm chart repositories, and internal mirrors of these.

Out of scope: application deployment to runtime environments, source-code review policy, and general CI pipeline design, except where they produce or gate the artifact.

## Inputs and assumptions

Before acting, confirm:

- Target registry, namespace or owner, and package name. Check that the name is not already claimed by an unrelated party.
- Source commit or tag, and that the artifact was built from it.
- Current published versions in the registry, fetched live, not from memory.
- Release type: patch, minor, major, or prerelease, per the project's declared versioning scheme.
- Publishing identity: which account, token scope, or trusted-publisher configuration will be used.
- Changelog or release notes exist and match the commit range.

If any input is unverified, stop and record it as an open item.

## Operating workflow

1. Reconcile versions. Compare the version in manifest files against the registry's existing versions. Reject any version that already exists; published versions are immutable on most registries.
2. Verify the artifact. Build from a clean checkout at the tagged commit. Compare the file list and manifest metadata (name, version, license field, entry points, declared dependencies) against expectations. Remove development-only files that would leak into the package.
3. Scan for leaks. Search the artifact contents for credentials, environment files, private keys, internal hostnames, and test fixtures containing real data.
4. Dry run where the tool supports it. Confirm the dry-run output lists exactly the intended files and version. Verify the exact dry-run flag against current official documentation before use.
5. Request approval (see Decision gates).
6. Publish with the approved identity. Record the exact command, registry URL, and timestamp.
7. Verify from the registry, not the local build: fetch the published metadata, download the artifact into an empty directory, and compare checksums against the local build output.
8. Install the artifact into a clean environment and run the smoke test defined by the project.
9. Tag the release commit if not already tagged, and attach the checksums and release notes.

## Decision gates

Require explicit human approval, recorded with the approver's name and date, before:

- Any publish, because it is external-impacting and usually irreversible.
- Any unpublish, yank, or deletion of a version. Prefer deprecation or yanking where the registry supports it, and verify its semantics in current documentation first, since yanked artifacts may still resolve for existing lockfiles.
- Changing package ownership, maintainers, access tokens, or trusted-publisher bindings.
- Publishing under a new package name or namespace.
- Any change to license metadata.

Proceed without a gate only for read-only operations: listing versions, downloading for comparison, and running local builds.

Stop and escalate if the dry-run file list contains unexpected files, if checksums mismatch between local and registry copies, or if the token has broader scope than the release requires.

## Verification and evidence

A release is complete only when all of the following hold:

- The registry reports the new version as the latest or intended channel.
- Downloaded checksum equals the local build checksum.
- Clean-environment install succeeds with no resolution warnings.
- Smoke test passes against the installed artifact, not the source tree.
- Release record contains: commit hash, version, registry, publish identity (name only, never the secret), checksum, timestamp, and approver.

Do not claim provenance or signing guarantees unless signature or attestation verification was actually performed and the verification output is recorded.

## Failure handling

- Publish rejected as duplicate version: do not retry with the same number. Increment per the versioning scheme and rebuild.
- Publish partially succeeded (artifact uploaded, metadata missing): query the registry state before any retry. Do not republish blindly.
- Auth failure: rotate or reissue the token through the owner. Never paste secrets into logs or chat.
- Bad release discovered after publish: publish a fixed higher version and deprecate the broken one. Obtain gate approval for each step.
- Name squatting or ownership conflict: stop, document, and escalate to the registry's support process.

## Deliverable contract

The delivery returns:

1. Release record as described above.
2. Dry-run and final file lists.
3. Checksum table for each artifact.
4. Verification log summary with pass or fail per check.
5. Open items, each with an owner.

Do not:

- Publish from an uncommitted working tree or an unreviewed branch.
- Use long-lived personal tokens where scoped automation identities exist.
- Assert version-specific registry behavior, flags, or limits from memory. Verify against current official registry documentation and mark the verified date in the release record.
- Modify a published artifact in place.