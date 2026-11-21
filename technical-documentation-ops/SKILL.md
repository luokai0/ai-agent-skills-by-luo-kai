---
name: technical-documentation-ops
description: Use when creating, restructuring, auditing, or maintaining technical documentation for software systems, APIs, runbooks, architecture records, or developer onboarding, and when documentation must stay accurate against code, configuration, or operational reality.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Technical Documentation Ops

## Purpose and boundaries

This skill governs the lifecycle of technical documentation: deciding what must be written, writing it against verifiable sources, validating that it matches the running system, and keeping it current. It covers API references, READMEs, setup and contributor guides, architecture decision records (ADRs), runbooks, incident postmortems, configuration references, and changelogs.

It does not cover marketing copy, end-user product manuals, legal or compliance documents, or authoring application code. If a request requires asserting security, compliance, or performance guarantees, stop and route that claim to the owning team.

## Inputs and assumptions

Before writing, collect:

- **Audience**: who reads this (new engineer, on-call responder, integrator, auditor) and what task they must complete.
- **Source of truth**: code, OpenAPI/schema files, config templates, infrastructure definitions, tests, or a named human expert. Documentation is derived from these, never the reverse.
- **Scope and version**: the exact system, service, or release the document describes.
- **Existing docs**: current content, its last-verified date, and known gaps.
- **Target location and format**: repo path, docs site generator, or wiki. Confirm the format's syntax against its current official documentation, since generator directives and front-matter keys are version-sensitive.

Assumptions must be written at the top of the draft under "Assumptions" with the reason. Unverified claims are labeled `UNVERIFIED`.

## Operating workflow

1. **Classify the document** by type (reference, how-to, explanation, runbook, decision record). Each type has one job. Do not mix a tutorial with a reference table.
2. **Build an evidence list.** Map every factual claim to a source: a file path, a command output, a test, or a stakeholder confirmation. Claims with no source are removed or marked `UNVERIFIED`.
3. **Outline by task**, not by code structure. Runbooks follow symptom → diagnosis → remediation. Setup guides follow prerequisite → install → configure → verify.
4. **Draft with concrete values.** Use real parameter names, real endpoints from the schema, and real example payloads that were executed or validated. Mark sample values explicitly as `SAMPLE` and state each one's meaning once.
5. **Run verification** (see below) before submitting.
6. **Record metadata**: owner, last-verified date, source commit or revision, and review cadence.

## Decision gates

- **Gate A: Source conflict.** If code and existing docs disagree, the code is authoritative for behavior; the owner is consulted for intent. Do not silently pick one.
- **Gate B: Undocumentable behavior.** If behavior is undefined, ambiguous, or appears to be a bug, document the observed behavior flagged as such and open a question to the owner. Do not document intent as fact.
- **Gate C: Sensitive content.** Before including hostnames, internal IPs, account identifiers, tokens, customer data, incident details naming individuals, or vulnerability specifics, require explicit approval from the document owner and the security or privacy contact. Never reproduce a live secret, even partially.
- **Gate D: Externally published docs.** Publishing to public sites, partner portals, or changing a shared API contract requires explicit approval from a named accountable person.
- **Gate E: Destructive edits.** Deleting or replacing published pages, redirects, or version archives requires explicit approval and a recorded rollback path (prior revision identifier).
- **Gate F: Compliance or guarantee language.** Statements about certification, uptime, SLAs, data residency, or regulatory status are out of scope unless the owning function supplies the approved wording.

## Verification and evidence

- **Command check**: every command in a how-to is executed in a clean environment matching the documented prerequisites; record the exit code and the key output line.
- **Example check**: every request/response example is replayed against the target version. Mismatched fields fail the check.
- **Link check**: all internal links resolve; all external links are checked for redirects and deprecation notices.
- **Name check**: every identifier (flag, key, environment variable, endpoint, function) appears in the source file it claims to come from. Use search, not memory.
- **Version check**: any tool version, package version, or generator directive is confirmed against current official documentation and labeled with the version it was verified against. Never state a version number from memory without this check.
- **Freshness check**: no doc is marked verified more than its review cadence allows (default 90 days for references, 30 days for runbooks).
- **Readability check**: a reviewer who did not write the document completes the task using only the document. Record the number of points where they needed to ask for help; target zero for runbooks.

Evidence is recorded in a short verification table in the pull request or ticket: check name, method, result, date.

## Failure handling

- If a command fails in verification, do not edit the doc to match the failure silently. Record the failure, determine whether the doc or the system is wrong, and fix the correct one.
- If a source cannot be found for a required claim, leave the section with `UNVERIFIED` and a named owner; do not fill it with plausible content.
- If a reviewer disputes accuracy and evidence is inconclusive, escalate to the system owner rather than resolving by majority opinion.
- If a runbook step has side effects (data deletion, traffic change, failover), mark it as requiring approval and do not present it as a routine step.

## Deliverable contract

Each deliverable contains:

1. Front matter: title, type, owner, audience, scope/version, last-verified date, source revision.
2. Assumptions and `UNVERIFIED` items, listed explicitly.
3. The document body, structured by its type.
4. Verification table with checks run, method, and result.
5. Open questions with named owners.
6. A changelog entry describing what changed and why.

Do not deliver a document with unresolved `UNVERIFIED` items in any section presented as authoritative. Do not deliver prose without at least one traceable source per factual section.

## What not to do

- Do not write documentation from memory of an API, library, or configuration you have not checked.
- Do not paste secrets, credentials, real customer identifiers, or internal topology without Gate C approval.
- Do not state performance numbers, benchmark results, or uptime figures without a cited measurement.
- Do not restate the code line by line; document contracts, constraints, and failure modes.
- Do not duplicate content across documents; link to a single authoritative page.
- Do not change published URLs or delete pages without Gate E approval.
- Do not add generic introductions, filler, or unverified best-practice claims.

## Ultron routing contract

**Choose this skill when:** managing the full lifecycle of technical documentation: scope, authoring, source verification, consistency, maintenance, runbooks, ADRs, API references, changelogs, and documentation quality across a product or engineering system.

**Choose document-authoring-publishing when:** documentation must be packaged and published as part of an artifact or external registry release, with version alignment and publication approval.

**Handoff contract:** provide the verified document content, version, source references, review status, and unresolved caveats. The publishing skill returns the published URL/version, artifact linkage, and publication evidence. Reconcile the published copy against the approved source and update the documentation inventory.

**Why the boundary exists:** technical documentation operations own accuracy over time; the publishing skill owns the controlled external release of a particular document set.
