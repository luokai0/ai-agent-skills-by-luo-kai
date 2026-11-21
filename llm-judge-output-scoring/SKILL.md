---
name: llm-judge-output-scoring
description: Use when designing, running, or auditing an LLM-as-judge rubric to score model outputs (answers, summaries, agent traces, code, tool-call results) against explicit criteria, including calibrating the judge against human labels and reporting scores with evidence.
author: Luo Kai
provenance: original
version: 1.0.0
---

# LLM Judge Output Scoring

## Purpose and boundaries

This skill covers building and operating a rubric-driven evaluation in which a language model assigns scores or pass/fail labels to other model outputs. It owns: rubric design, judge prompt structure, sampling, calibration against human labels, bias checks, score aggregation, and the evidence package that accompanies results.

It does not cover: training reward models, choosing production models for end users, deciding product launches, or certifying compliance. Those require other owners. If a request asks the judge to be the final authority on safety, legal, medical, or financial correctness, stop and escalate to a qualified human reviewer; a judge score is a signal, not a verdict.

## Inputs and assumptions

Collect before scoring:

1. **Task definition**: what the output is supposed to accomplish, for whom, in what format.
2. **Candidate outputs**: the artifacts to score, with stable IDs, model/version labels, and the prompt or input that produced each.
3. **Reference material** (optional): gold answers, source documents, tool logs, test results. Note which criteria need references and which do not.
4. **Human-labeled calibration set**: at least 40 items with human scores on the same rubric, covering the full score range. If none exists, say so; scores are then exploratory only.
5. **Judge model identifier and settings**: record exact model name, version string, temperature, and max tokens. Exact model availability and parameter names are version-sensitive; verify against current provider documentation before reporting.

Assumptions to state explicitly in the report: the judge's knowledge cutoff, whether it can access references, and whether candidate outputs were shown to it with their source model labels hidden.

## Operating workflow

1. **Decompose the quality target** into 3–6 independent criteria (e.g., factual grounding, instruction following, completeness, format compliance, safety of content). Merge criteria that always co-vary. Drop criteria that cannot be observed from the output.
2. **Write anchored scales.** For each criterion define a 1–5 (or binary) scale with a concrete description at every level. Example for grounding: 5 = every claim traceable to the provided source; 3 = one unsupported claim that does not change the conclusion; 1 = central claim contradicts source.
3. **Write the judge prompt** with: role, task, rubric, the output to score, optional reference, required output schema, and an instruction to cite the evidence span before assigning each score. Request structured output (JSON) so parsing is deterministic.
4. **Randomize and blind.** Shuffle item order, strip model names and length cues where possible, and randomize position in pairwise comparisons.
5. **Run a pilot** on 20–30 calibration items. Inspect reasoning for rubric misreadings before scaling.
6. **Calibrate** (see Decision gates), then score the full set with the frozen prompt and settings. Do not edit the prompt mid-run.
7. **Aggregate** per criterion and overall, with confidence intervals (bootstrap over items is acceptable), and report disagreement cases separately.

## Decision gates

- **Gate A: Rubric readiness.** Proceed only if two reviewers, given the rubric alone, assign the same level to at least 80% of five sample outputs. Otherwise rewrite the anchors.
- **Gate B: Judge agreement.** Compare judge scores with human labels on the calibration set. Use quadratic-weighted kappa for ordinal scales or Cohen's kappa for binary labels. Proceed at kappa ≥ 0.6 and adjacent-agreement (within one point) ≥ 85%. Below this, revise the criterion or split it; do not average away the gap.
- **Gate C: Bias screen.** Test for position bias (swap order in pairwise tests; flip-rate above 15% is a failure), length bias (correlation between score and length residualized on quality labels above 0.3 is a concern), and self-preference (if the judge and candidate share a model family, run a sample scored by a second, different judge family).
- **Gate D: Escalation.** Any output flagged for safety, privacy exposure, or legal/medical/financial harm goes to a human reviewer. Any action to publish scores externally, alter a production gate, or delete candidate data requires explicit owner approval first.

## Verification and evidence

Each reported score must be traceable. For every scored item retain: item ID, candidate ID, prompt version hash, judge model string, settings, raw judge response, parsed scores, and any human label. Spot-check at least 10% of judge responses by reading the cited evidence span; record how many citations were accurate. A citation that does not exist in the output is a failed item regardless of score.

Report calibration metrics beside every headline score. A score without its agreement statistic is not a result.

## Failure handling

- **Unparseable output**: retry once with identical input; if it fails again, log and exclude, reporting the exclusion rate. Exclusion above 5% invalidates the run.
- **Judge refuses or hedges**: record as a separate category; do not coerce into a score.
- **Score collapse** (more than 80% of items at one level): the anchors are not discriminating; revisit Gate A.
- **Calibration drift** after a judge model update: rerun Gate B before trusting any new scores; do not compare across judge versions without a bridge set scored by both.
- **Conflicting references**: flag the item rather than letting the judge choose silently.

## Deliverable contract

Produce a single report containing:

1. Rubric with anchored scales and version identifier.
2. Judge configuration, marked where version-sensitive details need verification against current official documentation.
3. Calibration results: kappa, adjacent agreement, sample size, and the score range covered.
4. Bias screen results with pass/fail per test.
5. Per-criterion and overall scores with confidence intervals and item counts.
6. Disagreement and exclusion summary with representative examples.
7. Explicit list of limitations, including where the judge was not validated.
8. Recommended use boundary, stating what the scores may and may not support.

Do not: report scores without calibration; tune the prompt on the test set; claim the judge is objective or equivalent to human expert review; present a judge score as a guarantee of correctness, safety, or regulatory compliance; or invent benchmark figures for comparison.