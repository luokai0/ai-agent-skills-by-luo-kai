---
name: containers-and-kubernetes
description: Use when building, reviewing, debugging, or operating container images and Kubernetes workloads, including Dockerfile hardening, manifest design, rollout and rollback decisions, resource sizing, and cluster troubleshooting.
author: Luo Kai
provenance: original
version: 1.0.0
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