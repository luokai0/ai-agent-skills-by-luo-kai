---
name: agent-memory-persistence
description: Use when an AI agent or automation must store, retrieve, update, or expire information across sessions, runs, or tasks, including designing memory schemas, deciding what to persist, and auditing stored memory for accuracy, privacy, and staleness.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Agent Memory Persistence

## Purpose and boundaries

This skill governs how an agent decides what survives beyond the current context window, where it is stored, how it is retrieved, and how it is corrected or deleted. It covers:

- Classifying candidate memories (facts, preferences, task state, decisions, artifacts, pointers).
- Choosing a storage form (structured record, document, vector index, key-value state, file).
- Writing, reading, updating, superseding, and expiring entries.
- Auditing memory for accuracy, staleness, duplication, and sensitive content.

It does not cover model fine-tuning, general database administration, or the design of the agent's core reasoning loop. Use it when persistence is a deliberate design question, not an incidental side effect of logging.

## Inputs and assumptions

Before writing any memory, establish:

1. **Consumer**: who or what will read the memory (the same agent next session, a human reviewer, a downstream automation).
2. **Lifetime**: session, task, project, or indefinite. Default to the shortest lifetime that meets the need.
3. **Source authority**: whether the content came from the user, a verified system of record, a tool output, or the model's own inference. Inferred content is never stored as fact without a provenance tag.
4. **Storage target and its access controls**: which store is approved, who can read it, and whether it is encrypted at rest. Confirm this rather than assuming.
5. **Retention rule**: any policy from the organization or user that limits what may be kept.

If any of these is unknown and the write would be durable, stop and ask.

## Operating workflow

1. **Extract candidates.** List discrete claims or state items from the current work. One fact per entry.
2. **Classify each candidate** using the table in Decision gates.
3. **Check for duplicates and conflicts.** Query the existing store by stable key (entity ID, task ID, preference name), not by free-text similarity alone. If a matching entry exists, compare values.
4. **Assign metadata to every write:**
   - `id`, `kind`, `value`
   - `source` and `source_authority`
   - `observed_at` (ISO 8601 timestamp) and `valid_until` or `review_after` where applicable
   - `confidence`: `verified`, `user_stated`, `tool_returned`, or `inferred`
   - `supersedes` (id of replaced entry), if any
5. **Write atomically.** Write the new entry and mark the superseded one as superseded in the same operation. Never leave two live entries for one key.
6. **Retrieve with scope.** On read, filter by key, kind, and validity window first; only then rank by relevance. Return the entry with its metadata so the consumer can judge freshness.
7. **Expire.** At each run start, surface entries past `review_after` for revalidation before use.

## Decision gates

Persist only if all of the following hold:

| Gate | Pass condition | Otherwise |
|---|---|---|
| Reuse | Will change a future decision or save material re-work | Keep in session only |
| Stability | Expected to remain true for the stated lifetime | Store with short `review_after` or do not store |
| Provenance | Source and authority are known | Store as `inferred` with a review date, or discard |
| Sensitivity | Contains no credentials, health, financial identifiers, or third-party personal data beyond need | Stop; request explicit approval |
| Retention | Permitted by policy and consumer's instructions | Do not store |

**Require explicit user approval before:**
- Writing any personal, health, financial, or legal-adjacent data to durable storage.
- Overwriting or deleting an entry that was `user_stated` or `verified`.
- Writing to any store shared with other users, teams, or external services.
- Bulk deletion, bulk export, or migration of a memory store.
- Storing anything that looks like a secret. Never persist API keys, passwords, tokens, or session cookies; store only a reference to the secret manager entry if the approved design allows it.

## Verification and evidence

Quality checks to run after each write batch and on periodic audits:

- **Key uniqueness**: zero live entries share a stable key. Target: 0 duplicates.
- **Provenance coverage**: 100% of live entries have `source`, `confidence`, and `observed_at`.
- **Staleness**: no live entry is used past `valid_until`. Count entries past `review_after`; each must be revalidated or retired before use.
- **Round-trip fidelity**: a sample of 10 writes is read back and matches byte-for-byte on `value` and metadata.
- **Supersession integrity**: every `supersedes` reference resolves to an entry now marked superseded.
- **Sensitive scan**: scan values for patterns such as key prefixes, card-like digit runs, and email or phone formats. Any hit is escalated, not silently redacted.

Report results as counts with the sample size. Do not claim a store is "clean" or "compliant" from these checks; they establish only the stated properties.

## Failure handling

- **Write fails**: do not retry blindly on non-idempotent writes. Read back by key to determine whether the write landed, then reconcile.
- **Conflict between sources**: keep the higher-authority value live, mark the other `disputed` with both sources, and ask the user if the conflict affects a decision.
- **Retrieval returns stale or contradictory entries**: do not merge them into a new value silently. Surface both with timestamps.
- **Store unavailable**: continue the task in session memory, record the pending writes in a local queue marked as unpersisted, and flush once available after verification.
- **Suspected corruption or unexpected deletion**: stop writes, preserve the current state, and escalate. Do not attempt automatic repair.
- **Schema version mismatch**: treat unrecognized fields as opaque, do not drop them, and flag for migration review.

## Deliverable contract

Every persistence task closes with:

1. **Change record**: list of entries created, updated, superseded, or expired, each with id and key.
2. **Gate log**: for each candidate not stored, the gate that failed and why.
3. **Verification summary**: the checks above with counts and sample sizes.
4. **Open approvals**: any action awaiting explicit user consent, stated as a specific question.
5. **Version note**: if any storage API, client library, or schema format was used, record its version and state that its exact calls and options were checked against current official documentation before use.

## What not to do

- Do not persist raw conversation transcripts as memory by default.
- Do not store inferred content as user-stated fact.
- Do not use free-text similarity as the only key for updates.
- Do not invent storage APIs, field names, or flags; verify them against official documentation for the version in use.
- Do not present these checks as proof of security, privacy, or regulatory compliance.
- Do not delete or overwrite approved records without the approval gate above.