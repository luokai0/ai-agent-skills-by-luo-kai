---
name: aws-serverless-and-data
description: Use when designing, reviewing, or operating AWS serverless applications (Lambda, API Gateway, EventBridge, Step Functions, SQS/SNS, DynamoDB, S3-based data pipelines, Glue/Athena analytics) and need architecture decisions, IAM and cost guardrails, or failure-mode analysis.
author: Luo Kai
provenance: original
version: 1.0.0
---

# AWS Serverless and Data

## Purpose and boundaries

This skill guides work on event-driven and serverless systems on AWS, including the data paths that feed them: ingestion, transformation, storage layout, and query access. It covers:

- Compute and orchestration: Lambda functions, Step Functions workflows, EventBridge routing, SQS/SNS messaging.
- API surfaces: API Gateway (REST or HTTP APIs) fronting Lambda or other integrations.
- Data stores and lakes: DynamoDB table design, S3 partitioning and lifecycle, Glue cataloging, Athena querying.
- Operational concerns: IAM least privilege, timeouts and retries, idempotency, observability, and cost controls.

It does not cover container-only platforms (ECS/EKS internals), on-premises migration programs, or general application code beyond what a function needs to be correct. Service limits, quotas, pricing, and runtime support windows change; treat any specific number as something to confirm against current AWS documentation before committing to it.

## Inputs and assumptions

Collect these before recommending a design:

1. Workload profile: request rate (average and peak), event size, fan-out, latency target, and acceptable staleness for data.
2. Consistency and ordering needs: whether duplicates are tolerable, whether ordering per key matters, and whether a transaction spans stores.
3. Data access patterns: list the top read and write queries. For DynamoDB, design from these, not from entities.
4. Compliance constraints: data classification, residency, encryption requirements. Do not assert that a configuration satisfies any regulation; state what it enables and defer certification to the owner.
5. Existing estate: accounts, Organizations structure, IaC tool in use, and deployment pipeline.

If any input is missing, state the assumption explicitly in the deliverable and mark it as unverified.

## Operating workflow

1. Restate the workload in one paragraph and list the access patterns.
2. Choose the invocation model. Synchronous API calls suit request/response with latency budgets under the API integration limits; asynchronous events suit decoupling; queues suit smoothing bursts and controlling concurrency.
3. Select orchestration. Use Step Functions when a flow has branching, waits, or compensating steps; use plain EventBridge rules when routing is the only need.
4. Design idempotency. Assign every message a business key; write with conditional expressions or a deduplication record with a TTL. Assume at-least-once delivery everywhere.
5. Define failure policy per integration: retry count, backoff, dead-letter destination, and whether partial batch failure reporting is enabled for queue-triggered functions.
6. Specify IAM as a per-function role scoped to named resource ARNs and the exact actions used. No wildcard resources on write actions.
7. For DynamoDB, document partition key, sort key, every index, projected attributes, and capacity mode with the reasoning. Flag hot-key risk for any key with skewed traffic.
8. For S3 data lakes, specify prefix layout (commonly by dataset, then partition columns such as date), file format and target file size, lifecycle transitions, and Glue catalog ownership.
9. Attach observability: structured logs with correlation IDs, metrics for errors and latency, and alarms tied to a named owner.
10. Estimate cost drivers (invocations, duration, requests, storage, scanned bytes) and identify the top two, with the controls that bound them.

## Decision gates

Stop and request explicit approval before proceeding when the work involves:

- Deleting or replacing tables, buckets, queues, streams, or stacks with stateful resources.
- Changing IAM policies that broaden permissions, or any cross-account trust.
- Modifying production event source mappings, API stages, or DNS/custom domains.
- Purging queues or replaying events into production consumers.
- Enabling public access on any bucket or API endpoint.
- Sending data to external systems or third-party endpoints.
- Changing encryption keys or key policies.

Proceed without a gate for read-only analysis, drafting IaC in a non-deployed branch, and writing tests against local or ephemeral resources.

Choose Step Functions Standard versus Express based on duration and execution-semantics needs; confirm current quota and pricing details in official documentation before finalizing.

## Verification and evidence

Every design must include:

- A table mapping each access pattern to the key, index, or query path that serves it.
- A failure matrix listing each component, failure mode (throttle, timeout, poison message, downstream unavailability), and handling behavior.
- A replay test: send the same event twice and state the observed outcome, from a test environment.
- Permission check: list each action granted and the code path that requires it. Remove any action without a corresponding path.
- Cost assumption table with units (requests per day, average duration, memory size, GB scanned) and the formula used.
- Pass criteria: p95 latency target, error budget, maximum acceptable duplicate rate (should be zero effective duplicates after idempotency), and maximum Athena bytes scanned per query for the defined query set.

Mark any service limit, pricing figure, or runtime deprecation date as "verify against current AWS documentation" unless you have confirmed it in the session.

## Failure handling

- If a throttle appears, check reserved and account concurrency, then batch size and event source mapping concurrency before increasing limits. Do not raise limits without a capacity estimate.
- If a poison message loops, route it to a dead-letter queue after the configured receive count, and add a quarantine procedure rather than deleting messages.
- If DynamoDB shows hot partitions, redesign the key or add write sharding; do not simply raise capacity.
- If Athena cost spikes, inspect partition filters and file sizes first; small-file proliferation is a common cause.
- If a design requires a stateful change to production, stop and escalate using the decision gate.

## Deliverable contract

Return a document containing, in order:

1. Summary of workload and assumptions, with unverified items flagged.
2. Architecture diagram in text form listing components and event flows.
3. Access-pattern-to-key table and data layout.
4. Per-integration failure policy and idempotency method.
5. IAM role list with scoped actions and resources.
6. Observability plan with named metrics and alarm thresholds.
7. Cost drivers and controls.
8. Open decisions requiring approval, each with the gate it falls under.
9. Verification results or a clear list of checks still pending.

Do not present the design as production-ready until the verification items are complete and the gated decisions are approved.