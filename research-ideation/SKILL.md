---
name: research-ideation
description: Use when turning a data or AI problem, dataset, or observed phenomenon into a set of testable research or project hypotheses, prioritized by value, feasibility, and risk, before any large experiment or build commitment is made.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Research Ideation

## Purpose and boundaries

This skill produces ranked, testable research or project ideas in data science and AI. It covers problem framing, hypothesis generation, literature and prior-art scoping, feasibility assessment, and experiment design sketches. It does not execute experiments, train production models, make compliance determinations, or commit resources. Output is a proposal for a human decision-maker.

## Inputs and assumptions

Collect before generating ideas:
- Problem statement or business/research question, and who will act on the result.
- Available data: sources, schema, volume, label availability, collection date range, known gaps and biases.
- Constraints: compute budget, timeline, team skills, deployment target, latency and cost limits.
- Success criteria: a metric the stakeholder accepts, and the threshold that would count as a win.
- Prior work already attempted, if any.

If any of these are missing, state the assumption explicitly in the output and mark affected ideas as conditional. Do not silently fill gaps with plausible-sounding specifics.

## Operating workflow

1. Restate the problem in one sentence with the decision it informs. If the decision is unclear, stop and ask.
2. Characterize the data: unit of observation, target definition, label source and its noise, temporal structure, leakage risks (features computed after the outcome, post-treatment variables), and class or subgroup imbalance.
3. Generate 8–15 candidate hypotheses spanning at least three families where applicable: data-centric (cleaning, labeling, new signals), modeling (architecture or method change), problem reformulation (different target, ranking vs. classification, causal vs. predictive), and evaluation (better metric, slice analysis, calibration).
4. For each candidate, write a falsifiable form: "If X, then Y will change by at least Z on metric M over holdout H; if not, we reject this direction."
5. Score each on four axes, 1–5 each: expected value to the decision, feasibility with stated resources, cost to test (time and compute), and risk (privacy, fairness, reproducibility, misuse).
6. Check prior art: search for existing methods and published results on the same task type. Record sources you actually consulted; do not cite from memory without marking it unverified.
7. Select a shortlist of 3–5 with a cheapest-informative-test for each: the smallest experiment that could kill the idea.
8. Produce the deliverable contract below.

## Decision gates

- **Gate A (framing):** Proceed only if the decision owner and success metric are named. Otherwise return with questions.
- **Gate B (data validity):** If label leakage, severe sampling bias, or unavailable ground truth is identified, downgrade all ideas depending on that data until the issue is addressed.
- **Gate C (shortlist):** Advance an idea only if its cheapest test costs under a fixed budget agreed with the requester (default: under 10% of the project's compute or time allocation, if no budget is given, flag this).
- **Gate D (approval):** Any step involving access to sensitive or personal data, use of external APIs or third-party services with user data, deletion or overwrite of datasets, publication of results, or actions affecting people outside the team requires explicit written approval before proceeding. Ideation alone never triggers these actions; plans that include them must be flagged.

## Verification and evidence

- Every numeric claim about expected gains must be labeled as a prior estimate with its basis, or removed.
- Distinguish observed facts (from supplied data or cited sources) from hypotheses.
- Check each hypothesis against the leakage and split checklist: is the holdout temporally or group-separated where needed?
- Confirm each shortlisted test has a pre-registered metric and a decision threshold.
- Mark any library, API, hardware, or version-specific detail as requiring verification against current official documentation.

## Failure handling

- If the problem cannot be stated with a decision owner: return a list of clarifying questions, no ideas.
- If data is insufficient for any hypothesis: say so, and propose data collection as a candidate idea with its own cost estimate.
- If all candidates score low on feasibility: report this honestly and recommend scoping down the question.
- If prior art reveals the idea was already tested: state the result, and only proceed if the new variant differs in a stated, material way.

## Deliverable contract

Return a document with these sections in order:
1. Problem restatement and decision owner.
2. Assumptions and open questions (explicit list).
3. Data characterization, including leakage and bias risks.
4. Ranked candidate table: hypothesis, falsifiable form, four scores, prior-art note, cheapest test.
5. Shortlist (3–5) with test design: data split, metric, threshold, estimated effort range.
6. Approval items: any steps requiring Gate D approval, listed plainly.
7. Version-sensitive items flagged for verification.

Do not: invent benchmark numbers, cite papers or tools not verified, promise performance gains, recommend using personal data without a stated approval path, or present ideas as decided. Keep the tone plain and the claims bounded.