---
name: azure-app-and-data-services
description: Use when designing, deploying, configuring, troubleshooting, or reviewing Azure application hosting (App Service, Functions, Container Apps) and managed data services (Azure SQL, Cosmos DB, Storage, Redis-compatible caches) in a production or pre-production environment.
author: Luo Kai
provenance: original
version: 1.1.1
---

# Azure App And Data Services

## Purpose and boundaries

This skill guides an agent through planning, configuring, verifying, and troubleshooting Azure application hosting and managed data services. It covers:

- Hosting: App Service (web apps, slots), Azure Functions, Azure Container Apps.
- Data: Azure SQL Database, Cosmos DB, Storage accounts (Blob, Queue, Table), managed Redis-compatible caches.
- Connectivity: managed identity, private endpoints, virtual network integration, DNS for private links.
- Operations: deployment slots, scaling, backup and restore, diagnostics, cost signals.

It does not cover: on-premises data migration tooling, Azure networking hub design beyond the app and data boundary, Kubernetes internals (AKS), or billing dispute handling. Refer those to specialized skills.

## Inputs and assumptions

Before acting, confirm or obtain:

1. Subscription, resource group, region, and target environment (dev, test, staging, prod).
2. Workload type and traffic profile: request rate, peak concurrency, latency target, data volume, growth expectation.
3. Data classification and residency requirements, stated by the requester. Do not assume compliance status.
4. Existing resource IDs, identity model, and network topology (public, VNet-integrated, private endpoint).
5. Recovery objectives (RPO and RTO) as provided by the owner. If absent, record "not defined" and flag it.
6. The current version of Azure CLI, Bicep/ARM tooling, or Terraform provider in use.

Assumptions must be written down in the deliverable. Never assume a SKU, tier, or region capacity is available; verify it.

**Version-sensitive details:** SKU names, runtime stack identifiers, supported language versions, API versions, CLI parameters, and pricing change over time. Mark every such detail as "verify against current Microsoft Learn documentation" before it is applied.

## Operating workflow

1. **Classify the request.** Determine whether it is design, deployment, configuration change, incident, or review.
2. **Read current state.** Query existing resources in read-only mode (list, show, get configuration). Record names, SKUs, identity, network mode, and backup settings.
3. **Build the target state.** Specify each resource, its SKU, region, identity type, network exposure, and dependencies.
4. **Prefer declarative definitions.** Express changes in Bicep or ARM templates, or the team's IaC tool, so changes are reviewable and repeatable.
5. **Validate before apply.** Run template validation and what-if or plan output. Review every delete and replace operation.
6. **Stage the change.** Deploy to non-production first. For App Service, use a deployment slot with traffic routing when available.
7. **Verify** against the checks in the verification section.
8. **Record** the change, rollback path, and open items.

## Decision gates

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

## Verification and evidence

Every completed change must include evidence for each relevant check:

- **Identity:** the app uses a system or user-assigned managed identity, and role assignments are scoped to the minimum resource, not the subscription. Confirm with an authenticated read through the app, not only by inspecting configuration.
- **Network:** public access is disabled on data resources where required; private endpoint DNS resolves to a private address from the app's network. Test resolution from inside the network.
- **Health:** health check endpoint returns success after restart; App Service slot swap or Container Apps revision shows healthy replicas.
- **Data:** a restore test has succeeded within the documented RTO for the most recent backup point, or the gap is reported. Backup retention matches the approved policy.
- **Performance:** p95 latency and error rate measured against the stated target over a representative window. Do not claim a target is met without measurements.
- **Cost signal:** scaling limits and minimum instance counts are set deliberately, and the expected monthly cost range is stated with the source of the estimate.
- **Diagnostics:** logs and metrics flow to the designated workspace; alerts exist for error rate, latency, and resource exhaustion.

## Failure handling

- **Deployment failure:** read the operation log for the first error, not the last. Do not retry blindly. Roll back the slot or revision to the last healthy version.
- **Connection failure to data service:** check, in order, DNS resolution, firewall or private endpoint state, identity role assignment, token audience, and connection string format. Change one variable at a time.
- **Quota or SKU unavailable:** report the exact error, propose an alternate region or SKU, and ask for approval.
- **Data corruption or accidental deletion:** stop writes if safe to do so, preserve the current state, identify the restore point, and request approval before any restore. Do not overwrite the live resource to test a restore; restore to a new target.
- **Unverifiable documentation claim:** if a setting cannot be confirmed against current official documentation, state that it is unverified and do not apply it.

## Deliverable contract

Every output must include:

1. **Summary:** one paragraph stating the goal, scope, and outcome.
2. **Resource inventory:** table of resource type, name, region, SKU (marked version-sensitive), identity, and network mode.
3. **Changes applied or proposed:** ordered list with the exact IaC file or command reference, and whether each step is destructive.
4. **Approval requests:** every gated action, with the risk and the rollback path.
5. **Verification results:** each check in the verification section marked pass, fail, or not tested, with evidence.
6. **Assumptions and open items:** including unverified version-sensitive details and missing RPO/RTO values.
7. **Rollback plan:** specific steps to return to the prior state.

Do not state that a deployment is production-ready, compliant, or secure unless the specific evidence for that claim is attached. Do not include secret values, connection strings, or keys in any output.

## Ultron routing contract

**Choose this skill when:** the work concerns Azure application workload resources and managed data services: App Service, Functions, Container Apps, Azure SQL, Cosmos DB, Storage, managed cache, deployment slots, backups, scaling, private connectivity, and workload-level operations.

**Choose `azure-landing-zone-identity` when:** the decision concerns tenant and subscription identity foundations: Entra roles, Azure RBAC scope, privileged access, managed/workload identity governance, service principals, emergency access, or identity-wide policy.

**Handoff contract:** the workload skill states the exact resource, environment, required capability, and least-privilege identity need. The identity skill returns the approved principal type, role or custom action set, scope, assignment path, and audit requirement. The workload skill then verifies that the application uses the identity without exposing secrets. Do not create broad tenant permissions to make an application deployment convenient.

**Why the boundary exists:** workload configuration consumes identity capabilities; it should not independently redefine the tenant's identity governance.
