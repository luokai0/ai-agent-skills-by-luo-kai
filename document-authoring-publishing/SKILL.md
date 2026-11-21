---
name: document-authoring-publishing
description: Use when preparing documentation, README files, changelogs, model or dataset cards, or package metadata for release to an external registry or documentation host, including checking that published text matches the artifact version and passes registry rules.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Document Authoring Publishing

## Purpose and boundaries

This skill covers writing user-facing documentation and metadata for an artifact, then publishing that text to an external registry or documentation host (package indexes, container or model hubs, documentation sites, artifact repositories). It covers the document set, its version alignment, and the publish readiness check.

Out of scope: writing the software itself, designing registry infrastructure, and changing organization-wide publishing policy. Do not use this skill to publish anything without the approval gate below.

## Inputs and assumptions

Before writing, confirm:

- Artifact name, version, and the exact registry or host target.
- Target audience (end users, integrators, maintainers, auditors).
- Existing documents and their owners.
- Licensing and sensitivity status supplied by the owner. Do not infer these.
- Whether the registry is public, private, or mirrored. Mirrors often cache metadata and cannot be fully retracted.

Assume nothing about registry metadata rules, field limits, rendering engines, or accepted file formats. Check the current official documentation for each target and record the URL and date consulted. Treat any field name, size limit, or syntax from memory as unverified.

## Operating workflow

1. **Freeze the version.** Record the exact version string that will be published. Every version reference in the documents must match it.
2. **Inventory existing text.** List every README, changelog, example, badge, install command, and metadata field. Mark each as current, stale, or unknown.
3. **Draft in layers.** Write in this order: one-paragraph summary, install or access steps, minimal working example, configuration reference, limitations, changelog entry, contact and support path.
4. **Make examples executable.** Every command or code sample must run against the frozen version in a clean environment. Record the environment used.
5. **Translate to registry fields.** Map each piece to the target's metadata fields. Note any field that is truncated, rendered differently, or unsupported.
6. **Run the verification checklist** (below).
7. **Prepare a publish package** containing the final text, a diff against the previous published version, and the verification evidence.
8. **Request approval** (see Decision gates) before any publish, overwrite, deletion, or visibility change.

## Decision gates

Stop and obtain explicit owner approval before:

- Publishing a new version, or any version to a public or shared registry.
- Overwriting, editing, or replacing an already published document or version page.
- Yanking, deprecating, deleting, or changing visibility of any release.
- Adding a license, copyright notice, or attribution claim that the owner did not supply.
- Including contact details, internal hostnames, customer names, credentials, or unreleased feature names.
- Publishing a model or dataset card that describes evaluation results, safety properties, or data provenance without supporting records.

If an action is irreversible or mirrors externally, state that explicitly in the approval request.

## Verification and evidence

Pass all of the following before requesting approval:

- Version strings in all documents equal the frozen version (zero mismatches across grep-style search of the package).
- Every command or code block was executed and the result recorded.
- All links resolve; relative links work from the published location.
- Metadata fields are within the target's current documented limits; cite the source checked.
- No unresolved sample text or unfinished sections, or unresolved status markers remain.
- No secrets or credentials appear in examples (scan for token-like strings and private hostnames).
- Changelog entry lists user-visible changes only and matches the diff.
- Benchmarks or quantitative claims include the method, environment, and date, or are removed.

Record results as a table: check, method, result, evidence location.

## Failure handling

- **Version mismatch found:** fix in the source, re-freeze if the version itself was wrong, and rerun all checks. Do not patch only the published copy.
- **Example fails:** correct the example or the documented prerequisites. Do not hide the failing step.
- **Registry rejects metadata:** shorten or restructure the field without changing meaning, then recheck limits against current documentation. Report any content lost.
- **Publish already occurred with an error:** stop, report the exact state, and ask for approval on the corrective action (edit, deprecate, or yank). Do not take corrective action unilaterally.
- **Documentation source is ambiguous:** ask the owner rather than inferring behavior.

## Deliverable contract

Return to the requester:

1. Final document set, one file per document, with the frozen version stated at the top of the changelog entry.
2. Registry field mapping with any truncations or omissions listed.
3. Diff against the last published version.
4. Verification table with evidence locations.
5. A list of documentation sources consulted, with dates.
6. A pending-approval section listing each gated action, its reversibility, and its external impact.

Do not state that the artifact is compliant, secure, or certified. Describe only what was checked and how.

## Ultron routing contract

**Choose this skill when:** producing version-aligned documentation or metadata for an artifact and preparing or performing its approved publication to a registry, documentation host, package index, container/model hub, or artifact repository.

**Choose technical-documentation-ops when:** the work is the broader lifecycle of technical documentation: deciding what documentation is needed, maintaining runbooks/ADRs/API guides, validating content against a running system, and keeping documents current.

**Handoff contract:** the documentation-ops skill supplies verified source content, version identity, review status, and internal publication policy. This skill packages the external-facing document set with the artifact version, checks registry/host-specific publication requirements, obtains the required approval, and verifies the published result.

**Why the boundary exists:** maintaining trustworthy documentation and publishing documentation alongside an artifact have different release and external-impact controls.
