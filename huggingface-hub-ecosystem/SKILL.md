---
name: huggingface-hub-ecosystem
description: Use when selecting, auditing, downloading, versioning, publishing, or governing models, datasets, Spaces, and repositories on the Hugging Face Hub, including model cards, licenses, gated access, revisions, and access tokens.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Huggingface Hub Ecosystem

## Purpose and boundaries

This skill covers professional work with the Hugging Face Hub as a source and host for ML artifacts: model and dataset discovery, due diligence on repositories, pinned retrieval, artifact publication, and Hub-hosted demos (Spaces). It does not cover model training methodology, inference serving architecture, or fine-tuning recipes, except where a Hub decision depends on them.

Out of scope: general Python packaging, cloud account administration, and legal opinions on licensing. Flag licensing and compliance questions for qualified review rather than resolving them.

## Inputs and assumptions

Collect before acting:
- Task definition: modality, language, expected input/output, latency and hardware limits.
- Governance constraints: permitted licenses, data sensitivity, whether data or prompts may leave the environment.
- Target: read-only evaluation, local mirror, production dependency, or public publication.
- Current Hub state: fetch live repository metadata; do not rely on memory for download counts, licenses, or file layouts.

Assume the Hub web interface and client libraries change over time. Any specific function name, CLI flag, token scope label, or package version must be checked against current official Hugging Face documentation before use. Mark such details as unverified in your output until checked.

## Operating workflow

1. **Define the artifact need.** Write one sentence: task, modality, and acceptance metric. Reject candidates that cannot be evaluated against it.
2. **Shortlist repositories.** Filter by task tag, library compatibility, license, and recency. Record owner, repo ID, and commit hash for each candidate.
3. **Audit each candidate.** Read the model card or dataset card in full. Check: stated training data, intended use, known limitations, evaluation protocol, license text, gating status, and whether the card's claims cite verifiable sources.
4. **Inspect files.** Review the file list for weight format (prefer safetensors over pickle-based formats), tokenizer and config consistency, presence of custom code, and size.
5. **Pin the revision.** Record the exact commit hash. Never depend on a moving branch such as `main` for production.
6. **Retrieve into a controlled location.** Use the official client library with an explicit revision and a local cache directory. Verify checksums where the Hub provides them.
7. **Evaluate locally.** Run your own held-out evaluation on the pinned artifact before any integration decision.
8. **Document provenance.** Write a manifest (see Deliverable contract).

For publication: create the repository privately first, validate card metadata and license fields, check that no credentials, personal data, or restricted datasets are included, then request explicit approval before changing visibility to public.

## Decision gates

Stop and obtain explicit approval before:
- Making any repository public, or changing visibility, gating, or license of an existing repository.
- Uploading any dataset or model derived from data that is not clearly licensed for redistribution.
- Deleting, force-overwriting, or renaming a repository, branch, or revision.
- Sending private data, prompts, or proprietary code to a third-party Space or hosted inference endpoint.
- Using a token with write scope in a shared, CI, or untrusted environment.
- Adopting a model whose license is restrictive, unclear, or non-commercial when the use case is commercial.
- Executing custom repository code (`trust_remote_code`-style loading). Review the code first and get approval.

Proceed without a gate when: the action is read-only, the artifact is public and permissively licensed, and the revision is pinned.

## Verification and evidence

Each adopted artifact requires:
- Repo ID, commit hash, retrieval date, and license identifier as stated on the card and in the LICENSE file. If they disagree, treat as blocked.
- Gating status and whether access was granted to the account used.
- Checksum or file-size comparison against the Hub listing for downloaded files.
- Local evaluation results on your held-out set, with the metric, sample size, and seed or split identifier.
- A note on any card claim you could not reproduce.

Quality bar: no adoption without a local metric. Reported benchmark numbers from a model card are context, not evidence. Do not state performance figures you did not measure.

## Failure handling

- **Gated or access error:** Report the requirement; do not attempt to circumvent access controls or borrow another account's token.
- **Revision missing or changed:** Halt, record the discrepancy, and select a new pinned commit after review.
- **Checksum mismatch or corrupted download:** Discard the file, re-retrieve once, and escalate if the mismatch persists.
- **Unsafe format or unexpected code:** Quarantine the artifact; do not load it in production environments.
- **License ambiguity:** Mark the artifact as blocked pending human legal review.
- **Evaluation below threshold:** Do not tune on the test split to rescue the result; report the gap.

## Deliverable contract

Return a manifest with these fields:
- Task statement and acceptance metric
- Candidate table: repo ID, commit hash, license, format, gating, card completeness (yes/partial/no)
- Selected artifact with rationale tied to the metric and constraints
- Local evaluation summary with sample size and split identifier
- Open items: unverified API or version details, unresolved license questions, required approvals
- Retrieval and publication log with dates

Avoid: pinning to unverified version numbers, presenting card-reported scores as results, uploading unreviewed data, and proceeding past any decision gate without recorded approval.