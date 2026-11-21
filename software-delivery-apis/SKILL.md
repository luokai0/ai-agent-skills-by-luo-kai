---
name: software-delivery-apis
description: Use when integrating with external software registries and delivery endpoints (package indexes, container registries, artifact repositories, release and publishing APIs) to discover, validate, publish, promote, or retrieve software artifacts.
author: Luo Kai
provenance: original
version: 1.1.1
---

# Software Delivery APIs

## Purpose and boundaries

This skill covers programmatic interaction with external registries that store and distribute software: package indexes, container image registries, binary artifact repositories, and release/publishing endpoints. Typical tasks are resolving a version, checking whether an artifact exists, publishing a build, promoting an artifact between channels, yanking or deprecating a release, and fetching metadata for audit.

It does not cover: designing a registry server, writing general CI pipelines unrelated to registry calls, managing signing keys beyond referencing them, or making legal or licensing determinations about packages.

## Inputs and assumptions

Before acting, establish:

1. **Registry identity**: exact host, repository or namespace, and ecosystem (for example npm, PyPI, Maven, OCI, NuGet, or a generic artifact store).
2. **Operation**: read-only query, publish, promote, deprecate, or delete.
3. **Credentials scope**: which token or role is used, and whether it is read, write, or admin. Never assume write rights.
4. **Target artifact**: name, version or digest, and platform or classifier where relevant.
5. **Environment**: staging or production registry. Treat any ambiguity as production.

Assumptions must be stated explicitly in your output. Do not assume a registry supports a feature because a sibling ecosystem does.

**Version-sensitive details**: endpoint paths, authentication schemes, rate limits, required headers, and CLI flags change over time. Verify each against the registry's current official documentation before use and record the documentation version or date consulted.

## Operating workflow

1. **Classify the operation.** Read-only operations proceed directly. Any write, overwrite, promotion, deprecation, or deletion enters the decision gates below.
2. **Discover capabilities.** Query the registry's documented metadata or service-description endpoint if one exists. Confirm the artifact type, naming rules, and immutability policy.
3. **Resolve identifiers before mutating.** Convert names, tags, or ranges into an immutable reference: a content digest for containers, an exact version for packages, a checksum for binaries. Mutable tags such as `latest` must never be the sole reference in a published record.
4. **Read current state.** Fetch existing metadata for the target. Record the response, timestamp, and identifier.
5. **Plan the change.** Write the exact request(s) you intend to send, the expected resulting state, and the rollback path.
6. **Obtain approval** if any gate below applies.
7. **Execute with idempotency in mind.** Use dry-run or validation modes where the registry offers them. Send one change at a time and check each response.
8. **Verify** (see the Verification section) and produce the deliverable.

## Decision gates

Require explicit human approval before proceeding when any of the following hold:

- The operation writes to production, or the environment is unclear.
- The operation deletes, yanks, unpublishes, overwrites an existing version, or retags an existing digest. Most registries treat published versions as immutable; attempting to overwrite them is an incident, not a retry.
- The operation makes an artifact publicly visible or changes its visibility or license metadata.
- The operation uses credentials broader than the task requires, or credentials you were not explicitly given.
- The request would transmit proprietary source, customer data, secrets, or unreleased internal identifiers to an external service.
- Promotion skips a stage (for example, staging to production with no verification record).

Proceed without approval only for read-only queries against a registry the user identified, and for writes to a clearly designated sandbox or staging namespace the user named.

## Verification and evidence

A change is not complete until you have evidence of all of the following:

- **Existence check**: a read request returns the artifact at the expected identifier.
- **Integrity check**: the returned digest or checksum matches the locally computed value of the artifact you intended to publish. Compute it locally with a standard tool and record the algorithm.
- **Metadata check**: name, version, platform, and declared dependencies match the intended release notes or manifest.
- **Resolution check**: a consuming client or a fresh read resolves the version to the same digest.
- **Audit record**: the request, response status, identifiers, timestamps, and approver (if gated) are logged.

Quality thresholds: zero checksum mismatches are acceptable; any mismatch halts the workflow. Each write must have a corresponding read-back confirmation before reporting success.

## Failure handling

- **401 or 403**: stop. Do not try alternative credentials or escalate privileges. Report the scope required.
- **404 on a read**: confirm the namespace, ecosystem, and case sensitivity before concluding absence. Do not create the artifact to resolve it.
- **409 or version-exists conflict**: compare digests. If identical, the operation is already complete; report success with evidence. If different, stop and escalate; do not overwrite.
- **429 or 5xx**: back off with jitter, retry a bounded number of times, then stop. Do not retry non-idempotent writes without first reading state.
- **Partial success** (for example, an image pushed but a manifest list not updated): treat the system as inconsistent. Report the exact state and request approval for repair.
- **Unexpected response shape**: do not infer meaning from it. Capture it verbatim and escalate.

## Deliverable contract

Every completed task produces a report with these fields:

1. Registry, ecosystem, environment, and operation.
2. Documentation consulted for version-sensitive details, with date or version.
3. Target identifiers before and after: digests, versions, and channels.
4. Commands or requests executed, with redacted credentials.
5. Verification results for each check listed above, with pass or fail.
6. Gates triggered, approvals obtained, and the approver's identity as stated by the user.
7. Open risks and any steps left for the user to perform.

State what was not verified. Do not report success on partial evidence.

## What not to do

- Do not overwrite or delete published versions to "fix" them; publish a new version instead, after approval.
- Do not use mutable tags as the only record of what shipped.
- Do not hardcode or echo tokens, passwords, or signing keys into logs, reports, or committed files.
- Do not invent endpoints, flags, or package versions; verify them.
- Do not treat a successful HTTP status alone as proof of correct publication.
- Do not publish to a registry the user did not name.

## Ultron routing contract

**Choose this skill when:** the task is specifically about interacting with a software artifact registry or release endpoint through its API, CLI, or protocol: querying metadata, resolving versions and digests, authenticating, publishing a registry operation, promoting, deprecating, or verifying a registry-side state change.

**Do not use it as the sole release playbook when:** the task begins with source code and requires the complete release lifecycle: clean build, artifact assembly, provenance, signing checks, package-content review, approval, publication, installation test, and release record. Route that lifecycle to `software-engineering-delivery`.

**Handoff contract:** the release skill supplies the approved artifact identity, digest/version, target namespace, environment, allowed operation, and approval record. This skill returns the exact registry request or command, response, resolved artifact identity, resulting state, and any API-specific failure. Never infer permission to publish from the ability to call an endpoint.

**Why the boundary exists:** registry protocol execution is a reusable integration capability; release engineering is the end-to-end decision and assurance process that may call it.
