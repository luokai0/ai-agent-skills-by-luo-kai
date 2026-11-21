---
name: cosmic-dark-sector
description: Use when analyzing, modeling, or reviewing work on dark matter and dark energy, including cosmological parameter inference, galaxy rotation and lensing evidence, large-scale structure constraints, and comparison of dark sector models against observational data.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Cosmic Dark Sector

## Purpose and boundaries

This skill guides professional analysis of the dark sector: dark matter (gravitational effects attributed to non-luminous mass) and dark energy (the component driving cosmic acceleration, often parameterized as a cosmological constant or an equation of state w). It covers:

- Evaluating observational evidence (rotation curves, weak and strong lensing, cosmic microwave background, baryon acoustic oscillations, supernova distance measurements, cluster dynamics, large-scale structure).
- Setting up, checking, and interpreting parameter inference and model comparison.
- Reviewing papers, pipelines, or proposals for statistical and physical soundness.

It does not cover: particle-physics detection experiment operations, instrument hardware design, or claims of new discoveries intended for public release. Those require the relevant collaboration's internal review.

## Inputs and assumptions

Before analysis, establish and record:

1. **Question type**: evidence assessment, model fit, pipeline review, or literature synthesis.
2. **Data products**: survey name, data release, sample definition, footprint, redshift range, systematics budget.
3. **Model space**: ΛCDM baseline, extensions (w0wa, modified gravity, interacting dark sector, warm or self-interacting dark matter), and stated priors.
4. **Fiducial assumptions**: flat versus curved geometry, neutrino mass treatment, radiation content, baryon treatment.
5. **Software and versions**: record exact versions; treat any version-specific behavior as requiring verification against current official documentation.

If any of these are missing, state the gap and limit conclusions accordingly. Do not assume a survey's systematics model or a code's default settings.

## Operating workflow

1. **Define the claim.** Write it as one falsifiable sentence, e.g., "Dynamical evolution of dark energy with w0 > -1 and wa < 0 is preferred over ΛCDM at >3σ by combined datasets X and Y."
2. **Map the evidence chain.** List each dataset, the physical quantity it constrains, and its dominant systematics.
3. **Check internal consistency.** Verify units (km/s/Mpc, h-scaling, Mpc versus Mpc/h), distance conventions, and redshift frames (heliocentric versus CMB).
4. **Reproduce a baseline.** Recover a published ΛCDM result from the same data before evaluating extensions. Accept reproduction only within the stated uncertainties.
5. **Test sensitivity.** Vary priors, scale cuts, and nuisance treatment one at a time; record shifts in key parameters (H0, Ωm, σ8, w).
6. **Assess tension.** Compute the difference between datasets using a stated metric (Gaussian parameter-difference, Monte Carlo suite-based, or Bayesian evidence ratio) and report the method.
7. **Write conclusions** only at the confidence the tests support.

## Decision gates

- **Gate A (data adequacy):** Proceed only if systematics budgets are published or can be derived. If not, restrict output to qualitative assessment.
- **Gate B (baseline reproduction):** Proceed to extensions only if the baseline reproduces within 1σ of the published value on the same data.
- **Gate C (model comparison):** Report Bayes factors or information criteria only when priors are documented and sensitivity tests are complete. A preference from a single prior choice is not a result.
- **Gate D (strong claims):** Claims of a >5σ departure from ΛCDM, or of a new dark-sector particle or interaction, require independent replication plus explicit external review before any statement beyond internal notes.

## Verification and evidence

Quality checks, each measurable:

- Baseline reproduction within 1σ of the published central value.
- Parameter chains: Gelman-Rubin or equivalent convergence statistic below the threshold stated in the sampler documentation (verify current recommended value); effective sample size reported for each key parameter.
- Prior sensitivity: key posterior mean shifts below 0.5σ under reasonable alternative priors, or the shift is reported as a limitation.
- Goodness of fit: chi-squared or equivalent reported with degrees of freedom and p-value.
- Example check: for a rotation-curve fit, residuals should show no systematic trend beyond the stated velocity error; a flat residual pattern with a single offset indicates a normalization issue, not a dark-matter halo signal.
- Example check: for a lensing claim, confirm the source-redshift distribution and photometric-redshift calibration are included in the error budget.

Cite every numeric value to its source table or equation. Never state a benchmark or constraint from memory without marking it for verification.

## Failure handling

- **Baseline fails to reproduce:** stop; diagnose units, priors, and data version before continuing. Do not adjust parameters to force agreement.
- **Chains do not converge:** extend run length once; if still unconverged, report results as provisional and do not compare models.
- **Results depend strongly on one nuisance choice:** report the dependence explicitly as a systematic, not as a finding.
- **Conflicting datasets:** report the tension with its metric; do not average datasets to hide it.
- **Missing or ambiguous documentation:** state the ambiguity and the interpretation chosen; flag for author clarification.

## Deliverable contract

Every output contains:

1. Claim statement and question type.
2. Data and model inventory with versions and sources.
3. Gate results (A–D) with pass, fail, or not applicable, and reasons.
4. Quantitative results with uncertainties, methods, and priors.
5. Sensitivity and tension tables.
6. Limitations, including unverified version-sensitive details.
7. Recommendation: accept, revise, or defer, with the specific missing evidence.

## What not to do

- Do not present a dark-sector model as established from a single dataset or a single prior.
- Do not tune nuisance parameters or cuts to remove a tension.
- Do not invent survey numbers, code flags, or package versions; mark them for verification.
- Do not release unreviewed discovery claims, including in summaries for non-specialists.
- Do not run or modify shared collaboration data products, catalogs, or public archives without explicit approval.
- Do not transmit unpublished datasets or internal results externally without explicit approval.