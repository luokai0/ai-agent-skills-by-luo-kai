---
name: statistical-and-classical-ml
description: Use when designing, fitting, validating, or explaining classical statistical models and machine learning baselines (regression, GLMs, tree ensembles, linear classifiers, clustering, time-series baselines) on tabular or structured data, especially when deciding whether a simple model suffices or when results must be defensible to stakeholders.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Statistical And Classical ML

## Purpose and boundaries

This skill governs end-to-end work on classical statistical and machine learning models for structured data: problem framing, data splitting, feature handling, model fitting, uncertainty estimation, validation, and reporting. It covers linear and logistic regression, generalized linear models, regularized regression, decision trees and gradient-boosted ensembles, k-nearest neighbors, naive Bayes, support vector methods, k-means and hierarchical clustering, and classical forecasting baselines.

Out of scope: deep learning architecture design, large language model evaluation, causal identification from observational data beyond stating assumptions, and production deployment infrastructure. Hand off those tasks to the appropriate skill or specialist.

## Inputs and assumptions

Before modeling, confirm and record:

1. Question type: prediction, explanation (coefficient interpretation), or decision support. Each implies different acceptable models and metrics.
2. Unit of analysis and target definition, including the exact timestamp or observation window used to compute the label.
3. Data provenance, collection period, known selection biases, and missingness mechanism (MCAR, MAR, MNAR if assessable).
4. Class balance or outcome distribution, and the cost of each error type, stated by the requester.
5. Constraints: latency, interpretability requirements, regulatory or fairness obligations, and retraining cadence.

If the target leaks future information, or the requester cannot define the label precisely, stop and resolve this first.

## Operating workflow

1. Define the baseline. Fit the simplest defensible model (mean, majority class, last-value forecast, or a regularized linear model) and record its score. Every later model must beat this baseline by a margin larger than its estimated noise.
2. Split data before any transformation. Use time-ordered splits for temporal data; use grouped splits when rows share an entity (customer, patient, device). Hold out a final test set and do not inspect it during iteration.
3. Build preprocessing inside the training pipeline. Imputation, scaling, encoding, and target-informed feature selection must be fit only on training folds.
4. Encode categoricals by cardinality: one-hot for low cardinality, target or frequency encoding with out-of-fold fitting for high cardinality, with explicit handling of unseen levels.
5. Tune hyperparameters with cross-validation on the training portion only. Use a bounded search budget and record it.
6. Estimate uncertainty: bootstrap or repeated CV intervals for metrics, and prediction intervals or calibrated probabilities where the decision needs them.
7. Evaluate once on the held-out test set. Report the metric, interval, baseline comparison, and subgroup performance.
8. Examine residuals or errors by segment, checking for systematic failure.

## Decision gates

- Gate A (proceed to modeling): target definition is written, leakage review passed, baseline recorded.
- Gate B (prefer complex model): complex model beats the regularized linear or tree baseline by more than the cross-validated standard error, and the gain persists on the test set. Otherwise choose the simpler model.
- Gate C (interpretability): if explanation is the goal, use GLMs or sparse models; use tree ensembles only with post-hoc attribution, stating its limits. Coefficients from correlated predictors must not be read causally.
- Gate D (calibration): if probabilities drive thresholds or costs, check calibration curves and Brier score; recalibrate on a separate validation fold if needed.
- Gate E (release): stakeholder has approved metric choice, threshold, and known limitations. Any model affecting individuals, credit, employment, health, or access requires explicit approval and a documented fairness review before use.

## Verification and evidence

- Leakage check: no feature is computed from data after the prediction time; target-correlated features with implausibly high importance are investigated.
- Class imbalance: report precision-recall curves alongside ROC; state the prevalence of the positive class.
- Regression: report MAE or RMSE in original units, and a naive baseline ratio.
- Clustering: report internal indices and stability under resampling; do not claim discovered groups are real without external validation.
- Time series: report errors over at least two forecast horizons against seasonal naive baselines.
- Reproducibility: fix random seeds, record library versions, and store the exact split indices.
- Library APIs, function names, and default hyperparameters change across versions; verify each call against current official documentation before reporting results.

## Failure handling

- Test score far below validation score: suspect leakage, split contamination, or distribution shift; re-run the split audit before tuning further.
- Baseline outperforms all models: report this honestly; do not add complexity to rescue the result.
- Unstable coefficients under resampling: increase regularization or reduce collinear features, and disclose instability.
- Calibration failure: apply Platt scaling or isotonic regression on a held-out fold; isotonic needs more data.
- Missing data mechanism unknown: run sensitivity analysis with at least two imputation assumptions and report the range.

## Deliverable contract

Produce a report containing:

1. Question, target definition, and observation window.
2. Data summary: row counts per split, missingness, class balance.
3. Baseline and final model, with hyperparameter search budget.
4. Test metrics with intervals, baseline comparison, and calibration where relevant.
5. Subgroup and error analysis.
6. Limitations, assumptions, and conditions under which the model should be re-validated.
7. Reproducibility record: seeds, split identifiers, library versions (marked as to be verified if unconfirmed).

## What not to do

- Do not tune on the test set or report the best of many runs as the result.
- Do not use random splits on time-dependent or grouped data.
- Do not interpret predictive coefficients as causal effects without an identification argument.
- Do not present clusters as ground truth.
- Do not deploy, share externally, or act on model outputs affecting individuals without explicit approval from the accountable owner.
- Do not delete or overwrite source datasets or prior model artifacts without explicit approval.