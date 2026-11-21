---
name: development-ecology-evolution
description: Use when analyzing, designing, or reviewing studies that connect developmental mechanisms (chemical signaling, gene regulation, morphogenesis) with ecological context (environment, interactions, resources) and evolutionary change (plasticity, heritability, selection), including eco-evo-devo literature synthesis, experimental design, and chemical-ecology data interpretation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Development Ecology Evolution

## Purpose and boundaries

This skill supports professional work at the intersection of developmental biology, ecology, evolutionary biology, and the chemistry that mediates them: morphogen and hormone gradients, metabolite-driven signaling, environmentally induced phenotypes, semiochemicals, and reaction-network reasoning about developmental outcomes.

In scope:
- Reviewing and synthesizing evidence on developmental plasticity, genotype-by-environment effects, and evolutionary developmental change.
- Designing or critiquing factorial experiments that separate genetic, environmental, and developmental variance.
- Interpreting chemical-ecology and metabolomic datasets in a developmental or evolutionary frame.
- Writing analysis plans, reports, and protocol reviews.

Out of scope: clinical or human-subject interventions, wet-lab protocols for hazardous synthesis, field releases of organisms, and regulatory or biosafety determinations. Route these to qualified personnel and institutional committees.

## Inputs and assumptions

Before analysis, establish:
1. The question type: mechanistic (how), ecological (under what conditions), or evolutionary (what changed across lineages or generations).
2. Study system: organism, life stage, tissue, and taxonomic reference.
3. Data provenance: raw versus processed, instrument or method, units, and sample size per treatment.
4. Environmental variables: which were manipulated, which were measured, and which are confounded.
5. Explicit assumptions, such as additivity, linearity of reaction rates, or stationarity of selection.

State any assumption you cannot verify as an assumption. Do not fill gaps with typical values from memory.

## Operating workflow

1. Restate the question in one sentence and classify it by level (molecular, organismal, population, lineage).
2. Map the causal chain: signal or chemical input, receptor or pathway, developmental process, phenotype, ecological consequence, fitness-relevant outcome. Mark each link as observed, inferred, or assumed.
3. Check design adequacy: are treatment and control matched in timing and stage? Is there a reciprocal or cross-environment component? Are maternal or parental effects separated from direct effects?
4. For data, run unit and scale checks, identify missing values and batch effects, and record normalization steps.
5. Choose an analysis matched to the question. Use mixed models for nested or repeated measures; reaction-norm analysis for plasticity; variance partitioning for heritability versus environmental contribution; multivariate methods for chemical profiles, with compositional care.
6. Interpret effect sizes with confidence intervals, not only p-values.
7. Separate what the data show from what the mechanism would predict and from what the evolutionary history would require.

## Decision gates

Proceed to conclusions only when:
- Treatment assignment is documented and randomized or justified.
- Sample size supports the claimed effect size, or the report states the power limitation.
- Chemical identities are confirmed by standard or reference data, not spectral match alone.
- Confounds (stage, batch, density, maternal environment) are either controlled or explicitly bounded.

Stop and request approval before:
- Any wet-lab, animal, or field action, including sampling protocols beyond the approved design.
- Deleting, overwriting, or re-processing shared raw datasets.
- Publishing or sharing sequence, specimen location, or unpublished data outside the project team.
- Making claims about human health, pesticides, or environmental release.

## Verification and evidence

Quality checks, each with a measurable criterion:
- Every quantitative claim traces to a named table, figure, or dataset row.
- Reaction-norm or interaction claims report the interaction term and its interval, not just main effects.
- Chemical assignments list the confidence level and reference used.
- Replication: at least the biological replicates stated in the design; pseudoreplication flagged if present.
- Sensitivity check: conclusions hold after excluding the single most influential sample or batch.

Version-sensitive items (statistical package functions, instrument software, database accession formats, reference genome builds, metabolomic library versions): verify against current official documentation before stating a specific setting. Do not cite function names or flags from memory as authoritative.

## Failure handling

- Missing metadata: list the missing fields, state which conclusions are blocked, and request them.
- Confounded design: report the confound, downgrade the claim to association, and propose the minimal additional treatment that would resolve it.
- Contradictory evidence across studies: compare system, life stage, and environment before attributing conflict to biology.
- Unidentified compounds: report as features with mass or retention information only; do not assign structures.

## Deliverable contract

A completed deliverable contains:
1. One-paragraph summary with the question, the answer's strength, and the main limitation.
2. Causal chain table: link, evidence, classification (observed, inferred, assumed).
3. Analysis description sufficient for reproduction, including model structure and software versions to verify.
4. Verification checklist results with pass, fail, or not-applicable per item.
5. Open items requiring approval or additional data.

Do not: invent citations, benchmark values, or compliance statements; present inferred mechanisms as measured; or extend conclusions beyond the studied system and life stage.