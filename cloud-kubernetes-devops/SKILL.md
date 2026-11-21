---
name: cloud-kubernetes-devops
description: Use when deploying, upgrading, or troubleshooting workloads on managed or self-hosted Kubernetes that pull images or charts from external registries, including image pull failures, credential rotation, digest pinning, mirroring, and registry-related admission decisions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Cloud Kubernetes DevOps (External Registries)

## Purpose and boundaries

This skill covers how Kubernetes workloads obtain artifacts from registries outside the cluster's own network boundary: container images, Helm charts, and OCI artifacts. It covers pull authentication, image reference hygiene, mirroring and caching decisions, rate-limit and availability risk, and verification of pulled artifacts before they run.

It does not cover general cluster provisioning, application code changes, or building images from source except where build output must be verified before publication.

## Inputs and assumptions

Collect before acting:

- Cluster type and version, provider, and the namespaces and service accounts in scope.
- Full image references currently deployed, including tags and digests where present.
- Registry hostnames, their authentication method, and who owns the credentials.
- Network path constraints: egress rules, proxies, private endpoints, air-gapped segments.
- Compliance or change-control requirements that apply to the environment.

Assume nothing about registry rate limits, retention policies, or signing support. Verify each against the provider's current documentation. Kubernetes API behavior, admission features, and pull-secret mechanics vary by version; treat exact field names and feature gates as version-sensitive and confirm them in the official reference for the cluster's version.

## Operating workflow

1. **Inventory.** List every distinct registry host referenced by running pods, pending pods, and chart values. Group by namespace and owner.
2. **Classify each reference.** Record whether it uses a mutable tag, a digest, or a tag resolved at deploy time. Flag `latest` and unpinned branch-style tags.
3. **Map credentials.** For each registry, identify the secret type, the namespaces it is bound to, the service accounts that reference it, and its expiry or rotation mechanism.
4. **Check reachability.** From a node or a debug workload with the same network policy, confirm DNS resolution and TLS connectivity to each registry. Do not infer reachability from another environment.
5. **Plan the change.** Prefer, in order: pin by digest, add a mirror or pull-through cache, then adjust credentials. Each change is a separate, reversible step.
6. **Stage and observe.** Apply to a non-production namespace first. Watch pod events and image pull status, not only deployment rollout status.
7. **Promote** only after the verification checks below pass.

## Decision gates

Stop and request explicit approval before:

- Deleting or rotating pull secrets, service account bindings, or registry credentials.
- Changing image references in production workloads, including digest updates.
- Adding or removing mirrors, changing DNS or egress rules, or altering proxy settings.
- Enabling or changing admission policies that can reject pods cluster-wide.
- Any action that publishes images or charts to an external registry, or that sends credentials to a third party.
- Garbage collection or retention changes in a registry you do not own.

Proceed without approval only for read-only inventory, dry-run or server-side validation, and changes confined to a sandbox namespace that you created.

## Verification and evidence

Measurable checks before promotion:

- Every production image reference resolves to a digest. Count of unpinned references must be zero, or each exception must have a recorded owner and expiry date.
- Pull success rate on the target nodes is 100% across at least one full rollout, with no `ErrImagePull` or `ImagePullBackOff` events in the window.
- Each pull credential is bound only to the namespaces and service accounts that need it. Verify with a listing of bindings, not from memory.
- Mirror content matches upstream digests for the sampled set. Record the comparison output.
- If signature or attestation verification is in use, record the verifier identity and policy name used. Do not claim verification passed without the tool output.
- Rollback path tested: the previous digest is recorded and redeployable.

Keep the evidence: command output, event excerpts, digest lists, and change ticket references.

## Failure handling

- **Unauthorized (401/403):** Check the secret's type, the registry host string exactly as referenced in the image, and token expiry. Do not reuse credentials from another team to unblock.
- **Not found (manifest unknown):** Confirm the tag or digest exists upstream. Do not retag or push to satisfy the reference.
- **Rate limited or throttled:** Reduce pull concurrency, use an authenticated identity if policy allows, or introduce a cache. Do not disable retries across the cluster.
- **TLS or DNS failure:** Check the certificate chain, proxy configuration, and node resolver. Involve the network owner before changing trust stores.
- **Partial rollout stall:** Pause the rollout, identify the failing node set, and roll back the affected revision if pods are unavailable.

Escalate to the registry or platform owner when the failure involves provider-side incidents or shared credentials.

## Deliverable contract

Produce a short change record containing:

1. Scope: clusters, namespaces, and registries affected.
2. Inventory summary with counts of pinned, unpinned, and exception references.
3. Planned changes, each marked with the approval gate it passed or is awaiting.
4. Verification results with the raw evidence references listed above.
5. Rollback steps with the exact prior references.
6. Open risks, including any version-sensitive behavior not yet confirmed against official documentation.

Do not state that a deployment is secure, compliant, or certified. State only what was observed and verified.