---
name: containers-and-kubernetes
description: Use when building, reviewing, debugging, or operating container images and Kubernetes workloads, including Dockerfile hardening, manifest design, rollout and rollback decisions, resource sizing, and cluster troubleshooting.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Containers And Kubernetes

## Purpose and boundaries

This skill covers the practical lifecycle of containerized workloads: building images, writing and reviewing Kubernetes manifests, deploying and rolling out changes, diagnosing failing pods, and sizing resources. It applies to application teams and platform teams working with a Kubernetes cluster and an OCI-compatible build toolchain.

In scope: Dockerfile and build hygiene, image tagging and provenance, workload manifests (Deployment, StatefulSet, Job, CronJob, Service, Ingress or Gateway, ConfigMap, Secret references, HorizontalPodAutoscaler, PodDisruptionBudget, NetworkPolicy), rollout strategy, probes, resource requests and limits, and incident-level pod diagnosis.

Out of scope: cluster provisioning from scratch, cloud-account IAM design, service mesh internals, and application code changes beyond what a container requires. Route those to the relevant domain skill.

## Inputs and assumptions

Gather before acting:

1. Target cluster name, environment (dev, staging, production), and Kubernetes version. Treat API availability and field support as version-dependent.
2. Current manifests or Helm/Kustomize source, and the image reference being deployed.
3. Application runtime, listening ports, startup time, graceful shutdown behavior, and whether it is stateful.
4. Observed symptoms, recent changes, and relevant events or logs.
5. Access level. Assume read-only access unless the user explicitly grants write access for a named namespace and action.

If any of these are missing and they change the recommendation, ask. Do not assume a production cluster is a test cluster.

## Operating workflow

1. **Classify the request**: build, manifest review, deployment, rollback, or diagnosis.
2. **Establish current state** with read-only commands: current image digest, desired versus available replicas, recent events, and rollout status.
3. **Make the smallest change** that addresses the stated problem. Prefer declarative edits to manifests in version control over imperative patches to live objects.
4. **Validate before apply**: schema and server-side dry-run, policy checks if the cluster uses them, and diff against the live object.
5. **Roll out incrementally**: one namespace or one cluster at a time, watching readiness and error rates.
6. **Verify** against the criteria in the verification section before declaring success.

For Dockerfiles: use a multi-stage build; pin base images by digest or a deliberate tag; copy dependency manifests before source to preserve layer caching; run as a non-root user with an explicit numeric UID; exclude secrets and build context junk with `.dockerignore`; keep the final stage minimal.

For manifests: set `resources.requests` on every container; set `resources.limits` for memory and make a deliberate decision on CPU limits; define readiness and liveness probes with different semantics (liveness must not depend on downstream dependencies); set `terminationGracePeriodSeconds` to match real shutdown time; use `preStop` only when the application needs it; add a PodDisruptionBudget for multi-replica workloads that must survive node drains.

## Decision gates

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

## Verification and evidence

A change is verified only when all of these hold:

- `kubectl rollout status` reports completion within the expected window for the workload.
- All new pods are Ready, with zero restarts since the rollout began, or restarts are explained and accepted.
- The running image digest matches the digest built and approved, confirmed from the pod spec, not from the tag.
- Service endpoints list the expected pod IPs, and a smoke request through the real ingress path succeeds.
- Error rate and latency for the workload are within the pre-change baseline on the monitoring system you have access to. State the baseline value and the observed value.
- For autoscaled workloads, the HPA reports current metrics (not `unknown`).

Record evidence: the command, the timestamp, and the relevant output excerpt. Do not report success based on the apply command returning without error.

## Failure handling

Diagnose in this order: events, then pod status, then logs, then node and cluster conditions.

- **ImagePullBackOff / ErrImagePull**: verify the reference, the registry credentials in the referenced pull secret, and network reachability. Do not add broad credentials to work around it.
- **CrashLoopBackOff**: read `previous` container logs; check the exit code (137 typically indicates OOMKill or SIGKILL; 143 indicates SIGTERM); check that the entrypoint and config match the image.
- **Pending**: check `describe` output for insufficient CPU or memory, taints, affinity, or unbound PVCs. Do not lower requests blindly to force scheduling.
- **Running but not Ready**: check the readiness probe path, port, and startup duration. Confirm the probe does not hit an endpoint requiring authentication.
- **Rollout stuck**: check ProgressDeadlineSeconds, PDB blocking, and quota. Roll back if the new revision is unhealthy and rollback is safe under the decision gates.

Rollback: use the previous ReplicaSet revision or re-apply the last known-good manifest from version control. Confirm the rollback target's digest before executing. Rollback is itself a gated action when it touches stateful components.

## Deliverable contract

Every response in this domain must provide:

1. A one-paragraph summary of the finding or change.
2. The exact manifest, Dockerfile, or command set, in fenced blocks, with the target namespace and cluster named.
3. Assumptions made, and any values that must be checked against current official documentation for the cluster's Kubernetes or tool version.
4. The verification checklist from this skill, with each item marked as confirmed, pending, or not applicable, and the evidence for each confirmed item.
5. Any gated actions still awaiting approval, listed explicitly.

Do not invent flags, API fields, image versions, benchmark figures, or compliance certifications. When a detail is version-sensitive, state it and mark it for verification against the official documentation for the relevant release.

## Isolated execution environments for agent workloads (v1.1)

A container is a packaging boundary, not automatically a security sandbox. Treat agent-generated code, downloaded dependencies, browser content, and tool-returned files as untrusted workloads. Design the execution boundary so a compromised task cannot inherit the host's credentials or reach unrelated workloads.

### Separate control plane from compute plane
Keep orchestration, policy decisions, identity, billing, audit, and approval logic in a trusted control plane. Run generated code and other untrusted operations in disposable compute environments. The model must not be able to modify the sandbox supervisor, policy engine, credential broker, or host configuration.

### Sandbox baseline
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

### Network and dependency policy
Network access should be off by default. If dependencies must be downloaded, use a controlled build or package proxy with allowlisted registries, integrity verification, and logging. Do not allow arbitrary shell commands to contact arbitrary hosts. Block access to cloud metadata endpoints, internal control planes, loopback services, and private address ranges unless a narrowly reviewed exception is required. Revalidate DNS results and redirects at the egress enforcement point to reduce SSRF and rebinding risk.

### Lifecycle and artifact handling
1. Create a clean environment from a pinned, reviewed base image.
2. Mount only task inputs required for the assigned work.
3. Start the workload with explicit resource, filesystem, process, and network policies.
4. Observe execution through host-side telemetry; do not rely on logs generated by the untrusted process as the only evidence.
5. Export only declared artifacts through a separate validation step.
6. Scan exported files for secrets, unsafe file types, unexpected executables, and path traversal before making them available to other tasks or users.
7. Destroy the environment and task-scoped credentials after completion, preserving only approved artifacts and minimal audit evidence.

### Acceptance tests
Verify that the workload cannot:
- Read host home directories, unrelated task workspaces, runtime sockets, or secret mounts.
- Reach cloud metadata services, private control-plane endpoints, or unapproved external hosts.
- Spawn processes or consume resources beyond configured limits.
- Persist executable changes into the base image or a later task's workspace.
- Export files outside the declared artifact directory or use symlinks and path traversal to escape it.
- Retain a usable credential after the task is terminated.

Record the sandbox image digest, policy version, resource limits, network policy, task identifier, exported artifact digests, and teardown result. Report the isolation mechanism and the tests actually run; never describe a container as a security boundary without evidence.
