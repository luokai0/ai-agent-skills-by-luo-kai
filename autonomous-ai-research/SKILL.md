---
name: autonomous-ai-research
description: Use when an agent must plan, run, and report multi-step AI or data research (literature and codebase surveys, experiment design, model or data comparisons, reproducibility checks) with minimal supervision but auditable evidence and explicit approval gates.
author: Luo Kai
provenance: original
version: 1.3.0
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

## Ultron routing contract

**Choose this skill when:** an agent must conduct a multi-stage research task autonomously: formulate questions, plan evidence collection, discover and compare sources, extract claims, track uncertainty, and produce a defensible synthesis.

**Choose `research-retrieval` when:** the work is a bounded source discovery and synthesis task with a defined question and deliverable, without a need for an autonomous multi-stage research plan.

**Choose `web-search-retrieval-and-live-data` when:** the answer depends on current public-web facts, recent updates, live values, or freshness verification at response time.

**Handoff contract:** this skill supplies research objectives, subquestions, source-quality policy, claim schema, and evidence coverage. Retrieval specialists return dated source records and atomic claims; this skill integrates them while preserving provenance, disagreement, and unanswered questions.

**Why the boundary exists:** autonomous research governs the full investigation; retrieval skills provide specialized evidence-acquisition paths within that investigation.

## Research protocol integrity and evidence coverage (v1.2)

### Freeze the investigation protocol before interpreting results

For decision-sensitive research, create a compact protocol before reviewing outcome evidence. Record the decision question, subquestions, inclusion and exclusion criteria, source classes to search, date and version boundaries, languages, search locations, extraction fields, quality rules, and stopping conditions. Mark any later protocol amendment with its reason, timestamp, and whether it was made before or after seeing relevant results. This makes exploratory changes visible and reduces outcome-driven scope drift.

Separate discovery from eligibility: a search hit is a candidate, not an included source. Maintain a source ledger with stable ID, canonical URL or artifact digest, title, publisher or owner, publication/update date, access date, version, source class, screening decision, exclusion reason, and full-text availability. Record searches that returned no useful results as well as successful searches.

### Measure coverage without pretending it is exhaustive

Build a question-to-evidence matrix. For every subquestion, list the source classes and systems searched, the claims found, the evidence quality, unresolved contradictions, and unsearched areas. Distinguish “searched and found none” from “not searched”, “inaccessible”, and “not reported”. A zero-result search is evidence about the search process, not proof that no evidence exists.

Define a practical stopping rule before searching: for example, all named primary sources checked, all required source classes searched, and no material new claim or source family discovered in a specified number of consecutive search iterations. If the rule is not met, report the search as incomplete. Do not describe a bounded search as exhaustive merely because the result set feels sufficient.

### Preserve negative, null, and contradictory findings

Extract null results, failed replications, adverse outcomes, limitations, and author-reported caveats with the same care as positive findings. Search for corrections, retractions, errata, superseding specifications, and later releases where these could change a claim. Do not infer absence of effect from a non-significant result; inspect the estimate, uncertainty interval, sample size, and power limitations where reported.

When a source reports a result that conflicts with the hypothesis, keep it in the claim ledger. Do not discard it because its method is inconvenient unless a predeclared eligibility or quality rule justifies exclusion. Record whether the conflict is substantive, methodological, temporal, population-specific, or only apparent because terms or metrics differ.

### Validate each material claim at its source

Before using a claim, open the cited primary passage, table, figure, API reference, or dataset record. Verify that it supports the exact proposition and that the context, version, date, units, and qualifications have not been lost. For numerical claims, capture numerator, denominator, unit, population, time window, and uncertainty where available. For versioned technical behavior, record the tested version and a reproducible check rather than relying on a search snippet or copied example.

Maintain explicit claim states: candidate, source-checked, independently corroborated, contradicted, stale, inaccessible, or unresolved. Only source-checked claims may be presented as directly supported. Corroboration must be genuinely independent; multiple pages repeating one upstream statement count as one lineage.

### Calibrate uncertainty and communicate the boundary

For each decision-critical conclusion, identify the strongest supporting evidence, strongest contrary evidence, key assumptions, plausible alternative explanations, and what observation would change the conclusion. Distinguish confidence in source accuracy from confidence that the evidence transfers to the target decision. Do not convert a qualitative judgment into a numeric probability unless a defensible calibration method exists.

If evidence is too weak, stale, inaccessible, or non-transferable, narrow the conclusion or return “inconclusive”. State the exact boundary: which population, version, date range, task family, language, or operating condition was not established. Provide the smallest next research action that would reduce the uncertainty, with its expected decision value and cost.

### Revalidation triggers

Attach a review trigger to claims whose validity can decay: major software releases, API deprecations, security advisories, new benchmark versions, changes in pricing or service limits, corrected papers, or a material change in the target population. Record the trigger and owner in the research artifact. A future agent should re-check the claim when the trigger fires rather than treating an old finding as permanently current.
