---
name: health-clinical-analytics
description: Use when analyzing clinical data drawn from external health registries (disease, device, cancer, vaccine, or patient-outcome registries) to build cohorts, compute outcome measures, assess data quality, or prepare registry-based evidence for research, quality improvement, or regulatory submissions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Health Clinical Analytics

## Purpose and boundaries

This skill covers analysis of data extracted from external clinical registries: the registry's own extracts, linked administrative data, or registry-derived aggregate tables. It produces cohort definitions, outcome tables, data-quality assessments, and analysis code or specifications with an audit trail.

In scope: cohort construction from registry fields, codebook mapping, denominator and numerator logic, survival and incidence calculations, risk adjustment design, missingness assessment, and reporting that states limitations.

Out of scope: individual patient re-identification, linking records to identifiers the user is not authorized to hold, making treatment recommendations for individual patients, and asserting causal effects without an explicit design that supports them.

## Inputs and assumptions

Required before starting:
- Registry name, version or data-release date, and the data use agreement or governance basis.
- Data dictionary or codebook. If absent, stop and request it.
- Study question stated as population, exposure or intervention, comparator, outcome, time window, and estimand.
- Intended use: research, internal quality improvement, or regulatory. Each requires different sign-off.

Assumptions to state explicitly in every deliverable: registry completeness is unknown unless the registry publishes a validated completeness figure; coding changes across release years are possible; field definitions may differ from clinical usage.

## Operating workflow

1. **Confirm governance.** Verify that the requested use matches the data use terms. Record the approver's name and date.
2. **Map the codebook.** Build a table: registry field, permitted values, meaning, and the study variable it feeds. Flag any value that has no mapping.
3. **Define the cohort in code-independent prose first.** Write inclusion and exclusion criteria with the index date rule. Then translate to logic. Keep both versions in the deliverable.
4. **Profile data quality.** For each analytic variable, compute missingness rate, out-of-range counts, impossible date sequences (for example, death before diagnosis), and duplicate record keys. Report by year and by reporting site if available.
5. **Resolve duplicates and conflicts.** Apply a documented rule, such as retaining the most recent record per patient-event key. Never silently drop records.
6. **Compute outcomes.** Use the pre-specified time windows. For time-to-event outcomes, state the censoring rule and handle competing risks explicitly.
7. **Run sensitivity checks** (see Verification).
8. **Write the limitations section** before the results, not after.

## Decision gates

- **Gate A, codebook complete?** Proceed only if every analytic variable maps to a documented definition. Otherwise return to step 2.
- **Gate B, missingness acceptable?** If a key exposure or outcome field exceeds 10% missing, do not impute without a pre-specified method and a missing-data sensitivity analysis. Above 30%, report the analysis as exploratory only.
- **Gate C, linkage valid?** If records are linked across sources, require a documented linkage method and an estimate of false match or missed match rates. Without these, do not present linked results as definitive.
- **Gate D, external impact?** Any output leaving the analyst's team (publication, regulator submission, public dashboard, patient-facing material) requires explicit written approval from the data steward and the responsible clinical lead. Small-cell counts (fewer than 11 in a reported cell, unless the governance terms specify otherwise) must be suppressed or aggregated before release.

## Verification and evidence

Measurable checks before release:
- Cohort size reconciles: starting population minus each exclusion equals the final N, with a flow table.
- Outcome rates recomputed independently by a second person or a second method match within rounding.
- Date sanity: zero records with event dates outside the registry coverage period, or each such record is listed with a disposition.
- Sensitivity analysis: at least one alternative definition of the primary outcome and one alternative handling of missing data. Report whether conclusions change.
- Temporal stability: compare rates across release years; explain any shift greater than the pre-stated threshold by coding change, policy, or true change.

Evidence to retain: codebook version, query or code hash, run date, data release identifier, and reviewer sign-off.

## Failure handling

- **Codebook ambiguity:** Stop. List the ambiguous codes with counts and request clarification from the registry maintainers. Do not guess a mapping.
- **Unexpected count change between runs:** Diff the input extracts before investigating the code. Most discrepancies come from data refresh, not logic.
- **Small cells breaching disclosure rules:** Aggregate categories or suppress. Do not report the value in a footnote or chart label.
- **Results contradict the registry's published figures:** Report the discrepancy with both calculations and do not choose the more favorable one.
- **Requested analysis implies individual-level disclosure:** Decline and offer aggregate alternatives.

## Deliverable contract

Every deliverable contains, in order:
1. Study question and estimand, governance reference, and intended use.
2. Data source identifier, release date, and codebook version.
3. Cohort definition in prose and logic, with a flow table.
4. Data-quality profile with missingness and conflicts.
5. Limitations and assumptions.
6. Results with confidence intervals and suppression notes.
7. Sensitivity analyses and verification results.
8. Approval status and reviewer names.

Do not include unverified external benchmark figures or claims of regulatory compliance. Where software functions, library versions, or registry-specific API endpoints are referenced, mark them "verify against current official documentation" unless confirmed in the current release notes.

## What not to do

- Do not merge registries or link identifiers without documented authorization.
- Do not report precision beyond the data's accuracy.
- Do not present registry rates as population rates without stating the coverage denominator.
- Do not treat absence of a record as absence of an event without checking reporting completeness.
- Do not alter outcome definitions after viewing results.