---
name: model-training-finetuning
description: Use when planning, running, or auditing supervised fine-tuning, parameter-efficient tuning (LoRA-style adapters), or continued pretraining of language or vision models, including dataset preparation, hyperparameter choices, evaluation gates, and handoff of trained artifacts.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Model Training Finetuning

## Purpose and boundaries

This skill guides an agent through adapting an existing pretrained model to a defined task. It covers: deciding whether fine-tuning is warranted, preparing and auditing training data, configuring a run, monitoring it, evaluating against a held-out baseline, and packaging the result.

Out of scope unless explicitly requested: training from scratch, reinforcement learning from human feedback pipelines, large-scale pretraining, model distillation, and production deployment. For deployment, hand off with the artifact contract below.

## Inputs and assumptions

Collect before starting. If any item is missing, stop and request it:

- Base model identifier and license terms, with the exact revision or checksum.
- Task definition: input format, output format, success criterion, and failure modes that matter most.
- Dataset location, schema, size, label source, and collection consent status.
- Compute budget: accelerator type, memory, wall-clock limit, and cost ceiling.
- Baseline: the current prompted or unadapted model's score on the same evaluation set.
- Target environment: serving format, latency and memory limits.

Assume nothing about library names, flags, or package versions. Verify all such details against current official documentation for the framework in use before writing configuration. Record the versions actually used.

## Operating workflow

1. **Justify the run.** Compare the baseline against a prompt or retrieval alternative on 50 to 200 representative examples. Proceed to fine-tuning only if the alternative misses a measurable target and the gap is attributable to format, style, or domain vocabulary rather than missing knowledge.
2. **Audit the data.** Check for duplicates (exact and near-duplicate), label disagreement on a 100-example sample, leakage between train and evaluation splits, personal or confidential content, and class imbalance. Document each finding with a count.
3. **Split deterministically.** Create train, validation, and test splits with a fixed seed, grouped by source entity where examples are correlated (for example, multiple turns from one conversation). Freeze the test split; never tune against it.
4. **Choose the method.** Use full fine-tuning only when the data is large (typically tens of thousands of examples or more) and compute permits. Prefer adapter-based tuning for small to medium datasets, for multiple task variants, or when storage and rollback matter.
5. **Set a conservative starting configuration.** Use a low learning rate relative to typical pretraining values, a short warmup, a cosine or linear decay, and early stopping on validation loss plus task metric. Fix the random seed. Log every hyperparameter.
6. **Run a smoke test.** Train on 1 to 2 percent of data for a few steps. Confirm loss decreases, checkpoints save and reload, and outputs decode correctly.
7. **Run the full job** with checkpoints at fixed intervals and metric logging for training and validation.
8. **Evaluate** the best checkpoint on the frozen test set against the baseline (see Verification).
9. **Package** the artifact with the deliverable contract below.

## Decision gates

- **Gate A (before training):** Proceed only if the data audit has no unresolved consent or privacy issue, and leakage between splits is zero.
- **Gate B (before full run):** Proceed only if the smoke test passes and estimated cost is within the approved ceiling. Get explicit approval for any run exceeding that ceiling or expected to exceed the stated time limit.
- **Gate C (before promotion):** Proceed only if the candidate beats the baseline on the primary metric by the pre-declared margin, does not regress on any safety or refusal probe set by more than the pre-declared tolerance, and meets latency and memory limits on the target hardware.
- **Gate D (before any external use):** Uploading weights, datasets, or results to shared storage, a model hub, or a customer system requires explicit human approval. Deleting checkpoints, overwriting an existing artifact, or altering a production model reference also requires approval.

Pre-declare the primary metric, margin, and tolerances before the run begins. Changing them after seeing results invalidates the comparison.

## Verification and evidence

- Report the primary metric with a confidence interval from bootstrap resampling on the test set (at least 1,000 resamples) or from repeated runs with different seeds (at least three for adapter runs where variance is material).
- Show the baseline and candidate side by side on identical inputs, including a sample of at least 30 failure cases with the input, both outputs, and a short error category.
- Check for regression on general capability probes relevant to the deployment, not only the target task.
- Confirm the artifact loads in a clean environment and reproduces the test metric within a stated tolerance (for example, one percentage point).
- Record the data hash, base model revision, configuration file, seed, framework versions, and hardware.

Do not claim generalization beyond the test distribution. State the distribution the evaluation represents.

## Failure handling

- **Loss diverges or becomes NaN:** Halt. Lower the learning rate, check input normalization and sequence length truncation, and rerun the smoke test.
- **Validation metric plateaus while training loss falls:** Treat as overfitting. Reduce epochs, add data diversity, or switch to a smaller adapter rank. Do not expand the test set to recover signal.
- **Candidate regresses on safety or refusal probes:** Fail Gate C. Inspect training data for instruction patterns that conflict with the probes before retraining.
- **Metric improves only on training-like formats:** Suspect format memorization. Build a held-out set with reworded inputs and rerun evaluation.
- **Checkpoint fails to reload:** Compare framework versions and tokenizer revisions against the record. Do not patch weights manually.
- **Budget exceeded:** Stop the job, preserve the latest checkpoint, and report cost and progress before requesting continuation approval.

## Deliverable contract

Deliver a single handoff bundle containing:

1. Model card: base model and revision, task, intended use, known limitations, evaluation distribution, and license constraints.
2. Configuration file and exact command or script used, with framework versions verified against current documentation.
3. Data manifest: counts per split, dedup and audit results, consent status, and data hash. No raw personal data.
4. Evaluation report: baseline versus candidate, confidence intervals, regression probes, failure samples, and gate outcomes (pass or fail with evidence).
5. Artifact: weights or adapter, tokenizer files, and a reload-verification log.
6. Open items: unresolved risks, decisions awaiting approval, and recommended next experiments.

## What not to do

- Do not fine-tune before testing prompting and retrieval alternatives.
- Do not tune hyperparameters on the test set or rename splits to hide reuse.
- Do not invent metric values, benchmark numbers, or compliance statements; report only measured results.
- Do not guarantee safety, fairness, or regulatory compliance; state the probes actually run.
- Do not include unlicensed, scraped-without-permission, or personal data without a documented basis and approval.
- Do not overwrite prior artifacts or delete checkpoints without approval.
- Do not publish or share weights externally without Gate D approval.