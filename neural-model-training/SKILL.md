---
name: neural-model-training
description: Use when designing, launching, debugging, or evaluating training runs for neural networks, including data pipeline setup, hyperparameter choices, distributed training, checkpointing, and training-quality verification.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Neural Model Training

## Purpose and boundaries

This skill governs the end-to-end work of training a neural network: defining the objective, preparing data splits, configuring the optimizer and schedule, running and monitoring jobs, selecting checkpoints, and producing evidence that the resulting model meets its acceptance criteria.

In scope: supervised and self-supervised training, fine-tuning of pretrained models, training-loop debugging, mixed precision and distributed setup, checkpoint management, and run reporting.

Out of scope: model architecture invention without a training question attached, production serving and latency engineering, dataset licensing decisions, and any claim about fairness, safety, or regulatory compliance beyond what was explicitly measured.

## Inputs and assumptions

Before starting, confirm and write down:

1. Task definition: input, output, label source, and the metric that defines success.
2. Data: location, size, schema, label noise estimate, known collection biases, and the permitted use under the data's terms.
3. Compute: accelerator type and count, memory per device, wall-clock budget, and whether the run can be resumed.
4. Baseline: a trivial predictor score (majority class, mean, previous model) that the new run must beat.
5. Framework and versions: record exact versions. Treat any API name, flag, or default from memory as unverified until checked against the current official documentation for that version.

If any of these is missing, stop and request it. Do not fill gaps with assumed values.

## Operating workflow

1. **Freeze the split first.** Create train, validation, and test partitions before any model code runs. Split by the unit that leaks information (patient, user, session, document), not by row. Record the random seed and the split manifest hash.
2. **Audit the data.** Check class balance, duplicate rate across splits (exact and near-duplicate), missing values, and label distribution per split. A duplicate rate above zero across train and test invalidates test results until resolved.
3. **Overfit one batch.** Train on a single small batch until training loss approaches zero. Failure here indicates a bug in the loss, labels, preprocessing, or optimizer wiring, not a tuning problem.
4. **Run a short pilot.** Train 1–5% of the planned steps. Confirm loss decreases, gradient norms are finite, and throughput matches the estimate. Extrapolate the full run cost before committing.
5. **Set the schedule.** Use warmup followed by a decay schedule appropriate to the optimizer. Record learning rate, weight decay, batch size, gradient clipping threshold, and precision mode in a single config file.
6. **Launch with checkpoints and logging.** Save model, optimizer, scheduler, and RNG state at a fixed interval. Log training loss, validation metric, learning rate, gradient norm, and throughput.
7. **Monitor against thresholds** (see Decision gates) and act on them, not on intuition.
8. **Select and evaluate once.** Choose the checkpoint using validation data only. Evaluate the test set once, for the selected checkpoint.

## Decision gates

- **Proceed to full run** only if the single-batch overfit reaches near-zero loss and the pilot shows finite gradients for the whole pilot window.
- **Reduce learning rate** if loss spikes above 2× its recent moving average or gradient norm exceeds 10× its median, and the spike does not recover within 200 steps.
- **Stop early** if validation metric has not improved for a patience window agreed in advance (for example, 5 evaluation intervals) and training loss continues to fall, which indicates overfitting.
- **Halt and investigate** if training loss is NaN or infinite, or if validation metric is worse than the baseline after 20% of the planned steps.
- **Escalate for approval** before using the test set a second time, changing the split, deleting checkpoints or run artifacts, or sharing weights or data outside the project.

## Verification and evidence

Each completed run must produce:

- Config hash and exact framework, CUDA, and driver versions (version-specific details to be verified against current official documentation).
- Loss and validation curves with step numbers, not wall-clock time alone.
- Seed-variance estimate: at least three seeds for any claim that a difference is real, or an explicit statement that only one seed was run.
- Confidence intervals on the test metric (bootstrap over test units is acceptable).
- A comparison table against the baseline and the prior best model.
- A check that no test-set duplicates appear in training data.

Quality bar: a reported improvement smaller than the seed standard deviation is not reported as an improvement.

## Failure handling

- **NaN loss:** lower learning rate by a factor of 2–10, enable gradient clipping, check for division by zero in the loss and log-of-zero in custom losses, then check mixed-precision overflow.
- **Train-validation gap widening with no metric gain:** add regularization, reduce capacity, or add data. Do not tune on test.
- **Throughput far below estimate:** profile data loading first. Input pipelines are the most common bottleneck.
- **Distributed divergence across ranks:** verify identical initialization and seed handling, and that gradient synchronization is active on every rank.
- **Resumed run differs from uninterrupted run:** check restored optimizer state, scheduler step count, and data loader position. Small differences from nondeterministic kernels are acceptable only if documented.

## Deliverable contract

Deliver a run report containing: objective and metric; split manifest hash; data audit summary; config file; launch command as executed; curves; selected checkpoint identifier and selection rule; seed results; test metric with interval; baseline comparison; known limitations; and a list of open items requiring approval. Do not present results without the run identifier and the config that produced them.

Do not:
- tune hyperparameters on the test set;
- report a best-of-many run as typical performance;
- delete failed runs without recording why they failed;
- claim generalization to populations not represented in the data;
- transfer weights, data, or logs outside the project without explicit approval.