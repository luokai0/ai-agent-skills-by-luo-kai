---
name: data-pipelines-analytics
description: Use when designing, building, validating, or auditing analytics pipelines that ingest, normalize, join, or report on data pulled from external registries (public records, company or product registries, package or model registries, open government datasets).
author: Luo Kai
provenance: original
version: 1.1.0
---

# Data Pipelines Analytics

## Purpose and boundaries

This skill covers analytics pipelines whose source of truth is an external registry: extraction from registry APIs, bulk exports, or scraped public pages; staging; normalization; entity resolution; metric computation; and delivery of analytical outputs.

In scope: source assessment, ingestion design, schema mapping, incremental loads, data quality checks, reconciliation against registry totals, and documented analytical outputs.

Out of scope: writing to or modifying a registry, bypassing access controls or rate limits, re-identifying individuals in personal records, and making legal or compliance determinations on the registry's data. Route those to the appropriate owner.

## Inputs and assumptions

Before work begins, collect:

1. Registry name, operator, and the exact dataset or endpoint version used.
2. Published terms of use, licence, and rate limits. Record the date read.
3. Snapshot or release identifier, and whether the registry publishes change feeds, tombstones, or only full dumps.
4. Intended analytical question and consumers.
5. Target storage location and retention period.

Assumptions must be written down. Treat registry counts as unverified until reconciled. Treat field semantics as unverified until checked against the registry's own documentation.

## Operating workflow

1. **Profile the source.** Pull a bounded sample (for example, one page or one dated slice). Record field names, types, null rates, code lists, and encoding.
2. **Define the grain.** State what one row represents (a filing, a package version, a registration event). Every downstream join depends on this.
3. **Build raw landing.** Store responses unmodified with the request parameters, retrieval timestamp, and HTTP status. Never transform in the landing zone.
4. **Normalize in staging.** Cast types, trim strings, map code lists to a versioned lookup table, and keep the original value beside the normalized one.
5. **Resolve entities.** Use the registry's stable identifiers first. Fuzzy matching only with documented thresholds and a manual review sample.
6. **Load incrementally.** Use the registry's change markers if they exist. Otherwise, use full-snapshot diffs keyed on the natural identifier. Handle deletions explicitly.
7. **Compute metrics** from the staged layer only. Version metric definitions in a file kept alongside the pipeline code.
8. **Reconcile** against any published aggregate totals and record the variance.
9. **Publish** with lineage: source snapshot ID, pipeline version, run timestamp, and row counts per stage.

## Decision gates

For production data movement, require owner sign-off whenever any of these conditions apply:

- Bulk extraction would exceed published rate limits or terms, or the terms are unclear.
- The dataset contains personal data, and the analysis needs fields beyond the minimum required for the question.
- Output will be shared outside the owning team, published, or used to inform decisions affecting individuals or third parties.
- A step deletes or overwrites previously landed snapshots, or changes a published metric definition.
- Any job writes back to the registry or calls a write endpoint.
- Credentials, tokens, or access to restricted registry tiers are required.

Proceed without approval only for read-only sample pulls within published limits and local staging work.

## Verification and evidence

Quality checks must be measurable and recorded per run:

- Row count reconciliation: landed rows equal source-reported rows within a stated tolerance; any gap is explained.
- Key uniqueness: zero duplicate natural keys in the staged grain, or a documented dedupe rule with counts.
- Null and domain checks: null rate and out-of-code-list rate per critical field, compared with the profiling baseline. Flag changes above a set threshold (choose and document one, for example 2 percentage points).
- Referential checks: foreign keys resolve at a stated rate.
- Entity resolution: precision estimated from a reviewed random sample of at least 100 matches or the full set if fewer.
- Idempotence: rerunning the same snapshot produces identical staged output (compare checksums).
- Freshness: retrieval timestamp is within the agreed window.

Mark any version-sensitive detail (API paths, parameter names, rate limit values, schema versions) as "verify against current official documentation" in the run record. Do not assert these from memory.

## Failure handling

- **HTTP errors or throttling:** back off per the registry's guidance, resume from the last committed checkpoint, and never retry in a tight loop.
- **Schema drift:** halt the load, snapshot the new schema, and diff it against the mapping. Do not silently drop or coerce new fields.
- **Reconciliation mismatch above tolerance:** do not publish. Report the delta by stage to locate the loss.
- **Partial snapshot:** mark the run incomplete; never backfill metrics from it.
- **Upstream correction:** re-land affected snapshots and recompute dependent metrics; record the correction in the changelog.

## Deliverable contract

Each completed run delivers:

1. Run manifest: source, snapshot ID, parameters, timestamps, pipeline commit, metric definition version.
2. Stage row counts and reconciliation table.
3. Quality check results with pass/fail against the thresholds stated above.
4. List of open assumptions and unresolved field mismatches.
5. Approval log for any gated action taken.
6. Analytical output with the grain and filters stated in the first paragraph.

Do not present figures without the manifest. Do not describe output as authoritative for the registry; describe it as derived from a named snapshot.\n\n## Ultron routing contract

**Choose this skill when:** the deliverable is a repeatable, auditable flow that retrieves data from an external registry and transforms it into a reliable analytical dataset. It owns extraction, raw preservation, staging, normalization, incremental changes, reconciliation, quality checks, and pipeline delivery.

**Choose `data-analytics-modeling` when:** the dataset is ready and the unresolved work is analytical design or interpretation: choosing a metric, modeling entities and time, estimating rates or trends, validating a statistical model, or explaining results.

**Handoff contract:** publish a dataset contract with source and snapshot digests, row grain, schema version, key strategy, time semantics, quality metrics, known gaps, and refresh cadence. Receive from the modeling skill the required fields, metric definitions, and analytical quality thresholds. Preserve raw data and do not silently change metric meaning in the pipeline.

**Why the boundary exists:** the pipeline is accountable for the lineage and quality of inputs; the modeling skill is accountable for the validity of conclusions drawn from those inputs.
