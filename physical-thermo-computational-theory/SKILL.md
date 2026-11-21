---
name: physical-thermo-computational-theory
description: Use when modeling thermodynamic or statistical-mechanical properties of chemical and biological systems computationally, including free energy estimation, phase and equilibrium analysis, reaction thermochemistry, and validating simulation or theory outputs against experimental data.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Physical Thermo Computational Theory

## Purpose and boundaries

This skill guides computational work on equilibrium thermodynamics, statistical mechanics, and thermochemistry for molecular chemistry and biomolecular systems. It covers: choosing an appropriate theoretical level, setting up free energy or equilibrium calculations, checking convergence and sampling adequacy, deriving thermodynamic quantities (ΔG, ΔH, ΔS, Kd, pKa, partition coefficients, phase boundaries), and reporting results with uncertainty.

It does not cover: kinetic rate prediction beyond transition-state estimates, wet-lab protocol design, clinical or pharmacological recommendations, or production of hazardous-material synthesis routes. Redirect those requests.

## Inputs and assumptions

Before computing, record:

1. System definition: species, protonation states, tautomers, ionic strength, pH, temperature, pressure, solvent model, and standard state convention.
2. Target quantity and its defining ensemble (NVT, NPT, grand canonical, isothermal-isobaric reaction).
3. Available experimental reference values with source, conditions, and stated uncertainty.
4. Compute budget and required precision (for example, ±0.5 kcal/mol for relative binding free energy).
5. Software and force field or electronic-structure method, with exact version. Mark any version-specific behavior as "verify against current official documentation" unless confirmed in this session.

Assumptions must be written down explicitly. If protonation states or standard states are unknown, stop and resolve them rather than assuming.

## Operating workflow

1. Restate the question as a thermodynamic statement: which state change, which ensemble, which reference state.
2. Select method by accuracy tier:
   - Screening, large sets: empirical or semi-empirical estimates, with calibration against a reference subset.
   - Reaction energetics, small molecules: correlated wavefunction or composite schemes, with basis-set extrapolation where feasible.
   - Condensed phase, binding, solvation: explicit-solvent sampling with alchemical or path-based free energy methods; implicit solvent only for trend work.
3. Build the system and equilibrate. Record equilibration criteria (energy, density, RMSD plateau) before production.
4. Run production sampling with at least two independent replicas from different initial conditions.
5. Compute the free energy or equilibrium constant using an estimator appropriate to the method (for example, MBAR or BAR for alchemical windows, with overlap matrices reported).
6. Propagate uncertainty: report replica spread, block-averaged or autocorrelation-corrected standard error, and systematic error from force field or method choice.
7. Compare with experiment and state agreement in units of the stated uncertainty.

## Decision gates

- Gate A (before production): Are protonation states and ionic conditions fixed and justified? If not, stop.
- Gate B (sampling): Is the slowest observable autocorrelation time shorter than one-fifth of the production length? If not, extend sampling or flag the result as unconverged.
- Gate C (overlap): For alchemical or umbrella methods, is adjacent-window overlap sufficient (typically a nonzero overlap well above noise in the overlap matrix)? If any window pair has negligible overlap, add windows.
- Gate D (agreement): If calculated values differ from experiment by more than three times the combined uncertainty, do not report a conclusion. Investigate protonation, convergence, force field terms, and reference data quality first.
- Gate E (external action): Any submission to shared compute queues with cost above the approved budget, data release, or publication-grade claims requires explicit user approval.

## Verification and evidence

Each result must include:

- Convergence plots or numeric summaries for energy, density, or the target observable versus time.
- Replica agreement: difference between independent runs within stated uncertainty.
- Sensitivity check: vary one key assumption (cutoff, thermostat, charge model, basis set) and report the change.
- Internal consistency: thermodynamic cycle closure where applicable (for example, a ΔG cycle closing within reported error), and ΔG = ΔH − TΔS consistency if components are reported.
- Units and standard states stated explicitly; check that concentration-dependent values are corrected to the declared standard state (for example, 1 M versus 1 atm).

Quality threshold: a result is "reportable" only when convergence, replica agreement, and at least one sensitivity check pass. Otherwise it is "exploratory" and labeled as such.

## Failure handling

- Non-convergent sampling: extend runs, increase replicas, or enhance sampling; do not average unconverged blocks.
- Poor window overlap or hysteresis between forward and reverse transformations: add intermediate states, increase per-window time, or switch estimator. Report the hysteresis magnitude.
- Unphysical energies (large negative values from clashes, failed minimization): re-minimize and re-equilibrate; check topology and atom typing before rerunning.
- SCF or electronic-structure non-convergence: change initial guess, damping, or convergence algorithm; do not silence convergence warnings.
- Missing experimental reference: report computed values with uncertainty only, and state that no validation was performed.

## Deliverable contract

Return a structured report containing:

1. Question statement with ensemble, state change, and standard state.
2. Method, software, and versions (version-sensitive items marked for verification).
3. Input parameters and assumptions, including protonation and ionic conditions.
4. Results table: quantity, value, uncertainty (replica and systematic), units, status (reportable or exploratory).
5. Verification evidence per the checklist above.
6. Comparison with experiment, stated as deviation in units of combined uncertainty.
7. Limitations and what would change the conclusion.
8. Reproducibility package: input files, seeds, and analysis scripts, with any data sharing or external submission held for user approval.

Do not report bare numbers without uncertainty, do not mix standard states silently, and do not present implicit-solvent trend results as absolute binding energies.