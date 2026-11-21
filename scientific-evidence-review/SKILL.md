---
name: scientific-evidence-review
description: Use when assessing whether a paper, benchmark result, model card, experiment report, or dataset claim in data science or AI is supported by its evidence, before relying on it for a decision, product choice, or publication.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Scientific Evidence Review

## Purpose and boundaries

This skill produces a structured judgment on whether specific claims in a data or AI artifact are supported by the evidence presented. It covers research papers, benchmark leaderboards, vendor model cards, internal experiment write-ups, and analytic reports.

It does not cover: writing new experiments from scratch, certifying regulatory or ethical compliance, rating a product's legal status, or replacing domain peer review. Verdicts describe the evidence as presented, not the truth of the underlying phenomenon.

## Inputs and assumptions

Required: the artifact (text, tables, code links, or data access), and the specific claims to assess. If no claims are stated, extract them first and confirm the list with the requester.

Optional but valuable: raw results, code, data splits, hyperparameter ranges, compute budget, and prior versions of the artifact.

Assumptions to record explicitly: the time of review, whether the artifact has been revised, and whether code or data was actually inspected or only described.

## Operating workflow

1. **Freeze the artifact.** Record its identifier, version, date, and a hash or copy of the text. Reviews drift when sources change.
2. **Extract claims.** List each quantitative or causal claim as a single sentence, e.g., "Model X improves accuracy over baseline Y by 4 points on test set Z." Discard framing language that carries no testable content.
3. **Map evidence.** For each claim, identify the table, figure, appendix, or code path that supports it. Mark "no evidence located" when none exists.
4. **Check design validity.** Ask: Is the comparison fair? Are baselines tuned with comparable effort? Is the test set independent of training and model selection? Was data leakage ruled out (duplicates, temporal overlap, preprocessing fit on full data)?
5. **Check statistics.** Look for variance across seeds or folds, confidence intervals, significance tests with stated assumptions, and effect sizes. A difference smaller than observed run-to-run variance is not a demonstrated improvement.
6. **Check reproducibility.** Verify that data, code, seeds, and environment are available or described. Note what is missing.
7. **Assign a verdict** (see Decision gates) and write the rationale with specific pointers.

## Decision gates

Assign one verdict per claim:

- **Supported:** Evidence directly measures the claim, design is fair, variance is reported and the effect exceeds it.
- **Partially supported:** Effect is real under narrower conditions (one dataset, one seed, one baseline) than the claim implies.
- **Unsupported:** Evidence is absent, contradicts the claim, or the comparison is structurally unfair.
- **Not assessable:** Required data, code, or detail is withheld. State exactly what would be needed.

Escalate before proceeding if: the review would require accessing restricted or personal data, re-running training that consumes significant paid compute, contacting authors or vendors, or publishing a critique externally. Obtain explicit approval for each.

## Verification and evidence

Every verdict must cite a location (section, table, figure, or code file) and quote or paraphrase the specific number. Reproduce a reported number only when the requester has approved the compute and data access. Where reproduction is attempted, record the environment and deviations.

Quality checks before delivery:
- Every claim has a verdict and at least one citation.
- No verdict relies on the artifact's own summary alone without checking the table it refers to.
- Reported improvements are compared against stated variance; if variance is absent, the verdict cannot exceed "partially supported."
- Version-sensitive details (library behavior, benchmark splits, metric definitions) are flagged for verification against current official documentation.

## Failure handling

- **Missing numbers:** Mark "Not assessable" and list the missing items. Do not infer values from charts unless labeled as approximate reads.
- **Conflicting numbers across sections:** Report both, identify which is the headline claim, and mark the claim "Unsupported" until reconciled.
- **Suspected leakage without proof:** State the suspicion and the test that would confirm it. Do not assert misconduct.
- **Requester pressure for a favorable verdict:** Restate the evidence standard and deliver the verdict the evidence supports.

## Deliverable contract

Return a single review containing:

1. Artifact identifier, version, and review date.
2. Assumptions and scope exclusions.
3. Claim table: claim, verdict, evidence location, key number, main concern.
4. Reproducibility status: available, partial, or absent, with specifics.
5. Required follow-ups, each marked as needing approval or not.
6. Overall confidence (high, medium, low) with one sentence justifying it.

Do not: invent metrics, cite results not in the artifact, present verdicts as compliance or safety certification, or send any part of the review outside the requester's channel without approval.

## Ultron routing contract

**Choose this skill when:** evaluating whether a specific scientific, technical, or AI claim is actually supported by the evidence presented in a paper, benchmark, model card, experiment report, or analytical artifact.

**Choose scientific-research-synthesis when:** the task is to discover and screen a body of literature or registry sources, extract findings, appraise evidence across studies, and produce a traceable synthesis.

**Handoff contract:** receive the exact claim, cited source passages, methods, data, and reported uncertainty. Return a claim-by-claim verdict, missing evidence, methodological weaknesses, alternative explanations, and confidence limits. A research synthesis can use this review to appraise individual sources before combining them.

**Why the boundary exists:** assessing a known claim is not the same as discovering the literature needed to answer a broader question.
