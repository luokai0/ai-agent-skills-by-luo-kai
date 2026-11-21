---
name: experiment-tracking
description: Use when an agent or automation workflow must record, compare, reproduce, or audit experiments such as prompt variants, model or agent configuration sweeps, evaluation runs, or A/B tests, and needs a reliable run ledger with parameters, metrics, artifacts, and provenance.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Experiment Tracking

## Purpose and boundaries

This skill governs how an agent logs, organizes, compares, and reports experiments run against AI systems and automation pipelines. An experiment is a defined change (a prompt, model, tool set, retrieval setting, routing rule, or hyperparameter) measured against a fixed evaluation set under recorded conditions.

In scope: defining experiment records, capturing configuration and environment, logging metrics and artifacts, comparing runs, identifying regressions, and producing a decision-ready report.

Out of scope: choosing the business objective, designing the evaluation dataset from scratch without a reviewer, deploying winning variants to production, and altering shared evaluation data or baselines.

## Inputs and assumptions

Before running anything, confirm:

1. **Hypothesis**: one sentence stating the expected change and the metric it should move.
2. **Primary metric and guardrails**: one primary metric with a direction (higher or lower is better), plus at least one guardrail (cost, latency, refusal rate, safety score).
3. **Frozen evaluation set**: identifier, version, row count, and checksum. If absent, stop and request it.
4. **Baseline run**: an existing run ID with full configuration, or a request to create one first.
5. **Budget**: maximum runs, token or compute spend, and wall-clock limit.
6. **Variables**: the single factor or a declared small grid being varied. All others are held constant.

Assume nondeterminism unless proven otherwise. Sampling temperature, provider-side model updates, and concurrency can all shift results.

## Operating workflow

1. **Register the experiment.** Create a record with ID, hypothesis, owner, date, primary metric, guardrails, and the list of varied parameters. Record the record before the first run.
2. **Snapshot configuration.** Store the full resolved config: model identifier and version string as reported by the provider, system prompt or template hash, tool definitions, retrieval index version, seeds, sampling parameters, and code commit hash. Store secrets by reference only.
3. **Run with fixed conditions.** Execute the evaluation set with the frozen dataset. Use the same seed policy across variants. Run each condition at least three times when outputs are stochastic, and log every repetition, not only the mean.
4. **Log metrics per item and in aggregate.** Store per-example scores so that comparisons can be paired. Log latency, token counts, and cost alongside quality metrics.
5. **Attach artifacts.** Save raw outputs, judge prompts, judge versions, and failure traces. Hash each artifact.
6. **Compare against baseline.** Compute paired differences on the primary metric and each guardrail. Report confidence intervals or a bootstrap estimate; for small sets, report the count of items that improved versus regressed.
7. **Write the summary.** Record the decision, the evidence, and open questions. Mark the run as complete only after the ledger is consistent.

## Decision gates

Stop and request explicit approval before:

- Overwriting or deleting any existing run, baseline, dataset, or artifact.
- Running against production traffic, live user data, or customer-facing endpoints.
- Sending evaluation data containing personal, confidential, or regulated information to any external model or judge service.
- Spending beyond the stated budget or exceeding the declared run count.
- Promoting a variant, changing a shared configuration, or notifying external stakeholders.
- Changing the primary metric, evaluation set, or success threshold after results are visible. This is post-hoc fitting and must be disclosed and approved.

Proceed without a gate when the action is a new, append-only run record within budget on a frozen, non-sensitive dataset.

## Verification and evidence

Before reporting a result, check:

- Every run record has a complete configuration snapshot; no field reads "unknown" or "default" without a resolved value.
- Dataset checksum matches the registered value for every run.
- Baseline and candidate used identical evaluation items, counts, and judge versions.
- Paired comparison uses the same item IDs; mismatched counts block the comparison.
- Repeated runs show variance; report spread, not a single lucky run.
- A difference is called meaningful only if it exceeds the observed run-to-run variance and the guardrails do not regress beyond the declared tolerance.

Example: a prompt variant raises the primary accuracy from 0.81 to 0.84 on 400 items, but p95 latency rises from 1.2 s to 2.9 s. Report as "quality gain within noise on three repeats; latency guardrail breached; not recommended without further work."

Model version strings and pricing must be verified against the provider's current official documentation at the time of logging, since they change over time.

## Failure handling

- **Run crashes or times out**: log the partial run as failed with the error class and the last completed item index. Do not silently resume with changed settings; resume only with an identical config and note the resume in the record.
- **Missing metric for some items**: count and report them. Do not drop them to inflate scores. If more than 2% are missing, mark the comparison invalid.
- **Judge disagreement or drift**: if a judge model changes version, re-score the baseline with the new judge before comparing.
- **Config drift detected**: halt the comparison, identify the differing field, and either re-run or label the result as a different experiment.
- **Non-reproducible result**: re-run the identical config once. If the spread exceeds the claimed effect, report the experiment as inconclusive.

## Deliverable contract

Each completed experiment produces:

1. **Ledger entry**: ID, hypothesis, configuration snapshot, dataset checksum, run count, timestamps, cost, and artifact hashes.
2. **Results table**: baseline and candidate values for the primary metric and each guardrail, with spread and paired item counts (improved / regressed / tied).
3. **Decision statement**: one of *adopt for further testing*, *reject*, or *inconclusive*, with the single strongest reason.
4. **Limitations**: dataset coverage gaps, judge reliability, unexplored variables, and any gate approvals obtained.
5. **Reproduction instructions**: the exact steps and config references needed to rerun the experiment, without embedded secrets.

Do not present results without the ledger entry, and do not describe a candidate as better than baseline unless the verification criteria above are met.