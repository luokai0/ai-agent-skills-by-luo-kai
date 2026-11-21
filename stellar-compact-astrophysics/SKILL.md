---
name: stellar-compact-astrophysics
description: Use when analyzing, modeling, or reporting on white dwarfs, neutron stars, or stellar-mass black holes, including mass-radius inference, cooling or spin-down analysis, X-ray binary or gravitational-wave source classification, and pulsar timing interpretation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Stellar Compact Astrophysics

## Purpose and boundaries

This skill supports quantitative work on stellar remnants: white dwarfs (WDs), neutron stars (NSs), and stellar-mass black holes (BHs). It covers observational data reduction checks, parameter inference, model comparison, source classification, and written findings.

In scope: mass and radius estimates, cooling and spin-down interpretation, binary mass functions, compact-object classification from multiwavelength or gravitational-wave data, and equation-of-state (EOS) constraint assessment.

Out of scope: supermassive black holes, stellar evolution from first principles without a remnant target, cosmological inference, and operational guidance for any hazardous physical process.

## Inputs and assumptions

Before analysis, record:

- Source identifier, coordinates, distance estimate and method (parallax with zero-point correction, dynamical, or distance-modulus).
- Photometry or spectra with bands, extinction law, and calibration references.
- Timing data (pulse TOAs, ephemeris, reference epoch, time standard) or orbital radial-velocity curves.
- Gravitational-wave strain or posterior samples, with detector network, waveform family, and prior specification.
- Units and constants used by each source. Convert to SI or solar units once, then state the convention.

Assumptions must be explicit: atmosphere model (H or He for WDs), EOS family, spin state, inclination prior, and whether the binary is circular.

## Operating workflow

1. **Define the question** as one measurable target, such as "posterior on NS radius at 1.4 Msun" or "is the secondary above the mass gap."
2. **Audit inputs.** Check distance units, parallax zero-point handling, extinction consistency across bands, and epoch alignment for timing solutions.
3. **Select the model** matched to the regime. For WD mass-radius, use cold degenerate or Hamada-Salpeter-type relations with stated atmospheric composition. For NS, use TOV-integrated EOS families. For BH, use mass functions and spin priors.
4. **Run a forward sanity check.** Predict an observable from a canonical case (e.g., 1.4 Msun NS, R ≈ 10–13 km for typical EOS families) and confirm the pipeline reproduces it.
5. **Infer parameters** with stated priors and convergence diagnostics.
6. **Stress-test** against alternative priors, distance estimates, and excluded data subsets.
7. **Write the finding** using the deliverable contract below.

## Decision gates

- **Gate A (data quality):** Proceed only if distance uncertainty is documented and timing residuals show no unmodeled structure above stated tolerance. Otherwise flag and quantify impact.
- **Gate B (classification):** Assign BH status only if the dynamical mass exceeds the maximum NS mass allowed by the EOS posterior, and report the EOS-dependence explicitly. Typical TOV-limited maxima are near 2–2.5 Msun, so treat any claim near this boundary as model-dependent.
- **Gate C (WD):** Chandrasekhar mass (~1.4 Msun) bounds non-rotating, non-accreting cold WDs. A WD mass above this requires a stated mechanism (rotation, magnetic support, accretion history) and a source for that mechanism.
- **Gate D (external action):** Stop before submitting results to catalogs, publishing, or overwriting shared datasets. Obtain explicit user approval.

## Verification and evidence

- Report posteriors as median with 16th–84th percentile intervals, plus the prior used. Never report a single value without uncertainty.
- Confirm units by recomputing one known quantity (e.g., Schwarzschild radius ≈ 2.95 km × M/Msun).
- For MCMC or nested sampling, report effective sample size and convergence statistic; flag any value that fails the tolerance stated in the software documentation.
- Show at least one sensitivity test changing the most influential assumption.
- Mark any software behavior, parameter name, or package version as "verify against current official documentation." Do not assert it from memory.

## Failure handling

- **Degenerate posterior** (prior-dominated): report it as unconstrained and state which prior drives the result.
- **Parallax unreliable** (low signal-to-noise or systematic concerns): switch to an alternative distance method or report the result as conditional on distance.
- **Conflicting measurements:** do not average silently. Present both, with the tension quantified.
- **Pipeline failure on the canonical check:** stop. Do not proceed to science targets until the cause is identified.

## Deliverable contract

Every output contains:

1. Question and classification of the source regime.
2. Inputs table: value, uncertainty, units, source.
3. Assumptions list, including EOS, atmosphere, and priors.
4. Results with credible intervals and sensitivity summary.
5. Limitations, including what would change the conclusion.
6. Items requiring verification against current documentation.

Do not state findings beyond what the data constrain. Do not present model-dependent BH or EOS claims as established facts.