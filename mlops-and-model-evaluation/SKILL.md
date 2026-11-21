---
name: mlops-and-model-evaluation
description: Use when designing, reviewing, or operating machine learning model evaluation, validation gates, experiment tracking, model registry promotion, deployment monitoring, or drift and retraining decisions for production ML systems.
author: Luo Kai
provenance: original
version: 1.0.0
---

# MLOps and Model Evaluation

## Purpose and boundaries

This skill governs how a model moves from experiment to production and how it is judged while it runs. It covers offline evaluation design, reproducibility of training runs, promotion gates in a model registry, staged rollout, production monitoring, and retraining triggers.

It does not cover model architecture search for its own sake, general data engineering pipelines, or application-level product metrics unless they directly gate a model decision. Hand off pure infrastructure provisioning and security review to the owning teams, but state the dependency in the deliverable.

## Inputs and assumptions

Before acting, confirm and record:

- Task type (classification, ranking, regression, forecasting, generation, retrieval) and the decision the model informs.
- Business cost of each error type. Without this, no threshold can be justified.
- Data sources, label provenance, label delay, and known leakage paths.
- Baseline: current production model, heuristic, or human process. Every candidate is compared against it.
- Evaluation population: the traffic slice the model will actually serve, not only the training distribution.
- Fairness and sensitive attributes in scope, and whether they may be used for evaluation.
- Available compute, latency budget, and rollback mechanism.

If any item is missing, state the assumption explicitly in the deliverable and mark its risk level. Do not silently fill gaps.

## Operating workflow

1. **Freeze the question.** Write one sentence: what decision the model changes, for whom, and what failure costs most.
2. **Define the split before training.** Use time-based splits for anything with temporal drift. Keep entity-level separation (same user, device, or patient never spans train and test). Lock the test set; do not tune against it.
3. **Check for leakage.** Verify that no feature is computed from post-outcome data, that aggregates are windowed as of prediction time, and that label timestamps precede feature cutoffs.
4. **Establish baselines.** Include the trivial baseline (majority class, last value, popularity) and the incumbent production model. A candidate that does not beat the incumbent on the primary metric and on at least one guardrail does not advance.
5. **Select metrics by cost.** Choose a primary metric that matches the cost structure (for example, precision at fixed recall for review queues, calibrated probability for pricing, NDCG@k for ranking). Add guardrail metrics for subgroups, latency, and calibration.
6. **Run slice analysis.** Report metrics for each material segment: region, device, customer tier, rare class, and new versus returning entities. Flag any slice with materially worse performance even if the aggregate improves.
7. **Record the run.** Log code revision, data snapshot identifier, feature set version, hyperparameters, random seeds, hardware class, and evaluation outputs. A run that cannot be reproduced from its record is not eligible for promotion.
8. **Register and stage.** Register the artifact with its lineage. Promote first to shadow mode (scored, not served), then to a limited canary, then to full traffic, passing each gate in Decision gates.
9. **Monitor after release.** Track input drift, prediction distribution, calibration against delayed labels, and business outcome. Set alert thresholds before launch.
10. **Decide retraining.** Retrain on a schedule only when the monitored signal justifies it; otherwise prefer investigation of the cause.

## Decision gates

Advance to the next stage only when all conditions hold:

- **Offline gate:** primary metric improves over the incumbent with a confidence interval (bootstrap or paired test) that excludes zero; no guardrail regresses beyond a threshold agreed with the owner before evaluation; calibration error within the agreed bound (for example, expected calibration error below a stated value for probabilistic outputs).
- **Reproducibility gate:** a second independent rerun with the recorded configuration reproduces the primary metric within the tolerance stated in advance.
- **Shadow gate:** prediction distributions match offline expectations within the agreed tolerance; latency at p95 and p99 meets budget; no pipeline errors over the shadow window that covers at least one full business cycle.
- **Canary gate:** outcome metric not worse than control beyond the pre-registered margin; no subgroup regression flagged in slice analysis; rollback tested in the same window.
- **Full rollout gate:** canary ran long enough to observe delayed labels for the primary outcome, or a documented proxy is accepted by the owner.

Stop and escalate if a gate threshold is changed after results are seen. Thresholds must be set before the comparison.

## Verification and evidence

Every promotion requires an evidence bundle containing:

- Metric table with point estimates, intervals, sample sizes, and the incumbent comparison.
- Slice table with the same metrics per segment and minimum sample size noted for each.
- Calibration plot or reliability statistic for probabilistic outputs.
- Leakage checklist result with the specific checks performed.
- Drift baseline: reference distributions for top features and predictions.
- Lineage record linking code, data snapshot, features, and artifact.

Measurable checks to run before sign-off: train-serve skew test on a sample of logged requests (feature values must match within stated tolerance); schema and null-rate comparison against reference; reproducibility rerun; latency benchmark under production-like concurrency.

## Failure handling

- **Metric improves, slice regresses:** do not promote. Investigate the segment, then either fix, reweight, or document an accepted tradeoff with the owner's written approval.
- **Offline gain disappears in shadow:** suspect train-serve skew or leakage first. Compare feature values for identical requests before retuning the model.
- **Label delay makes outcome unavailable:** use the agreed proxy, label it as a proxy in all reports, and schedule re-evaluation when true labels arrive.
- **Drift alert fires:** determine whether the input change is real, a pipeline defect, or a seasonal pattern before retraining. Roll back if the output degrades materially.
- **Irreproducible result:** halt promotion. Do not promote from a notebook state that cannot be reconstructed.

## Deliverable contract

Each evaluation or promotion review returns:

1. Decision: promote, hold, or reject, with the gate that determined it.
2. Summary of the decision question, the primary metric, and the cost assumption.
3. Evidence bundle as specified above, with missing items named.
4. Assumptions and their risk levels.
5. Rollback plan and monitoring thresholds.
6. Open items with named owners.

## Safety and approval controls

Obtain explicit human approval before any action that deletes or overwrites registered models or data snapshots, changes production traffic allocation, sends model outputs to external parties, uses personal or sensitive attributes beyond the approved evaluation scope, or alters alert thresholds that govern customer-facing decisions.

## What not to do

- Do not tune hyperparameters on the held-out test set.
- Do not report only aggregate metrics.
- Do not compare against a weaker or stale baseline when the incumbent is available.
- Do not promote from an unlogged or unreproducible run.
- Do not state compliance, fairness, or safety guarantees; report measured results and their limits.
- Do not cite library versions, flags, or API behavior from memory. Mark any version-sensitive detail for verification against current official documentation before use.