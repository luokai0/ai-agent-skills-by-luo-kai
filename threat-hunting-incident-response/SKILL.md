---
name: threat-hunting-incident-response
description: Use when hunting for or responding to suspicious activity involving external package registries (npm, PyPI, RubyGems, Maven Central, container registries, Helm, crates.io), including malicious package detection, dependency confusion, typosquatting, compromised maintainer accounts, and poisoned build artifacts.
author: Luo Kai
provenance: original
version: 1.1.1
---

# Threat Hunting Incident Response

## Purpose and boundaries

This skill covers hypothesis-driven hunting and incident response for supply-chain threats that enter an organization through external package registries and container registries. It applies when an analyst must determine whether a package, image, or registry credential was used maliciously in internal builds, developer workstations, CI runners, or deployed workloads, and then contain and remediate.

In scope: identifying malicious or suspicious packages already consumed; tracing dependency and image provenance; detecting dependency confusion and typosquatting in resolution logs; investigating leaked or abused publish tokens; assessing install-time and runtime execution; coordinating removal and rollback.

Out of scope: general endpoint forensics unrelated to package execution; vulnerability scanning program design; reporting malicious packages to registry operators without approval (that is an external action); attribution beyond what evidence supports.

## Inputs and assumptions

Required before starting:
- Trigger source (advisory, registry notice, EDR alert, anomalous egress, developer report).
- Package names, versions, digests, or image tags under suspicion. Treat unverified indicators as hypotheses.
- Access to lockfiles, SBOMs, build logs, package-manager proxy or mirror logs, CI audit trails, and registry publish/audit logs where available.
- Inventory of internal registries, mirrors, and scopes mapped to internal namespaces.

Assumptions to state explicitly in the case record: the time window; whether the proxy caches upstream content; whether lockfiles were committed and enforced; whether install scripts run in the affected ecosystem by default (verify against current official package-manager documentation, as behavior changes across versions).

## Operating workflow

1. **Open the case and freeze evidence.** Record the trigger, hypothesis, and scope. Snapshot relevant logs and lockfiles before any cleanup. Do not delete caches or rebuild images yet.
2. **Build the consumption inventory.** Search lockfiles, manifests, SBOMs, and image layers for the suspect name, version range, and digest. Include transitive dependencies. Record each hit with repository, commit, branch, and first-seen date.
3. **Establish the consumption timeline.** From proxy and mirror logs, CI logs, and developer resolution records, determine when each suspect artifact was first fetched and by which hosts or identities.
4. **Analyze the artifact.** Compare the suspect artifact to the last known-good version and to the publisher's historical releases: added install hooks, new network calls, obfuscated payloads, credential-file reads, environment-variable harvesting, new binaries, changed maintainer or publish metadata. Perform analysis in an isolated sandbox with no production credentials.
5. **Hunt for execution.** Search EDR, CI, and runtime telemetry for child processes spawned during install or build, outbound connections to unfamiliar domains, reads of credential stores (cloud configs, SSH keys, `.npmrc`, `.pypirc`, Docker config), and new persistence artifacts.
6. **Hunt for lateral and credential impact.** If execution is confirmed, enumerate exposed secrets in the affected environment and their usage since first execution.
7. **Contain.** Block the package or version at the proxy, pin known-good versions, and quarantine affected build outputs. See decision gates for approval requirements.
8. **Eradicate and recover.** Rebuild from clean lockfiles against a verified source, redeploy from images with verified digests, and rotate exposed credentials.
9. **Close with lessons learned.** Record detection gaps and convert hunting queries into standing detections.

## Decision gates

- **Gate A, escalate severity:** Any confirmed install-time or runtime execution of the artifact, or any evidence of credential access, raises the incident to high severity and requires incident commander notification.
- **Gate B, block at proxy:** Permitted on analyst judgment when the artifact is clearly malicious or untrusted. Requires change record. Blocking a widely used internal dependency requires owner approval because it can halt builds.
- **Gate C, credential rotation:** Requires approval from the credential owner. Rotate in dependency order: publish tokens and CI secrets first, then cloud keys, then user tokens. Confirm revocation succeeded.
- **Gate D, external actions:** Reporting to a registry operator, requesting takedown, contacting a package maintainer, or publishing a public advisory requires explicit approval from legal and the incident lead. Never perform these unilaterally.
- **Gate E, destructive actions:** Deleting images, purging registry caches, force-pushing branches, revoking shared credentials, or rebuilding production artifacts requires explicit approval with a documented rollback path.
- **Gate F, sensitive data:** Do not copy secrets, customer data, or full memory dumps into tickets or chat. Reference storage locations and hashes instead.

## Verification and evidence

Quality checks, each measurable:
- Every consumption hit has a repository reference, artifact digest or hash, and a first-seen timestamp.
- Every conclusion of "no execution" cites the telemetry source and query window covering the full consumption period.
- Every indicator is classified as confirmed, suspected, or refuted, with the evidence supporting each class.
- Blocked artifacts are verified as unresolvable from a test client after the block is applied.
- Rebuilt artifacts match expected digests from a trusted build, and the lockfile diff contains no unexplained changes.
- Rotated credentials show no use from old values after the rotation timestamp.

Example: a `postinstall`-style hook in a newly published minor version of a utility package, fetched by a CI runner at 02:14 UTC, followed by an outbound request to an unregistered domain and a read of the runner's cloud config. This is confirmed execution; escalate under Gate A and rotate the runner's cloud credentials under Gate C.

## Failure handling

- **Missing proxy logs:** Mark the timeline as partial. Use CI logs and lockfile history as secondary sources. Do not infer absence of consumption.
- **Ambiguous artifact analysis:** Escalate to a second analyst. Do not label as malicious or benign without reproducible evidence.
- **Telemetry gap during the window:** Document the gap explicitly and treat affected hosts as potentially exposed.
- **Blocking breaks builds:** Roll back the block, pin a verified prior version, and reassess with the owner.
- **Credential rotation fails:** Escalate immediately; keep the exposed credential flagged as compromised.

## Deliverable contract

The final case report must contain: incident summary and severity; hypothesis and scope; consumption inventory table (repository, artifact, version, digest, first-seen, last-seen); execution findings with evidence references; credential exposure and rotation status; containment and remediation actions with approval references; open items with owners; detection rules added. Do not claim the environment is clean without the verification checks above being satisfied. Version-sensitive package-manager and registry behaviors must be confirmed against current official documentation before being cited in the report.

## Ultron routing contract

**Choose this skill when:** there is a credible indication that a registry artifact or credential has already affected an organization. Triggers include a package or image found in builds or deployed systems, suspicious install-time/runtime execution, dependency-confusion evidence in resolution logs, abnormal registry publishing, or possible token theft.

**Use `security-threat-defense` for preventive review when:** the artifact has not been consumed and the question is whether it should be trusted, whether its provenance is valid, or whether a registry/publisher is suspicious.

**Handoff contract:** receive the suspected artifact identity and initial indicators, then establish where it was resolved, downloaded, installed, executed, or published. Return a time-bounded evidence timeline, affected assets and tenants, credential exposure assessment, containment decisions, recovery verification, and unresolved attribution. Preserve uncertainty; a malicious artifact finding does not prove every consumer executed it.

**Why the boundary exists:** incident response is driven by possible impact and evidence of exposure, not merely by an artifact being unusual. Keep preventive screening and retrospective hunting connected but operationally distinct.
