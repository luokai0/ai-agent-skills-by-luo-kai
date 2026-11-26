# Physics, Earth, and Space Science

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## classical-mechanics-fields-waves

**Use when:** Use when solving, checking, or documenting problems in classical mechanics, electromagnetic fields, or wave phenomena, including derivations, boundary-value setups, dispersion and mode analysis, and numerical verification of analytic results.

### Purpose and boundaries

Use this skill to set up, solve, and verify problems in Newtonian and Lagrangian/Hamiltonian mechanics, rigid bodies, continuum mechanics limited to linear elasticity and fluids at the level of wave propagation, Maxwell's equations in media, and linear wave equations (strings, membranes, acoustics, electromagnetic guides, dispersive media).

Out of scope: quantum treatments, relativistic general theory beyond special-relativistic kinematics, nonlinear turbulence closure, and design sign-off for structures, aircraft, medical devices, or radiation-emitting equipment. For those, produce analysis only and state that a licensed engineer or domain authority must review it.

### Inputs and assumptions

Before solving, record:

- Governing system: particle, rigid body, continuum, or field.
- Coordinates, units system (SI or Gaussian; never mix), and sign conventions.
- Constraints, boundary conditions, and initial conditions, each stated explicitly.
- Material parameters and their validity range (linear, isotropic, lossless, nondispersive, etc.).
- Required output: closed form, numerical value, mode table, dispersion relation, or plot.

If any of these is missing and cannot be inferred without changing the answer, ask. Do not silently assume a medium is lossless or a boundary is perfectly conducting.

### Operating workflow

1. Restate the problem in one paragraph with all assumptions listed.
2. Choose a formulation: Newton for simple force balance, Lagrange when constraints or symmetry dominate, Hamilton for conserved-quantity or canonical analysis, field equations with boundary conditions for wave problems.
3. Nondimensionalize where scales are clear. Identify the small parameter if a perturbation is used.
4. Derive symbolically. Keep intermediate expressions; do not jump to numbers.
5. Check limits: zero coupling, large-time behavior, symmetric cases, known textbook recovery.
6. Verify numerically when a closed form is unavailable or as a cross-check (see Verification).
7. Write the result with units, validity conditions, and an uncertainty or neglected-term statement.

### Decision gates

- **Gate A, formulation:** Use Lagrangian when more than two coupled degrees of freedom or holonomic constraints exist. Use direct Newtonian force balance for single-body problems with clear free-body diagrams.
- **Gate B, linearity:** Linearize only if displacements or fields are small relative to the scale that matters, and state the criterion (e.g., amplitude ratio below a stated threshold). If not justified, solve nonlinearly or bound the error.
- **Gate C, dispersion:** If phase and group velocities differ, report both and specify which governs energy or signal transport.
- **Gate D, numerical method:** Use analytic solution first. Adopt a numerical solver only when the analytic form is intractable, and record discretization, tolerance, and convergence evidence.
- **Gate E, external impact:** Stop and request explicit approval before any result is used for safety-critical design, regulatory filing, publication with third-party data, or overwriting shared simulation or lab files.

### Verification and evidence

- Dimensional analysis of every final expression. Reject any result failing it.
- Conservation checks: energy, momentum, angular momentum, or charge where applicable, with the source of each conserved quantity named.
- Limit recovery: at least two independent limits matching known results.
- Numerical cross-check: agreement within a stated tolerance (for example, relative error below 1% for smooth solutions) and a grid or timestep refinement showing convergence.
- For solver code, record library name and version, and verify all function signatures and option names against current official documentation before use. Do not rely on remembered APIs.
- Report any benchmark or literature value only with its citation; never fabricate reference numbers.

### Failure handling

- If dimensions fail, locate the first inconsistent term and re-derive from that step.
- If a numerical result diverges from analytic limits, reduce timestep or grid spacing, then check boundary implementation before revising physics.
- If conservation is violated beyond tolerance, suspect integrator choice or sign errors in forcing terms.
- If conditions are ambiguous, return a conditional answer with each branch labeled rather than choosing silently.

### Deliverable contract

Every deliverable contains:

1. Problem statement and assumptions table.
2. Derivation with numbered equations.
3. Final result with units and validity range.
4. Verification record: dimensional check, limits checked, numerical tolerance achieved.
5. Open items and neglected effects.
6. Approval status line: "Analysis only; not approved for design or external use" unless a named reviewer has approved.

Do not present unverified results as final. Do not omit validity ranges. Do not claim compliance with any standard or code unless the user supplies the standard text and asks for a check against it.


## cosmic-dark-sector

**Use when:** Use when analyzing, modeling, or reviewing work on dark matter and dark energy, including cosmological parameter inference, galaxy rotation and lensing evidence, large-scale structure constraints, and comparison of dark sector models against observational data.

### Purpose and boundaries

This skill guides professional analysis of the dark sector: dark matter (gravitational effects attributed to non-luminous mass) and dark energy (the component driving cosmic acceleration, often parameterized as a cosmological constant or an equation of state w). It covers:

- Evaluating observational evidence (rotation curves, weak and strong lensing, cosmic microwave background, baryon acoustic oscillations, supernova distance measurements, cluster dynamics, large-scale structure).
- Setting up, checking, and interpreting parameter inference and model comparison.
- Reviewing papers, pipelines, or proposals for statistical and physical soundness.

It does not cover: particle-physics detection experiment operations, instrument hardware design, or claims of new discoveries intended for public release. Those require the relevant collaboration's internal review.

### Inputs and assumptions

Before analysis, establish and record:

1. **Question type**: evidence assessment, model fit, pipeline review, or literature synthesis.
2. **Data products**: survey name, data release, sample definition, footprint, redshift range, systematics budget.
3. **Model space**: ΛCDM baseline, extensions (w0wa, modified gravity, interacting dark sector, warm or self-interacting dark matter), and stated priors.
4. **Fiducial assumptions**: flat versus curved geometry, neutrino mass treatment, radiation content, baryon treatment.
5. **Software and versions**: record exact versions; treat any version-specific behavior as requiring verification against current official documentation.

If any of these are missing, state the gap and limit conclusions accordingly. Do not assume a survey's systematics model or a code's default settings.

### Operating workflow

1. **Define the claim.** Write it as one falsifiable sentence, e.g., "Dynamical evolution of dark energy with w0 > -1 and wa < 0 is preferred over ΛCDM at >3σ by combined datasets X and Y."
2. **Map the evidence chain.** List each dataset, the physical quantity it constrains, and its dominant systematics.
3. **Check internal consistency.** Verify units (km/s/Mpc, h-scaling, Mpc versus Mpc/h), distance conventions, and redshift frames (heliocentric versus CMB).
4. **Reproduce a baseline.** Recover a published ΛCDM result from the same data before evaluating extensions. Accept reproduction only within the stated uncertainties.
5. **Test sensitivity.** Vary priors, scale cuts, and nuisance treatment one at a time; record shifts in key parameters (H0, Ωm, σ8, w).
6. **Assess tension.** Compute the difference between datasets using a stated metric (Gaussian parameter-difference, Monte Carlo suite-based, or Bayesian evidence ratio) and report the method.
7. **Write conclusions** only at the confidence the tests support.

### Decision gates

- **Gate A (data adequacy):** Proceed only if systematics budgets are published or can be derived. If not, restrict output to qualitative assessment.
- **Gate B (baseline reproduction):** Proceed to extensions only if the baseline reproduces within 1σ of the published value on the same data.
- **Gate C (model comparison):** Report Bayes factors or information criteria only when priors are documented and sensitivity tests are complete. A preference from a single prior choice is not a result.
- **Gate D (strong claims):** Claims of a >5σ departure from ΛCDM, or of a new dark-sector particle or interaction, require independent replication plus explicit external review before any statement beyond internal notes.

### Verification and evidence

Quality checks, each measurable:

- Baseline reproduction within 1σ of the published central value.
- Parameter chains: Gelman-Rubin or equivalent convergence statistic below the threshold stated in the sampler documentation (verify current recommended value); effective sample size reported for each key parameter.
- Prior sensitivity: key posterior mean shifts below 0.5σ under reasonable alternative priors, or the shift is reported as a limitation.
- Goodness of fit: chi-squared or equivalent reported with degrees of freedom and p-value.
- Example check: for a rotation-curve fit, residuals should show no systematic trend beyond the stated velocity error; a flat residual pattern with a single offset indicates a normalization issue, not a dark-matter halo signal.
- Example check: for a lensing claim, confirm the source-redshift distribution and photometric-redshift calibration are included in the error budget.

Cite every numeric value to its source table or equation. Never state a benchmark or constraint from memory without marking it for verification.

### Failure handling

- **Baseline fails to reproduce:** stop; diagnose units, priors, and data version before continuing. Do not adjust parameters to force agreement.
- **Chains do not converge:** extend run length once; if still unconverged, report results as provisional and do not compare models.
- **Results depend strongly on one nuisance choice:** report the dependence explicitly as a systematic, not as a finding.
- **Conflicting datasets:** report the tension with its metric; do not average datasets to hide it.
- **Missing or ambiguous documentation:** state the ambiguity and the interpretation chosen; flag for author clarification.

### Deliverable contract

Every output contains:

1. Claim statement and question type.
2. Data and model inventory with versions and sources.
3. Gate results (A–D) with pass, fail, or not applicable, and reasons.
4. Quantitative results with uncertainties, methods, and priors.
5. Sensitivity and tension tables.
6. Limitations, including unverified version-sensitive details.
7. Recommendation: accept, revise, or defer, with the specific missing evidence.

### What not to do

- Do not present a dark-sector model as established from a single dataset or a single prior.
- Do not tune nuisance parameters or cuts to remove a tension.
- Do not invent survey numbers, code flags, or package versions; mark them for verification.
- Do not release unreviewed discovery claims, including in summaries for non-specialists.
- Do not run or modify shared collaboration data products, catalogs, or public archives without explicit approval.
- Do not transmit unpublished datasets or internal results externally without explicit approval.


## earth-fluid-climate-systems

**Use when:** Use when analyzing, modeling, or reviewing atmospheric or oceanic fluid dynamics and climate-system data, including reanalysis or observation processing, budget closure checks, regional climate diagnostics, and interpreting model-versus-observation discrepancies in Earth and Space Sciences work.

### Purpose and boundaries

This skill guides professional analysis of the atmosphere and ocean as geophysical fluids: circulation, thermodynamics, energy and moisture budgets, and their statistical characterization over time and space. It covers:

- Diagnosing gridded fields (reanalysis, satellite retrievals, reference model output, in-situ networks).
- Computing and checking conservation budgets (mass, energy, moisture, momentum where relevant).
- Assessing model skill and model-observation mismatch for climate variables.
- Producing reproducible, caveated technical summaries.

It does not cover: operational forecast issuance, legal or insurance attribution claims, policy recommendations, or engineering certification. Causal attribution claims require a stated method and uncertainty range; do not present single-run or single-event results as definitive attribution.

### Inputs and assumptions

Before analysis, record:

1. Dataset identity: product name, version, release date, spatial grid, temporal resolution, vertical coordinate (pressure, height, sigma, depth, isopycnal).
2. Variable definitions: units, sign conventions, averaging type (instantaneous, daily mean, monthly mean), and whether fields are on native or regridded grids.
3. Time base: calendar (including leap-year handling), time zone or UTC convention, and any known discontinuities from observing-system changes.
4. Reference state: climatology period and method used for anomalies.
5. Assumptions: hydrostatic balance, Boussinesq approximation (ocean), negligible horizontal divergence at specified scales, or other simplifications. State each one and where it breaks down.

If any item is unknown, mark it as unknown and propagate that uncertainty into conclusions. Do not infer units silently; verify against product documentation.

### Operating workflow

1. **Scope the question.** Write one sentence stating the physical quantity, region, period, and decision it supports.
2. **Audit the data.** Check coordinate monotonicity, missing-value encoding, grid-cell area weighting, leap-day handling, and duplicated time steps. Count missing fraction per variable and per region.
3. **Harmonize.** Regrid only when necessary; prefer conservative remapping for flux-like quantities and bilinear or nearest methods for state variables. Record the method.
4. **Compute diagnostics** with explicit formulas. Use area-weighted means (cosine-of-latitude weighting for regional averages). Use mass-weighted vertical integrals for column quantities.
5. **Check budgets.** Compare the residual of the closed budget (for example, column energy tendency versus net flux convergence plus sources) against the stated tolerance. Report the residual, not only the result.
6. **Quantify uncertainty.** Use ensemble spread, dataset intercomparison, or bootstrap resampling with autocorrelation-aware block lengths. Do not treat autocorrelated daily samples as independent.
7. **Interpret physically.** Connect each result to a mechanism (e.g., thermal wind balance, Ekman transport, moisture convergence) and state what alternative mechanism would produce the same signal.
8. **Write the deliverable** per the contract below.

### Decision gates

- **Gate A (data fitness):** Proceed only if missing data is under 10% in the analysis domain and period, or if gaps are documented and handled by a stated method. Otherwise, narrow the domain or period.
- **Gate B (budget closure):** Residual must be below 10% of the largest individual term, or a stated physical reason must explain the excess (e.g., unresolved subgrid process, known reanalysis increment). If unexplained, stop and report the inconsistency before drawing conclusions.
- **Gate C (model-observation comparison):** Compare only on a common grid, common period, and common sampling (e.g., model output sampled at observation times where relevant). Mismatched sampling invalidates bias estimates.
- **Gate D (attribution or trend claims):** Require at least two independent datasets or an explicit statistical test with stated significance and method. Otherwise, label the result as exploratory.
- **Gate E (external use):** Any output intended for publication, public release, policy, or client decisions requires explicit human review and approval before release. Do not distribute results externally on your own authority.

### Verification and evidence

- Reproduce one known statistic from the dataset documentation or a published reference value before trusting a pipeline. Record the match tolerance.
- Test sign conventions with a synthetic field of known structure (e.g., uniform eastward wind yields positive zonal wind).
- Check that global-mean energy and moisture budgets are plausible in magnitude relative to published reference ranges; cite the reference used.
- Verify unit conversions by dimensional analysis in each equation.
- Confirm that area-weighted and unweighted results differ in the expected direction for high-latitude-dominated fields.
- Record software environment, library versions, and random seeds. Mark any version-specific behavior as requiring verification against current official documentation.

### Failure handling

- **Unit or sign mismatch:** Stop, trace the variable's metadata, and correct before recomputing. Report the original error and affected outputs.
- **Budget residual exceeds tolerance:** Decompose the residual by term and by region or level to locate the source. Do not adjust a term to force closure.
- **Dataset disagreement larger than stated uncertainty:** Report the spread and the candidate causes (observing-system change, retrieval algorithm, grid artifacts). Do not average away the disagreement.
- **Missing or corrupted files:** Report the exact files and time ranges affected; never fill gaps silently with climatology unless labeled as imputation with its uncertainty.
- **Ambiguous physical interpretation:** State two competing explanations and the observation that would distinguish them.

### Deliverable contract

Every output must include:

1. **Question and scope:** physical quantity, region, period, decision context.
2. **Data provenance table:** dataset, version, grid, period, missing fraction, known caveats.
3. **Method summary:** formulas, weighting, regridding, tolerances, assumptions.
4. **Results:** values with units and uncertainty ranges; budget residuals reported explicitly.
5. **Gate status:** pass, conditional, or fail for each applicable gate A through E.
6. **Limitations:** unresolved assumptions and out-of-scope conclusions.
7. **Reproduction record:** code location or procedure, environment, seeds, and the verification checks performed.

### What not to do

- Do not present model output as observations or vice versa.
- Do not compute anomalies against a reference period you have not stated.
- Do not use unweighted grid-cell averages for regional means on lat-lon grids.
- Do not treat a single season, year, or model run as a climate trend.
- Do not invent dataset versions, variable names, or citation details; if unknown, mark them unknown.
- Do not state exact software function names, command flags, or package versions from memory; verify against current official documentation.
- Do not overwrite or delete source data, raw archives, or prior results without explicit approval.
- Do not transmit, publish, or share outputs externally without explicit approval.


## matter-thermal-plasma

**Use when:** Use when analyzing, estimating, or verifying properties of thermal (near local thermodynamic equilibrium) plasmas, such as ionization equilibrium, Debye shielding, LTE validity, collisionality, and equilibrium composition for arc, torch, or high-temperature gas problems.

### Purpose and boundaries

This skill supports quantitative analysis of thermal plasmas: partially or fully ionized gases whose electrons, ions, and heavy particles share a common temperature (or near-equal temperatures) and whose composition is governed mainly by collisional equilibrium. Typical cases include atmospheric-pressure arcs, plasma torches, equilibrium composition calculations, and screening estimates for laboratory or process plasmas.

In scope: Saha ionization balance, Debye length and plasma parameter, LTE validity checks, collision and equilibration time scales, order-of-magnitude transport estimates, and dimensional checks on published formulas.

Out of scope: non-equilibrium kinetic modeling (use a kinetic or collisional-radiative model), plasma-wall sheath design for hardware, radiation-safety or operational safety of high-voltage or high-temperature equipment, and any claim of experimental validation without measured data.

### Inputs and assumptions

Before calculating, record:

- Gas species and molecular or atomic data, including ionization energies χ and statistical weights g for each ionization stage.
- Temperature T (state whether it is electron, heavy-particle, or a common value) in K or eV. Use 1 eV ≈ 11604 K as a conversion, and verify this constant.
- Pressure or total number density, and whether the plasma is at atmospheric pressure, reduced pressure, or unspecified.
- Spatial scale L and the characteristic time scale of interest.
- Whether the system is steady, time-varying, or spatially inhomogeneous.

If any of these is missing, state the assumed value explicitly and show how the result changes across a plausible range. Do not silently assume a pressure or composition.

### Operating workflow

1. Normalize all units to SI, then convert to eV or K only at the final evaluation. Write every formula with symbols before substituting numbers.
2. Compute the ionization balance. Use the Saha relation for each adjacent stage pair: n_{i+1} n_e / n_i = (2 g_{i+1} / g_i) (2π m_e k_B T / h²)^{3/2} exp(−χ_i / k_B T). Solve jointly with charge neutrality and total particle density conservation.
3. Compute the Debye length λ_D = sqrt(ε₀ k_B T_e / (n_e e²)) and the plasma parameter N_D = (4π/3) n_e λ_D³. Confirm N_D ≫ 1 for a collective plasma.
4. Evaluate LTE validity using the McWhirter-type criterion: n_e ≥ 1.6 × 10¹² T^{1/2} (ΔE)³ (cm⁻³, T in K, ΔE in eV, largest relevant level spacing). Treat this as a necessary condition, not a sufficient one, and check spatial and temporal gradients separately.
5. Estimate the electron–heavy-particle equilibration time and the collision frequency, then compare with the time and length scales of interest.
6. Record the result with uncertainty propagated from input ranges.

### Decision gates

- **Gate A (collectivity):** If N_D < 10, stop and report that the plasma is not clearly collective; do not apply Debye-based screening conclusions.
- **Gate B (LTE):** If the McWhirter criterion fails by less than a factor of 10, present results as bounds only. If it fails by more, switch to a non-equilibrium method and say so.
- **Gate C (two-temperature):** If electron and heavy-particle equilibration time exceeds the process time, do not use a single temperature in the Saha calculation without justification.
- **Gate D (data provenance):** Atomic data, partition functions, and constants must come from a cited, current source. Mark any value taken from memory as requiring verification.

### Verification and evidence

- Dimensional check: every term in each equation must reduce to the same unit. Report the check result.
- Limit checks: as T → high, ionization fraction must approach 1; as n → high at fixed T, ionization must decrease. Confirm the trend.
- Charge neutrality residual must be below 10⁻⁶ relative after solving.
- Compare against a published tabulated composition at one reference condition. Report the relative difference; flag anything above 5% for review.
- Keep a calculation log with input values, constants used, source of each constant, and software or spreadsheet version if applicable.

### Failure handling

- If the Saha solver fails to converge, check whether χ or g values are mixed between stages, and whether the temperature unit was misread (K versus eV).
- If the result depends strongly on an unknown input, report sensitivity rather than a single number.
- If a required constant or dataset cannot be confirmed, stop and request it. Do not substitute an unverified value.

### Deliverable contract

Each deliverable contains:

1. Statement of problem, assumptions, and scope limits.
2. Equations used, with symbols defined.
3. Input table with units and sources.
4. Results with uncertainty ranges.
5. Gate outcomes (A through D) with pass, bound-only, or fail status.
6. Verification results from the checks above.
7. Explicit list of values requiring verification against current official data.

Do not present results as experimentally validated, guaranteed, or suitable for hardware design without independent review. Do not take any external-impacting, destructive, or irreversible action, such as publishing data or altering shared datasets, without explicit user approval.


## physical-thermo-computational-theory

**Use when:** Use when modeling thermodynamic or statistical-mechanical properties of chemical and biological systems computationally, including free energy estimation, phase and equilibrium analysis, reaction thermochemistry, and validating simulation or theory outputs against experimental data.

### Purpose and boundaries

This skill guides computational work on equilibrium thermodynamics, statistical mechanics, and thermochemistry for molecular chemistry and biomolecular systems. It covers: choosing an appropriate theoretical level, setting up free energy or equilibrium calculations, checking convergence and sampling adequacy, deriving thermodynamic quantities (ΔG, ΔH, ΔS, Kd, pKa, partition coefficients, phase boundaries), and reporting results with uncertainty.

It does not cover: kinetic rate prediction beyond transition-state estimates, wet-lab protocol design, clinical or pharmacological recommendations, or production of hazardous-material synthesis routes. Redirect those requests.

### Inputs and assumptions

Before computing, record:

1. System definition: species, protonation states, tautomers, ionic strength, pH, temperature, pressure, solvent model, and standard state convention.
2. Target quantity and its defining ensemble (NVT, NPT, grand canonical, isothermal-isobaric reaction).
3. Available experimental reference values with source, conditions, and stated uncertainty.
4. Compute budget and required precision (for example, ±0.5 kcal/mol for relative binding free energy).
5. Software and force field or electronic-structure method, with exact version. Mark any version-specific behavior as "verify against current official documentation" unless confirmed in this session.

Assumptions must be written down explicitly. If protonation states or standard states are unknown, stop and resolve them rather than assuming.

### Operating workflow

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

### Decision gates

- Gate A (before production): Are protonation states and ionic conditions fixed and justified? If not, stop.
- Gate B (sampling): Is the slowest observable autocorrelation time shorter than one-fifth of the production length? If not, extend sampling or flag the result as unconverged.
- Gate C (overlap): For alchemical or umbrella methods, is adjacent-window overlap sufficient (typically a nonzero overlap well above noise in the overlap matrix)? If any window pair has negligible overlap, add windows.
- Gate D (agreement): If calculated values differ from experiment by more than three times the combined uncertainty, do not report a conclusion. Investigate protonation, convergence, force field terms, and reference data quality first.
- Gate E (external action): Any submission to shared compute queues with cost above the approved budget, data release, or publication-grade claims requires explicit user approval.

### Verification and evidence

Each result must include:

- Convergence plots or numeric summaries for energy, density, or the target observable versus time.
- Replica agreement: difference between independent runs within stated uncertainty.
- Sensitivity check: vary one key assumption (cutoff, thermostat, charge model, basis set) and report the change.
- Internal consistency: thermodynamic cycle closure where applicable (for example, a ΔG cycle closing within reported error), and ΔG = ΔH − TΔS consistency if components are reported.
- Units and standard states stated explicitly; check that concentration-dependent values are corrected to the declared standard state (for example, 1 M versus 1 atm).

Quality threshold: a result is "reportable" only when convergence, replica agreement, and at least one sensitivity check pass. Otherwise it is "exploratory" and labeled as such.

### Failure handling

- Non-convergent sampling: extend runs, increase replicas, or enhance sampling; do not average unconverged blocks.
- Poor window overlap or hysteresis between forward and reverse transformations: add intermediate states, increase per-window time, or switch estimator. Report the hysteresis magnitude.
- Unphysical energies (large negative values from clashes, failed minimization): re-minimize and re-equilibrate; check topology and atom typing before rerunning.
- SCF or electronic-structure non-convergence: change initial guess, damping, or convergence algorithm; do not silence convergence warnings.
- Missing experimental reference: report computed values with uncertainty only, and state that no validation was performed.

### Deliverable contract

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


## planetary-exoplanet-science

**Use when:** Use when analyzing, validating, or reporting on exoplanet detections, candidate vetting, transit or radial-velocity characterization, atmospheric retrieval interpretation, or population statistics for planets orbiting other stars.

### Purpose and boundaries

This skill guides rigorous work on planets outside the Solar System: detection analysis, candidate vetting, bulk property estimation, atmospheric interpretation, and population-level inference. It covers reasoning about data products and published results, and producing defensible summaries or analysis plans.

Out of scope: solar system planetary science, stellar evolution modeling beyond what planet inference requires, instrument hardware design, and any claim of a confirmed biosignature. Biosignature questions are treated as unresolved unless independent, peer-reviewed evidence exists, and are flagged for expert review.

### Inputs and assumptions

Collect before analysis:
- Target identifiers, host-star parameters (Teff, log g, metallicity, radius, mass, distance), and their sources and uncertainties.
- Data type: photometry (cadence, aperture, detrending method), radial velocities (instrument, reduction pipeline, activity indicators), imaging, or spectra (resolution, wavelength range, transmission or emission).
- Existing dispositions (confirmed, candidate, false positive) and the archive snapshot date.
- Units and reference frames. Assume nothing about units; confirm them.

Assumptions must be stated explicitly. Stellar parameters from older catalogs are frequently revised; treat any value without uncertainty as provisional.

### Operating workflow

1. **Freeze the data version.** Record archive name, table, retrieval date, and pipeline or data release identifier. Verify current release details against official mission or archive documentation, since these change.
2. **Re-derive host-star parameters** or confirm their provenance. Radius errors propagate directly into planet radius (Rp = Rs × sqrt(depth)).
3. **Check transit geometry.** Compare duration against the expected duration for the stellar density and period. Large mismatches suggest eccentricity, blending, or a wrong host.
4. **Vet for false positives** in this order: odd/even depth difference, secondary eclipse presence, centroid shift, ephemeris match to known binaries, and background eclipsing binary modeling.
5. **For radial velocities,** fit a Keplerian with and without a linear or quadratic trend, then compare activity indicators (log R'HK, bisector span, FWHM) against the signal's period. A signal tracking rotation or activity is not a planet.
6. **Derive bulk properties** (mass, density, equilibrium temperature) with propagated uncertainties via sampling, not linear error bars alone. Use the full posterior when available.
7. **For atmospheric spectra,** separate instrument systematics and stellar contamination (transit light source effect) before interpreting molecular features. Report retrieval priors and model grids.
8. **For populations,** state selection function, completeness, and detection bias before fitting occurrence rates.

### Decision gates

- **Gate A (candidate to planet):** Proceed only if at least two independent lines of evidence pass (photometric vetting, RV detection, or imaging) and no unresolved false-positive test remains.
- **Gate B (mass measurement):** Report a mass only from RV or TTV signals with semi-amplitude significance above roughly 4 sigma, or with a documented stability test. Otherwise report a minimum mass (M sin i).
- **Gate C (atmospheric claim):** Claim detection only at a stated significance after accounting for model-grid choice. Claim absence only with stated upper limits and injection-recovery tests.
- **Gate D (external release):** Any public statement, catalog submission, or result sent to collaborators requires explicit human approval.

### Verification and evidence

- Injection-recovery: inject a synthetic transit or RV signal at the reported period and amplitude; recovery rate must be reported.
- Residual checks: no remaining periodicity above the noise in the residual periodogram at the claimed period.
- Consistency: derived density and equilibrium temperature must fall within physically allowed bounds for stated composition classes.
- Every quantitative claim carries units, uncertainty, method, and source.

### Failure handling

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

### Deliverable contract

Each deliverable contains:
1. Data provenance table (source, version, retrieval date).
2. Host-star parameters with uncertainties.
3. Evidence summary by gate, with pass/fail and reasoning.
4. Derived planetary properties with uncertainties and method.
5. Verification results (injection-recovery, residuals).
6. Limitations and open questions.
7. Approval status for any external-facing use.


## quantum-photonic-computing

**Use when:** Use when designing, evaluating, or reviewing photonic quantum computing approaches (boson sampling, linear optical quantum computing, photonic qubit architectures, integrated photonic circuits for quantum information), including feasibility analysis, loss budgets, resource estimates, and claims validation.

### Purpose and boundaries

Use this skill to analyze photonic quantum computing work at the level of physical architecture, component performance, resource scaling, and evidence quality. It covers:

- Photonic qubit encodings (polarization, time-bin, dual-rail, path, continuous-variable squeezed/cat states).
- Linear optical networks, boson sampling, and measurement-based or fusion-based photonic architectures.
- Integrated photonics platforms (waveguides, phase shifters, beam splitters, single-photon sources and detectors, multiplexing).
- Loss, indistinguishability, and detection-efficiency budgets; error-correction overhead for photonic loss.
- Vetting vendor, paper, or internal claims about advantage, fidelity, or throughput.

It does not cover: general quantum algorithm design unrelated to photonic hardware, cryptographic deployment decisions, export-control classification, or procurement advice. Refer those to appropriate specialists.

### Inputs and assumptions

Collect before analysis:

1. Target task: sampling, computation, communication, or sensing; the logical or physical operation count.
2. Encoding and architecture: qubit encoding, source type (SPDC, quantum dot, multiplexed heralded), network topology, detector type.
3. Component figures with conditions: source brightness and g2(0), detector efficiency and dark count rate, propagation and coupling loss (dB/cm or dB per facet), phase-shifter insertion loss and drift, two-photon interference visibility (HOM dip).
4. Claimed results with their measurement definitions: fidelity definition, post-selection rates, sample sizes, confidence intervals.
5. Stated assumptions about classical simulability and the comparison baseline.

If any input is missing, state the assumption explicitly and label conclusions as conditional on it. Do not fill gaps with typical literature values presented as facts.

### Operating workflow

1. **Define the object.** Write one sentence: what is being built, for what task, and what counts as success.
2. **Build the loss budget.** Multiply transmission across every element in the optical path: source-to-circuit coupling, circuit insertion loss, phase shifters, switches, fiber links, detector efficiency. Express total end-to-end efficiency η as a single number and as dB.
3. **Compute photon-rate and multi-photon yield.** For N-photon events, yield scales roughly as η^N times source emission probability^N; show the scaling explicitly and identify the dominant term.
4. **Assess indistinguishability.** Convert HOM visibility V into an effective mode-overlap penalty for multi-photon interference; note that small reductions compound with photon number.
5. **Assess noise sources.** Dark counts, multi-pair emission (g2), timing jitter, and temporal mode mismatch; estimate their contribution to error rate in the target observable.
6. **Evaluate error correction overhead** if fault tolerance is claimed: identify the photon-loss threshold assumed by the scheme, the loss budget against it, and the resource multiplier (multiplexing factor, fusion success probability, ancilla count). Provide these as parameter-dependent ranges, not single values.
7. **Check classical baselines.** State the best known classical method for the task and whether the claimed regime is tested against it, including its cost.
8. **Document conclusions** with explicit conditions and open questions.

### Decision gates

Proceed to design or investment review only if all hold:

- End-to-end efficiency is computed from measured or specified component values, not nominal datasheet figures alone.
- Multi-photon yield at the target photon number is nonzero and its scaling is stated.
- Claimed fidelity or advantage has a stated definition, sample size, and uncertainty.
- The classical baseline is named and was considered.

Halt and escalate if:

- A fault-tolerance claim lacks an explicit loss threshold and overhead model.
- Results rely on post-selection without reporting the post-selection rate and its effect on the claimed statistic.
- Comparison is made against a weakened classical baseline or an unstated one.

### Verification and evidence

Quality checks, each with a pass criterion:

- Loss budget sums to the stated η within 1 dB when recomputed from listed components.
- Yield table covers at least three photon numbers, with the scaling exponent reported.
- HOM visibility, g2(0), and detector efficiency are reported with measurement conditions (wavelength, temporal bin width, pump power).
- Sample size yields a confidence interval narrower than the claimed margin; otherwise the claim is unsupported.
- Every cited value has a source identifier (publication, datasheet revision, or internal test record) and date.

Mark any component figure, software interface, toolkit version, or standard as "verify against current official documentation" when it depends on a version or vendor release. Do not assert benchmark numbers from memory.

### Failure handling

- **Missing component data:** produce a bounded estimate with explicit low/high assumptions and list the measurement that would close the gap.
- **Inconsistent figures** (e.g., claimed rate exceeds source brightness times efficiency): flag the contradiction, identify the most likely faulty input, and request clarification. Do not average conflicting numbers.
- **Unverifiable advantage claims:** report what is verified, what is not, and what experiment would discriminate.
- **Out-of-scope request** (device fabrication instructions for restricted technology, procurement, export matters): decline the specific part and state the boundary.

### Deliverable contract

Return a report with these sections, in order:

1. Summary (three sentences maximum, including the main conditional conclusion).
2. Assumptions table (parameter, value, source, confidence).
3. Loss budget and yield table with computed η and scaling exponent.
4. Noise and indistinguishability assessment.
5. Baseline comparison.
6. Gate status (pass, halt, or escalate, per gate).
7. Open questions and required measurements.
8. Version-sensitive items flagged for verification.

Approval required before: committing procurement or experimental resources, sharing results externally, publishing performance claims, or taking any action that alters shared lab or production systems.

Do not: present estimates as measured results; omit the loss budget from advantage claims; accept fault-tolerance claims without an overhead model; or cite specific figures from memory without a verifiable source.


## quantum-subatomic

**Use when:** Use when working on quantum mechanics or quantum field theory calculations for subatomic systems, including particle decays, scattering amplitudes, nuclear states, angular momentum coupling, symmetry and group-theory reductions, and unit or convention checks.

### Purpose and boundaries

This skill supports rigorous analytical and numerical work on subatomic quantum systems: hadron and lepton decays, two-body and multi-body kinematics, scattering amplitudes at tree level, nuclear shell and angular momentum structure, isospin and flavor symmetry, and Clebsch-Gordan or Wigner coefficient bookkeeping.

It does not cover: experimental data acquisition, detector design, weapons-relevant nuclear engineering, handling of controlled radioactive material, or claims about real-world hazards. Decline and redirect those requests.

### Inputs and assumptions

Before calculating, record:

1. The system: particles or nucleons, their quantum numbers (spin, parity, charge, isospin, flavor, color if relevant).
2. The process and the observable requested (amplitude, width, cross section, branching ratio, spectrum, expectation value).
3. The unit system and metric signature. Default to natural units (ħ = c = 1) only if stated; otherwise carry SI or explicit factors.
4. The approximation level: tree level, leading order, nonrelativistic, perturbative order, or exact diagonalization.
5. Reference constants (masses, lifetimes, couplings). Mark each as sourced from the current Particle Data Group compilation or a named paper with its edition. Constants change between editions; verify against the current official release before reporting numbers.

If any input is missing and affects the result, stop and ask. Do not fill gaps with remembered values.

### Operating workflow

1. Restate the problem in one line with the quantum numbers and conserved quantities checked. Confirm charge, baryon number, lepton number, strangeness or flavor, and angular momentum conservation for each vertex.
2. Choose the formalism: Feynman rules, partial-wave expansion, Hamiltonian matrix, or group-theory reduction. State why.
3. Write the symbolic result before substituting numbers.
4. Track dimensions at every step. Check that the final quantity has the correct units.
5. Reduce angular structure using Wigner or Clebsch-Gordan coefficients. Verify coefficients against a standard table or a computed orthogonality check.
6. Evaluate numerically with stated constants and significant figures matched to input precision.
7. Run the verification checks below, then report.

### Decision gates

- **Gate A (conservation):** If any conservation law is violated at a vertex, stop. Either the process is forbidden or the particle assignment is wrong.
- **Gate B (approximation validity):** Proceed with a perturbative or nonrelativistic expansion only if the small parameter is quantified (for example, coupling constant or v/c). Report the estimate of the neglected term.
- **Gate C (convention):** If the source uses a different sign convention, metric, or normalization for amplitudes or states, convert explicitly before comparing results.
- **Gate D (numerical stiffness):** For matrix diagonalization with near-degenerate levels, require convergence in basis size and report the change.

### Verification and evidence

Each deliverable must include at least three of the following checks, with results shown:

- Dimensional analysis of the final expression.
- Limiting case: recover a known result (for example, a nonrelativistic or massless limit) within stated accuracy.
- Sum rule or unitarity check, such as branching ratios summing to unity within the quoted uncertainty.
- Symmetry check: swap identical particles, apply a parity or charge conjugation transformation, confirm sign behavior.
- Independent recalculation by a second method (different gauge, different basis, or numerical versus analytic).
- Coefficient orthogonality or normalization check.

Quote uncertainties propagated from input constants. Never report more significant figures than the inputs support.

### Failure handling

- If a check fails, locate the first step where the failing quantity departs from expectation; do not adjust constants to force agreement.
- If a required constant or coefficient cannot be verified, label the result conditional and name the missing value.
- If two methods disagree beyond uncertainty, report both and the discrepancy; do not average them silently.
- Version-sensitive details (current PDG values, software library functions, numerical package interfaces) must be marked for verification against current official documentation before use.

### Deliverable contract

Return:

1. Problem statement with quantum numbers and conventions.
2. Symbolic result.
3. Numerical result with units, uncertainties, and significant figures.
4. Verification table listing each check, method, and outcome.
5. Assumptions and open items, including any version-sensitive constants to re-verify.

Do not:

- Invent constants, coefficients, or benchmark numbers.
- Present a tree-level result as exact without stating the truncation.
- Omit sign or phase conventions.
- Claim a result has been validated against experiment unless the comparison data and source are cited.


## solid-earth-systems

**Use when:** Use when analyzing, modeling, or interpreting solid Earth processes (seismology, geodesy, geodynamics, rock mechanics, tectonics, geophysical imaging, volcanology, geohazard assessment) and producing quantitative results, data products, or interpretive reports that must be traceable and defensible.

### Purpose and boundaries

This skill guides quantitative work on the solid Earth: earthquake catalogs and waveforms, GNSS/InSAR deformation, gravity and magnetic anomalies, seismic and electrical imaging, stress and rock-mechanics estimates, and geohazard screening (landslide, subsidence, induced seismicity, volcanic unrest).

In scope: data QC, processing-chain design, parameter selection, uncertainty budgets, model fitting, interpretation with stated alternatives, and reporting.

Out of scope: operational emergency alerts or public warnings (these require the responsible agency), engineering safety certification of dams, mines, or structures, hydrocarbon or mineral-exploration targeting decisions, and any claim of deterministic earthquake or eruption prediction.

### Inputs and assumptions

Before computing, record:

1. Data provenance: instrument or network, processing center, product version, retrieval date, and license terms.
2. Reference frame, coordinate system, datum, and time standard (UTC vs. local; GPS vs. UTC leap-second handling).
3. Units and sign conventions (e.g., displacement positive east/north/up; magnitude scale type such as Mw, ML, mb).
4. Spatial and temporal extent, sampling rate, and known gaps.
5. Velocity model, Earth model, or rheology assumed by any upstream product.
6. Stated question: what decision or conclusion the result must support.

If any of items 1–3 are unknown, stop and flag them; do not assume a convention silently.

### Operating workflow

1. **Define the question** in one sentence, with a measurable output (e.g., "estimate interseismic slip-deficit rate on segment X with 1σ uncertainty").
2. **Audit the data.** Check time monotonicity, duplicate events, station outages, outliers (median absolute deviation > 5 is a starting flag, not a rule), and metadata consistency.
3. **Document the processing chain.** List every filter, detrending, correction (tidal, atmospheric, seasonal, orbital), and reference choice. Keep raw and processed versions separate.
4. **Run the baseline method** before any advanced one. Example: fit a secular velocity plus annual and semi-annual terms to GNSS time series before interpreting transients.
5. **Quantify uncertainty** with at least two sources: formal (least-squares covariance) and empirical (residual scatter, bootstrap, or alternative-parameter sensitivity).
6. **Test alternatives.** Vary one major assumption at a time (e.g., 1-D vs. 3-D velocity model, cutoff frequency, prior on smoothing) and report the spread.
7. **Interpret with limits.** State what the data constrain and what they cannot, including non-uniqueness and resolution.
8. **Package the outputs** per the deliverable contract.

### Decision gates

- **Gate A (data sufficiency):** Proceed only if coverage is at least 80% of the target window and no single station or sensor dominates the estimate. Otherwise reduce scope or report as provisional.
- **Gate B (model choice):** Use a more complex model only if it reduces misfit beyond expected noise (reduced chi-square moving toward 1, or a information criterion improvement with physical justification) and remains stable under resampling.
- **Gate C (extrapolation):** Do not extrapolate beyond the sampled magnitude range, depth range, or time window without explicit labeling and a separate uncertainty term.
- **Gate D (causal claims):** Correlation in space or time is not causation. Require at least one independent line of evidence (geological, geodetic, seismic, or hydrological) before stating a causal mechanism.
- **Gate E (external impact):** Stop and request explicit approval before publishing hazard levels, contacting authorities, releasing data under embargo, or altering shared catalogs or production pipelines.

### Verification and evidence

Each result must carry:

- Residual RMS compared with stated measurement noise, and a residual plot or table.
- Checkerboard or restoration test for tomographic or slip inversions where resolution is claimed.
- Magnitude of completeness and completeness method for seismicity rate work; Gutenberg–Richter b-value with its standard error.
- Explicit comparison against at least one independent dataset or published reference result, with the reference cited by its own identifier.
- A reproducibility record: input file hashes, software name and version, configuration, and random seeds.

Software versions and algorithm defaults change. Mark any command, library function, or parameter default as "verify against current official documentation" unless confirmed in the current release.

### Failure handling

- **Unphysical result** (negative stiffness, velocities exceeding plausible plate rates by an order of magnitude): trace back to units, sign, and reference frame before revising physics.
- **Non-convergence:** Report the last iterate, the stopping criterion, and the parameter at the boundary; do not present the boundary value as a solution.
- **Conflicting datasets:** Report both, quantify the discrepancy, and identify which assumption explains it. Do not average without justification.
- **Missing metadata:** Quarantine the affected data and flag the gap in the deliverable.

### Deliverable contract

Every deliverable includes:

1. Question and scope statement.
2. Data inventory with provenance, versions, and gaps.
3. Method summary with parameters and the reason for each choice.
4. Results with uncertainties, units, and reference frame stated next to each number.
5. Sensitivity table of alternatives tested.
6. Limitations and what would change the conclusion.
7. Reproducibility record.
8. Approval status for any action at Gate E.

Do not: present single-number results without uncertainty; mix reference frames or time standards without conversion; claim prediction skill without a retrospective test; omit negative or null findings; or transmit hazard-related conclusions outside the review chain without approval.


## stellar-compact-astrophysics

**Use when:** Use when analyzing, modeling, or reporting on white dwarfs, neutron stars, or stellar-mass black holes, including mass-radius inference, cooling or spin-down analysis, X-ray binary or gravitational-wave source classification, and pulsar timing interpretation.

### Purpose and boundaries

This skill supports quantitative work on stellar remnants: white dwarfs (WDs), neutron stars (NSs), and stellar-mass black holes (BHs). It covers observational data reduction checks, parameter inference, model comparison, source classification, and written findings.

In scope: mass and radius estimates, cooling and spin-down interpretation, binary mass functions, compact-object classification from multiwavelength or gravitational-wave data, and equation-of-state (EOS) constraint assessment.

Out of scope: supermassive black holes, stellar evolution from first principles without a remnant target, cosmological inference, and operational guidance for any hazardous physical process.

### Inputs and assumptions

Before analysis, record:

- Source identifier, coordinates, distance estimate and method (parallax with zero-point correction, dynamical, or distance-modulus).
- Photometry or spectra with bands, extinction law, and calibration references.
- Timing data (pulse TOAs, ephemeris, reference epoch, time standard) or orbital radial-velocity curves.
- Gravitational-wave strain or posterior samples, with detector network, waveform family, and prior specification.
- Units and constants used by each source. Convert to SI or solar units once, then state the convention.

Assumptions must be explicit: atmosphere model (H or He for WDs), EOS family, spin state, inclination prior, and whether the binary is circular.

### Operating workflow

1. **Define the question** as one measurable target, such as "posterior on NS radius at 1.4 Msun" or "is the secondary above the mass gap."
2. **Audit inputs.** Check distance units, parallax zero-point handling, extinction consistency across bands, and epoch alignment for timing solutions.
3. **Select the model** matched to the regime. For WD mass-radius, use cold degenerate or Hamada-Salpeter-type relations with stated atmospheric composition. For NS, use TOV-integrated EOS families. For BH, use mass functions and spin priors.
4. **Run a forward sanity check.** Predict an observable from a canonical case (e.g., 1.4 Msun NS, R ≈ 10–13 km for typical EOS families) and confirm the pipeline reproduces it.
5. **Infer parameters** with stated priors and convergence diagnostics.
6. **Stress-test** against alternative priors, distance estimates, and excluded data subsets.
7. **Write the finding** using the deliverable contract below.

### Decision gates

- **Gate A (data quality):** Proceed only if distance uncertainty is documented and timing residuals show no unmodeled structure above stated tolerance. Otherwise flag and quantify impact.
- **Gate B (classification):** Assign BH status only if the dynamical mass exceeds the maximum NS mass allowed by the EOS posterior, and report the EOS-dependence explicitly. Typical TOV-limited maxima are near 2–2.5 Msun, so treat any claim near this boundary as model-dependent.
- **Gate C (WD):** Chandrasekhar mass (~1.4 Msun) bounds non-rotating, non-accreting cold WDs. A WD mass above this requires a stated mechanism (rotation, magnetic support, accretion history) and a source for that mechanism.
- **Gate D (external action):** Stop before submitting results to catalogs, publishing, or overwriting shared datasets. Obtain explicit user approval.

### Verification and evidence

- Report posteriors as median with 16th–84th percentile intervals, plus the prior used. Never report a single value without uncertainty.
- Confirm units by recomputing one known quantity (e.g., Schwarzschild radius ≈ 2.95 km × M/Msun).
- For MCMC or nested sampling, report effective sample size and convergence statistic; flag any value that fails the tolerance stated in the software documentation.
- Show at least one sensitivity test changing the most influential assumption.
- Mark any software behavior, parameter name, or package version as "verify against current official documentation." Do not assert it from memory.

### Failure handling

- **Degenerate posterior** (prior-dominated): report it as unconstrained and state which prior drives the result.
- **Parallax unreliable** (low signal-to-noise or systematic concerns): switch to an alternative distance method or report the result as conditional on distance.
- **Conflicting measurements:** do not average silently. Present both, with the tension quantified.
- **Pipeline failure on the canonical check:** stop. Do not proceed to science targets until the cause is identified.

### Deliverable contract

Every output contains:

1. Question and classification of the source regime.
2. Inputs table: value, uncertainty, units, source.
3. Assumptions list, including EOS, atmosphere, and priors.
4. Results with credible intervals and sensitivity summary.
5. Limitations, including what would change the conclusion.
6. Items requiring verification against current documentation.

Do not state findings beyond what the data constrain. Do not present model-dependent BH or EOS claims as established facts.


## thermal-fluid-energy-systems

**Use when:** Use when sizing, analyzing, troubleshooting, or documenting thermal-fluid energy systems such as heat exchangers, pumps, piping networks, boilers, chillers, cooling loops, and heat recovery circuits, where hydraulic and thermal performance must be verified against design intent.

### Purpose and boundaries

This skill supports engineering analysis of closed and open thermal-fluid circuits: pumped liquid loops, steam and condensate systems, air-side and water-side heat exchange, boiler and chiller plant, and heat recovery arrangements. It covers steady-state energy balances, pressure-drop and pump-operating-point checks, heat-exchanger rating, control-loop behavior at the design level, and documentation of results.

Out of scope unless explicitly supplied with authority: pressure-vessel code stamping, boiler or pressure-equipment certification, life-safety sign-off, regulatory emissions compliance, and detailed CFD interpretation. Treat outputs as engineering support for a licensed professional who owns the decision.

### Inputs and assumptions

Before calculating, confirm and record:

1. Fluid identity and properties source (water/glycol concentration, steam tables, refrigerant, gas composition). Note the property correlation and its validity range.
2. Operating envelope: design, minimum, and maximum flow, inlet/outlet temperatures, pressures, ambient conditions.
3. Equipment data: pump curve and impeller trim, exchanger geometry and fouling factors, pipe material, nominal and internal diameter, roughness, fittings list, valve Cv or Kv at stated openings.
4. Control intent: setpoints, sequencing, and what the system is supposed to do on failure.
5. Units and sign convention. Convert everything to one consistent system before arithmetic and state it at the top of the work.

If any input is missing, mark the affected result as provisional and list the assumed value with its justification. Do not silently fill gaps with typical values.

### Operating workflow

1. **Define the question.** State whether the task is rating, sizing, verification, or fault diagnosis. Each has a different acceptance standard.
2. **Close the energy balance.** For each control volume, compare heat in, heat out, work input, and stored energy. Mismatches above roughly 2 to 3 percent of throughput indicate a missing term, a bad measurement, or a property error. Investigate before proceeding.
3. **Establish hydraulics.** Compute Reynolds number to confirm flow regime. Use Darcy-Weisbach with a friction factor from a documented correlation for pipe runs; use K-factors with stated sources for fittings. Sum losses and compare to pump head at the operating flow.
4. **Locate the operating point.** Intersect the system curve with the pump curve at the actual impeller diameter. Check NPSH available against NPSH required with margin, and confirm the point lies within the manufacturer's recommended range.
5. **Rate the heat exchanger.** Use effectiveness-NTU or LMTD with a correction factor for multipass or crossflow geometry. Include fouling resistances. Check the temperature cross and approach temperatures for physical feasibility.
6. **Check control behavior.** Verify valve authority (typically the controlled-element pressure drop should be a meaningful fraction of total loop drop at design flow), and identify whether the loop can reach setpoint across the full load range.
7. **Document assumptions and sensitivities.** Show how results shift with fouling, ambient temperature, and property uncertainty.

### Decision gates

- **Gate A, Data sufficiency:** Proceed only if fluid properties, pump curve, and exchanger geometry (or equivalent) are available. Otherwise, deliver a provisional result or request data.
- **Gate B, Balance closure:** Energy balance within tolerance. If not, do not issue operating-point or rating conclusions.
- **Gate C, NPSH and flow range:** Pump operating point must have NPSH margin and stay within the manufacturer's allowable range. Failing either requires a recommendation to change design, not a numerical workaround.
- **Gate D, Thermal feasibility:** Temperature cross violation in a counterflow or crossflow exchanger, or approach temperatures below physical limits, invalidates the rating.
- **Gate E, Authority:** Control valve authority below roughly 0.25 at design flow is a flag for review, not an automatic fail; document the consequence.
- **Gate F, Escalation:** Any action touching live plant, isolation procedures, pressure relief, boiler firing, or refrigerant handling requires explicit written approval from the responsible operator or engineer before recommendation is executed.

### Verification and evidence

Each conclusion must cite the calculation step, the input value with its source, and the check it passed. Quality checks:

- Energy balance closes within stated tolerance.
- Reynolds number and friction factor method stated for every pipe segment.
- Pump operating point is within the vendor's allowable range and NPSHa exceeds NPSHr by a stated margin.
- Exchanger effectiveness is between 0 and 1, and the heat duty from effectiveness matches the duty from the energy balance within a few percent.
- Recomputed values with a second method (for example LMTD versus effectiveness-NTU) agree within a stated tolerance.
- Sensitivity to fouling and ambient temperature is reported, not hidden.

Mark any version-sensitive data (property correlations, standard tables, software function behavior, vendor curve revisions) as requiring verification against current official documentation before use.

### Failure handling

- **Balance does not close:** Check units, sign convention, and missing streams first. Re-measure before adjusting property values.
- **Pump curve and system curve do not intersect in range:** Check impeller trim, static head, and valve position assumptions. Do not extrapolate the pump curve beyond published range.
- **Cavitation risk:** Recommend increasing suction head, reducing suction losses, or lowering fluid temperature; do not recommend simply raising margin on paper.
- **Exchanger underperforms:** Separate fouling, flow maldistribution, and bypass as hypotheses, and list the measurement that would distinguish each.
- **Conflicting data sources:** Report both values, identify which is more authoritative, and state the impact on the conclusion.

### Deliverable contract

Every deliverable includes:

1. Scope statement and unit system.
2. Input table with source and confidence for each value.
3. Calculation summary with equations named and results shown to justified significant figures.
4. Gate results (pass, fail, or provisional) with reasons.
5. Sensitivity summary and key uncertainties.
6. Recommendations ranked by risk, with any approval-required actions marked.
7. Verification notes flagging version-sensitive items.

### What not to do

- Do not issue pressure-rating, certification, or code-compliance statements.
- Do not execute or recommend valve changes, pump starts, isolation, or setpoint changes on live systems without explicit approval.
- Do not use assumed or unverified property values or unstated typical numbers.
- Do not extrapolate pump or exchanger performance beyond published ranges.
- Do not present a single number without its uncertainty or assumption set.

