# Cloud Infrastructure and Operations

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## cicd-and-progressive-delivery

**Use when:** Use when designing, reviewing, or troubleshooting CI/CD pipelines and progressive delivery rollouts (canary, blue-green, feature-flag gating, automated rollback) for services deployed to cloud or container platforms.

### Purpose and boundaries

This skill guides the design and review of build, test, and deployment pipelines and the staged rollout of changes to production traffic. It covers:

- Pipeline stage structure, artifact promotion, and environment parity.
- Rollout strategies: rolling, blue-green, canary, and percentage or cohort-based feature flags.
- Metric-driven promotion and automated or manual rollback decisions.

It does not cover: application architecture, infrastructure provisioning internals (see infrastructure-as-code skills), incident command, or security tooling selection. Tool-specific syntax must be checked against current vendor documentation; this skill does not assert exact flags, field names, or versions.

### Inputs and assumptions

Before proposing changes, collect:

1. Service inventory: runtime, deployment target (Kubernetes, VM fleet, serverless, managed PaaS), statefulness, and dependency graph.
2. Current pipeline definition and the last 20 run outcomes with durations.
3. Existing SLIs and SLOs (error rate, latency percentiles, saturation) and their data source.
4. Database and schema change history; whether migrations are backward compatible.
5. Traffic profile: request volume, peak windows, and minimum volume needed for statistically meaningful canary comparison.
6. Rollback mechanism currently available and its measured time to execute.

If any input is missing, state the assumption explicitly in the deliverable. Do not assume zero-downtime capability, schema compatibility, or metric coverage without evidence.

### Operating workflow

1. **Map the path to production.** List every stage from commit to full traffic. Mark each stage as automated, manual, or gated, and record its median duration.
2. **Verify artifact immutability.** Build once; promote the same digest or artifact through environments. Rebuilding per environment is a finding.
3. **Check test placement.** Unit and static checks run on every commit; integration and contract tests run before artifact promotion; end-to-end smoke tests run after each deploy. Flag suites that run only nightly on a path that ships daily.
4. **Classify each change.** Label as stateless code, configuration, schema migration, or infrastructure. Each class has a different rollout ceiling (see Decision gates).
5. **Select a strategy per service tier.** Match the strategy to blast radius and rollback speed.
6. **Define promotion metrics before rollout.** Write the thresholds in the plan: for example, canary error rate no more than baseline plus a stated margin, p99 latency within a stated ratio of baseline, and no new error signatures in logs. Thresholds must be derived from observed baseline data, not chosen arbitrarily.
7. **Specify rollback triggers and procedure.** Automated rollback on hard SLO breach; human decision on soft signals. Record the expected rollback duration and test it.
8. **Produce the rollout plan** using the deliverable contract below.

### Decision gates

- **Canary sizing:** Do not conclude a canary comparison until the canary cohort has accumulated enough requests to detect the target regression at the chosen confidence level. If volume is too low, extend the observation window or use synthetic traffic, and say so.
- **Schema changes:** Require expand-then-contract sequencing. A deploy that removes or renames a column used by the previous version must not proceed without an explicit approval gate and a verified rollback path.
- **Feature flags:** Flags introduced for rollout must have an owner and a removal date. Flags controlling data-writing paths require the same review as schema changes.
- **Blue-green:** Permitted only when the environment doubles cost acceptably and session or cache state is shared or drainable.
- **Full promotion:** Requires that the canary or first cohort met all promotion thresholds for the defined window, with no unexplained error signatures.
- **Approval required (human, explicit):** Any production deployment outside the normal change window, any action that deletes data or environments, any rollback of a schema migration, any change affecting external customers or partners, and any step that touches credentials, secrets, or access policies.

### Verification and evidence

Each recommendation must cite evidence:

- Pipeline timing from actual run history, not estimates.
- Baseline metrics over at least one representative traffic cycle (for example, one full weekday peak).
- Canary comparison results showing both cohorts, the metric, the window, and sample sizes.
- Rollback rehearsal result with measured duration.

Quality checks:
- Every promotion threshold names a metric, a comparison baseline, a window, and an action.
- Artifact digest or version is identical across all promoted environments.
- Every stage has an owner and a failure action.
- No gate depends on a manual step that has no documented timeout or escalation.

### Failure handling

- **Failed promotion metric:** Halt the rollout at current percentage; do not auto-advance. Roll back if the breach is a hard SLO violation; otherwise hold and request review.
- **Inconclusive canary (insufficient data):** Extend the window once; if still inconclusive, report it as inconclusive rather than passing it.
- **Rollback failure:** Escalate immediately to the on-call owner. Do not attempt a second untested rollback path without approval.
- **Flaky tests blocking promotion:** Quarantine the test with a tracked ticket and an expiry; do not disable the gate globally.
- **Metric pipeline outage:** Treat as failed verification. Pause promotions; do not infer health from absence of alerts.

### Deliverable contract

The output must contain:

1. **Current-state summary:** stages, durations, strategy per service, and identified gaps.
2. **Change classification** for the proposed release.
3. **Rollout plan table:** step, traffic percentage, duration or sample requirement, promotion thresholds, rollback trigger.
4. **Assumptions register:** each unverified assumption with the verification owner.
5. **Approval requests:** list of actions requiring explicit human approval, with the risk and reversibility stated.
6. **Version-sensitive items:** any tool features, flags, or API behaviors referenced, marked "verify against current official documentation" with the vendor name.
7. **Open risks** ranked by impact.

Do not state that a deployment is safe, compliant, or guaranteed to meet any SLO. State what was measured and what remains unverified.

### What not to do

- Do not rebuild artifacts between environments.
- Do not set canary thresholds without baseline data.
- Do not advance a rollout on elapsed time alone.
- Do not run destructive operations (environment deletion, data rollback, forced database changes) without explicit approval.
- Do not disable failing gates to unblock a release.
- Do not present unverified tool behavior as fact.


## cloud-infrastructure-audits-and-deployment

**Use when:** Use when auditing an existing cloud environment (accounts, networks, identity, compute, storage, data stores, cost, logging) or planning and executing an infrastructure deployment change that must be verified, reviewed, and reversible.

### Purpose and boundaries

This skill covers two linked activities: (1) read-only audits that establish what exists, how it is configured, and where it deviates from stated requirements; and (2) controlled deployments that change infrastructure through reviewed, reversible steps. It applies to any major provider, and to infrastructure-as-code (IaC) and console-driven environments alike.

In scope: inventory, configuration review, identity and access review, network exposure, encryption and secrets handling, backup and recovery posture, logging and monitoring coverage, cost anomalies, plan-and-apply deployments, post-deployment verification, and rollback planning.

Out of scope: application code review, penetration testing or active exploitation, incident response during a live breach (hand off to the incident owner), compliance certification (this skill produces evidence, not attestations), and procurement or contract decisions.

### Inputs and assumptions

Before starting, confirm and record:

- Target scope: account or subscription identifiers, regions, projects, environments (prod, staging, dev), and explicit exclusions.
- Objective: audit question, or the change being deployed, with its success criteria.
- Access level granted: read-only roles for audits; for deployments, the named change owner and the approving party.
- Source of truth: IaC repository and commit, or "console-only" if none exists. Drift between the two is a finding in itself.
- Requirements baseline: internal standards, data classification, and any external framework the owner wants referenced. Do not assume a framework applies.
- Change window and freeze calendar.

Assumptions must be written down and labeled. If a provider feature, CLI flag, or quota behavior is version-sensitive, mark it "verify against current official documentation" and do not rely on memory for exact names or limits.

### Operating workflow

#### Audit track

1. Snapshot inventory. Enumerate resources per scope using read-only listing or export tools. Record counts by type, region, and owner tag. Save the raw output with a timestamp.
2. Identity review. List human and workload principals, privileged role assignments, long-lived credentials, unused principals (no activity in 90 days is a common starting threshold, adjust to policy), and cross-account trust.
3. Network exposure. Identify every resource reachable from the public internet: load balancers, public IPs, storage with public access settings, databases with public endpoints, and management ports. Trace each to a justified owner and purpose.
4. Data protection. Check encryption at rest and in transit settings, key ownership and rotation policy, backup enablement, backup retention, and whether restore has ever been tested (look for evidence, not claims).
5. Observability. Confirm audit/control-plane logging is enabled in all regions and retained to a location the workload team cannot alter. Confirm alerts exist for root or break-glass usage and for security-group or policy changes.
6. Cost and capacity. Flag unattached volumes, idle reserved capacity, oversized instances with sustained low utilization, and untagged spend. Report as observations; do not recommend termination without owner confirmation.
7. Classify findings using the severity table in Decision gates, then write the report.

#### Deployment track

1. Write the change request: target state, affected resources, dependencies, expected downtime (state "none" only if verified), and rollback procedure.
2. Produce a plan or dry run with the IaC tool or provider's preview mechanism. Save the full plan output.
3. Review the plan line by line. Every destroy, replace, or IAM/network-policy change requires explicit mention in the request.
4. Stage in a non-production environment first when one exists that mirrors the target configuration. Record differences that make staging non-representative.
5. Obtain approval (see gates), then apply the exact reviewed plan artifact. Never re-plan silently between review and apply; if the plan changed, return to step 3.
6. Verify (see Verification and evidence), then monitor for the agreed soak period before closing.
7. Record outcome, deviations, and any manual steps taken.

### Decision gates

Stop and obtain explicit written approval from the named owner before:

- Deleting, replacing, or resizing any stateful resource (databases, volumes, object buckets, key vaults, DNS zones).
- Changing IAM policies, role trust, or key material.
- Opening any inbound path to the internet or widening an existing one.
- Disabling logging, backups, encryption, or deletion protection, even temporarily.
- Any action affecting resources outside the approved scope, or that sends data to a new external party.
- Any apply performed outside a change window or during a freeze.
- Any action where rollback is partial or unknown.

Severity classification for audit findings:

- Critical: publicly reachable stateful data with no authentication, or privileged credentials exposed in plaintext. Escalate immediately.
- High: privileged access without MFA or review, logging disabled in a production account, backups absent for production data.
- Medium: overbroad but authenticated access, missing encryption-at-rest settings on non-sensitive stores, unowned resources.
- Low: tagging gaps, naming inconsistency, unused non-sensitive resources.

Proceed autonomously only with read-only inventory, plan generation, and report drafting.

### Verification and evidence

Every claim in a report needs a source: a command output, export file, or console screenshot reference, with timestamp and account identifier. Unsourced claims are excluded.

Deployment checks, all required before closing:

- Plan artifact applied matches the reviewed plan (hash or stored artifact ID recorded).
- Resource state matches the declared configuration on a fresh read, not the apply output alone.
- Health checks pass on every changed endpoint for the soak window.
- Security configuration re-audited: exposure, IAM, encryption, and logging for changed resources.
- Backup or snapshot taken before the change exists and is restorable (confirm restore metadata; a full restore test is required for stateful changes).
- Drift check: IaC source and live state agree; any manual change is either codified or reverted.

Audit quality bar: at least 95% of inventoried resources have an assigned owner tag or a recorded "unowned" finding; every critical or high finding has reproduction evidence and a named remediation owner.

### Failure handling

- Permission denied during audit: record the gap as a coverage limitation. Do not escalate privileges to fill it.
- Plan shows unexpected destroy: halt, do not apply, return to change owner with the diff.
- Apply partially fails: stop further changes, capture state and error output, and follow the pre-written rollback. If no rollback exists, escalate before any corrective action.
- Health check fails after apply: roll back if the rollback is verified and within window; otherwise escalate.
- Evidence conflicts (console versus IaC disagree): report both, treat live state as authoritative for risk, and do not "fix" either side without approval.
- Rate limits or timeouts: pause, record progress, resume from the last recorded checkpoint.

### Deliverable contract

Audit report, in this order:

1. Scope, timestamp, and access level used.
2. Coverage statement: what was checked, what was not, and why.
3. Findings table: ID, severity, resource, evidence reference, owner, recommended action.
4. Assumptions and version-sensitive items flagged for verification.
5. Recommended next actions requiring approval, listed separately.

Deployment record:

1. Change request and approvals with names and dates.
2. Plan artifact reference and reviewed summary of destroy/replace/IAM/network changes.
3. Apply result, verification evidence, and soak outcome.
4. Rollback procedure status and any deviations or manual steps.

Do not state that a system is compliant, secure, or fully recovered. State only what the evidence shows.


## cloud-infrastructure-cost

**Use when:** Use when analyzing, forecasting, or reducing cloud infrastructure spend that flows through external registries, such as container image registries, package mirrors, or artifact stores, including storage, egress, pull traffic, and retention costs.

### Purpose and boundaries

This skill covers cost attribution, analysis, and optimization for cloud resources whose spend is driven by external registries: image and artifact storage, cross-region or cross-cloud pulls, registry-to-compute egress, mirror synchronization, vulnerability-scan and replication features, and retention sprawl.

In scope: cost drivers, usage-to-cost mapping, retention and lifecycle policy proposals, pull-path redesign (caching, regional placement), and savings estimates with stated confidence.

Out of scope: general application performance tuning, changing production registry access controls, deleting or moving artifacts, purchasing commitments, and making claims about provider pricing without a current source.

### Inputs and assumptions

Collect before analysis:

- Billing exports for the review window (minimum 30 days; 90 preferred to capture release cycles).
- Registry inventory: repositories, artifact counts, total stored bytes, tag and digest counts.
- Pull and push telemetry: request counts, bytes transferred, source region, destination region or cluster.
- Topology: which compute environments pull from which registries, and across which network boundaries.
- Retention and lifecycle policies currently configured, and who owns each repository.

Assumptions must be written down explicitly. Pricing is version-sensitive: treat all unit prices as unverified until checked against the provider's current pricing documentation and the contracted rate card. Do not use remembered prices.

### Operating workflow

1. **Define the window and currency.** Fix the date range, currency, and whether figures are amortized or on-demand.
2. **Attribute spend.** Map each billing line item to a cost category: storage, inter-region transfer, internet egress, managed feature fees, or compute tied to pulls. Items without an owner go into an explicit "unattributed" bucket, which must stay under 10% of total spend before recommendations are finalized.
3. **Rank drivers.** Sort categories by monthly cost. For the top five repositories or paths, compute cost per pull and cost per stored GB-month.
4. **Diagnose waste patterns.** Check for: untagged or orphaned digests still referenced by nothing; excessive historical tags; the same image duplicated across regions; cross-region pulls where a regional replica would serve; CI pipelines pulling uncached base layers repeatedly; mirrors syncing content that is never consumed.
5. **Model options.** For each candidate change, estimate monthly savings as a range: low, expected, high. Show the formula and inputs.
6. **Rank by value and risk.** Prefer changes that remove stored bytes nobody references or that keep traffic within a region, over changes that alter how builds authenticate or resolve images.
7. **Draft the change plan**, staged so each step is reversible and measurable.

### Decision gates

- **Gate A (before any deletion or lifecycle enforcement):** Requires written owner approval per repository, a list of digests to be affected, and confirmation that no environment pins them. Obtain explicit approval; do not proceed on inference.
- **Gate B (before replication or regional changes):** Requires approval because it changes data residency and external-facing traffic. Confirm compliance owners have reviewed.
- **Gate C (before changing pull credentials, endpoints, or DNS):** Requires explicit approval and a rollback path. Treat as external-impacting.
- **Gate D (before committing spend commitments or sharing estimates externally):** Requires approval from the budget owner.

If a gate is not cleared, record the recommendation as "pending approval" and stop that branch.

### Verification and evidence

- Reconciliation: recomputed category totals must match billing totals within 2%.
- Savings claims require a before-and-after measurement plan, not just a projection.
- Every recommendation cites its evidence: billing line, telemetry query, or inventory record.
- Dry-run lifecycle rules where the platform supports it; if dry-run is unavailable, state that and reduce confidence.
- Confirm all version-sensitive product behavior, pricing, and feature availability against current official documentation, and record the retrieval date.

### Failure handling

- **Missing telemetry:** Lower confidence one tier and report the gap; do not backfill with estimates presented as measurements.
- **Unattributed spend above 10%:** Stop recommendations and report the attribution gap first.
- **Conflicting numbers between billing and telemetry:** Report both, identify the likely cause (timezone, currency, aggregation window), and resolve before ranking.
- **Owner unreachable for a gate:** Hold the change. Do not treat silence as approval.

### Deliverable contract

Produce a single report containing:

1. Scope and window, with currency and pricing verification date.
2. Spend attribution table: category, monthly cost, share, owner.
3. Top drivers with cost per pull and cost per stored GB-month.
4. Recommendations table: action, evidence reference, savings low/expected/high, confidence, gate required, status.
5. Staged change plan with rollback steps and success metrics.
6. Open questions and approvals outstanding.

Do not include unverified prices, invented tool flags, or guarantees of savings or compliance outcomes.


## cloud-kubernetes-devops

**Use when:** Use when deploying, upgrading, or troubleshooting workloads on managed or self-hosted Kubernetes that pull images or charts from external registries, including image pull failures, credential rotation, digest pinning, mirroring, and registry-related admission decisions.

### Purpose and boundaries

This skill covers how Kubernetes workloads obtain artifacts from registries outside the cluster's own network boundary: container images, Helm charts, and OCI artifacts. It covers pull authentication, image reference hygiene, mirroring and caching decisions, rate-limit and availability risk, and verification of pulled artifacts before they run.

It does not cover general cluster provisioning, application code changes, or building images from source except where build output must be verified before publication.

### Inputs and assumptions

Collect before acting:

- Cluster type and version, provider, and the namespaces and service accounts in scope.
- Full image references currently deployed, including tags and digests where present.
- Registry hostnames, their authentication method, and who owns the credentials.
- Network path constraints: egress rules, proxies, private endpoints, air-gapped segments.
- Compliance or change-control requirements that apply to the environment.

Assume nothing about registry rate limits, retention policies, or signing support. Verify each against the provider's current documentation. Kubernetes API behavior, admission features, and pull-secret mechanics vary by version; treat exact field names and feature gates as version-sensitive and confirm them in the official reference for the cluster's version.

### Operating workflow

1. **Inventory.** List every distinct registry host referenced by running pods, pending pods, and chart values. Group by namespace and owner.
2. **Classify each reference.** Record whether it uses a mutable tag, a digest, or a tag resolved at deploy time. Flag `latest` and unpinned branch-style tags.
3. **Map credentials.** For each registry, identify the secret type, the namespaces it is bound to, the service accounts that reference it, and its expiry or rotation mechanism.
4. **Check reachability.** From a node or a debug workload with the same network policy, confirm DNS resolution and TLS connectivity to each registry. Do not infer reachability from another environment.
5. **Plan the change.** Prefer, in order: pin by digest, add a mirror or pull-through cache, then adjust credentials. Each change is a separate, reversible step.
6. **Stage and observe.** Apply to a non-production namespace first. Watch pod events and image pull status, not only deployment rollout status.
7. **Promote** only after the verification checks below pass.

### Decision gates

Stop and request explicit approval before:

- Deleting or rotating pull secrets, service account bindings, or registry credentials.
- Changing image references in production workloads, including digest updates.
- Adding or removing mirrors, changing DNS or egress rules, or altering proxy settings.
- Enabling or changing admission policies that can reject pods cluster-wide.
- Any action that publishes images or charts to an external registry, or that sends credentials to a third party.
- Garbage collection or retention changes in a registry you do not own.

Proceed without approval only for read-only inventory, dry-run or server-side validation, and changes confined to a sandbox namespace that you created.

### Verification and evidence

Measurable checks before promotion:

- Every production image reference resolves to a digest. Count of unpinned references must be zero, or each exception must have a recorded owner and expiry date.
- Pull success rate on the target nodes is 100% across at least one full rollout, with no `ErrImagePull` or `ImagePullBackOff` events in the window.
- Each pull credential is bound only to the namespaces and service accounts that need it. Verify with a listing of bindings, not from memory.
- Mirror content matches upstream digests for the sampled set. Record the comparison output.
- If signature or attestation verification is in use, record the verifier identity and policy name used. Do not claim verification passed without the tool output.
- Rollback path tested: the previous digest is recorded and redeployable.

Keep the evidence: command output, event excerpts, digest lists, and change ticket references.

### Failure handling

- **Unauthorized (401/403):** Check the secret's type, the registry host string exactly as referenced in the image, and token expiry. Do not reuse credentials from another team to unblock.
- **Not found (manifest unknown):** Confirm the tag or digest exists upstream. Do not retag or push to satisfy the reference.
- **Rate limited or throttled:** Reduce pull concurrency, use an authenticated identity if policy allows, or introduce a cache. Do not disable retries across the cluster.
- **TLS or DNS failure:** Check the certificate chain, proxy configuration, and node resolver. Involve the network owner before changing trust stores.
- **Partial rollout stall:** Pause the rollout, identify the failing node set, and roll back the affected revision if pods are unavailable.

Escalate to the registry or platform owner when the failure involves provider-side incidents or shared credentials.

### Deliverable contract

Produce a short change record containing:

1. Scope: clusters, namespaces, and registries affected.
2. Inventory summary with counts of pinned, unpinned, and exception references.
3. Planned changes, each marked with the approval gate it passed or is awaiting.
4. Verification results with the raw evidence references listed above.
5. Rollback steps with the exact prior references.
6. Open risks, including any version-sensitive behavior not yet confirmed against official documentation.

Do not state that a deployment is secure, compliant, or certified. State only what was observed and verified.


## containers-and-kubernetes

**Use when:** Use when building, reviewing, debugging, or operating container images and Kubernetes workloads, including Dockerfile hardening, manifest design, rollout and rollback decisions, resource sizing, and cluster troubleshooting.

### Purpose and boundaries

This skill covers the practical lifecycle of containerized workloads: building images, writing and reviewing Kubernetes manifests, deploying and rolling out changes, diagnosing failing pods, and sizing resources. It applies to application teams and platform teams working with a Kubernetes cluster and an OCI-compatible build toolchain.

In scope: Dockerfile and build hygiene, image tagging and provenance, workload manifests (Deployment, StatefulSet, Job, CronJob, Service, Ingress or Gateway, ConfigMap, Secret references, HorizontalPodAutoscaler, PodDisruptionBudget, NetworkPolicy), rollout strategy, probes, resource requests and limits, and incident-level pod diagnosis.

Out of scope: cluster provisioning from scratch, cloud-account IAM design, service mesh internals, and application code changes beyond what a container requires. Route those to the relevant domain skill.

### Inputs and assumptions

Gather before acting:

1. Target cluster name, environment (dev, staging, production), and Kubernetes version. Treat API availability and field support as version-dependent.
2. Current manifests or Helm/Kustomize source, and the image reference being deployed.
3. Application runtime, listening ports, startup time, graceful shutdown behavior, and whether it is stateful.
4. Observed symptoms, recent changes, and relevant events or logs.
5. Access level. Assume read-only access unless the user explicitly grants write access for a named namespace and action.

If any of these are missing and they change the recommendation, ask. Do not assume a production cluster is a test cluster.

### Operating workflow

1. **Classify the request**: build, manifest review, deployment, rollback, or diagnosis.
2. **Establish current state** with read-only commands: current image digest, desired versus available replicas, recent events, and rollout status.
3. **Make the smallest change** that addresses the stated problem. Prefer declarative edits to manifests in version control over imperative patches to live objects.
4. **Validate before apply**: schema and server-side dry-run, policy checks if the cluster uses them, and diff against the live object.
5. **Roll out incrementally**: one namespace or one cluster at a time, watching readiness and error rates.
6. **Verify** against the criteria in the verification section before declaring success.

For Dockerfiles: use a multi-stage build; pin base images by digest or a deliberate tag; copy dependency manifests before source to preserve layer caching; run as a non-root user with an explicit numeric UID; exclude secrets and build context junk with `.dockerignore`; keep the final stage minimal.

For manifests: set `resources.requests` on every container; set `resources.limits` for memory and make a deliberate decision on CPU limits; define readiness and liveness probes with different semantics (liveness must not depend on downstream dependencies); set `terminationGracePeriodSeconds` to match real shutdown time; use `preStop` only when the application needs it; add a PodDisruptionBudget for multi-replica workloads that must survive node drains.

### Decision gates

Stop and request explicit approval before any of the following:

- Deleting or recreating any namespace, PersistentVolumeClaim, StatefulSet, or stateful data path.
- Changing a Service selector, Ingress host, or LoadBalancer type in a way that alters external traffic.
- Applying changes to production or any cluster the user has not named.
- Modifying RBAC bindings, admission policies, NetworkPolicies that restrict traffic, or Secret contents.
- Force-deleting pods, draining nodes, or running `kubectl delete` with broad selectors or `--all`.
- Pushing or retagging images in a shared registry, or overwriting an existing tag.
- Rollbacks that discard database migrations or data written by the new version.

Proceed without a gate only for read-only inspection, local builds, rendering manifests, and dry-run validation.

Choose a rollout strategy by criteria: use RollingUpdate with `maxUnavailable: 0` when capacity is tight and the app tolerates mixed versions; use a blue/green or canary approach when the change alters an API contract; use Recreate only when two versions cannot run concurrently and downtime is approved.

### Verification and evidence

A change is verified only when all of these hold:

- `kubectl rollout status` reports completion within the expected window for the workload.
- All new pods are Ready, with zero restarts since the rollout began, or restarts are explained and accepted.
- The running image digest matches the digest built and approved, confirmed from the pod spec, not from the tag.
- Service endpoints list the expected pod IPs, and a smoke request through the real ingress path succeeds.
- Error rate and latency for the workload are within the pre-change baseline on the monitoring system you have access to. State the baseline value and the observed value.
- For autoscaled workloads, the HPA reports current metrics (not `unknown`).

Record evidence: the command, the timestamp, and the relevant output excerpt. Do not report success based on the apply command returning without error.

### Failure handling

Diagnose in this order: events, then pod status, then logs, then node and cluster conditions.

- **ImagePullBackOff / ErrImagePull**: verify the reference, the registry credentials in the referenced pull secret, and network reachability. Do not add broad credentials to work around it.
- **CrashLoopBackOff**: read `previous` container logs; check the exit code (137 typically indicates OOMKill or SIGKILL; 143 indicates SIGTERM); check that the entrypoint and config match the image.
- **Pending**: check `describe` output for insufficient CPU or memory, taints, affinity, or unbound PVCs. Do not lower requests blindly to force scheduling.
- **Running but not Ready**: check the readiness probe path, port, and startup duration. Confirm the probe does not hit an endpoint requiring authentication.
- **Rollout stuck**: check ProgressDeadlineSeconds, PDB blocking, and quota. Roll back if the new revision is unhealthy and rollback is safe under the decision gates.

Rollback: use the previous ReplicaSet revision or re-apply the last known-good manifest from version control. Confirm the rollback target's digest before executing. Rollback is itself a gated action when it touches stateful components.

### Deliverable contract

Every response in this domain must provide:

1. A one-paragraph summary of the finding or change.
2. The exact manifest, Dockerfile, or command set, in fenced blocks, with the target namespace and cluster named.
3. Assumptions made, and any values that must be checked against current official documentation for the cluster's Kubernetes or tool version.
4. The verification checklist from this skill, with each item marked as confirmed, pending, or not applicable, and the evidence for each confirmed item.
5. Any gated actions still awaiting approval, listed explicitly.

Do not invent flags, API fields, image versions, benchmark figures, or compliance certifications. When a detail is version-sensitive, state it and mark it for verification against the official documentation for the relevant release.

### Isolated execution environments for agent workloads (v1.1)

A container is a packaging boundary, not automatically a security sandbox. Treat agent-generated code, downloaded dependencies, browser content, and tool-returned files as untrusted workloads. Design the execution boundary so a compromised task cannot inherit the host's credentials or reach unrelated workloads.

#### Separate control plane from compute plane
Keep orchestration, policy decisions, identity, billing, audit, and approval logic in a trusted control plane. Run generated code and other untrusted operations in disposable compute environments. The model must not be able to modify the sandbox supervisor, policy engine, credential broker, or host configuration.

#### Sandbox baseline
For each task, create an isolated environment with:
- A dedicated non-root UID/GID and no privileged mode.
- A read-only base filesystem plus a task-specific writable workspace.
- No host Docker socket, container runtime socket, host PID namespace, host network namespace, or sensitive host mounts.
- Default-deny network egress, with explicit destination allowlists enforced outside the sandbox where network access is approved.
- CPU, memory, process-count, disk, file-size, and wall-clock limits.
- Restricted Linux capabilities and syscall surface; use seccomp, AppArmor, SELinux, or an equivalent platform control where available.
- No ambient cloud instance credentials or inherited environment secrets.
- A narrow, explicit artifact import/export path with file type, size, and content checks.
- Ephemeral credentials only when necessary, scoped to one task and revoked at task completion.

Do not treat a container alone as a complete boundary for hostile multi-tenant workloads. Select a stronger isolation mechanism, such as a microVM or dedicated execution host, when the threat model includes kernel escape, hostile native code, or mutually untrusted tenants.

#### Network and dependency policy
Network access should be off by default. If dependencies must be downloaded, use a controlled build or package proxy with allowlisted registries, integrity verification, and logging. Do not allow arbitrary shell commands to contact arbitrary hosts. Block access to cloud metadata endpoints, internal control planes, loopback services, and private address ranges unless a narrowly reviewed exception is required. Revalidate DNS results and redirects at the egress enforcement point to reduce SSRF and rebinding risk.

#### Lifecycle and artifact handling
1. Create a clean environment from a pinned, reviewed base image.
2. Mount only task inputs required for the assigned work.
3. Start the workload with explicit resource, filesystem, process, and network policies.
4. Observe execution through host-side telemetry; do not rely on logs generated by the untrusted process as the only evidence.
5. Export only declared artifacts through a separate validation step.
6. Scan exported files for secrets, unsafe file types, unexpected executables, and path traversal before making them available to other tasks or users.
7. Destroy the environment and task-scoped credentials after completion, preserving only approved artifacts and minimal audit evidence.

#### Acceptance tests
Verify that the workload cannot:
- Read host home directories, unrelated task workspaces, runtime sockets, or secret mounts.
- Reach cloud metadata services, private control-plane endpoints, or unapproved external hosts.
- Spawn processes or consume resources beyond configured limits.
- Persist executable changes into the base image or a later task's workspace.
- Export files outside the declared artifact directory or use symlinks and path traversal to escape it.
- Retain a usable credential after the task is terminated.

Record the sandbox image digest, policy version, resource limits, network policy, task identifier, exported artifact digests, and teardown result. Report the isolation mechanism and the tests actually run; never describe a container as a security boundary without evidence.


## dns-and-network-diagnostics

**Use when:** Use when resolving DNS failures, slow name lookups, certificate or routing symptoms that look like name resolution problems, split-horizon confusion, or when a user asks to trace why a hostname does or does not reach a service.

### Purpose and boundaries

This skill covers layered diagnosis of name resolution and basic network reachability: stub resolver behavior, recursive and authoritative answers, record correctness, TTL and caching effects, TCP/UDP connectivity to the resolved address, and path-level checks such as MTU or firewall drops. It produces a root-cause statement backed by captured evidence.

Out of scope unless explicitly approved: changing production DNS zones, altering firewall or routing policy, running packet captures on hosts you do not administer, load-testing resolvers, and any scanning of address space you do not own or have written authorization to test.

### Inputs and assumptions

Collect before testing:
- The exact hostname (FQDN, trailing dot noted), record type expected, and the symptom as observed (NXDOMAIN, SERVFAIL, timeout, wrong address, connection refused, TLS failure).
- Client location, OS, and whether the client uses a VPN, proxy, or DNS-over-HTTPS.
- Expected answer: the intended address, CNAME target, or zone owner, from the authoritative source or change record.
- Time of onset and any recent changes (zone edits, registrar changes, certificate renewals, firewall rule updates).

Assume nothing about resolver software or flags. Confirm the tools available on the host and check their current manual pages or vendor documentation before relying on any option, since syntax and output formats vary across versions and platforms.

### Operating workflow

1. **Reproduce from the failing client.** Run the same lookup the application makes. Record the resolver in use (system stub, search domains, `ndots` effects, hosts file overrides).
2. **Check local overrides first.** Inspect the hosts file and any resolver configuration for stale pins. A stale local entry explains a surprising number of "DNS" failures.
3. **Query the configured resolver, then an independent resolver.** Compare answers, TTLs, and status codes. Divergence points to caching, split-horizon views, or resolver-side filtering.
4. **Walk the delegation.** Starting from the root, follow referrals to the parent zone and the authoritative nameservers. Confirm the parent delegation matches the child NS set.
5. **Query each authoritative server directly** with recursion disabled. Compare SOA serial, record sets, and TTLs across all nameservers. Inconsistent serials indicate incomplete propagation.
6. **Validate the record chain.** Follow every CNAME to its terminal target. Check for CNAME at apex, loops, and dangling targets.
7. **Test reachability to the resolved address.** Attempt TCP connection on the expected port, then application-level handshake if relevant. Separate name failure from transport failure.
8. **Check DNSSEC status if the zone is signed.** A validation failure at a validating resolver often presents as SERVFAIL while the authoritative data looks correct.
9. **Record evidence** (commands, timestamps, responses) and state the root cause.

### Decision gates

- If the local override matches the failing answer: stop; the fix is client-side. Propose removal, do not perform it without approval if the file is managed centrally.
- If configured and independent resolvers disagree: investigate caching or split-horizon before touching authoritative data.
- If authoritative nameservers disagree on the record set: escalate to the zone owner; do not edit zones yourself.
- If the name resolves correctly but TCP fails: move to routing, firewall, or service diagnosis; do not keep varying DNS queries.
- If SERVFAIL appears only at validating resolvers: check DNSSEC chain and signature expiry before blaming authoritative servers.
- Any step that changes state (flushing shared resolver caches, modifying records, altering firewall rules, capturing traffic on others' systems) requires explicit approval from the system owner first.

### Verification and evidence

A diagnosis is complete only when:
- The failing symptom is reproduced, with timestamp and exact error text.
- The root cause is confirmed by a test that would fail before the fix and pass after it.
- At least two independent vantage points (for example, the client resolver and a direct authoritative query) agree on the corrected state.
- TTL expectations are stated: the time until clients should see the change, derived from observed TTLs, not assumed.
- Each authoritative server's serial and answer are recorded in a table.

Do not claim propagation is complete while any authoritative server differs. Do not claim a fix works from a single cached answer.

### Failure handling

- **Timeouts with no response:** check whether UDP and TCP port 53 are reachable; large responses may require TCP fallback. Note that some networks block TCP 53 selectively.
- **Inconsistent results on repeated queries:** likely load-balanced or anycast resolvers. Record each responder and test them individually.
- **Diagnostic tool missing or output format unexpected:** verify the installed version and consult its current documentation; do not guess flags.
- **No access to authoritative servers:** report the limitation and request the zone owner's output rather than attempting intrusive probing.
- **Conflicting evidence:** document both observations and rank by how directly each was measured.

### Deliverable contract

Produce a report with these fields:
1. Symptom and reproduction steps (client, time, exact error).
2. Resolution path table: resolver, query, status, answer, TTL, serial.
3. Root cause in one sentence, with the evidence reference.
4. Recommended change, owner, and approval status.
5. Residual risk and the verification check to run after the change.
6. Explicit list of actions not taken because they required approval.

Do not include speculative causes without evidence, and do not present version-specific command syntax as verified unless checked against current official documentation.


## machine-image-builds

**Use when:** Use when creating, updating, validating, or promoting golden machine images (VM images, AMIs, container base images, or similar OS images) through an automated build pipeline, including image hardening, provenance capture, and rollout to fleets.

### Purpose and boundaries

This skill governs the lifecycle of reproducible machine images: defining the build, producing an artifact, verifying it, recording provenance, and promoting it to consumers. It applies to VM images (for example cloud AMIs or disk images built with a declarative image builder), immutable base images, and container base images built from a Dockerfile or equivalent.

In scope: build definitions, base OS selection, package and configuration layering, hardening steps, artifact tagging, smoke and compliance tests, promotion between channels, and deprecation of old images.

Out of scope: application code build, runtime configuration management for already-running hosts, and organization-wide cloud account setup. Redirect those to the relevant skill.

### Inputs and assumptions

Before acting, collect and confirm:

1. Target platform and format (cloud provider image catalog, hypervisor template, container registry).
2. Upstream base image identifier and the policy for accepting it (vendor-supported, internally mirrored, pinned digest).
3. Build tool and its version, read from the repository lockfile or pipeline definition. Do not assume a version.
4. Intended consumers, rollout channels (dev, staging, production), and the current production image identifier.
5. Required hardening baseline and its source (internal standard, CIS-style benchmark, or vendor guidance). Record the exact benchmark version used.
6. Retention and deprecation policy.

Assumptions must be stated in the work log. If any input is missing, stop and request it rather than guessing.

### Operating workflow

1. **Pin inputs.** Resolve the base image to an immutable digest or snapshot ID. Record package repository snapshot dates where the build tool supports them.
2. **Validate the definition.** Run the builder's syntax or validation mode. Confirm variables that carry secrets are injected at build time from the secret store, never written into the definition.
3. **Dry-run the layer order.** Confirm that changes are layered so that frequently changing components sit above stable ones, and that security updates are applied after base selection.
4. **Build in an isolated environment.** Use a dedicated build account or project with no production network routes. Tag the build with a unique ID, the git commit SHA, and the builder version.
5. **Harden and scan.** Apply the hardening baseline, then run a vulnerability scan and a configuration compliance check against the artifact. Save raw reports.
6. **Boot test.** Launch the artifact in a throwaway environment, confirm it boots, passes the health check, has the expected agent or service set, and has no leftover build credentials, shell history, or temporary keys.
7. **Generate provenance.** Record base digest, package snapshot, builder version, commit SHA, build timestamp, builder identity, and checksums or content digests of the final artifact.
8. **Promote.** Copy to the dev channel first. Promote to staging and production only after gates pass. Update channel pointers rather than overwriting artifact names.
9. **Deprecate.** Mark superseded images as deprecated with a date. Remove only after the retention period and confirmation that no running fleet references them.

### Decision gates

- **Base image gate:** Reject unpinned tags such as `latest` or floating major-version tags. Accept only digests, snapshot IDs, or versions explicitly listed in the approved base catalog.
- **Vulnerability gate:** Block promotion if any critical or high finding lacks an approved, dated exception. Medium and low findings are recorded with owner and target date.
- **Compliance gate:** Block promotion if mandatory hardening controls fail. Document any deviation with a risk owner and expiry date.
- **Boot and health gate:** Block if the instance fails to boot within the agreed timeout or the health check does not pass after the agreed warm-up period.
- **Secret scan gate:** Block if the artifact or its build logs contain credentials, tokens, or private keys. Treat any finding as an incident: stop, notify the security owner, and rotate the exposed material.
- **Promotion gate (requires explicit human approval):** Any promotion to production, any overwrite of a channel pointer, any deletion of an image, and any change that alters the default image for a fleet requires explicit approval from the named owner.

### Verification and evidence

Each build must produce these artifacts, stored with the build record:

- Build log with timestamps and the builder version.
- Provenance record in a machine-readable format.
- Vulnerability and compliance reports with tool name and version.
- Boot and health test output.
- Artifact checksum or content digest, and the list of channels it was promoted to.

Quality checks: the build is reproducible if rebuilt from the same inputs and yields an equivalent package set and configuration (exact byte identity is not required unless the tool guarantees it). Image size and boot time should be compared with the previous production image; a change beyond 20 percent in either requires a written explanation.

Do not claim compliance with any framework on the basis of these checks alone. Report the specific control results and the benchmark version that was run.

Version-sensitive details (builder flags, plugin names, cloud API parameters, scanner rule sets, benchmark revisions) must be checked against current official documentation before use and noted as verified with the date.

### Failure handling

- **Build failure:** Preserve logs, do not retry more than twice without a diagnosis, and do not change pinned inputs silently to get past the error.
- **Scan failure caused by tool error:** Re-run with the same tool version. If the tool itself is failing, treat the gate as not passed.
- **Boot failure:** Capture console output and cloud-init or equivalent logs. Do not promote a partially valid image.
- **Secret exposure:** Stop the pipeline, quarantine the artifact, and escalate to the security owner. Do not attempt to delete evidence.
- **Failed promotion:** Leave the channel pointer unchanged and record the reason.

### Deliverable contract

A completed run delivers:

1. Image identifier, channel status, and checksum or digest.
2. Pinned input list (base digest, snapshot dates, builder version, commit SHA).
3. Gate results table with pass, fail, or exception and evidence link for each gate.
4. Known risks, open exceptions with owners and expiry dates.
5. Explicit statement of any step not performed and why.
6. Rollback target: the previous approved image identifier.

What not to do:

- Do not use floating tags or `latest` in any definition or consumer reference.
- Do not embed credentials, keys, or tokens in build definitions, images, or logs.
- Do not overwrite an existing versioned artifact.
- Do not promote, delete, or repoint channels without explicit approval.
- Do not build directly against production networks or accounts.
- Do not state benchmark results, scan counts, or compliance status that were not actually measured in the run.


## network-time-connectivity

**Use when:** Use when a Linux host cannot reach, synchronize with, or stay accurately synced to its configured NTP or time sources, or when clock drift is traced to network path, DNS, firewall, or time-daemon reachability issues.

### Purpose and boundaries

This skill diagnoses why a Linux host cannot reach its time sources and restores reliable network time synchronization. It covers name resolution of time servers, UDP/123 path reachability, firewall and proxy interference, time-daemon configuration (chrony, ntpd, systemd-timesyncd), and reachability evidence from the daemon itself.

It does not cover hardware clock failure analysis, PTP or precision timing hardware design, leap-second policy, or application-level timestamp logic. Escalate those separately.

### Inputs and assumptions

Collect before acting:

- Distribution, init system, and the active time daemon (determine it from the running service, not from installed packages alone).
- Configured sources: `pool`, `server`, or `peer` entries and any DHCP- or cloud-provided sources.
- Whether the host is on a restricted network, behind an egress proxy, or in a segmented VPC or VLAN.
- Current clock offset and the time of last successful sync.
- Change window and owner approval status for config or firewall changes.

Assume nothing about upstream NTP availability until tested. Assume the host has no network access to public pools unless proven otherwise.

### Operating workflow

1. Record baseline state: current offset, daemon status, last sync time, and the configured source list. Save output to the incident record before changing anything.
2. Confirm the daemon's own view. Query the daemon's source table (for chrony, `chronyc sources -v`; for ntpd, `ntpq -p`; for systemd-timesyncd, check `timedatectl` status output). Note each source's reachability or poll state.
3. Resolve each configured hostname with the system resolver. A name that fails here fails in the daemon. Test with the same resolver path the daemon uses.
4. Test UDP/123 reachability per source. Use a time-aware client query where possible rather than ICMP, since ICMP success does not prove NTP reachability. Check the source's response, stratum, and offset.
5. If DNS and UDP succeed from the host but the daemon shows unreachable, inspect daemon config, bind address, and any AppArmor or SELinux denial in the audit log.
6. If UDP fails, trace the path: local firewall rules, cloud security groups, network ACLs, upstream NAT, and egress proxy policy. Identify the exact hop or policy that drops traffic.
7. Apply the smallest fix that restores reachability to at least two independent sources, then confirm sync.
8. Verify after a full poll cycle, not immediately after restart.

### Decision gates

- Gate A, DNS failure: if names do not resolve, fix resolver configuration first. Do not add raw IP sources as a workaround without approval, because IPs may change or be unauthorized.
- Gate B, firewall or security-group change: requires explicit approval from the network or security owner. State the exact rule, scope, and rollback.
- Gate C, source change: switching to a new or internal time source changes trust boundaries. Requires explicit approval and confirmation the source is authorized.
- Gate D, clock step: stepping a clock with a large offset can break databases, certificates, and Kerberos. Confirm the offset magnitude and get approval for a step before running it. Prefer slewing where the daemon permits.
- Gate E, daemon replacement or config rewrite: obtain approval and keep a backup of the original config.

### Verification and evidence

A fix is complete only when all of the following hold:

- At least two configured sources show reachable state with recent successful polls.
- The daemon reports synchronized status and offset below the threshold defined by the owning team (default assumption: under 100 ms unless the service requires tighter bounds).
- Offset remains stable across three consecutive polls.
- The fix survives a reboot or service restart, confirmed by a second check.

Keep raw command output as evidence. Do not report "fixed" from a single green line.

### Failure handling

- If no source becomes reachable, stop changing rules. Report the failed hops and the evidence.
- If the offset grows during troubleshooting, do not force a step without Gate D approval. Escalate.
- If a firewall rule was added and reachability is still broken, remove the rule after recording it and restore prior state.
- Do not disable time synchronization to silence alerts.

### Deliverable contract

Produce a report with:

1. Summary: host, daemon, root cause category, and final status.
2. Baseline and final offset with timestamps.
3. Source table before and after.
4. Commands run and their key outputs.
5. Changes made, with approvals referenced and rollback steps.
6. Open risks and follow-up owners.

Version-sensitive details (exact daemon subcommands, output formats, and systemd tooling options) must be verified against current official documentation for the installed version before being used in a production runbook.


## pipeline-and-supply-chain

**Use when:** Use when auditing, hardening, or designing CI/CD pipelines, build provenance, dependency and third-party action trust, artifact signing, or SBOM generation and review for software delivery.

### Purpose and boundaries

This skill covers the integrity of how software is built, dependencies are admitted, and artifacts are released. It applies to CI/CD configuration, build runners, package resolution, container and binary artifacts, signing and attestation, and SBOM production and review.

It does not cover runtime application security, network perimeter design, or vulnerability triage of application logic. Hand those off explicitly and note the handoff.

### Inputs and assumptions

Before acting, collect:

- Pipeline definitions (workflow files, pipeline YAML, Jenkinsfiles, build scripts) and the repositories that trigger them.
- Runner types (hosted, self-hosted, ephemeral or persistent) and who can administer them.
- Credential inventory: where tokens, signing keys, and registry credentials live and how they are scoped.
- Dependency manifests and lockfiles, and the registries or mirrors used.
- Release targets: registries, deployment environments, and consumers.
- Any existing SBOMs, provenance attestations, or signatures.

Assume the pipeline runs with privileges that can publish artifacts or reach production until shown otherwise. Assume pinned references are mutable until verified.

### Operating workflow

1. **Map trust edges.** List every input the build consumes: source ref, base image, third-party actions or plugins, package dependencies, build tools, secrets, and cache contents. Mark each as pinned-by-digest, pinned-by-version, or floating.
2. **Map trigger paths.** Identify which events can run privileged jobs, especially those triggered by pull requests from forks, comments, or external contributors. Check whether untrusted code can reach secrets or signing steps.
3. **Audit permissions.** For each job, record granted token scopes and secret access. Flag any default or write-all permission, long-lived credentials, and secrets exposed to untrusted triggers.
4. **Check build integrity.** Verify that builds are reproducible or at least recorded: source commit, builder identity, parameters, and dependency resolution are captured.
5. **Check artifact chain.** Confirm artifacts are signed, the signing identity is bound to the pipeline (not a human laptop), and consumers verify signatures before deployment.
6. **Review SBOM.** Confirm an SBOM is generated from the built artifact (not only the manifest), in a standard format such as SPDX or CycloneDX, and that it lists components with versions and hashes.
7. **Produce findings** using the deliverable contract below.

### Decision gates

- **Gate A, privileged execution from untrusted input:** If untrusted code can access signing keys, deploy credentials, or write tokens, rate as critical and stop recommending fixes that merely document it. Require isolation redesign.
- **Gate B, mutable third-party references:** Floating tags on actions, plugins, or base images are high severity when the step holds secrets or produces release artifacts. Recommend digest or commit pinning, with a verification step.
- **Gate C, key custody:** Signing keys stored as plain pipeline secrets are medium-to-high. Prefer keyless or hardware-backed signing where the platform supports it. Confirm the exact mechanism against current official documentation before recommending it.
- **Gate D, changes to production pipelines:** Any edit to release, signing, or deployment workflows, rotation of credentials, revocation of signing identities, or changes to branch protection requires explicit human approval with the specific diff shown.
- **Gate E, external impact:** Publishing packages, pushing images, opening disclosure, or contacting upstream maintainers requires explicit approval.

### Verification and evidence

Every finding must cite file path and line or job name, the exact configuration fragment, and the trigger condition that makes it exploitable. Verify claims by:

- Reproducing the trigger in a non-production fork or dry-run mode where the platform allows it.
- Confirming pinned digests resolve to the intended content.
- Verifying signatures and attestations with the consumer-side tooling, and recording the identity and issuer matched.
- Checking that SBOM component counts are plausible against the resolved lockfile.

Quality checks: 100% of privileged jobs have an explicit permission block; zero floating references in release jobs; every release artifact has a verifiable signature and provenance record; SBOM covers all shipped components.

Do not state that a control "guarantees" supply chain safety or satisfies a named compliance framework. Describe what was verified and what was not.

### Failure handling

- If a config cannot be read or a platform feature is unclear, state the gap and mark the finding as unverified. Do not guess syntax or feature availability.
- If a version-sensitive detail (action syntax, attestation format, platform permission model) is uncertain, mark it for verification against current official documentation.
- If a secret may have been exposed in logs or repository history, stop, report it, and request approval for rotation. Do not attempt to use it to test.
- If a dry run would publish or deploy, do not run it.

### Deliverable contract

Return:

1. **Summary:** scope, pipelines reviewed, overall risk rating.
2. **Trust map:** table of inputs with pinning status.
3. **Findings:** ordered by severity, each with location, evidence, trigger, impact, and recommended change.
4. **Proposed changes:** minimal diffs, marked as requiring approval where Gates D or E apply.
5. **Unverified items:** what could not be checked and why.
6. **Verification plan:** commands or steps the owner can run, with expected results.

Do not include real secret values, tokens, or private key material in any output.


## platform-delivery

**Use when:** Use when shipping, promoting, or rolling back a frontend application through build, preview, staging, and production environments, including CI/CD pipeline changes, asset hosting, cache and CDN configuration, environment variables, and release verification for web apps.

### Purpose and boundaries

This skill covers getting a frontend build from a commit to users safely: build configuration, artifact creation, environment promotion, static hosting and CDN behavior, cache invalidation, feature exposure, and rollback. It applies to single-page apps, server-rendered frontends, and static sites.

It does not cover application feature logic, backend API design, database migrations, or infrastructure provisioning beyond the frontend's own hosting. Hand those to the owning skill or team.

### Inputs and assumptions

Collect before acting:

- Target platform (static host, CDN, container, edge runtime, or SSR server) and its current documentation version.
- Build tool and framework versions from the lockfile. Do not assume them from memory.
- Environment matrix: which variables differ per environment and which are build-time versus runtime.
- Current production artifact identifier and the last known-good release.
- Caching rules: asset hashing scheme, HTML cache headers, CDN TTLs, service worker presence.
- Who owns approval for production promotion.

If any item is unknown, state the assumption in the delivery record and mark it unverified.

### Operating workflow

1. **Freeze the candidate.** Identify the exact commit and lockfile. Confirm the build is reproducible: a clean install and build from the lockfile must produce the same asset manifest hashes twice in succession, or differences must be explained.
2. **Audit configuration diffs.** Compare environment variables and build flags against the previous release. List every changed key. Flag any secret-looking value that appears in client bundles.
3. **Build once, promote many.** Produce one immutable artifact and deploy the same bytes to preview, staging, and production. Rebuilding per environment is forbidden unless the difference is strictly runtime configuration.
4. **Deploy to preview or staging.** Verify routing, asset paths, base URL, and `index.html` cache headers.
5. **Run verification** (see below) against staging.
6. **Request promotion approval** with the evidence bundle.
7. **Promote** using the platform's atomic alias or pointer switch, not file-by-file copies.
8. **Post-release watch.** Monitor error rates, failed asset loads, and core web vitals for a defined window before closing the release.

### Decision gates

- **Gate A, build reproducibility:** Hash mismatch on a clean rebuild blocks release until explained.
- **Gate B, bundle hygiene:** Any secret in a client bundle, or any new source map published to a public location, blocks release.
- **Gate C, cache correctness:** Hashed assets must be served with long-lived immutable caching. The HTML entry point and any non-hashed files must revalidate. Violations block release.
- **Gate D, compatibility:** If the release changes a cached contract (service worker scope, localStorage schema, API client shape), a migration or fallback must exist. Otherwise require explicit approval with a stated risk.
- **Gate E, production promotion:** Requires named human approval. Automated pipelines may deploy to staging but must not promote to production without an approval record.

### Verification and evidence

Run and record:

- Asset manifest diff between current and candidate releases. Expected changes should match the commit scope.
- Smoke test of critical routes: load, authenticated shell, one primary user action per major feature. Record status codes and console error counts.
- Header check on `index.html`, one hashed JS chunk, and one non-hashed public file. Record `Cache-Control` values as observed.
- Client-side route fallback: a deep link returns the app shell with a 200 status, not a 404.
- Error budget comparison: client error rate and failed chunk loads for a bounded window after promotion, against the prior baseline. Set the window and threshold before release.
- Performance regression check on a representative page using the team's agreed metric set. Compare against the stored baseline; do not claim improvement without the baseline.

Mark any tool flags, header names, or platform features you cite as requiring confirmation against current vendor documentation for the version in use.

### Failure handling

- **Failed smoke test on staging:** Stop. Do not promote. Diagnose from build logs and the asset manifest before retrying.
- **Elevated client errors after promotion:** Roll back to the prior pointer immediately if the threshold is breached. Rollback is pre-approved only when the runbook explicitly says so; otherwise escalate to the approver with the recommendation.
- **Stale users on old chunks:** Confirm old assets remain available for the retention window. Do not delete previous release artifacts until the window passes.
- **Cache poisoning suspicion** (wrong content served under a hashed URL): Purge affected paths, verify origin content, and treat as an incident.
- **Partial deploy:** Re-run the atomic promotion. Do not hand-patch individual files on the host.

### Deliverable contract

Each release produces a delivery record containing:

- Commit SHA, lockfile hash, artifact identifier, and build timestamp.
- Environment variable diff with secrets redacted by name only.
- Gate results A through E, each marked pass, fail, or waived with the approver's name.
- Verification outputs listed above, including observed headers.
- Rollback target identifier and the exact rollback command or pointer switch as documented for the platform.
- Open assumptions and items marked for documentation verification.
- Post-release watch outcome and a close or rollback decision.

### What not to do

- Do not rebuild separately per environment.
- Do not put secrets in client-side configuration or source maps served publicly.
- Do not set long cache lifetimes on `index.html` or unhashed entry files.
- Do not delete prior release artifacts during the rollback window.
- Do not promote to production, purge global caches, change DNS, or alter production headers without explicit approval.
- Do not state performance, uptime, or compliance outcomes without measured evidence.
- Do not invent configuration keys, CLI flags, or version numbers. Verify them against current official documentation.


## terraform-iac-authoring

**Use when:** Use when writing, refactoring, reviewing, or planning Terraform configurations (HCL) for cloud infrastructure, including module design, state-safe changes, plan review, and provider upgrades.

### Purpose and boundaries

This skill covers authoring and changing Terraform root configurations and reusable modules written in HCL. It includes resource and data source design, variable and output contracts, module composition, remote state usage, plan interpretation, and safe refactoring with `moved`, `import`, and `removed` blocks.

It does not cover: cloud account bootstrap or organization policy, CI/CD pipeline engineering beyond the plan/apply handoff, configuration management tools, Kubernetes manifests, or runtime application code. Hand those to the relevant skill.

### Inputs and assumptions

Before writing code, establish:

1. Target providers and their pinned version constraints (read `required_providers` and `.terraform.lock.hcl`).
2. Terraform CLI version constraint in `required_version`. Confirm the installed version matches.
3. Backend type and state location, and who holds write access.
4. Environment layout: single root per environment, or shared modules consumed by multiple roots.
5. Whether the change touches existing, live resources. If yes, treat it as a stateful change.

If any item is unknown, ask. Do not guess account IDs, regions, ARNs, CIDRs, or secret paths. Use variables or clearly marked input requirements instead.

Version-sensitive details (provider argument names, lifecycle behavior, CLI flags, backend options, and deprecations) must be checked against current official Terraform and provider documentation before being relied on.

### Operating workflow

1. **Read before writing.** Inspect the existing root module, the lock file, and any remote state data sources. Map which resources are managed where.
2. **Classify the change.** Label it as additive (new resources), in-place update, replacement (destroy then create), refactor (address change only), or state operation (import, removal from state).
3. **Design the interface first.** Define input variables with `type`, `description`, and `validation` where a value has a constrained domain. Define outputs only for values consumers need. Mark sensitive outputs with `sensitive = true`.
4. **Write resources with explicit intent.** Prefer named arguments over inferred defaults for anything that affects cost, network exposure, encryption, or deletion protection. Use `for_each` over `count` when items have stable identities.
5. **Refactor with declarative moves.** When renaming or moving resources between modules, use `moved` blocks rather than manual `terraform state mv`. Use `import` blocks for adopting existing infrastructure.
6. **Format and validate locally.** Run formatting, validation, and linting available in the repository. Do not invent tool names; use what the project already declares.
7. **Produce a plan and read it.** Run plan against the correct workspace or state. Review every action line, not just the summary counts.
8. **Hand off** with the plan summary, risk notes, and rollback posture (see Deliverable contract).

### Decision gates

Stop and request explicit human approval before proceeding if any of the following hold:

- The plan contains any destroy or replace action on stateful resources (databases, storage buckets, encryption keys, DNS zones, identity objects, persistent volumes).
- The change alters IAM policies, network ingress rules, public exposure, or encryption settings.
- The change modifies or removes state, runs `import` against live resources, or edits backend configuration.
- The change upgrades a provider across a major version or raises `required_version`.
- The target workspace or state file is ambiguous, or appears to be production when the request suggested otherwise.
- The change would apply to infrastructure owned by another team.

Approval must name the specific actions being approved. A general "go ahead" does not cover new destroy actions discovered later in the plan. Re-plan and re-request if the plan changes.

Do not run `apply`, `destroy`, `state rm`, or `force-unlock` without this explicit approval. Do not suggest `-target` as a routine fix; it bypasses dependency analysis and requires justification in the handoff.

### Verification and evidence

Each change must carry:

- **Format check:** the repository's formatter reports no diff.
- **Validation:** configuration validates without errors in every affected root.
- **Plan review:** the plan is attached or quoted with resource addresses for every create, update, replace, and delete. Count of each action type matches what was described.
- **Expected-no-op check:** for refactors, the plan shows zero resource changes apart from moved addresses. Any other action indicates a bug.
- **Drift note:** if plan shows changes unrelated to the request, report them as drift and do not silently absorb them.
- **Lock file:** if providers changed, the lock file diff is included and reviewed.

Measurable checks: every variable without a default is documented; no resource uses hardcoded credentials, account IDs, or region strings that belong in variables; every module input has a type; every stateful resource has the protections the repository standard defines (for example, deletion protection or `prevent_destroy` lifecycle where appropriate). Confirm these by searching the diff, not by memory.

### Failure handling

- **Plan errors on dependency cycles:** restructure references or split the root. Do not add `depends_on` to paper over an unclear graph without explaining it.
- **Unexpected replacement:** stop. Identify the argument that forces replacement from the plan output and the provider documentation for that argument. Options are usually to revert the argument, use a `moved` block if the change is a rename, or obtain approval for a planned replacement with a data-preservation step.
- **State lock held:** do not force unlock. Confirm with the owner whether the lock is stale.
- **Apply partially failed:** do not re-run blindly. Re-plan, compare with the failed apply output, and report which resources reached which state.
- **Provider upgrade breaks plan:** pin the previous version, record the failing argument, and check the provider upgrade guide before retrying.

### Deliverable contract

Every completed change returns:

1. Summary of intent in one paragraph.
2. Change classification (additive, update, replacement, refactor, state operation).
3. Files changed, with a one-line reason per file.
4. Plan summary: counts per action type, and every replace or destroy listed by resource address.
5. Verification results from the checks above, with any failures stated plainly.
6. Approval status for each gated action, and what remains unapproved.
7. Rollback posture: how to revert the code, and whether reverting state is possible or requires restore from backup.
8. Open questions and version-sensitive items flagged for verification against current documentation.

### What not to do

- Do not hardcode secrets, passwords, tokens, or private keys in configuration or variable defaults. Reference the secret store the repository uses.
- Do not use `-target`, `-replace`, `state rm`, or `force-unlock` as routine workflow steps.
- Do not disable lifecycle protections to get a plan to pass.
- Do not wildcard IAM actions or resources without an explicit, recorded justification.
- Do not invent provider arguments, module sources, or version numbers. Verify them.
- Do not merge modules that serve different ownership or change cadence.
- Do not claim a configuration is compliant, secure, or cost-optimal. Report what was checked and what was not.

### Ultron routing contract

**Choose this skill when:** the deliverable is authoring or changing Terraform configuration: HCL resources, modules, variable/output contracts, providers, state references, composition, refactoring, and review of plan changes.

**Choose `terraform-test-and-import` when:** the task is writing Terraform native tests and assertions, validating behavior, or importing existing infrastructure into state without recreating it.

**Handoff contract:** this skill supplies the intended resource/module design and expected plan. The test/import skill returns test coverage, import mapping, state-address reconciliation, and evidence that adoption will not create or destroy unintended resources. Feed any required HCL corrections back here. Do not use import as a substitute for designing the desired configuration.

**Why the boundary exists:** authoring defines the desired infrastructure; tests and import workflows prove that the configuration behaves as intended and safely adopts existing resources.


## terraform-test-and-import

**Use when:** Use when writing or running Terraform test suites (.tftest.hcl), adding assertions to modules, or bringing existing cloud resources under Terraform management through import blocks or state adoption.

### Purpose and boundaries

This skill covers two tasks: (1) verifying Terraform configuration behavior with native test files and assertions, and (2) adopting existing infrastructure into Terraform state without recreating it. It does not cover provider authoring, multi-cloud architecture design, or general CI/CD pipeline setup. It does not authorize applying changes to shared environments.

### Inputs and assumptions

Collect before starting:
- Terraform version and provider version constraints from `required_providers` and the lock file. Treat all syntax below as version-sensitive; confirm `terraform test`, `run` blocks, `assert`, and `import` blocks against current official Terraform documentation for the pinned version.
- Module source and its variables, outputs, and resource graph.
- For imports: the resource addresses to create, the provider-specific import ID format (look it up in the provider's resource documentation; never guess), and the current remote state of each resource.
- Backend type and state location. Confirm whether it is local, remote, or shared.

If any input is missing, stop and request it.

### Operating workflow

**Testing**
1. Read the module's variables and outputs. List behaviors worth asserting: naming rules, encryption flags, CIDR validity, conditional resource counts, output shape.
2. Create `tests/` with one `.tftest.hcl` file per behavior group. Use `command = plan` for logic and input validation. Use `command = apply` only against disposable sandbox accounts and only with explicit approval.
3. Write each `run` block with explicit `variables`, then add `assert` blocks whose `condition` references concrete attributes. Prefer one assertion per property so failures are diagnosable.
4. Run `terraform test` with verbose output. Confirm test count and assertion count match your plan.
5. Add a negative case for every validation rule, using `expect_failures` where the version supports it.

**Importing**
1. Run `terraform plan` on the current configuration and confirm zero unexpected changes before adding anything.
2. Write the resource block with the minimum arguments needed to match the live resource.
3. Declare an `import` block with the target address and provider ID. Alternatively, use the CLI import path if the pinned version or workflow requires it.
4. Generate a draft configuration only where the version supports it, then review and edit it manually. Generated code is a starting point, not a deliverable.
5. Run `terraform plan`. Iterate on arguments until the plan shows no changes for the imported resource. Attribute diffs that Terraform wants to correct need a decision, not silent acceptance.
6. Remove the `import` block after the state is recorded, and keep it only when the workflow requires it for other team members.

### Decision gates

- **Stop and request approval** before any `apply`, state modification (`terraform state` subcommands, `import` into a shared backend), or any action touching production, shared, or billing-relevant accounts.
- **Stop** if the plan after import shows destroy or replace actions. Do not apply to clear them. Investigate the attribute mismatch first.
- **Stop** if the import ID format cannot be verified against provider documentation.
- **Proceed** with plan-only tests on any account without approval.
- **Escalate** if a resource contains sensitive attributes (keys, passwords, tokens) that would be written to state or plan output.

### Verification and evidence

Record the following before reporting success:
- `terraform test` output showing pass count equal to the number of `run` blocks, and zero failures.
- For each import: a plan with zero changes for that address, captured in a file.
- Confirmation that every validation rule has at least one failing-input test.
- State list output showing each imported address exists exactly once.
- Pinned versions of Terraform and the provider.

Do not claim coverage percentages or security compliance from these tests. They verify only what the assertions state.

### Failure handling

- **Assertion fails:** Determine whether the code or the expectation is wrong by reading the module logic. Fix the wrong side, then rerun. Do not weaken assertions to pass.
- **Import plan shows drift:** Compare the live attribute with the configuration. Update the configuration to match reality unless the drift is a defect to remediate, which requires approval.
- **Import ID rejected:** Re-check provider docs for the exact format. Do not try multiple IDs against live resources.
- **Partial import:** Use state inspection to identify what was recorded. Do not re-import blindly; that can duplicate or conflict.

### Deliverable contract

Return:
1. Changed files list with paths.
2. Test file contents or diff, plus the exact `terraform test` result.
3. Import table: address, provider ID format source, plan result.
4. Open items requiring approval, listed separately.
5. Tool versions used, with a note that version-specific syntax was checked against official docs for those versions.

Do not include credentials, account identifiers beyond what is necessary, or unredacted state contents in deliverables.

### Ultron routing contract

**Choose this skill when:** the task is to verify Terraform behavior using native test files/assertions or to bring existing infrastructure under Terraform state management without recreating it.

**Choose `terraform-iac-authoring` when:** the task is designing resources and modules, changing HCL architecture, defining variables and outputs, or refactoring configuration.

**Handoff contract:** receive the expected resource addresses, configuration intent, provider/version constraints, and plan baseline. Return test outcomes, import mappings, state reconciliation evidence, and any configuration mismatch. Stop if import or test evidence indicates an unexpected create, replace, or destroy; send the configuration issue back to the authoring skill rather than applying it.

**Why the boundary exists:** safely testing or adopting infrastructure is not the same as defining the infrastructure design, and neither grants permission to apply changes to shared environments.

