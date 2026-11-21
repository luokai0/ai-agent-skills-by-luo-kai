---
name: earth-fluid-climate-systems
description: Use when analyzing, modeling, or reviewing atmospheric or oceanic fluid dynamics and climate-system data, including reanalysis or observation processing, budget closure checks, regional climate diagnostics, and interpreting model-versus-observation discrepancies in Earth and Space Sciences work.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Earth Fluid Climate Systems

## Purpose and boundaries

This skill guides professional analysis of the atmosphere and ocean as geophysical fluids: circulation, thermodynamics, energy and moisture budgets, and their statistical characterization over time and space. It covers:

- Diagnosing gridded fields (reanalysis, satellite retrievals, reference model output, in-situ networks).
- Computing and checking conservation budgets (mass, energy, moisture, momentum where relevant).
- Assessing model skill and model-observation mismatch for climate variables.
- Producing reproducible, caveated technical summaries.

It does not cover: operational forecast issuance, legal or insurance attribution claims, policy recommendations, or engineering certification. Causal attribution claims require a stated method and uncertainty range; do not present single-run or single-event results as definitive attribution.

## Inputs and assumptions

Before analysis, record:

1. Dataset identity: product name, version, release date, spatial grid, temporal resolution, vertical coordinate (pressure, height, sigma, depth, isopycnal).
2. Variable definitions: units, sign conventions, averaging type (instantaneous, daily mean, monthly mean), and whether fields are on native or regridded grids.
3. Time base: calendar (including leap-year handling), time zone or UTC convention, and any known discontinuities from observing-system changes.
4. Reference state: climatology period and method used for anomalies.
5. Assumptions: hydrostatic balance, Boussinesq approximation (ocean), negligible horizontal divergence at specified scales, or other simplifications. State each one and where it breaks down.

If any item is unknown, mark it as unknown and propagate that uncertainty into conclusions. Do not infer units silently; verify against product documentation.

## Operating workflow

1. **Scope the question.** Write one sentence stating the physical quantity, region, period, and decision it supports.
2. **Audit the data.** Check coordinate monotonicity, missing-value encoding, grid-cell area weighting, leap-day handling, and duplicated time steps. Count missing fraction per variable and per region.
3. **Harmonize.** Regrid only when necessary; prefer conservative remapping for flux-like quantities and bilinear or nearest methods for state variables. Record the method.
4. **Compute diagnostics** with explicit formulas. Use area-weighted means (cosine-of-latitude weighting for regional averages). Use mass-weighted vertical integrals for column quantities.
5. **Check budgets.** Compare the residual of the closed budget (for example, column energy tendency versus net flux convergence plus sources) against the stated tolerance. Report the residual, not only the result.
6. **Quantify uncertainty.** Use ensemble spread, dataset intercomparison, or bootstrap resampling with autocorrelation-aware block lengths. Do not treat autocorrelated daily samples as independent.
7. **Interpret physically.** Connect each result to a mechanism (e.g., thermal wind balance, Ekman transport, moisture convergence) and state what alternative mechanism would produce the same signal.
8. **Write the deliverable** per the contract below.

## Decision gates

- **Gate A (data fitness):** Proceed only if missing data is under 10% in the analysis domain and period, or if gaps are documented and handled by a stated method. Otherwise, narrow the domain or period.
- **Gate B (budget closure):** Residual must be below 10% of the largest individual term, or a stated physical reason must explain the excess (e.g., unresolved subgrid process, known reanalysis increment). If unexplained, stop and report the inconsistency before drawing conclusions.
- **Gate C (model-observation comparison):** Compare only on a common grid, common period, and common sampling (e.g., model output sampled at observation times where relevant). Mismatched sampling invalidates bias estimates.
- **Gate D (attribution or trend claims):** Require at least two independent datasets or an explicit statistical test with stated significance and method. Otherwise, label the result as exploratory.
- **Gate E (external use):** Any output intended for publication, public release, policy, or client decisions requires explicit human review and approval before release. Do not distribute results externally on your own authority.

## Verification and evidence

- Reproduce one known statistic from the dataset documentation or a published reference value before trusting a pipeline. Record the match tolerance.
- Test sign conventions with a synthetic field of known structure (e.g., uniform eastward wind yields positive zonal wind).
- Check that global-mean energy and moisture budgets are plausible in magnitude relative to published reference ranges; cite the reference used.
- Verify unit conversions by dimensional analysis in each equation.
- Confirm that area-weighted and unweighted results differ in the expected direction for high-latitude-dominated fields.
- Record software environment, library versions, and random seeds. Mark any version-specific behavior as requiring verification against current official documentation.

## Failure handling

- **Unit or sign mismatch:** Stop, trace the variable's metadata, and correct before recomputing. Report the original error and affected outputs.
- **Budget residual exceeds tolerance:** Decompose the residual by term and by region or level to locate the source. Do not adjust a term to force closure.
- **Dataset disagreement larger than stated uncertainty:** Report the spread and the candidate causes (observing-system change, retrieval algorithm, grid artifacts). Do not average away the disagreement.
- **Missing or corrupted files:** Report the exact files and time ranges affected; never fill gaps silently with climatology unless labeled as imputation with its uncertainty.
- **Ambiguous physical interpretation:** State two competing explanations and the observation that would distinguish them.

## Deliverable contract

Every output must include:

1. **Question and scope:** physical quantity, region, period, decision context.
2. **Data provenance table:** dataset, version, grid, period, missing fraction, known caveats.
3. **Method summary:** formulas, weighting, regridding, tolerances, assumptions.
4. **Results:** values with units and uncertainty ranges; budget residuals reported explicitly.
5. **Gate status:** pass, conditional, or fail for each applicable gate A through E.
6. **Limitations:** unresolved assumptions and out-of-scope conclusions.
7. **Reproduction record:** code location or procedure, environment, seeds, and the verification checks performed.

## What not to do

- Do not present model output as observations or vice versa.
- Do not compute anomalies against a reference period you have not stated.
- Do not use unweighted grid-cell averages for regional means on lat-lon grids.
- Do not treat a single season, year, or model run as a climate trend.
- Do not invent dataset versions, variable names, or citation details; if unknown, mark them unknown.
- Do not state exact software function names, command flags, or package versions from memory; verify against current official documentation.
- Do not overwrite or delete source data, raw archives, or prior results without explicit approval.
- Do not transmit, publish, or share outputs externally without explicit approval.