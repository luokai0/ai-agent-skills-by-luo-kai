---
name: solid-earth-systems
description: Use when analyzing, modeling, or interpreting solid Earth processes (seismology, geodesy, geodynamics, rock mechanics, tectonics, geophysical imaging, volcanology, geohazard assessment) and producing quantitative results, data products, or interpretive reports that must be traceable and defensible.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Solid Earth Systems

## Purpose and boundaries

This skill guides quantitative work on the solid Earth: earthquake catalogs and waveforms, GNSS/InSAR deformation, gravity and magnetic anomalies, seismic and electrical imaging, stress and rock-mechanics estimates, and geohazard screening (landslide, subsidence, induced seismicity, volcanic unrest).

In scope: data QC, processing-chain design, parameter selection, uncertainty budgets, model fitting, interpretation with stated alternatives, and reporting.

Out of scope: operational emergency alerts or public warnings (these require the responsible agency), engineering safety certification of dams, mines, or structures, hydrocarbon or mineral-exploration targeting decisions, and any claim of deterministic earthquake or eruption prediction.

## Inputs and assumptions

Before computing, record:

1. Data provenance: instrument or network, processing center, product version, retrieval date, and license terms.
2. Reference frame, coordinate system, datum, and time standard (UTC vs. local; GPS vs. UTC leap-second handling).
3. Units and sign conventions (e.g., displacement positive east/north/up; magnitude scale type such as Mw, ML, mb).
4. Spatial and temporal extent, sampling rate, and known gaps.
5. Velocity model, Earth model, or rheology assumed by any upstream product.
6. Stated question: what decision or conclusion the result must support.

If any of items 1–3 are unknown, stop and flag them; do not assume a convention silently.

## Operating workflow

1. **Define the question** in one sentence, with a measurable output (e.g., "estimate interseismic slip-deficit rate on segment X with 1σ uncertainty").
2. **Audit the data.** Check time monotonicity, duplicate events, station outages, outliers (median absolute deviation > 5 is a starting flag, not a rule), and metadata consistency.
3. **Document the processing chain.** List every filter, detrending, correction (tidal, atmospheric, seasonal, orbital), and reference choice. Keep raw and processed versions separate.
4. **Run the baseline method** before any advanced one. Example: fit a secular velocity plus annual and semi-annual terms to GNSS time series before interpreting transients.
5. **Quantify uncertainty** with at least two sources: formal (least-squares covariance) and empirical (residual scatter, bootstrap, or alternative-parameter sensitivity).
6. **Test alternatives.** Vary one major assumption at a time (e.g., 1-D vs. 3-D velocity model, cutoff frequency, prior on smoothing) and report the spread.
7. **Interpret with limits.** State what the data constrain and what they cannot, including non-uniqueness and resolution.
8. **Package the outputs** per the deliverable contract.

## Decision gates

- **Gate A (data sufficiency):** Proceed only if coverage is at least 80% of the target window and no single station or sensor dominates the estimate. Otherwise reduce scope or report as provisional.
- **Gate B (model choice):** Use a more complex model only if it reduces misfit beyond expected noise (reduced chi-square moving toward 1, or a information criterion improvement with physical justification) and remains stable under resampling.
- **Gate C (extrapolation):** Do not extrapolate beyond the sampled magnitude range, depth range, or time window without explicit labeling and a separate uncertainty term.
- **Gate D (causal claims):** Correlation in space or time is not causation. Require at least one independent line of evidence (geological, geodetic, seismic, or hydrological) before stating a causal mechanism.
- **Gate E (external impact):** Stop and request explicit approval before publishing hazard levels, contacting authorities, releasing data under embargo, or altering shared catalogs or production pipelines.

## Verification and evidence

Each result must carry:

- Residual RMS compared with stated measurement noise, and a residual plot or table.
- Checkerboard or restoration test for tomographic or slip inversions where resolution is claimed.
- Magnitude of completeness and completeness method for seismicity rate work; Gutenberg–Richter b-value with its standard error.
- Explicit comparison against at least one independent dataset or published reference result, with the reference cited by its own identifier.
- A reproducibility record: input file hashes, software name and version, configuration, and random seeds.

Software versions and algorithm defaults change. Mark any command, library function, or parameter default as "verify against current official documentation" unless confirmed in the current release.

## Failure handling

- **Unphysical result** (negative stiffness, velocities exceeding plausible plate rates by an order of magnitude): trace back to units, sign, and reference frame before revising physics.
- **Non-convergence:** Report the last iterate, the stopping criterion, and the parameter at the boundary; do not present the boundary value as a solution.
- **Conflicting datasets:** Report both, quantify the discrepancy, and identify which assumption explains it. Do not average without justification.
- **Missing metadata:** Quarantine the affected data and flag the gap in the deliverable.

## Deliverable contract

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