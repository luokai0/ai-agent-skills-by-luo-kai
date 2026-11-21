---
name: biometric-health-analytics
description: Use when analyzing wearable or clinical biometric data (heart rate, HRV, sleep, activity, glucose, blood pressure, body composition) to build trends, cohort summaries, or wellness reports, and when deciding whether results are reliable enough to communicate.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Biometric Health Analytics

## Purpose and boundaries

This skill guides analysis of time-series and episodic biometric data for wellness monitoring, research summaries, and clinical-support analytics. It covers data quality assessment, cleaning, feature derivation, trend and variability analysis, cohort comparison, and reporting with stated uncertainty.

It does not cover diagnosis, treatment recommendations, medication changes, or clinical decisions. Any finding that could alter care must be escalated to a licensed clinician. It does not authorize transmitting identifiable health data to any external service, model, or person.

## Inputs and assumptions

Before analysis, record:

1. **Source and device**: manufacturer, model, firmware or app version when known, sensor type (optical PPG, chest strap ECG, CGM, cuff, scale).
2. **Sampling**: nominal interval, timestamp timezone, whether values are raw, averaged, or device-derived scores (e.g., proprietary "readiness" or "sleep score" values are not directly comparable across vendors).
3. **Context**: wear-time expectations, known events (illness, travel, medication change, shift work), user-reported labels.
4. **Consent and purpose**: the stated use, and whether the data is identifiable, pseudonymized, or aggregated.
5. **Unit and definition checks**: confirm units (bpm, ms for RR/HRV, mg/dL or mmol/L for glucose, mmHg), and the HRV metric (RMSSD, SDNN, or other). Do not assume.

Assume timestamps may drift, sensors may be worn inconsistently, and vendor-derived scores may change without notice.

## Operating workflow

1. **Profile the data.** Count records per day, gaps longer than the nominal interval, duplicate timestamps, out-of-range values, and timezone transitions (DST, travel).
2. **Assess wear and coverage.** Compute per-day coverage fraction (valid samples / expected samples). Flag days below the coverage threshold set in Decision gates.
3. **Clean conservatively.** Remove physiologically impossible values using documented bounds (for example, resting heart rate outside 25–220 bpm is suspect; confirm bounds for the population). Mark removals; never silently impute. Interpolate only gaps shorter than a pre-declared limit, and record the count.
4. **Derive features.** Use daily aggregates with the same definition across the period: median resting HR, nightly RMSSD from a fixed sleep window, sleep duration and timing, step totals, glucose time-in-range against a stated target band.
5. **Analyze trends.** Use robust methods: rolling medians, 7- and 28-day baselines, and personal z-scores or percent deviation from the individual's own baseline. Test for change with a method suited to autocorrelated series; state the method. Avoid reporting p-values from naive tests on dependent daily data as if they were independent.
6. **Contextualize.** Annotate known events. Check whether an apparent shift coincides with a firmware update, device change, or wear-pattern change before attributing it to physiology.
7. **Report with uncertainty.** Provide ranges, coverage, and the number of days behind each claim.

## Decision gates

- **Gate A, data sufficiency:** Proceed to trend claims only if at least 70% of expected days meet the coverage threshold and the baseline window has at least 14 valid days. Otherwise report descriptive statistics only and state the limitation.
- **Gate B, cross-source comparison:** Do not compare vendor scores across devices or firmware versions without a documented calibration or a side-by-side overlap period of at least 14 days.
- **Gate C, clinical relevance:** If a result crosses a commonly cited clinical threshold (for example, sustained resting HR above 100 bpm at rest, glucose persistently above target, blood pressure elevations across readings), state the observation and recommend clinician review. Do not characterize it as a diagnosis.
- **Gate D, external sharing:** Stop before sending any data, figures containing identifiers, or model outputs outside the approved environment. Obtain explicit approval from the data owner.
- **Gate E, irreversible actions:** Deletion of source data, overwriting raw files, or altering retention settings requires explicit written approval and a verified backup.

## Verification and evidence

Each report must include:

- Coverage table: expected vs. valid samples per day, and total excluded records with reasons.
- Method statement: cleaning bounds, interpolation limit, metric definitions, baseline window, and statistical test used.
- Sensitivity check: rerun the headline trend with the most aggressive exclusion rule and confirm direction is unchanged; report if it is not.
- Reproducibility: a script or step list that regenerates every number from the raw export. Record library names and versions, and mark any version-sensitive API behavior for verification against current official documentation.
- Spot check: manually verify at least five randomly selected days against the raw export.

Do not state accuracy or validity of a device against a reference unless a validation study with a named reference method is provided.

## Failure handling

- **Timestamp anomalies:** If timestamps are non-monotonic or shifted, stop and request the export with timezone metadata. Do not reorder silently.
- **Unit mismatch:** If values fall outside expected ranges for the stated unit, check for mg/dL vs. mmol/L or ms vs. s before excluding.
- **Missing baseline:** Report current values without deviation scores and state that no baseline exists.
- **Conflicting sources:** Report both, identify which is primary, and do not average across sources without calibration.
- **Result contradicts user report:** Present both, flag the discrepancy, and suggest clinician discussion if it concerns symptoms.

## Deliverable contract

Return:

1. Data summary (source, period, coverage, exclusions).
2. Findings, each with magnitude, direction, uncertainty, and number of supporting days.
3. Limitations and gate outcomes (A through E), with pass or fail stated.
4. Method appendix sufficient for independent reproduction.
5. Escalation items requiring clinician or data-owner review.

Do not include diagnostic language, treatment advice, or guarantees of accuracy. Do not claim compliance with any regulation unless the user supplies the governing policy and it has been reviewed.