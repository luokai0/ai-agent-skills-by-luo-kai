---
name: probability-statistics
description: Use when a physics or mathematics task requires building a probability model, computing distributions or moments, estimating parameters, propagating measurement uncertainty, testing hypotheses, performing Bayesian updates, or validating Monte Carlo results.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Probability Statistics

## Purpose and boundaries

This skill covers formulating probability models for physical and mathematical problems, deriving distributions and moments, estimating parameters, propagating measurement uncertainty, testing hypotheses, Bayesian updating, and checking simulation output. It does not cover experimental design logistics, regulatory or clinical statistics, safety-certified reliability claims, or any conclusion that will be published or acted on without expert human review.

## Inputs and assumptions

Required before work begins:
- The quantity of interest, its units, and the sample space or measurement model.
- Data (values, uncertainties, sample size, known correlations) or a precise description of the generating process.
- Stated assumptions: independence, identical distribution, stationarity, and the distribution family.

Record every assumption explicitly. If an input is missing or ambiguous, ask. Do not substitute a default that changes the answer.

## Operating workflow

1. Restate the question as a precise object: random variable, distribution family, parameter, estimator, or hypothesis pair.
2. Check consistency: densities integrate to one, probabilities lie in [0, 1], variances are nonnegative, and uncertainties carry the same units as the quantity.
3. Select the method. Use closed form for simple models. Use linear propagation for small uncertainties through smooth functions. Use sampling when the function is nonlinear, the posterior is multimodal, or tails are heavy.
4. Compute symbolically until the final numeric step. Carry at least two more significant figures than you will report.
5. Cross-check by a second route: analytic against simulation, two estimators, or a limiting case.
6. Report the result with its uncertainty, method, and assumptions.

## Decision gates

- **Independence:** If correlation is plausible (shared calibration, time series, common cause), do not multiply probabilities or add variances in quadrature until covariance is estimated or bounded.
- **Sample size:** Below roughly 30 points, do not rely on large-sample normal approximations without checking. Use exact or t-based methods.
- **Linearization:** If relative uncertainty exceeds about 10%, or the function curves strongly across the uncertainty range, switch to Monte Carlo or include second-order terms.
- **Priors:** State the prior. Run a sensitivity check with at least two alternative priors. If the posterior shifts materially, report the range, not a single value.
- **Multiple comparisons:** When testing many outcomes, adjust thresholds or state the number of tests.
- **Escalate** before finalizing any conclusion that would drive a safety, medical, financial, or publication decision.

## Verification and evidence

Each check must produce a measured value, not a qualitative judgment:
- **Normalization:** Numerical integral of the density over its support within 1e-6 relative tolerance.
- **Monte Carlo convergence:** Standard error below the target tolerance. Report sample count and seed. Confirm stability by doubling the sample count.
- **Limiting cases:** Zero variance recovers a deterministic result. Large n recovers the expected central-limit scaling. Known special cases match.
- **Coverage:** For interval claims, check empirical coverage on simulated data with known truth.
- **Residuals:** Inspect fit residuals for systematic structure and report any pattern.
- **Reporting:** Every numeric result includes units, uncertainty, and the confidence or credibility level.

## Failure handling

- **Analytic and numeric disagree beyond tolerance:** Evaluate both at a simple parameter value to locate the faulty step before rechecking everything.
- **Estimator unstable across seeds:** Increase samples, test for heavy tails, consider robust estimators (median, trimmed mean), and report the instability.
- **Data inconsistent with the model:** Report the discrepancy with a goodness-of-fit statistic. Do not refit silently to force agreement.
- **Contradictory or missing inputs:** Stop and request clarification.

## Deliverable contract

Return, in order:
1. The question as stated, with model and assumptions.
2. Method and key equations.
3. Result with uncertainty and stated confidence or credibility level.
4. Verification checks performed, each marked pass or fail with its measured value.
5. Limitations, and what new information would change the conclusion.

Do not:
- Interpret a p-value as the probability that the hypothesis is true.
- Report significance without effect size.
- Present simulation output without error bars.
- Add uncertainties linearly when independence is justified, without stating why.
- Cite library functions, package versions, or numerical benchmarks from memory. Mark any software-specific detail "verify against current official documentation."