---
name: planetary-exoplanet-science
description: Use when analyzing, validating, or reporting on exoplanet detections, candidate vetting, transit or radial-velocity characterization, atmospheric retrieval interpretation, or population statistics for planets orbiting other stars.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Planetary Exoplanet Science

## Purpose and boundaries

This skill guides rigorous work on planets outside the Solar System: detection analysis, candidate vetting, bulk property estimation, atmospheric interpretation, and population-level inference. It covers reasoning about data products and published results, and producing defensible summaries or analysis plans.

Out of scope: solar system planetary science, stellar evolution modeling beyond what planet inference requires, instrument hardware design, and any claim of a confirmed biosignature. Biosignature questions are treated as unresolved unless independent, peer-reviewed evidence exists, and are flagged for expert review.

## Inputs and assumptions

Collect before analysis:
- Target identifiers, host-star parameters (Teff, log g, metallicity, radius, mass, distance), and their sources and uncertainties.
- Data type: photometry (cadence, aperture, detrending method), radial velocities (instrument, reduction pipeline, activity indicators), imaging, or spectra (resolution, wavelength range, transmission or emission).
- Existing dispositions (confirmed, candidate, false positive) and the archive snapshot date.
- Units and reference frames. Assume nothing about units; confirm them.

Assumptions must be stated explicitly. Stellar parameters from older catalogs are frequently revised; treat any value without uncertainty as provisional.

## Operating workflow

1. **Freeze the data version.** Record archive name, table, retrieval date, and pipeline or data release identifier. Verify current release details against official mission or archive documentation, since these change.
2. **Re-derive host-star parameters** or confirm their provenance. Radius errors propagate directly into planet radius (Rp = Rs × sqrt(depth)).
3. **Check transit geometry.** Compare duration against the expected duration for the stellar density and period. Large mismatches suggest eccentricity, blending, or a wrong host.
4. **Vet for false positives** in this order: odd/even depth difference, secondary eclipse presence, centroid shift, ephemeris match to known binaries, and background eclipsing binary modeling.
5. **For radial velocities,** fit a Keplerian with and without a linear or quadratic trend, then compare activity indicators (log R'HK, bisector span, FWHM) against the signal's period. A signal tracking rotation or activity is not a planet.
6. **Derive bulk properties** (mass, density, equilibrium temperature) with propagated uncertainties via sampling, not linear error bars alone. Use the full posterior when available.
7. **For atmospheric spectra,** separate instrument systematics and stellar contamination (transit light source effect) before interpreting molecular features. Report retrieval priors and model grids.
8. **For populations,** state selection function, completeness, and detection bias before fitting occurrence rates.

## Decision gates

- **Gate A (candidate to planet):** Proceed only if at least two independent lines of evidence pass (photometric vetting, RV detection, or imaging) and no unresolved false-positive test remains.
- **Gate B (mass measurement):** Report a mass only from RV or TTV signals with semi-amplitude significance above roughly 4 sigma, or with a documented stability test. Otherwise report a minimum mass (M sin i).
- **Gate C (atmospheric claim):** Claim detection only at a stated significance after accounting for model-grid choice. Claim absence only with stated upper limits and injection-recovery tests.
- **Gate D (external release):** Any public statement, catalog submission, or result sent to collaborators requires explicit human approval.

## Verification and evidence

- Injection-recovery: inject a synthetic transit or RV signal at the reported period and amplitude; recovery rate must be reported.
- Residual checks: no remaining periodicity above the noise in the residual periodogram at the claimed period.
- Consistency: derived density and equilibrium temperature must fall within physically allowed bounds for stated composition classes.
- Every quantitative claim carries units, uncertainty, method, and source.

## Failure handling

- Conflicting host parameters: report both, compute planet properties under each, and state the spread.
- Non-converging fits: do not widen priors silently; report the failure and the prior sensitivity.
- Missing uncertainties: flag the value and exclude it from confirmatory conclusions.
- Suspected data artifacts: quarantine the dataset and note the artifact type rather than deleting points.

Do not:
- Present a candidate as confirmed.
- Quote a mass from transit data alone.
- Remove outliers without a documented criterion applied before fitting.
- Claim a biosignature.
- Cite benchmark or survey statistics from memory; retrieve and verify them.

## Deliverable contract

Each deliverable contains:
1. Data provenance table (source, version, retrieval date).
2. Host-star parameters with uncertainties.
3. Evidence summary by gate, with pass/fail and reasoning.
4. Derived planetary properties with uncertainties and method.
5. Verification results (injection-recovery, residuals).
6. Limitations and open questions.
7. Approval status for any external-facing use.