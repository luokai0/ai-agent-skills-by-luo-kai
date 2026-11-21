---
name: data-sourcing-and-quality
description: Use when selecting, acquiring, profiling, or validating datasets for analytics, machine learning, or AI evaluation, including assessing source provenance, licensing constraints, schema drift, label quality, and fitness for a stated use.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Sourcing And Quality

## Purpose and boundaries

This skill governs how a dataset is chosen, obtained, profiled, and judged fit for a specific use. It covers sourcing decisions, provenance and rights review, profiling, quality measurement, and a written fitness verdict.

In scope: candidate source comparison, acquisition plans, schema and content profiling, label and annotation quality review, leakage and bias screening for training or evaluation splits, and data quality reports.

Out of scope: building production ingestion pipelines (use a pipeline or ETL skill), model architecture choices, and legal opinions. Where licensing or privacy determinations matter, state the open question and route it to the accountable owner. Do not present a legal conclusion as settled.

## Inputs and assumptions

Before acting, confirm these inputs. If any is missing, ask for it or record it as an explicit assumption in the deliverable.

- Intended use: the decision, model, metric, or report the data will support.
- Unit of observation, time range, population, and geography required.
- Candidate sources, with access method and owner.
- Known constraints: license terms, consent basis, retention limits, residency, and sensitivity classification.
- Volume and freshness requirements, and acceptable latency.
- Ground-truth definition, if labels are involved, and who produced them.

Assume nothing about license terms, consent scope, or personal data presence until inspected. Assume a sample is representative only after comparison against the population definition.

## Operating workflow

1. **Restate the use.** Write one sentence stating what the data must support and the error that would matter most (false negatives, stale values, label noise, demographic gaps).
2. **Inventory candidates.** For each source record: origin, owner, collection method, update cadence, license or terms, known exclusions, and retrieval date.
3. **Screen provenance.** Trace each field to its origin. Flag derived fields, scraped content, synthetic data, and fields merged from multiple sources. Mark any source whose terms are unknown as blocked pending review.
4. **Acquire a bounded sample.** Pull a stratified sample sized to test the riskiest strata, not a convenience slice. Record the query, filters, and timestamp so the pull is reproducible.
5. **Profile structure.** Check types, nullability, cardinality, ranges, units, encodings, duplicate keys, and timezone handling. Compare against the documented schema and log every deviation.
6. **Profile content.** Examine distributions by key segments, missingness patterns (MCAR, MAR, or not-at-random where determinable), outliers, and temporal coverage gaps.
7. **Assess labels, if present.** Sample at least 200 labeled items or 5% of the set, whichever is larger, and have a second reviewer relabel them blind. Compute agreement (Cohen's kappa for two raters, Krippendorff's alpha for more) and document the guideline version.
8. **Check splits and leakage.** Confirm train, validation, and test partitions do not share entities, near-duplicates, or post-outcome fields. Split by entity or time where the deployment pattern requires it.
9. **Decide and document.** Produce the verdict per the deliverable contract.

## Decision gates

- **Gate A (rights):** Proceed only if the license, terms, or consent basis permits the stated use, as confirmed by the designated owner. Unknown terms block the source.
- **Gate B (sensitivity):** If personal, health, financial, or minors' data is detected or plausible, stop and obtain explicit approval before any further copying, export, or sharing. Prefer minimized extracts and aggregated views.
- **Gate C (coverage):** Proceed only if the sample covers every stratum the use requires. A stratum with fewer than 30 records is reported as unsupported, not averaged in.
- **Gate D (label reliability):** Labels with agreement below 0.6 kappa (or alpha below 0.67) require guideline revision and relabeling before use in evaluation. For training only, document the noise level and proceed with an explicit risk note.
- **Gate E (leakage):** Any detected train-test overlap above 1% of test records blocks evaluation use until repartitioned.

## Verification and evidence

Each claim in the verdict must cite a reproducible check. Minimum evidence set:

- Row counts, key uniqueness rate, and null rate per required field.
- Schema diff between documented and observed schema.
- Stratum counts against the coverage requirement.
- Agreement statistic and sample size for labels.
- Overlap counts for leakage checks, with method stated.
- Freshness: latest timestamp observed versus required latency.

Thresholds such as null-rate limits or acceptable drift must come from the stated use, not from generic defaults. Where a library, tool, or service behavior is referenced, mark it "verify against current official documentation" unless confirmed in this session.

## Failure handling

- **Schema drift:** Stop profiling, capture the diff, and report whether the change is additive or breaking. Do not coerce types silently.
- **Unexplained missingness above the required limit:** Report the pattern by segment; do not impute to hide it without disclosing the method.
- **Irreproducible pull:** Discard the sample and re-pull with recorded parameters.
- **Conflicting sources:** Keep both, document the disagreement rate, and name which source is authoritative and why.
- **Discovery of sensitive data:** Halt, do not quote values in output, and escalate under Gate B.

## Deliverable contract

Produce a single data fitness report containing:

1. Use statement and error priorities.
2. Source inventory table: source, owner, terms status, retrieval date, verdict.
3. Evidence summary with the metrics listed above and their methods.
4. Assumptions and open questions, each with an owner.
5. Verdict: Fit, Fit with stated limits, or Not fit, with the gate results.
6. Recommended next action with explicit approval requests where Gates A or B applied.

## What not to do

- Do not treat "publicly available" as "licensed for any use."
- Do not report averages over strata that failed coverage.
- Do not relabel a sample without recording guideline version and reviewer identity.
- Do not split data randomly when records share entities or timestamps that leak outcomes.
- Do not write raw sensitive values into reports, logs, or prompts.
- Do not state compliance, accuracy, or legal status as guaranteed.