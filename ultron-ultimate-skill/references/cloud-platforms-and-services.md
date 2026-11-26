# Cloud Platforms and Services

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## aws-cdk-cloudformation

**Use when:** Use when authoring, reviewing, synthesizing, diffing, or deploying AWS infrastructure defined with the AWS Cloud Development Kit (CDK) or raw CloudFormation templates, including stack design, construct choices, change set review, drift handling, and rollback planning.

### Purpose and boundaries

This skill covers infrastructure-as-code work on AWS using CDK (TypeScript, Python, or other supported languages) that synthesizes to CloudFormation, and hand-written CloudFormation templates (YAML or JSON). It covers stack structure, resource configuration, change review, deployment sequencing, drift investigation, and rollback.

It does not cover application code inside Lambda functions, runtime container images, non-AWS clouds, Terraform, or account-level governance such as AWS Organizations policy design. Route those to the appropriate skill.

### Inputs and assumptions

Collect these before acting:

- Target account ID, region, and environment label (dev, staging, prod). Never assume the account from ambient credentials alone; confirm it appears in the synth or deploy output.
- CDK app entry point and language, or the template path.
- Current deployed state: stack names, last successful deploy time, and whether a change set or drift report exists.
- Ownership: who approves production changes and which stacks hold stateful resources (databases, buckets, KMS keys, log groups with retention requirements).
- Toolchain versions. CDK CLI, construct library, and CloudFormation resource type versions change; treat any specific property name, default, or limit as **version-sensitive: verify against current AWS documentation** before relying on it.

If stateful resources or production targets are involved and ownership is unclear, stop and ask.

### Operating workflow

1. **Establish the target.** Confirm account, region, and stack names. Print the caller identity the tooling resolves and compare it with the intended account.
2. **Synthesize.** Run synthesis to produce the CloudFormation template. Save the output. Do not edit generated templates by hand; change the source.
3. **Lint the template.** Run a static checker (for example cfn-lint or the CDK-native rule set) and record findings. Fail the workflow on new errors; triage warnings explicitly.
4. **Review resource-level impact.** Identify every resource with `Replacement` or `Delete` behavior in the diff. Replacement of a stateful resource is a blocking finding.
5. **Generate a change set.** Create a change set rather than deploying directly. Review added, modified, removed, and replaced resources.
6. **Check IAM changes separately.** Any new or broadened IAM role, policy, or resource-based policy is reviewed line by line.
7. **Obtain approval** (see decision gates), then execute the change set.
8. **Verify post-deploy** (see verification section) and record outputs.
9. **Detect drift** on a schedule or after incidents: compare live state to template and classify each difference before remediating.

### Decision gates

For infrastructure changes, halt for human sign-off whenever any of the following conditions apply:

- The change set contains any Replacement or Delete on a stateful resource: databases, S3 buckets, DynamoDB tables, KMS keys, EFS file systems, log groups holding data needed for audit.
- The change modifies IAM permissions, resource policies, security group ingress rules, or public access settings.
- The target is production, or the account is shared across environments.
- The change alters DNS records, certificates, load balancer listeners, or anything that affects external traffic.
- A stack update requires disabling termination protection, deletion protection, or retention policies.
- Drift shows manual changes you cannot attribute to a known owner.
- Any action would delete a stack or empty a bucket.

Proceed without a gate only for additive, non-stateful, non-IAM changes in non-production environments that the diff confirms.

### Verification and evidence

Record evidence at each stage:

- Synthesis: template hash and size, count of resources by type.
- Lint: tool version, rule set, zero new errors.
- Change set: exported JSON or console summary showing exact action per resource. Expected action counts must match what the author predicted in the change description; any mismatch blocks execution.
- Post-deploy: stack status is a completed-success state; stack outputs match expected values; a health check or smoke test against the changed resource passes.
- Drift: detection status per stack, list of drifted resource IDs with property-level differences.

A deployment without a reviewed change set, or without a post-deploy check, is incomplete.

### Failure handling

- **Stack update fails and rolls back:** read the first failed event, not the last. Fix the root cause in source, re-synthesize, and generate a new change set. Do not force-continue rollback on a stack you have not diagnosed.
- **Stack stuck in an UPDATE_ROLLBACK_FAILED or similar state:** stop. Identify the blocking resource. Recovery options that skip resources or retain them can orphan infrastructure; they require approval and a written rollback note.
- **Resource creation fails due to quota or name collision:** do not rename or delete existing resources to make room without approval.
- **Lint or synth error:** fix the source. Do not suppress rules to pass the pipeline without a documented, scoped justification.
- **Drift found:** do not auto-revert. Determine whether the manual change was intentional, then either codify it in source or revert it through a reviewed change set.

### Deliverable contract

Every completed task returns:

1. Target: account, region, stack names, environment.
2. Change summary: resource-level actions (create, update, replace, delete) with counts.
3. Risk list: each gated item and its approval status.
4. Evidence: synthesis hash, lint result, change set reference, post-deploy check results.
5. Rollback plan: the specific previous template version or commit and the expected rollback behavior for stateful resources.
6. Open items: anything version-sensitive that was not verified against current documentation.

### What not to do

- Do not deploy directly from a local working tree with uncommitted changes.
- Do not hand-edit synthesized templates or live stacks through the console to "fix" them.
- Do not use retain or skip options on failed deletes as a shortcut without approval.
- Do not hardcode account IDs, secrets, or credentials in source; use parameters or secure references.
- Do not state a resource property, default, or quota as fact without checking current documentation.
- Do not disable rollback or termination protection to get a change through.
- Do not treat a successful deploy as proof of correctness; verify the behavior.


## aws-serverless-and-data

**Use when:** Use when designing, reviewing, or operating AWS serverless applications (Lambda, API Gateway, EventBridge, Step Functions, SQS/SNS, DynamoDB, S3-based data pipelines, Glue/Athena analytics) and need architecture decisions, IAM and cost guardrails, or failure-mode analysis.

### Purpose and boundaries

This skill guides work on event-driven and serverless systems on AWS, including the data paths that feed them: ingestion, transformation, storage layout, and query access. It covers:

- Compute and orchestration: Lambda functions, Step Functions workflows, EventBridge routing, SQS/SNS messaging.
- API surfaces: API Gateway (REST or HTTP APIs) fronting Lambda or other integrations.
- Data stores and lakes: DynamoDB table design, S3 partitioning and lifecycle, Glue cataloging, Athena querying.
- Operational concerns: IAM least privilege, timeouts and retries, idempotency, observability, and cost controls.

It does not cover container-only platforms (ECS/EKS internals), on-premises migration programs, or general application code beyond what a function needs to be correct. Service limits, quotas, pricing, and runtime support windows change; treat any specific number as something to confirm against current AWS documentation before committing to it.

### Inputs and assumptions

Collect these before recommending a design:

1. Workload profile: request rate (average and peak), event size, fan-out, latency target, and acceptable staleness for data.
2. Consistency and ordering needs: whether duplicates are tolerable, whether ordering per key matters, and whether a transaction spans stores.
3. Data access patterns: list the top read and write queries. For DynamoDB, design from these, not from entities.
4. Compliance constraints: data classification, residency, encryption requirements. Do not assert that a configuration satisfies any regulation; state what it enables and defer certification to the owner.
5. Existing estate: accounts, Organizations structure, IaC tool in use, and deployment pipeline.

If any input is missing, state the assumption explicitly in the deliverable and mark it as unverified.

### Operating workflow

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

### Decision gates

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

### Verification and evidence

Every design must include:

- A table mapping each access pattern to the key, index, or query path that serves it.
- A failure matrix listing each component, failure mode (throttle, timeout, poison message, downstream unavailability), and handling behavior.
- A replay test: send the same event twice and state the observed outcome, from a test environment.
- Permission check: list each action granted and the code path that requires it. Remove any action without a corresponding path.
- Cost assumption table with units (requests per day, average duration, memory size, GB scanned) and the formula used.
- Pass criteria: p95 latency target, error budget, maximum acceptable duplicate rate (should be zero effective duplicates after idempotency), and maximum Athena bytes scanned per query for the defined query set.

Mark any service limit, pricing figure, or runtime deprecation date as "verify against current AWS documentation" unless you have confirmed it in the session.

### Failure handling

- If a throttle appears, check reserved and account concurrency, then batch size and event source mapping concurrency before increasing limits. Do not raise limits without a capacity estimate.
- If a poison message loops, route it to a dead-letter queue after the configured receive count, and add a quarantine procedure rather than deleting messages.
- If DynamoDB shows hot partitions, redesign the key or add write sharding; do not simply raise capacity.
- If Athena cost spikes, inspect partition filters and file sizes first; small-file proliferation is a common cause.
- If a design requires a stateful change to production, stop and escalate using the decision gate.

### Deliverable contract

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


## azure-app-and-data-services

**Use when:** Use when designing, deploying, configuring, troubleshooting, or reviewing Azure application hosting (App Service, Functions, Container Apps) and managed data services (Azure SQL, Cosmos DB, Storage, Redis-compatible caches) in a production or pre-production environment.

### Purpose and boundaries

This skill guides an agent through planning, configuring, verifying, and troubleshooting Azure application hosting and managed data services. It covers:

- Hosting: App Service (web apps, slots), Azure Functions, Azure Container Apps.
- Data: Azure SQL Database, Cosmos DB, Storage accounts (Blob, Queue, Table), managed Redis-compatible caches.
- Connectivity: managed identity, private endpoints, virtual network integration, DNS for private links.
- Operations: deployment slots, scaling, backup and restore, diagnostics, cost signals.

It does not cover: on-premises data migration tooling, Azure networking hub design beyond the app and data boundary, Kubernetes internals (AKS), or billing dispute handling. Refer those to specialized skills.

### Inputs and assumptions

Before acting, confirm or obtain:

1. Subscription, resource group, region, and target environment (dev, test, staging, prod).
2. Workload type and traffic profile: request rate, peak concurrency, latency target, data volume, growth expectation.
3. Data classification and residency requirements, stated by the requester. Do not assume compliance status.
4. Existing resource IDs, identity model, and network topology (public, VNet-integrated, private endpoint).
5. Recovery objectives (RPO and RTO) as provided by the owner. If absent, record "not defined" and flag it.
6. The current version of Azure CLI, Bicep/ARM tooling, or Terraform provider in use.

Assumptions must be written down in the deliverable. Never assume a SKU, tier, or region capacity is available; verify it.

**Version-sensitive details:** SKU names, runtime stack identifiers, supported language versions, API versions, CLI parameters, and pricing change over time. Mark every such detail as "verify against current Microsoft Learn documentation" before it is applied.

### Operating workflow

1. **Classify the request.** Determine whether it is design, deployment, configuration change, incident, or review.
2. **Read current state.** Query existing resources in read-only mode (list, show, get configuration). Record names, SKUs, identity, network mode, and backup settings.
3. **Build the target state.** Specify each resource, its SKU, region, identity type, network exposure, and dependencies.
4. **Prefer declarative definitions.** Express changes in Bicep or ARM templates, or the team's IaC tool, so changes are reviewable and repeatable.
5. **Validate before apply.** Run template validation and what-if or plan output. Review every delete and replace operation.
6. **Stage the change.** Deploy to non-production first. For App Service, use a deployment slot with traffic routing when available.
7. **Verify** against the checks in the verification section.
8. **Record** the change, rollback path, and open items.

### Decision gates

Stop and obtain explicit human approval before:

- Deleting, replacing, or recreating any resource that holds data (SQL databases, Cosmos DB containers, storage accounts, Redis caches).
- Changing a data-tier SKU in a way that can cause downtime or data movement.
- Enabling public network access on a data resource, or disabling private endpoints.
- Modifying firewall rules, network security rules, or DNS zones shared with other workloads.
- Rotating or exposing secrets, keys, or connection strings. Prefer managed identity; never print secret values into logs or output.
- Changing retention, geo-replication, or backup policies, since these affect recovery and cost.
- Any action in production, or any action that affects external users or third-party integrations.
- Restoring a database over an existing one.

Proceed without a gate only for read-only queries, template validation, and changes in an explicitly designated sandbox resource group.

Choose hosting by criteria, not preference:
- App Service: long-running web APIs, standard web workloads, slot-based releases.
- Functions: event-driven or short-running work with scale-to-zero needs.
- Container Apps: containerized services needing revision-based traffic splitting and KEDA-style scaling.

Choose data services by access pattern: relational transactions and constraints point to Azure SQL; globally distributed, low-latency key-value or document access points to Cosmos DB; blob and object storage points to Storage accounts.

### Verification and evidence

Every completed change must include evidence for each relevant check:

- **Identity:** the app uses a system or user-assigned managed identity, and role assignments are scoped to the minimum resource, not the subscription. Confirm with an authenticated read through the app, not only by inspecting configuration.
- **Network:** public access is disabled on data resources where required; private endpoint DNS resolves to a private address from the app's network. Test resolution from inside the network.
- **Health:** health check endpoint returns success after restart; App Service slot swap or Container Apps revision shows healthy replicas.
- **Data:** a restore test has succeeded within the documented RTO for the most recent backup point, or the gap is reported. Backup retention matches the approved policy.
- **Performance:** p95 latency and error rate measured against the stated target over a representative window. Do not claim a target is met without measurements.
- **Cost signal:** scaling limits and minimum instance counts are set deliberately, and the expected monthly cost range is stated with the source of the estimate.
- **Diagnostics:** logs and metrics flow to the designated workspace; alerts exist for error rate, latency, and resource exhaustion.

### Failure handling

- **Deployment failure:** read the operation log for the first error, not the last. Do not retry blindly. Roll back the slot or revision to the last healthy version.
- **Connection failure to data service:** check, in order, DNS resolution, firewall or private endpoint state, identity role assignment, token audience, and connection string format. Change one variable at a time.
- **Quota or SKU unavailable:** report the exact error, propose an alternate region or SKU, and ask for approval.
- **Data corruption or accidental deletion:** stop writes if safe to do so, preserve the current state, identify the restore point, and request approval before any restore. Do not overwrite the live resource to test a restore; restore to a new target.
- **Unverifiable documentation claim:** if a setting cannot be confirmed against current official documentation, state that it is unverified and do not apply it.

### Deliverable contract

Every output must include:

1. **Summary:** one paragraph stating the goal, scope, and outcome.
2. **Resource inventory:** table of resource type, name, region, SKU (marked version-sensitive), identity, and network mode.
3. **Changes applied or proposed:** ordered list with the exact IaC file or command reference, and whether each step is destructive.
4. **Approval requests:** every gated action, with the risk and the rollback path.
5. **Verification results:** each check in the verification section marked pass, fail, or not tested, with evidence.
6. **Assumptions and open items:** including unverified version-sensitive details and missing RPO/RTO values.
7. **Rollback plan:** specific steps to return to the prior state.

Do not state that a deployment is production-ready, compliant, or secure unless the specific evidence for that claim is attached. Do not include secret values, connection strings, or keys in any output.

### Ultron routing contract

**Choose this skill when:** the work concerns Azure application workload resources and managed data services: App Service, Functions, Container Apps, Azure SQL, Cosmos DB, Storage, managed cache, deployment slots, backups, scaling, private connectivity, and workload-level operations.

**Choose `azure-landing-zone-identity` when:** the decision concerns tenant and subscription identity foundations: Entra roles, Azure RBAC scope, privileged access, managed/workload identity governance, service principals, emergency access, or identity-wide policy.

**Handoff contract:** the workload skill states the exact resource, environment, required capability, and least-privilege identity need. The identity skill returns the approved principal type, role or custom action set, scope, assignment path, and audit requirement. The workload skill then verifies that the application uses the identity without exposing secrets. Do not create broad tenant permissions to make an application deployment convenient.

**Why the boundary exists:** workload configuration consumes identity capabilities; it should not independently redefine the tenant's identity governance.


## azure-landing-zone-identity

**Use when:** Use when designing, reviewing, or troubleshooting identity foundations for an Azure landing zone, including Microsoft Entra ID tenant structure, RBAC role assignments, management group scope, managed identities, privileged access, and break-glass accounts.

### Purpose and boundaries

This skill guides the identity layer of an Azure landing zone: who can act, at what scope, with which privilege, and how that is proven and audited. It covers Microsoft Entra ID (tenant and directory configuration relevant to Azure access), Azure RBAC at management group, subscription, and resource scope, managed identities, workload identity, privileged access, and emergency access.

It does not cover network topology, policy-as-code authoring beyond identity-related policies, workload application auth design, or on-premises AD federation internals beyond the trust boundary. Hand those to the relevant skills.

### Inputs and assumptions

Collect before acting:

- Management group hierarchy (exported, not recalled from memory).
- Subscription inventory with owners, environment tags, and workload classification.
- Current role assignments at each management group and subscription, exported to a file.
- Entra ID licensing tier, since PIM, conditional access, and access reviews depend on it. Verify feature availability against current Microsoft documentation.
- Identity sources: cloud-only, synced, or federated users, and any external identities.
- Compliance obligations stated by the organization. Do not assume a framework is in scope; ask.

Assumptions must be written down in the deliverable. Any version-sensitive behavior (role names, portal labels, CLI syntax, licensing requirements) must be marked "verify against current official documentation" unless you have confirmed it in this session.

### Operating workflow

1. **Baseline.** Export management group tree, role assignments (including inherited and deny assignments where readable), Entra directory roles, and service principals with credentials. Store exports as evidence.
2. **Classify principals.** Group every principal as human user, group, service principal, managed identity, or external guest. Flag any principal with Owner or User Access Administrator above subscription scope.
3. **Map intent to scope.** For each required capability, choose the narrowest scope that serves the workload. Prefer resource group scope for application teams, subscription scope for platform operations, and management group scope only for cross-cutting governance roles.
4. **Select built-in roles first.** Use a built-in role whose actions match the need. Create a custom role only when no built-in role fits and document the exact action list and its owner.
5. **Assign through groups.** Bind roles to Entra groups, not individual users. Group names encode scope, function, and environment, for example `az-sub-prod-network-contributor`.
6. **Replace standing privilege.** Make elevated roles eligible rather than active where licensing allows, with justification, approval, and time limits.
7. **Use managed identities.** Replace stored secrets for Azure-hosted workloads with managed identities. Where a service principal is unavoidable, record its owner, purpose, credential type, and expiry.
8. **Configure break-glass.** Two or more cloud-only emergency accounts, excluded from routine conditional access only as documented, with credentials held under dual control and sign-in monitored.
9. **Validate and hand off.** Run the checks in the verification section and produce the deliverable.

### Decision gates

Stop and obtain explicit human approval before proceeding if any step would:

- Delete, move, or re-parent management groups or subscriptions.
- Remove role assignments, disable accounts, or delete service principals that may be in use.
- Grant Owner, User Access Administrator, Global Administrator, or any tenant-wide role.
- Change conditional access policies or exclusions that could lock out administrators.
- Rotate or revoke credentials for production workloads.
- Alter external sharing, guest invitation, or cross-tenant settings.
- Touch emergency access accounts.
- Apply changes to a production scope from a non-production analysis.

Approval must name the specific change, scope, and rollback step. A general "go ahead" is not sufficient for gates on irreversible actions. Read-only exports and analysis do not require approval.

### Verification and evidence

Each finding and change must be backed by evidence:

- **Least privilege check:** Count principals holding Owner or User Access Administrator at management group and subscription scope. Target: each count justified in writing, with zero unexplained entries.
- **Standing privilege check:** Percentage of elevated assignments that are eligible rather than active. Report the baseline and the target.
- **Secret exposure check:** Number of service principals with password or certificate credentials older than the organization's rotation standard. Report by owner.
- **Orphan check:** Role assignments whose principal no longer exists or is disabled. Target: zero.
- **Break-glass check:** Confirm at least two emergency accounts exist, have been tested in a sign-in exercise within the last review period, and that the test is logged.
- **Drift check:** Compare the current export against the approved baseline; every difference must map to a ticket or approval.

Record the date, tool, command or portal path, and operator for each check. Do not report a check as passed unless its output was reviewed.

### Failure handling

- **Export incomplete or permission denied:** Stop the affected analysis, record the gap, and do not infer missing assignments. Request the reader role needed.
- **Assignment cannot be removed due to dependency:** Document the dependent resource and owner, add a remediation item, and do not force removal.
- **Lockout risk discovered:** Halt changes to conditional access or role removal affecting administrators. Escalate to the tenant owner.
- **Conflicting requirements between teams:** Present the options with scope, risk, and cost; decision belongs to the accountable owner.
- **Unverifiable version behavior:** Mark the item as unverified in the deliverable instead of asserting a behavior.

### Deliverable contract

Produce a single report containing:

1. Scope statement and assumptions list.
2. Principal and role inventory summary with counts per scope.
3. Findings table: finding, scope, evidence reference, risk rating, proposed action, approval required (yes/no).
4. Ordered remediation plan with rollback step for each change.
5. Verification results for each check in the verification section, with status and evidence location.
6. Open items, including every unverified version-sensitive detail.

Do not include secrets, credential values, tokens, or full tenant identifiers in the report; reference them by a stable internal label.

### What not to do

- Do not assign Owner as a convenience to unblock a team.
- Do not assign roles to individual users when a group exists or should exist.
- Do not create a shared account for administrators.
- Do not store secrets in pipelines, scripts, or documents when a managed identity or federated credential is available.
- Do not remove emergency access or change its exclusions without approval.
- Do not state licensing, compliance, or feature availability as fact without verifying it against current Microsoft documentation.

### Ultron routing contract

**Choose this skill when:** the question concerns Azure identity and authorization foundations across tenants, management groups, subscriptions, and resources: Entra directory roles, Azure RBAC, managed identities, workload identities, privileged access, emergency accounts, and identity governance.

**Choose `azure-app-and-data-services` when:** the work is configuring or operating a particular application host or managed data service and only needs a workload-specific identity decision.

**Handoff contract:** receive the workload's exact resource scope, required actions, environment, principal lifecycle, and operational owner. Return the narrowest viable principal and role assignment, approval requirements, and verification evidence. Avoid granting subscription- or tenant-wide authority for a resource-level workload need.

**Why the boundary exists:** identity policy is a shared security foundation; application services are consumers of that foundation and must not create their own exceptions without governance.


## gcp-serverless-and-data

**Use when:** Use when designing, deploying, reviewing, or troubleshooting Google Cloud serverless workloads (Cloud Run, Cloud Functions, Cloud Scheduler, Pub/Sub, Eventarc) or data pipelines (BigQuery, Dataflow, Cloud Storage landing zones, Composer/Workflows orchestration) and needing concrete, verifiable guidance.

### Purpose and boundaries

This skill guides design, deployment, review, and incident work for event-driven serverless services and batch or streaming data pipelines on Google Cloud. It covers:

- Compute: Cloud Run services and jobs, Cloud Functions, Cloud Scheduler triggers.
- Messaging and events: Pub/Sub topics and subscriptions, Eventarc routing.
- Data: BigQuery datasets, tables, scheduled queries, load and streaming ingestion; Dataflow pipelines; Cloud Storage landing and archive buckets.
- Orchestration: Workflows and Cloud Composer DAG-level decisions.

It does not cover cluster administration (GKE internals), network architecture beyond service-facing ingress/egress choices, or cost negotiation with Google.

### Inputs and assumptions

Before acting, collect:

1. Project ID(s), region(s), and environment (dev, staging, prod).
2. Workload type and trigger model (HTTP, Pub/Sub push or pull, scheduled, storage event, batch).
3. Expected throughput, payload size, latency target, and acceptable data loss window.
4. Data classification and residency constraints.
5. Current IAM bindings and service account identities in use.
6. Existing IaC (Terraform, Deployment Manager, gcloud scripts) and whether it is source of truth.

Assumptions must be stated explicitly. If any input is missing and it changes the design, stop and ask.

Version-sensitive details (command flags, quota values, runtime versions, pricing, feature availability and GA/preview status) must be verified against current official Google Cloud documentation before being presented as fact.

### Operating workflow

1. **Classify the workload.** Request/response, asynchronous event, scheduled batch, or continuous stream. The classification determines the service choice.
2. **Select the runtime.** Use Cloud Run for containerized HTTP or event-handling services and for jobs with bounded runtime. Use Cloud Functions for small single-purpose handlers. Use Dataflow for streaming or large parallel transforms. Use BigQuery SQL (scheduled queries or Workflows calls) when transformation is set-based and fits in the warehouse.
3. **Define identity first.** Create one dedicated service account per workload with the minimum roles on specific resources. Never reuse the default Compute Engine service account in production.
4. **Design the event path.** For Pub/Sub, define acknowledgement deadline, retry policy, dead-letter topic, and ordering need. Make every consumer idempotent using a stable message or business key.
5. **Design the data path.** Choose partitioning and clustering on BigQuery tables based on the dominant filter and join columns. Set table expiration or partition expiration where retention is defined.
6. **Write configuration as code.** Keep service definitions, IAM bindings, and schedules in version-controlled IaC. Deploy from CI, not from workstations.
7. **Stage and promote.** Deploy to non-production with representative data volume, run the verification checks below, then promote the same artifact digest.
8. **Document operational runbook entries**: alert conditions, replay procedure, and rollback steps.

### Decision gates

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

### Verification and evidence

Each deliverable must include evidence for these checks:

- **Idempotency:** Replay one message twice in staging; the resulting row count and side effects are identical.
- **Retry and DLQ:** Force a handler failure; confirm redelivery count matches configuration and the message lands in the dead-letter topic after the maximum attempts.
- **Latency:** Measure p95 and p99 request or processing latency under the expected load profile. Report the measured numbers, not the target.
- **Least privilege:** List every granted role per service account with its resource scope; confirm no primitive roles.
- **Data correctness:** For pipeline changes, compare row counts and a checksum or aggregate (sum of a key measure, distinct key count) between source and target for a defined window.
- **Cost guardrail:** Confirm budget alerts exist and BigQuery bytes-scanned estimate is recorded for new queries.
- **Observability:** Confirm logs include a correlation ID, errors are alerting-routed, and dashboards show request count, error rate, and backlog age (Pub/Sub oldest unacked message age).

Quote exact command output or console-exported values as evidence. Do not state a check passed without the artifact.

### Failure handling

- **Duplicate processing detected:** Halt consumer scaling, identify the dedup key, and fix idempotency before resuming. Do not manually delete downstream rows without approval.
- **Backlog growing:** Check consumer error rate first, then max instances or concurrency limits, then downstream quota (BigQuery streaming or API limits). Scale only after cause is identified.
- **Permission errors after deploy:** Verify the runtime service account, not the deployer's identity, holds the needed role on the specific resource. Add the narrowest role and record the change.
- **Schema mismatch on load:** Quarantine the file or message to a separate bucket or topic. Do not auto-coerce types silently.
- **Timeout on long jobs:** Move work to a Cloud Run job or Dataflow batch rather than raising request timeouts beyond the documented maximum.
- **Unknown or conflicting documentation:** State the conflict, cite the official page checked, and escalate rather than guessing.

### Deliverable contract

Every output must contain:

1. Workload classification and chosen services with a one-line justification each.
2. Identity table: service account, roles, resource scope.
3. Configuration summary: triggers, retry policy, DLQ, partitioning or clustering, retention.
4. Verification results with captured evidence for each applicable check.
5. Open assumptions and items marked for verification against current official documentation.
6. Rollback procedure and the named approval gates that apply.

Do not claim performance numbers, cost savings, or compliance certifications without measured or documented evidence. Do not invent flags, API fields, or version numbers; mark them for verification instead.


## serverless-edge-functions

**Use when:** Use when designing, writing, deploying, or debugging serverless functions that run at CDN or edge locations, including request rewriting, auth gating, header and cache logic, A/B routing, and lightweight API responses under strict CPU, memory, and latency limits.

### Purpose and boundaries

Use this skill to produce edge function code and its deployment plan: request inspection, routing, header and cache manipulation, auth gating, redirects, and small synthesized responses that execute close to the user. It covers design trade-offs, runtime constraints, testing, and rollout.

Out of scope: long-running jobs, large data processing, stateful transactional writes to primary databases from the edge, and full origin-replacing application logic. If the task needs those, recommend a regional function or origin service instead.

### Inputs and assumptions

Collect before writing code:

1. Target platform and runtime (for example, a specific edge provider's worker or isolate model). Treat its limits as version-sensitive.
2. Trigger points: viewer request, origin request, origin response, viewer response, or equivalent.
3. Latency budget, expected request volume, and cache hit ratio goal.
4. Data needed: headers, cookies, geo fields, and any external calls. Note which are available at the edge and which are not.
5. Existing cache keys, cache TTLs, and origin behavior.
6. Security requirements: which paths need auth, which tokens or keys are involved, and where secrets are stored.

Assumptions must be written down. If the platform's CPU time, memory, subrequest count, bundle size, or header limits are not confirmed, mark them "verify against current official documentation" and do not state numbers.

### Operating workflow

1. **Define the single responsibility.** One function, one job (for example, "normalize locale redirects"). Reject bundles that mix auth, caching, and personalization without separation.
2. **Map the trigger.** Select the earliest stage that satisfies the need. Header normalization belongs on the viewer request; cache key adjustments usually belong before cache lookup; origin-specific header injection belongs on the origin request.
3. **Write a pure core.** Put routing and decision logic in a function that takes a plain request descriptor and returns an action (pass, redirect, rewrite, respond). Keep platform bindings in a thin adapter.
4. **Bound all work.** No unbounded loops, no recursive parsing of untrusted input, and no external fetch without a timeout and a fallback path.
5. **Handle failure explicitly.** Any error in the edge path must either pass the request through unchanged or return a defined error response. Never leave the response undefined.
6. **Test locally** with fixtures covering: missing headers, malformed cookies, oversized URLs, unicode paths, duplicate query keys, and boundary geo values.
7. **Stage the rollout:** deploy to a non-production route, compare responses against the baseline on sampled traffic, then increase exposure in steps.

### Decision gates

- **Gate A: Is edge the right place?** Proceed only if the logic is stateless or reads cacheable data, and needs to run before origin. If it needs a consistent write or heavy compute, stop and escalate.
- **Gate B: Does it touch secrets or auth?** Requires explicit approval from the service owner before implementation. Verify tokens with asymmetric signatures or platform-provided key stores; never embed secrets in source.
- **Gate C: Does it alter cache keys or vary headers?** Requires approval because it can cause cache poisoning or fragmentation. Show the before and after cache key for three sample requests.
- **Gate D: Does it change redirects or status codes for production paths?** Requires approval and a rollback plan with the previous configuration preserved.
- **Gate E: Does it call an external service?** Requires approval for the destination, timeout, retry policy, and data sent. Forwarding user identifiers or personal data needs a documented justification.

### Verification and evidence

Each deliverable must include:

- Unit tests for the pure core, covering every decision branch.
- A fixture table: input request, expected action, actual result.
- Measured or estimated bundle size, checked against the platform's current documented limit.
- A cache behavior check: the same URL requested twice, confirming hit or miss status as expected, with the vary and key settings noted.
- A canary result: error rate, p95 added latency, and status-code distribution compared against baseline. If no canary has run, state "not yet measured" and do not claim improvement.

Do not report performance gains without a measured baseline.

### Failure handling

- **Runtime exception:** return pass-through to origin if the request is safe to forward; otherwise return a static 500 with no internal detail.
- **Timeout on external call:** use the cached or default decision defined in the design; log the event with a request identifier.
- **Unexpected input shape:** treat as untrusted, reject with 400 for API paths, or pass through for content paths. Do not throw.
- **Rollback trigger:** error rate above the baseline threshold agreed in the plan, or any auth bypass observed. Roll back first, then diagnose.

### Deliverable contract

Return:

1. Function purpose statement (one sentence).
2. Trigger stage and platform assumptions, with version-sensitive items marked.
3. Source code: pure core and adapter, separated.
4. Configuration: route patterns, cache key settings, and environment variable names (no values).
5. Test suite and fixture table.
6. Gate status: which of A–E applied, and what approval is still pending.
7. Rollout and rollback steps with thresholds.

Do not include real secrets, invented platform flags, unverified benchmark numbers, or statements of compliance certification. Do not deploy to production paths, modify live cache rules, or alter auth behavior without explicit approval from the named owner.


## supabase-platform

**Use when:** Use when designing, provisioning, migrating, securing, or troubleshooting a Supabase project that combines Postgres schemas, row-level security, auth-linked tables, Storage buckets, or Realtime and Edge Function integrations.

### Purpose and boundaries

This skill guides work on a Supabase project's data and storage layer: Postgres schema and migrations, row-level security (RLS), Storage buckets and object policies, auth-linked user data, and the supporting Realtime and Edge Function touchpoints where they affect data access.

In scope: schema design, RLS policy authoring and review, Storage bucket configuration, migration sequencing, key and role hygiene, access-pattern verification, and diagnosing permission or data-access failures.

Out of scope: general Postgres tuning beyond what a Supabase project exposes, frontend client implementation, billing and plan decisions, and any claim about certifications or regulatory compliance. Those require separate review.

### Inputs and assumptions

Before acting, confirm:

1. Target environment (local, staging, production) and the project reference the user intends to change.
2. Current schema source of truth: migration files, dashboard-edited state, or both. Drift between them is a primary failure cause.
3. Access model: which roles call the database (anon, authenticated, service role, direct connections) and which tables hold per-user data.
4. Storage intent: public versus private buckets, expected file sizes, MIME types, and who uploads and reads.
5. Current Supabase CLI and documentation version. Treat exact CLI commands, dashboard labels, and feature availability as version-sensitive; verify them against current official Supabase documentation before issuing them to the user.

If any input is missing and it changes the outcome, ask. Do not assume production.

### Operating workflow

1. **Snapshot current state.** Capture the existing schema, policies, grants, and bucket settings. Record them before any edit.
2. **Map access paths.** For each table and bucket, list every role and operation (select, insert, update, delete, upload, download) that must succeed, and every one that must fail.
3. **Draft changes as migrations.** Express schema, RLS, grants, and bucket configuration as ordered, idempotent migration files. Avoid editing production through the dashboard alone.
4. **Enable RLS with policies in the same migration.** A table with RLS enabled and no policies denies all non-owner access; create policies deliberately, not after the fact.
5. **Scope policies to the authenticated subject.** Compare ownership columns against the authenticated user identifier obtained from the auth context. Index columns referenced by policies.
6. **Validate locally.** Apply migrations to a local or branch database, then run the access matrix from step 2 using each role.
7. **Review diffs.** Confirm that the only changes are the intended ones.
8. **Stage, then promote.** Apply to staging, run the same matrix, then request approval before production.

### Decision gates

Stop and obtain explicit user approval before:

- Dropping, truncating, or renaming tables, columns, policies, buckets, or schemas.
- Running any data-modifying statement against a non-local database.
- Making a bucket public, or loosening any policy so that anon or unauthenticated access expands.
- Rotating or revealing keys, JWT secrets, or database passwords.
- Changing auth provider settings, email templates, or redirect URLs, which affect external users.
- Deleting Storage objects or altering object retention.
- Any operation that cannot be reversed by a down migration or restore.

Proceed without a gate for read-only inspection, writing new migration files, and local validation.

Use the service role key only in trusted server contexts. Never place it in client code, logs, or chat output.

### Verification and evidence

Quality checks are measurable:

- **Access matrix pass rate:** 100% of expected allow and deny outcomes match across every role and operation listed in step 2. Record results as a table: role, operation, target, expected, actual.
- **RLS coverage:** every table in exposed schemas has RLS enabled unless a written justification exists. Query the catalog for tables where row security is off and confirm each exception.
- **Policy completeness:** each operation on each RLS table has an explicit policy or a documented reason for denial.
- **Index check:** every column used in a policy predicate has a supporting index, verified with an execution plan on a representative row count.
- **Storage check:** upload of a disallowed MIME type or oversized file is rejected; download of another user's private object is denied.
- **Migration idempotency:** applying the migration set twice to a fresh database yields an identical schema dump.

Attach evidence (query output, plan excerpts, matrix table) to every completed change.

### Failure handling

- **Permission denied on a query that should succeed:** check the role in use, whether RLS is enabled, whether a matching policy exists for that command, and whether the policy expression evaluates true for the test user. Do not respond by adding a broad `using (true)` policy.
- **Empty results instead of errors:** RLS silently filters rows. Compare results against an elevated context in staging only.
- **Migration drift:** when the dashboard state differs from migration files, stop, capture both, and ask the user which is authoritative. Do not overwrite silently.
- **Failed migration partway:** do not re-run blindly. Inspect applied state, write a corrective migration, and gate it.
- **Storage upload failures:** inspect bucket policy, object path, and MIME configuration before changing anything.

### Deliverable contract

Every deliverable includes:

1. Summary of intended change and affected environments.
2. Migration files or SQL, in apply order, with a matching down or rollback path where feasible.
3. Access matrix with actual results.
4. Explicit list of gated actions requiring approval, and the status of each.
5. Version-sensitive items flagged for verification against current official Supabase documentation.
6. Residual risks and anything not tested.

Do not state that a configuration is secure, compliant, or audit-ready. State only what the matrix and catalog checks demonstrated.

