---
name: manuscript-and-grant-writing
description: Use when drafting, restructuring, or reviewing research manuscripts, grant proposals, or technical reports in data science, machine learning, or AI, including claims, evidence tables, reproducibility and data statements, and funder or venue compliance checks.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Manuscript And Grant Writing

## Purpose and boundaries

This skill produces and revises written research artifacts in data and AI: journal and conference papers, workshop papers, preprints, grant proposals, specific aims pages, project narratives, and technical reports. It covers structure, argument, claim-evidence alignment, figures and tables, reproducibility statements, and submission-readiness checks.

It does not cover fabricating results, writing text that misrepresents authorship or funding, drafting legal or ethics approvals on an institution's behalf, or predicting funding outcomes.

## Inputs and assumptions

Required inputs before drafting:
- Target venue or funder, and its current call, template, and page or word limits.
- The core contribution stated in one sentence, plus the experiments or analyses that support it.
- Result files, logs, or tables. Numbers are copied from source artifacts, never from memory.
- Dataset provenance, licenses, and any consent or privacy constraints.
- Author list, contribution roles, and funding sources, as provided by the user.

Assume the user is responsible for scientific claims. If inputs are missing, ask; do not fill gaps with plausible values.

## Operating workflow

1. **Pin the contribution.** Write a single claim sentence and a list of two to four supporting claims. Reject any claim the artifacts do not directly support.
2. **Build a claim-evidence map.** For each claim, list the figure, table, or section that supports it, the metric, the dataset split, and the number of runs or seeds. Flag claims with no evidence.
3. **Check the template.** Confirm the venue's current template, anonymization rules, page limit, and required sections. Mark these as version-sensitive and verify against the official call before finalizing.
4. **Draft in this order:** methods, results, introduction, related work, discussion, abstract. Introduction and abstract come last because they must match what the results show.
5. **Write the reproducibility and data statements.** Include data sources with versions or access dates, preprocessing steps, hyperparameter search ranges, compute description, random seeds, and code availability status.
6. **For grants,** map each aim to a measurable objective, a method, a timeline milestone, and a deliverable. Include data management, risk, and broader-impact or ethics sections as the funder requires.
7. **Revise for tone.** Replace superlatives and unhedged causal language with the strength the evidence supports.

## Decision gates

- **Claim gate:** Proceed only if every headline claim maps to at least one artifact. Otherwise, narrow the claim or request the missing experiment.
- **Statistics gate:** Report variance across seeds or folds. If only single runs exist, state this and avoid ranking methods by differences smaller than the observed spread.
- **Novelty gate:** Compare against the closest three to five prior works by name. If the contribution overlaps heavily, reframe around the actual difference.
- **Sensitive-data gate:** If the work uses personal, health, or restricted data, stop and request explicit approval from the user before including any sample, identifier, or quoted record.
- **Submission gate:** Do not declare a document ready until the template, limits, and anonymization are checked against the current official source.

## Verification and evidence

- Every number in the text matches its source artifact. Record the artifact path next to each table entry during drafting.
- Metric names, dataset versions, and baseline configurations are consistent across abstract, results, and tables.
- Figures have labeled axes, units, error bars or a stated uncertainty measure, and captions readable without the body text.
- Abbreviations are defined on first use. References resolve to real, retrievable publications; never generate citation entries from memory without a check.
- Word and page counts are measured on the final formatted document, not the draft.

## Failure handling

- **Missing result:** Insert a clearly marked gap in the draft listing the required experiment. Never estimate the number.
- **Conflicting numbers:** Stop, list the conflicting sources, and ask which is authoritative.
- **Template uncertainty:** State which version was assumed and ask the user to confirm.
- **Over-length draft:** Cut related-work detail first, then repetitive method description, never the limitations.

## Deliverable contract

Each deliverable includes:
1. The revised document in the requested format.
2. A claim-evidence table linking each claim to its artifact.
3. A list of open items: missing evidence, unverified template rules, and decisions requiring the author's approval.
4. A limitations paragraph suitable for the document itself.

Do not invent benchmark results, funding amounts, deadlines, compliance certifications, or software version numbers. Do not present unverified tool or policy details as current facts.