---
name: autonomous-ai-research
description: Use when an agent must plan, run, and report multi-step AI or data research (literature and codebase surveys, experiment design, model or data comparisons, reproducibility checks) with minimal supervision but auditable evidence and explicit approval gates.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Autonomous AI Research

## Purpose and boundaries

This skill governs end-to-end research tasks in AI and data work: framing a question, gathering sources and data, running bounded experiments, verifying results, and reporting findings with their uncertainty. It covers offline analysis, benchmark comparisons, ablation studies, dataset audits, and evaluation design.

It does not cover: production deployment, model training at a scale that incurs material cost without approval, collection of personal data, publication of results externally, or legal and compliance determinations. Those require a human owner.

## Inputs and assumptions

Before starting, confirm or record:

1. **Research question**: one falsifiable sentence (e.g., "Does retrieval reranking improve answer exact-match on our internal QA set by at least 3 points?").
2. **Success criterion and stop rule**: metric, threshold, compute or time budget, and maximum number of experiment iterations.
3. **Data access**: which datasets, their license terms as stated by the owner, and whether they contain personal or confidential content.
4. **Environment**: available hardware, sandbox boundaries, and network access rules.
5. **Baselines**: at least one existing reference result to compare against.

If any of these is missing, record it as an assumption in the report header. Do not proceed on an assumption that changes the data used or the conclusion.

## Operating workflow

1. **Frame**: restate the question, the metric, and the decision the result will inform. Write the hypothesis and a result that would refute it.
2. **Survey**: collect relevant prior work and internal artifacts. Record each source with title, date, and version. Prefer primary sources and official documentation.
3. **Audit data**: check schema, row counts, duplicates, label balance, train/test leakage, and missingness. Save the audit output.
4. **Design**: list variables, controls, seeds, and the minimal experiment set that can answer the question. Prefer one change per run.
5. **Pilot**: run on a small subset (roughly 1–5% or a fixed small N) to catch pipeline errors before full runs.
6. **Execute**: run experiments with fixed seeds, logged configs, and pinned dependency versions recorded from the environment itself.
7. **Analyze**: compute the pre-declared metric, confidence intervals or variance across seeds, and per-slice breakdowns.
8. **Report**: deliver the artifact contract below.

Keep a running log of every run: config hash, dataset version, command, start and end time, and outcome.

## Decision gates

Stop and request human approval before:

- Deleting, overwriting, or migrating any dataset, checkpoint, or result store.
- Spending compute beyond the approved budget, or launching jobs on shared clusters.
- Sending data, prompts containing internal content, or results to any external service, API, or public repository.
- Using data containing personal, health, financial, or otherwise sensitive attributes, or any data whose use rights are unclear.
- Changing the success criterion after seeing results.
- Making claims that will be used for a product, policy, or customer-facing decision.

Continue autonomously for: reading documents, local read-only analysis, running pre-approved experiments within budget, and writing to the designated scratch directory.

## Verification and evidence

Every reported number must be traceable to a logged run. Apply these checks:

- **Reproduction**: rerun the best configuration with a different seed; the metric must fall within the declared tolerance (default: within one standard deviation of the seed-averaged result).
- **Baseline parity**: confirm the baseline was evaluated with the same data split, preprocessing, and metric implementation.
- **Leakage check**: verify zero overlap of identifiers between train and evaluation splits; document the check command and output.
- **Slice review**: report results on at least the top three data segments by frequency or known risk; flag any segment where the change reverses direction.
- **Significance**: with fewer than 5 seeds or small evaluation sets, state that differences are not established and do not call them improvements.
- **Version sensitivity**: any library behavior, API signature, or benchmark number you cite must be marked for verification against current official documentation or the original source, unless you checked it in this session and record the date.

Do not report numbers from memory. Do not extrapolate beyond the evaluated distribution.

## Failure handling

- **Pipeline error**: fix only if the fix is within scope and reversible; record the diff. Re-run the pilot before full runs.
- **Metric regression or no effect**: report it as a result. Do not iterate beyond the stop rule to find a positive outcome.
- **Non-reproducible result**: mark the claim as unverified, list suspected sources (seed handling, nondeterministic kernels, data ordering, hidden state), and halt dependent conclusions.
- **Missing data or access denied**: stop that branch, record the blocker, and ask the owner. Do not substitute public or synthetic data without approval, and label any substitution clearly.
- **Conflicting sources**: present both, note dates and provenance, and do not average them into a single claim.

## Deliverable contract

The final report must contain, in order:

1. **Question and decision** (one paragraph).
2. **Assumptions and approvals obtained** (table: item, status, approver if any).
3. **Method**: data versions, splits, configs, seeds, environment, and run count.
4. **Results**: primary metric with variance, baseline comparison, slice table, and reproduction outcome.
5. **Verification log**: each check from the evidence section marked pass, fail, or not run, with the reason.
6. **Limitations**: distribution limits, unresolved failures, and claims deliberately not made.
7. **Open items**: approvals still needed and recommended next experiment.
8. **Artifact index**: paths to logs, configs, and scripts.

Quality bar: every claim links to a run ID; no metric appears without its baseline and variance; the report states a clear "supported", "not supported", or "inconclusive" verdict for the original question.
## Evidence-led research execution (v1.1)

Run research as a repeatable pipeline: frame the decision, decompose it into independent questions, define inclusion criteria, search multiple source classes, inspect primary evidence, extract claims, compare conflicts, identify gaps, and synthesize with explicit confidence. Search results are candidate leads, not validated facts.

Prioritize primary sources for specifications, APIs, security advisories, papers, source repositories, and release notes. Use practitioner reports to understand operational behavior and failure modes. Record source URL, publisher, publication or update date, access date, exact claim supported, source type, and confidence. Separate what the source states from the agent's inference.

Deduplicate by canonical URL and underlying claim, but do not collapse independent corroboration. Resolve disagreement by checking dates, version scope, experimental method, and source incentives. If a source is inaccessible, stale, or only a snippet, label the claim accordingly. Never fabricate a citation or infer a current API from old examples.

For technical recommendations, extract prerequisites, supported versions, operational steps, failure modes, security boundaries, and verification commands. Turn reusable findings into capability requirements and tests rather than copying a source's wording or structure. Preserve a research-to-implementation map: each proposed skill improvement links to the requirement it addresses and the validation case that will test it.

Close with known gaps, unanswered questions, confidence limits, and a revalidation trigger such as a major release, security advisory, or material version change.

