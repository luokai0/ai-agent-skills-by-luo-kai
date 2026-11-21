---
name: llm-benchmark-harness
description: Use when designing, running, or auditing an evaluation harness that compares LLMs or agent configurations on a fixed task suite, including dataset curation, prompt and tool setup, scoring, reproducibility checks, and reporting results with uncertainty.
author: Luo Kai
provenance: original
version: 1.1.0
---

# LLM Benchmark Harness

## Purpose and boundaries

This skill covers building and operating a repeatable evaluation harness: a fixed task set, a controlled run configuration, automated and human-checked scoring, and a results report that states what was measured and how confidently. It applies to comparing models, prompt versions, retrieval settings, or agent tool policies against each other or against a baseline.

It does not cover: training models, choosing a model for production without a pilot, certifying safety or regulatory compliance, or producing public leaderboard claims. Those require separate review.

## Inputs and assumptions

Collect these before running anything:

- Objective: the decision the results will inform (for example, "which model meets a 90% pass rate on invoice field extraction at under $0.02 per document").
- Task definition: input format, expected output schema, and the success criterion for each task type.
- Dataset: source, license status, size, and label method. Confirm the data may be sent to each model provider.
- Candidate configurations: model identifier, version or snapshot string, temperature and other sampling settings, system prompt, tool definitions, and context limits.
- Budget: maximum tokens, wall-clock time, and spend per run.
- Baseline: the currently deployed configuration or a simple reference.

Assumptions must be written down. Model endpoints change; treat any version identifier as version-sensitive and verify it against the provider's current official documentation before use. Do not assume a sampling parameter is honored identically across providers.

## Operating workflow

1. Freeze the dataset. Split into a development set (for tuning the harness) and a held-out evaluation set (never used for prompt tuning). Record SHA-256 hashes of both files.
2. Write the scoring spec before running. For each task type, define: exact-match, normalized-match, schema validity, rubric score, or model-graded score. Model-graded scoring requires a separate judge configuration and a calibration sample checked by a human.
3. Pin every configuration. Store the full run config as a file: model string, sampling parameters, prompt text, tool schemas, seed if supported, retry policy, and max output tokens.
4. Run a smoke test on 20 items per configuration. Confirm outputs parse, costs match estimates, and no provider errors are being silently counted as wrong answers.
5. Run the full evaluation. Execute each configuration with at least three repetitions for stochastic settings. Log raw outputs, latency, token counts, and error codes per item.
6. Score outputs with the frozen scorer. Do not edit the scorer after seeing results; if a bug is found, rescore everything and log the change.
7. Compute metrics with uncertainty: point estimates, 95% bootstrap confidence intervals over items, and paired comparisons against the baseline on identical items.
8. Write the report using the deliverable contract below.

## Decision gates

Stop and request approval before:

- Sending any data containing personal, client, or confidential information to a third-party endpoint.
- Running a configuration whose projected spend exceeds the approved budget by more than 10%.
- Using a new provider or account not listed in the inputs.
- Overwriting or deleting prior run directories, scorers, or datasets.
- Publishing results outside the immediate team, or citing them in external claims.

Proceed without further approval when all inputs are present, hashes match, smoke test error rate is under 2%, and projected spend is within budget.

Choose the winning configuration only when the paired difference against baseline has a confidence interval excluding zero on the held-out set. If intervals overlap, report "no demonstrated difference" rather than naming a winner.

## Verification and evidence

Quality checks that must pass before a report is issued:

- Hash of the evaluation set matches the recorded value.
- Every configuration has a complete run config file and a commit or copy of the scorer used.
- Provider error rate is reported separately from task failure rate. Errors above 5% for any configuration invalidate that configuration's results until rerun.
- Output parse rate is reported. Items that fail to parse count as failures, not omissions.
- Judge calibration: model-graded scores agree with human labels on at least 90% of a 50-item calibration sample, or the rubric is revised and recalibrated.
- Sample size per task type is at least 100 items for claims about pass rate at ±10 percentage points precision; state the actual interval width otherwise.
- Dev and held-out sets showed no leakage: no held-out item appears in prompt examples.

Keep raw outputs so any score can be audited item by item.

## Failure handling

- Rate limits or timeouts: retry with exponential backoff up to the configured limit, log each attempt, and exclude nothing silently. If retries are exhausted, record as provider error.
- Malformed output: score as failure, store raw text, and sample 30 such cases for scorer review. If more than 20% of failures are scorer false negatives, fix the scorer, rescore all runs, and document the change.
- Version drift: if a provider reports a different underlying model than the pinned string, halt the configuration and report the discrepancy.
- Budget overrun: stop the run, preserve completed results, and request a decision on continuation.
- Inconsistent repeat runs: if repetition variance exceeds the gap between configurations, report the comparison as inconclusive.

## Deliverable contract

The final report must contain, in this order:

1. Decision question and recommendation (or "no demonstrated difference").
2. Dataset description: size, task types, hashes, and access constraints.
3. Configuration table: each candidate's pinned settings and version-sensitive identifiers flagged for verification.
4. Results table: pass rate with 95% confidence interval, parse rate, provider error rate, median latency, and cost per item.
5. Paired comparison against baseline with interval.
6. Failure analysis: top three error categories with example item IDs.
7. Limitations: sample size, judge reliability, untested conditions, and any unverified version details.
8. Artifact paths: config files, raw outputs, scorer, and report.

Do not state that a model is "safe," "compliant," "accurate in production," or "best overall." Report only what the held-out evaluation measured under the recorded conditions.

## Ultron routing contract

**Choose this skill when:** Ultron needs a repeatable evaluation instrument: curated task cases, execution harness, deterministic environment controls, graders, hidden holdouts, scoring, and benchmark reports for comparing models or agent configurations.

**Choose `experiment-tracking` when:** the evaluation machinery already exists and the need is to organize a series of controlled changes, preserve run metadata, compare variants, and decide which configuration performed better.

**Handoff contract:** this skill returns a versioned benchmark contract, dataset and grader identities, execution conditions, per-case scores, uncertainty, failure categories, and known validity limits. The experiment tracker records each candidate configuration against that stable measurement setup. A benchmark score must not be presented as universal capability or safety certification.

**Why the boundary exists:** measurement design must remain stable enough to compare experiments, while experiment management must preserve the context behind each result.
