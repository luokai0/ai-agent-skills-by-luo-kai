---
name: model-serving-and-inference
description: Use when deploying, scaling, benchmarking, or troubleshooting production model serving endpoints for ML or LLM inference, including batching, latency and throughput tuning, model packaging for serving, and rollout of new model versions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Model Serving And Inference

## Purpose and boundaries

This skill covers getting a trained model to answer requests reliably in production: choosing a serving pattern, packaging the artifact, configuring the inference runtime, meeting latency and throughput targets, and rolling out changes safely.

In scope: online (request/response) serving, batch inference jobs that reuse serving code, GPU/CPU sizing, request batching, quantization decisions at serving time, canary and shadow rollouts, and inference observability.

Out of scope: model training and hyperparameter search, feature pipeline design, data labeling, and model quality evaluation beyond serving regressions (use a dedicated evaluation skill for that).

## Inputs and assumptions

Before acting, confirm or record:

1. Model artifact: format, size, precision, framework version, and a checksum or immutable reference.
2. Traffic profile: requests per second (peak and average), input and output token or payload size distributions, and burstiness.
3. Service targets: p50/p95/p99 latency, minimum throughput, availability, and cost ceiling per 1k requests.
4. Hardware available: accelerator type and memory, CPU cores, host memory, network path.
5. Runtime constraints: approved serving framework, container base image policy, and required authentication.
6. Current production state: incumbent model version, rollback target, and traffic split mechanism.

If any input is missing, state the assumption explicitly in the deliverable. Do not guess hardware specs or traffic numbers and present them as measured.

## Operating workflow

1. Classify the workload: latency-bound interactive, throughput-bound batch, or mixed. Interactive LLM generation is dominated by time-to-first-token and per-token decode time; classic classifiers are dominated by per-request overhead and batching efficiency.
2. Establish a baseline on the current or reference configuration: load test at the expected traffic profile, recording latency percentiles, error rate, GPU/CPU utilization, and memory headroom.
3. Size the deployment from memory first. Weights plus activation and KV-cache (for generative models) must fit with headroom for peak concurrency. Compute the concurrency ceiling, then the replica count needed for peak load with one replica failure tolerated.
4. Tune batching: enable dynamic batching or continuous batching if the runtime supports it. Sweep max batch size and max queue delay; keep the setting that meets the p99 target at peak, not the one with the best average.
5. Choose precision deliberately. Test reduced precision or quantization against a fixed evaluation set of representative inputs; accept only if output deviation is within the agreed tolerance defined by the owning team.
6. Package the artifact with pinned runtime and dependency versions, a health endpoint, a readiness check that reflects model load completion, and structured logs containing model version, request ID, and timing breakdown.
7. Stage the rollout: shadow traffic first (responses discarded, outputs compared), then canary at a small traffic percentage, then progressive increase. Hold each stage for a defined window long enough to observe peak traffic.
8. Record the final configuration, measured results, and rollback procedure.

## Decision gates

- Proceed to canary only if: shadow outputs match the incumbent within agreed tolerance, p99 latency meets target at 1.2x expected peak, and memory headroom is at least 15% on the target hardware.
- Change batching only if the change is validated under the same load profile used for the baseline.
- Adopt quantization only if the accuracy-deviation check passes and latency or cost improves by a measured margin that justifies the risk.
- Scale out before scaling up when the bottleneck is queueing and per-replica utilization is high; scale up when a single request does not fit in memory or per-request latency is the bottleneck.
- Stop and escalate if error rate rises above the baseline by more than the agreed budget, or if any canary stage shows output divergence.

## Verification and evidence

Every rollout must produce:

- Load test report: traffic shape, duration, latency p50/p95/p99, throughput, error rate, with the exact configuration tested.
- Output parity report: sample size, comparison method, and divergence statistics against the incumbent.
- Resource report: peak GPU/CPU utilization, memory high-water mark, cold-start time.
- Rollback test: confirmation that reverting traffic to the previous version completes within the target window.

Measured values only. If a measurement was not taken, write "not measured."

## Failure handling

- OOM on load: reduce max batch size or context length, or move to a larger device; do not raise memory limits blindly on shared nodes.
- Latency spike with healthy utilization: inspect queueing, tokenization or preprocessing on the CPU, and network serialization before changing model config.
- Output divergence in canary: halt traffic increase, roll back the canary, and diff the artifact checksum, runtime version, and precision settings.
- Readiness flapping: check model load time against readiness timeout; do not mark ready before weights are resident.
- Version-specific behavior (flags, config keys, runtime options): verify against the current official documentation for the pinned version before use.

## Deliverable contract

Return a serving plan containing:

1. Workload classification and stated assumptions.
2. Sizing calculation with memory budget and replica count.
3. Runtime configuration (batching, precision, concurrency) with the rationale for each value.
4. Rollout stages, hold windows, and gate criteria.
5. Evidence artifacts listed above, marked measured or not measured.
6. Rollback procedure and owner.

Any action that changes production traffic, deletes or overwrites a deployed model version, modifies shared cluster quotas, or sends data to an external endpoint requires explicit written approval from the accountable owner before execution.

Do not claim specific throughput, latency, or cost figures without a measurement. Do not assert compliance, security, or privacy guarantees for a serving setup. Do not invent runtime flags or package versions; mark any such detail for verification against current official documentation.