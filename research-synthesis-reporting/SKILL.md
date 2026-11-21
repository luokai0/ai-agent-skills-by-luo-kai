---
name: research-synthesis-reporting
description: Use when turning multiple research sources, experiment results, literature, or internal analyses into a decision-ready synthesis report on data or AI topics, including evidence grading, conflict resolution, and recommendation writing.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Research Synthesis Reporting

## Purpose and boundaries

This skill produces a synthesis report that answers a specific question by combining several evidence sources, weighing their quality, stating what is known versus unknown, and recommending an action with explicit confidence. It covers literature reviews for technical decisions, model or method comparisons, experiment result roll-ups, and data-quality or metric investigations.

It does not cover: running new experiments or training jobs, producing raw data pipelines, legal or regulatory opinions, or publishing results externally. If the question requires new data collection, state that as a gap and stop short of collecting it.

## Inputs and assumptions

Before writing, confirm:

1. **Decision question**: one sentence, phrased so a yes/no, choose-A-or-B, or threshold answer is possible. If the question is vague, propose two sharper versions and ask the requester to pick.
2. **Audience and decision owner**: who acts on this and what they already know.
3. **Source set**: list every source with type (peer-reviewed paper, preprint, vendor documentation, internal experiment, dashboard export, interview notes), date, and access status.
4. **Constraints**: deadline, budget, risk tolerance, data-use restrictions.

Assumptions must be written down in a dedicated section. Do not assume a source's results transfer to the requester's data, model, or population without stating the mismatch.

## Operating workflow

1. **Scope the question.** Write the decision question, the outcome metric(s), and the explicit out-of-scope items.
2. **Inventory sources.** Build a table: ID, title, type, date, population or dataset, method, headline claim, reported uncertainty. Mark sources that could not be read in full.
3. **Extract claims atomically.** One row per claim, linked to its source ID and to the exact location (section, table, figure). Do not paraphrase numbers without checking them against the source.
4. **Grade evidence.** Apply the criteria in Decision gates.
5. **Map agreement and conflict.** Group claims by question. For each group, state whether sources agree, disagree, or are silent, and hypothesize reasons for disagreement (dataset shift, metric definition, evaluation protocol, baseline strength, leakage, sample size).
6. **Reconcile numbers.** Where internal figures are cited, recompute at least one from raw inputs or from the stated formula. Record the check.
7. **Draft the synthesis.** Lead with the answer, then the evidence, then the uncertainty, then the recommendation.
8. **Run the verification pass** (see Verification and evidence).
9. **Hand off** using the deliverable contract.

## Decision gates

**Gate 1 — Source admissibility.** Exclude a source if it lacks a stated method, has no identifiable date, or is a secondary summary with no traceable primary. Keep excluded sources in the inventory with a reason.

**Gate 2 — Evidence strength.** Rate each claim:
- Strong: replicated, or independently measured on data relevant to the decision, with reported variance.
- Moderate: single credible source with relevant data and method description.
- Weak: vendor marketing, anecdote, single run without variance, or data off-target for the decision.

A recommendation may rest on strong evidence alone or on moderate evidence only if the report labels it provisional.

**Gate 3 — Transferability.** For each key claim, state whether the population, model scale, language, domain, or time period matches the decision context. Mismatch on any of these downgrades the claim one level.

**Gate 4 — Recommendation readiness.** Proceed to a recommendation only if: the decision question is answered by at least one strong or two moderate transferable claims, and conflicts are either resolved or explicitly bounded. Otherwise, output a "not yet decidable" report that names the specific missing evidence and its cost to obtain.

**Gate 5 — External or sensitive content.** Stop and request explicit approval before including: confidential internal metrics in any document that will leave the team, personal or user data, unpublished partner results, or any claim that will be used in external communications or regulatory filings.

## Verification and evidence

- Every number in the report traces to a source ID and location. Untraceable numbers are removed.
- Every recomputed figure records the inputs and formula.
- Confidence statements use the graded labels above, not adjectives like "clearly" or "significantly." Use "significant" only with a named statistical test and its result from the source.
- Check for common defects: test-set contamination, baselines that were not tuned, metric changes between compared papers, mismatched dataset versions, and results reported only on favorable subsets.
- Version-sensitive facts (library behavior, model capabilities, vendor pricing, platform limits, benchmark leaderboards) must be marked "verify against current official documentation as of [date reviewed]." Do not state them as current facts without that marker.
- Do not invent benchmark scores, compliance certifications, or performance guarantees. If a source is absent, write "not reported."

## Failure handling

- **Conflicting sources with no resolution:** report both positions, the likely cause, and the single experiment or lookup that would resolve it.
- **Missing primary source:** mark the claim unverified; do not upgrade it because a secondary source repeats it.
- **Numbers do not reproduce:** report the discrepancy with both values and stop using the figure until the owner confirms.
- **Requester demands a conclusion the evidence cannot support:** state the strongest supportable conclusion and the gap, then ask for a decision on whether to proceed provisionally.
- **Source access blocked:** list it as unread; never summarize from abstract alone without labeling it.

## Deliverable contract

The report contains, in order:

1. Decision question and scope (including exclusions)
2. Answer or "not yet decidable" statement in two sentences or fewer
3. Recommendation with confidence label and conditions under which it would change
4. Evidence table: claim, source ID, location, grade, transferability
5. Conflicts and proposed resolutions
6. Assumptions and open questions, each with an owner or next step
7. Source inventory with included and excluded entries and reasons
8. Verification log: recomputed figures, version-sensitive items flagged, defects checked

Length target: 4–8 pages for a standard synthesis; a one-page executive version must reproduce items 1–3 exactly.

Do not: present a recommendation without its confidence grade; blend opinion into the evidence table; cite a source you have not read in the portion you rely on; omit excluded sources from the inventory; or release externally without the approval required by Gate 5.

## Cross-source synthesis controls (v1.1)

### Separate evidence units before combining them

Do not treat every document, experiment, dashboard, interview, and publication as an equivalent observation. Classify each unit as a primary observation, attributed interpretation, secondary synthesis, or decision constraint. A decision constraint shapes the decision but is not empirical evidence that a technical claim is true.

Create a claim-to-evidence graph rather than a flat source list. A claim may depend on multiple observations; one observation may support several claims; and a secondary source may point to primary evidence already inventoried. Record these relationships so repeated reporting of one result is not mistaken for independent agreement.

### Normalize before comparing

Before ranking methods or combining metrics, record unit of analysis, denominator, population, time window, measurement instrument, missing-data treatment, baseline, and aggregation method. Convert units only when exact and preserve original values. Do not average percentages with different denominators or pool metrics whose definitions merely share a label.

For experiment roll-ups, distinguish a repeated run from an independent replication. Preserve run-level results, sample counts, variance or uncertainty intervals, and the selection rule for the reported result. If only the best run is available, label the evidence as selected rather than representative.

### Separate association, prediction, and causation

Classify each conclusion as descriptive, predictive, causal, or normative. A predictive association does not establish causation; a causal estimate does not by itself determine the preferred action. For causal claims, inspect assignment mechanism, confounding, selection effects, temporal ordering, and the estimand. If the design cannot support causal inference, rewrite the claim descriptively or predictively.

### Make uncertainty decision-relevant

For every major conclusion, state the plausible outcome range, assumptions that dominate it, consequence if the estimate is wrong, and evidence that could change the decision. Prefer sensitivity analysis over a confidence adjective. When quantitative uncertainty cannot be calculated, name its source and give a qualitative confidence label with an explicit reason.

### Stop rules for synthesis quality

- If sources reuse the same underlying dataset, count it once for evidential independence.
- If outcome definitions or denominators cannot be reconciled, present parallel results rather than a pooled number.
- If a material subgroup is missing, do not generalize the aggregate result to it.
- If a conclusion depends on an unverified transformation, reproduce it or label the conclusion provisional.
- If a recommendation changes under a reasonable assumption range, make it conditional and identify the threshold at which it changes.

## Ultron routing contract

**Choose this skill when:** synthesizing heterogeneous evidence into a decision-ready report, especially when sources include internal experiments, operational metrics, technical comparisons, literature, interviews, or mixed evidence types. Its central job is reconciliation, confidence calibration, and recommendation readiness.

**Choose scientific-research-synthesis when:** discovering and screening a defined body of scientific literature or registry records using a reproducible search strategy and inclusion criteria. That skill owns search logs, study screening, extraction, and research-review flow counts.

**Choose scientific-evidence-review when:** checking a specific claim, paper, or conclusion against the evidence it cites.

**Handoff contract:** accept source IDs, primary/secondary classification, exact claim locations, population and method details, uncertainty, and duplicate-lineage links. Return a decision question, claim graph, comparability decisions, conflict register, confidence grades, sensitivity conditions, and evidence gaps. Do not imply a narrative synthesis is exhaustive.

**Why the boundary exists:** research synthesis owns discovery and screening of a scientific corpus; evidence review tests individual claims; this skill reconciles evidence across source types for a decision. This prevents double-counting and false certainty.
