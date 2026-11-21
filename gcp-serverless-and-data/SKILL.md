---
name: gcp-serverless-and-data
description: Use when designing, deploying, reviewing, or troubleshooting Google Cloud serverless workloads (Cloud Run, Cloud Functions, Cloud Scheduler, Pub/Sub, Eventarc) or data pipelines (BigQuery, Dataflow, Cloud Storage landing zones, Composer/Workflows orchestration) and needing concrete, verifiable guidance.
author: Luo Kai
provenance: original
version: 1.0.0
---

# GCP Serverless and Data

## Purpose and boundaries

This skill guides design, deployment, review, and incident work for event-driven serverless services and batch or streaming data pipelines on Google Cloud. It covers:

- Compute: Cloud Run services and jobs, Cloud Functions, Cloud Scheduler triggers.
- Messaging and events: Pub/Sub topics and subscriptions, Eventarc routing.
- Data: BigQuery datasets, tables, scheduled queries, load and streaming ingestion; Dataflow pipelines; Cloud Storage landing and archive buckets.
- Orchestration: Workflows and Cloud Composer DAG-level decisions.

It does not cover cluster administration (GKE internals), network architecture beyond service-facing ingress/egress choices, or cost negotiation with Google.

## Inputs and assumptions

Before acting, collect:

1. Project ID(s), region(s), and environment (dev, staging, prod).
2. Workload type and trigger model (HTTP, Pub/Sub push or pull, scheduled, storage event, batch).
3. Expected throughput, payload size, latency target, and acceptable data loss window.
4. Data classification and residency constraints.
5. Current IAM bindings and service account identities in use.
6. Existing IaC (Terraform, Deployment Manager, gcloud scripts) and whether it is source of truth.

Assumptions must be stated explicitly. If any input is missing and it changes the design, stop and ask.

Version-sensitive details (command flags, quota values, runtime versions, pricing, feature availability and GA/preview status) must be verified against current official Google Cloud documentation before being presented as fact.

## Operating workflow

1. **Classify the workload.** Request/response, asynchronous event, scheduled batch, or continuous stream. The classification determines the service choice.
2. **Select the runtime.** Use Cloud Run for containerized HTTP or event-handling services and for jobs with bounded runtime. Use Cloud Functions for small single-purpose handlers. Use Dataflow for streaming or large parallel transforms. Use BigQuery SQL (scheduled queries or Workflows calls) when transformation is set-based and fits in the warehouse.
3. **Define identity first.** Create one dedicated service account per workload with the minimum roles on specific resources. Never reuse the default Compute Engine service account in production.
4. **Design the event path.** For Pub/Sub, define acknowledgement deadline, retry policy, dead-letter topic, and ordering need. Make every consumer idempotent using a stable message or business key.
5. **Design the data path.** Choose partitioning and clustering on BigQuery tables based on the dominant filter and join columns. Set table expiration or partition expiration where retention is defined.
6. **Write configuration as code.** Keep service definitions, IAM bindings, and schedules in version-controlled IaC. Deploy from CI, not from workstations.
7. **Stage and promote.** Deploy to non-production with representative data volume, run the verification checks below, then promote the same artifact digest.
8. **Document operational runbook entries**: alert conditions, replay procedure, and rollback steps.

## Decision gates

Stop and obtain explicit human approval before any of the following:

- Deleting or recreating a BigQuery table, dataset, Pub/Sub topic or subscription, or bucket; or any action that drops retained data.
- Changing a production IAM binding, service account key, or granting `roles/owner`, `roles/editor`, or broad project-level roles.
- Replaying or purging messages from production Pub/Sub or dead-letter queues.
- Changing traffic split or rolling back a production Cloud Run revision.
- Enabling public (unauthenticated) invocation on any service.
- Moving data across regions or to a different project, or exporting data outside the organization.
- Any action with cost impact above the agreed budget, such as enabling large slot reservations or Dataflow autoscaling ceilings.
- Schema changes to shared tables consumed by other teams.

Proceed without gate approval only for read-only inspection, dry-run plans, and changes confined to a non-production project.

## Verification and evidence

Each deliverable must include evidence for these checks:

- **Idempotency:** Replay one message twice in staging; the resulting row count and side effects are identical.
- **Retry and DLQ:** Force a handler failure; confirm redelivery count matches configuration and the message lands in the dead-letter topic after the maximum attempts.
- **Latency:** Measure p95 and p99 request or processing latency under the expected load profile. Report the measured numbers, not the target.
- **Least privilege:** List every granted role per service account with its resource scope; confirm no primitive roles.
- **Data correctness:** For pipeline changes, compare row counts and a checksum or aggregate (sum of a key measure, distinct key count) between source and target for a defined window.
- **Cost guardrail:** Confirm budget alerts exist and BigQuery bytes-scanned estimate is recorded for new queries.
- **Observability:** Confirm logs include a correlation ID, errors are alerting-routed, and dashboards show request count, error rate, and backlog age (Pub/Sub oldest unacked message age).

Quote exact command output or console-exported values as evidence. Do not state a check passed without the artifact.

## Failure handling

- **Duplicate processing detected:** Halt consumer scaling, identify the dedup key, and fix idempotency before resuming. Do not manually delete downstream rows without approval.
- **Backlog growing:** Check consumer error rate first, then max instances or concurrency limits, then downstream quota (BigQuery streaming or API limits). Scale only after cause is identified.
- **Permission errors after deploy:** Verify the runtime service account, not the deployer's identity, holds the needed role on the specific resource. Add the narrowest role and record the change.
- **Schema mismatch on load:** Quarantine the file or message to a separate bucket or topic. Do not auto-coerce types silently.
- **Timeout on long jobs:** Move work to a Cloud Run job or Dataflow batch rather than raising request timeouts beyond the documented maximum.
- **Unknown or conflicting documentation:** State the conflict, cite the official page checked, and escalate rather than guessing.

## Deliverable contract

Every output must contain:

1. Workload classification and chosen services with a one-line justification each.
2. Identity table: service account, roles, resource scope.
3. Configuration summary: triggers, retry policy, DLQ, partitioning or clustering, retention.
4. Verification results with captured evidence for each applicable check.
5. Open assumptions and items marked for verification against current official documentation.
6. Rollback procedure and the named approval gates that apply.

Do not claim performance numbers, cost savings, or compliance certifications without measured or documented evidence. Do not invent flags, API fields, or version numbers; mark them for verification instead.