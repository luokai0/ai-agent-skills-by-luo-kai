---
name: pipeline-and-supply-chain
description: Use when auditing, hardening, or designing CI/CD pipelines, build provenance, dependency and third-party action trust, artifact signing, or SBOM generation and review for software delivery.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Pipeline And Supply Chain

## Purpose and boundaries

This skill covers the integrity of how software is built, dependencies are admitted, and artifacts are released. It applies to CI/CD configuration, build runners, package resolution, container and binary artifacts, signing and attestation, and SBOM production and review.

It does not cover runtime application security, network perimeter design, or vulnerability triage of application logic. Hand those off explicitly and note the handoff.

## Inputs and assumptions

Before acting, collect:

- Pipeline definitions (workflow files, pipeline YAML, Jenkinsfiles, build scripts) and the repositories that trigger them.
- Runner types (hosted, self-hosted, ephemeral or persistent) and who can administer them.
- Credential inventory: where tokens, signing keys, and registry credentials live and how they are scoped.
- Dependency manifests and lockfiles, and the registries or mirrors used.
- Release targets: registries, deployment environments, and consumers.
- Any existing SBOMs, provenance attestations, or signatures.

Assume the pipeline runs with privileges that can publish artifacts or reach production until shown otherwise. Assume pinned references are mutable until verified.

## Operating workflow

1. **Map trust edges.** List every input the build consumes: source ref, base image, third-party actions or plugins, package dependencies, build tools, secrets, and cache contents. Mark each as pinned-by-digest, pinned-by-version, or floating.
2. **Map trigger paths.** Identify which events can run privileged jobs, especially those triggered by pull requests from forks, comments, or external contributors. Check whether untrusted code can reach secrets or signing steps.
3. **Audit permissions.** For each job, record granted token scopes and secret access. Flag any default or write-all permission, long-lived credentials, and secrets exposed to untrusted triggers.
4. **Check build integrity.** Verify that builds are reproducible or at least recorded: source commit, builder identity, parameters, and dependency resolution are captured.
5. **Check artifact chain.** Confirm artifacts are signed, the signing identity is bound to the pipeline (not a human laptop), and consumers verify signatures before deployment.
6. **Review SBOM.** Confirm an SBOM is generated from the built artifact (not only the manifest), in a standard format such as SPDX or CycloneDX, and that it lists components with versions and hashes.
7. **Produce findings** using the deliverable contract below.

## Decision gates

- **Gate A, privileged execution from untrusted input:** If untrusted code can access signing keys, deploy credentials, or write tokens, rate as critical and stop recommending fixes that merely document it. Require isolation redesign.
- **Gate B, mutable third-party references:** Floating tags on actions, plugins, or base images are high severity when the step holds secrets or produces release artifacts. Recommend digest or commit pinning, with a verification step.
- **Gate C, key custody:** Signing keys stored as plain pipeline secrets are medium-to-high. Prefer keyless or hardware-backed signing where the platform supports it. Confirm the exact mechanism against current official documentation before recommending it.
- **Gate D, changes to production pipelines:** Any edit to release, signing, or deployment workflows, rotation of credentials, revocation of signing identities, or changes to branch protection requires explicit human approval with the specific diff shown.
- **Gate E, external impact:** Publishing packages, pushing images, opening disclosure, or contacting upstream maintainers requires explicit approval.

## Verification and evidence

Every finding must cite file path and line or job name, the exact configuration fragment, and the trigger condition that makes it exploitable. Verify claims by:

- Reproducing the trigger in a non-production fork or dry-run mode where the platform allows it.
- Confirming pinned digests resolve to the intended content.
- Verifying signatures and attestations with the consumer-side tooling, and recording the identity and issuer matched.
- Checking that SBOM component counts are plausible against the resolved lockfile.

Quality checks: 100% of privileged jobs have an explicit permission block; zero floating references in release jobs; every release artifact has a verifiable signature and provenance record; SBOM covers all shipped components.

Do not state that a control "guarantees" supply chain safety or satisfies a named compliance framework. Describe what was verified and what was not.

## Failure handling

- If a config cannot be read or a platform feature is unclear, state the gap and mark the finding as unverified. Do not guess syntax or feature availability.
- If a version-sensitive detail (action syntax, attestation format, platform permission model) is uncertain, mark it for verification against current official documentation.
- If a secret may have been exposed in logs or repository history, stop, report it, and request approval for rotation. Do not attempt to use it to test.
- If a dry run would publish or deploy, do not run it.

## Deliverable contract

Return:

1. **Summary:** scope, pipelines reviewed, overall risk rating.
2. **Trust map:** table of inputs with pinning status.
3. **Findings:** ordered by severity, each with location, evidence, trigger, impact, and recommended change.
4. **Proposed changes:** minimal diffs, marked as requiring approval where Gates D or E apply.
5. **Unverified items:** what could not be checked and why.
6. **Verification plan:** commands or steps the owner can run, with expected results.

Do not include real secret values, tokens, or private key material in any output.