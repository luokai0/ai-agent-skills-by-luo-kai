# Security, Identity, and Trust

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## access-control

**Use when:** Use when designing, reviewing, or auditing who can access which resources (authorization models, RBAC/ABAC policies, IAM roles, least-privilege reviews, access requests, or permission revocation) in applications or cloud/infrastructure environments.

### Purpose and boundaries

This skill guides the design, review, and verification of authorization: deciding and enforcing which principals (users, services, workloads, API clients) may perform which actions on which resources, under which conditions. It covers application-level checks, identity and cloud policy (roles, grants, resource policies), access-request and review processes, and revocation.

It does not cover: authentication mechanics (credential storage, MFA enrollment, session token issuance), network perimeter design, cryptographic key management, or legal compliance determinations. Where these touch access decisions, flag the dependency and hand off.

### Inputs and assumptions

Collect before acting:

- Protected resources and their owners, with sensitivity classification.
- Principal types in scope (human, service account, CI job, third party) and the identity provider that asserts them.
- Current permission model (roles, groups, attributes, ACLs, policy documents) and where it is enforced (application code, gateway, cloud IAM, database).
- Required business rules expressed as who/what/when/where statements.
- Environment: production vs. non-production, tenant boundaries.

Assumptions must be written down. If the identity source of truth or resource inventory is unknown, stop and request it rather than inferring.

### Operating workflow

1. **Inventory.** List resources, actions, and current grants. Export the actual state (role assignments, policy documents, group memberships) rather than relying on design docs.
2. **Model.** Choose the simplest model that meets requirements: RBAC for stable job functions; ABAC or relationship-based checks when decisions depend on resource ownership, tenant, or attributes. Define roles or attributes as a closed vocabulary.
3. **Derive least privilege.** For each principal, map required actions to the minimum resource scope and duration. Remove wildcards on actions and resources unless a documented reason exists.
4. **Locate enforcement.** Each protected action must have exactly one authoritative check point per layer, default-deny on error or missing rule. Check that object-level checks exist, not just route-level.
5. **Diff.** Compare derived minimum against actual grants. Classify each excess as stale, unjustified, or justified-with-owner.
6. **Propose changes** as an ordered set: additive grants before removals, with rollback steps for each.
7. **Verify** (see below), then obtain approval before applying.

### Decision gates

Stop and obtain explicit human approval before:

- Removing or modifying grants for production principals, or any change that could lock out an operator or break a running service.
- Granting administrative, owner, or wildcard privileges.
- Changes to cross-account, cross-tenant, or third-party access.
- Disabling audit logging or altering retention.
- Bulk revocation or any action affecting more than one team.
- Any action that touches live identity providers, cloud consoles, or production data.

Proceed without a gate only for read-only analysis and drafting proposals in a non-production copy.

Escalate to a security owner when: an excess grant reaches sensitive data, a broken object-level check is found in production code, or an access pattern suggests compromise.

### Verification and evidence

Each change must have:

- **Positive tests:** the intended principal performs each permitted action (one test per role-action pair).
- **Negative tests:** each non-permitted principal is denied, including cross-tenant and unauthenticated cases, and an object ID belonging to another owner.
- **Default-deny test:** an unknown role, missing attribute, or policy evaluation error results in denial.
- **Drift check:** exported grants match the approved model after the change.
- **Audit check:** denials and grant changes are logged with principal, action, resource, and decision.

Quality targets: zero wildcard grants without a recorded exception; 100% of protected endpoints have a mapped permission in the inventory; every standing privileged grant has a named owner and review date no more than 90 days out (a local policy choice; adjust to your governance standard).

Record evidence as: the exported before/after grant set, test names and results, approver identity and timestamp, and rollback command or procedure.

### Failure handling

- **Test failure after change:** halt further changes, revert to the prior state using the recorded rollback, and document the failing case.
- **Lockout or service outage:** prioritize restoring a break-glass path using the pre-approved emergency procedure; do not improvise new admin grants.
- **Unknown principal or resource discovered:** treat as unauthorized until owner is identified; do not grant it access to resolve the ambiguity.
- **Conflicting rules:** the more restrictive rule wins; surface the conflict to the owner.
- **Cloud or IdP behavior uncertain:** verify against current official documentation for the specific product version before acting. Mark any version-sensitive syntax or flag as unverified until confirmed.

### Deliverable contract

Produce a single report containing:

1. Scope and assumptions (listed explicitly).
2. Model summary: roles/attributes, enforcement points, and default-deny confirmation.
3. Findings table: principal, resource, current grant, minimum required, classification (stale / excess / justified / missing), severity.
4. Ordered change plan with per-step rollback.
5. Gate list: each change requiring approval, marked pending.
6. Verification plan and results (or explicit "not yet run" status).
7. Open questions and owner assignments.

Do not claim a control is effective without the test evidence above. Do not state that a configuration satisfies any regulatory or framework requirement; state only what was checked.

### What not to do

- Do not grant broad access to unblock a task; grant the narrowest scope and document it.
- Do not treat authenticated as authorized.
- Do not rely on client-side hiding of UI elements as a control.
- Do not apply changes directly to production from analysis output.
- Do not copy permissions from one principal to another without re-deriving need.
- Do not invent role names, policy syntax, or API calls; confirm against current documentation.


## appsec-code-review

**Use when:** Use when reviewing application source code, pull requests, diffs, or modules for security and authentication flaws, including session handling, access control, credential storage, token validation, and input handling in web and API services.

### Purpose and boundaries

This skill guides a security-focused review of application code, with emphasis on authentication (who the caller is) and authorization (what they may do), plus the input and data handling that those controls depend on.

In scope: authentication flows, session and token lifecycle, password and secret handling, authorization checks on every data access path, input validation and output encoding at trust boundaries, cryptographic API misuse, and insecure defaults in configuration that ships with the code.

Out of scope: running live exploits against systems, infrastructure or cloud posture review, penetration testing, dependency license review, and compliance attestation. Do not claim that code is "secure" or "compliant"; report what was reviewed, what was found, and what was not checked.

### Inputs and assumptions

Required inputs: the diff or file set, the language and framework, and the intended trust model (public, authenticated users, tenants, admins, service-to-service).

Ask for missing items before concluding. If the trust model is unknown, state the assumption explicitly in the report.

Assume nothing about runtime configuration. Where behavior depends on deployment settings, mark the finding as conditional and list the setting to verify.

### Operating workflow

1. Map entry points. List every route, RPC handler, message consumer, and CLI entry touched by the change. Record which ones require authentication.
2. Trace identity. Follow how the caller's identity is established: header, cookie, bearer token, client certificate, or session store. Note where it is trusted and where it is first checked.
3. Check authorization per object. For each read, write, and delete, confirm the code verifies the caller's rights to that specific object, not just the route. Look for identifiers taken from the request and used directly in queries.
4. Review credential and secret handling. Check hashing algorithm and parameters, comparison method, logging of secrets, storage location, and hardcoded values.
5. Review token and session logic. Check signature verification, algorithm pinning, expiry, audience and issuer checks, revocation on logout and password change, and cookie attributes.
6. Review input and output boundaries. Check parameterization of queries, path and command construction, deserialization of untrusted data, redirect targets, and template output encoding.
7. Review error and logging paths. Confirm failures do not reveal account existence, stack traces, or tokens, and that security events are logged without sensitive values.
8. Record each finding with evidence before classifying severity.

### Decision gates

Gate A, scope: Stop and request clarification if the change touches authentication code but the trust model is unknown.

Gate B, severity: Rate a finding High when it allows unauthenticated access, cross-tenant or cross-user data access, privilege escalation, credential disclosure, or token forgery. Rate Medium when exploitation requires an existing authenticated session plus an unusual condition. Rate Low for defense-in-depth gaps with no demonstrated path to impact.

Gate C, confidence: Mark a finding Confirmed only when the code path from input to impact is traced in the reviewed source. Mark it Suspected when a dependency, middleware, or config value outside the diff determines the outcome.

Gate D, external action: Do not run tests against shared, staging, or production environments, send requests to live systems, rotate credentials, or open tickets in external trackers without explicit user approval. Propose the action and wait.

Gate E, sensitive material: If the code contains real-looking secrets, keys, or personal data, do not reproduce them in the report. Redact to the first four characters and the location.

### Verification and evidence

Every finding must cite file path, line range, the relevant code, and the specific condition that makes it exploitable. Where possible, supply a local unit test or reasoning trace showing the failing behavior, executed only in an isolated local environment.

Verify version-sensitive claims (library defaults, algorithm recommendations, framework middleware behavior) against current official documentation. Mark anything unverified as "requires verification" rather than asserting it.

Quality checks before delivery:
- Every High and Medium finding has a file-and-line citation and a stated trigger condition.
- No finding restates a framework default without checking the version in use.
- The list of reviewed entry points matches the list of entry points touched by the diff, with no silent omissions.
- Each route that requires authentication shows an identity check on the path.
- Coverage statement lists files read, files not read, and assumptions made.

### Failure handling

If the diff is incomplete or context is missing, report the gap and list the files needed. Do not infer the content of unseen functions.

If a finding cannot be confirmed, downgrade it to Suspected and state the missing evidence.

If a test or tool fails to run, record the exact error and do not substitute a claimed result.

If you discover evidence of an active compromise, such as unexpected credentials or exfiltration code, stop the review, report it immediately, and do not attempt remediation or further interaction with the affected system.

### Deliverable contract

Produce a report with these sections in order:

1. Summary: reviewed scope, trust model assumed, count of findings by severity and confidence.
2. Findings: each with ID, title, severity, confidence, location, trigger condition, impact, and recommended fix.
3. Positive controls observed: specific checks that were correctly implemented.
4. Coverage and gaps: files read, files not read, unverified assumptions, items requiring verification against official documentation.
5. Approval requests: any actions that need explicit user approval before proceeding.

Recommended fixes must be specific to the code shown and must not introduce new unverified APIs. Do not declare the code free of vulnerabilities.

### Ultron routing contract

**Choose this skill when:** reviewing application code for security defects at identity and data trust boundaries, especially authentication, authorization, session/token lifecycle, secrets, input validation, output encoding, cryptographic API use, and insecure shipped defaults.

**Choose software-quality-and-security-review when:** the requested review spans broader correctness, reliability, maintainability, design quality, and security rather than being primarily an application-security assessment.

**Handoff contract:** this skill returns security-specific findings, exploit preconditions, affected principals/resources, data exposure or privilege impact, and focused regression cases. The broader review skill may integrate those findings with non-security defects but must preserve their severity and evidence.

**Why the boundary exists:** security review needs threat-oriented reasoning and abuse cases; broad code review also evaluates correctness and maintainability. A general review must not dilute a security-critical finding.


## auth-implementation

**Use when:** Use when designing, implementing, reviewing, or migrating authentication flows (login, sessions, tokens, MFA, password reset, OAuth/OIDC client or resource-server integration) in an application or service.

### Purpose and boundaries

This skill guides implementation of authentication: verifying who a user or client is, and establishing and maintaining that identity across requests. It covers credential storage, login and logout, session or token issuance and validation, multi-factor enrollment and verification, account recovery, and integration with external identity providers using OAuth 2.0 or OpenID Connect.

It does not cover authorization policy design (what an authenticated principal may do), network perimeter security, key management infrastructure, or cryptographic primitive invention. Route those to the relevant skill or to a security owner. Never design custom cryptography; use vetted libraries and platform facilities.

### Inputs and assumptions

Collect before writing code:

1. Client types: browser SPA, server-rendered web, mobile, machine-to-machine, third-party API consumers.
2. Existing identity source: local user table, corporate IdP, social login, or migration from a legacy system.
3. Required assurance level: password-only, password plus second factor, or phishing-resistant factors.
4. Session model constraints: stateful server sessions, signed tokens, or mixed. Note revocation requirements.
5. Compliance or contractual obligations. State them as requirements to verify, not guarantees you provide.
6. Language, framework, and deployment platform, with exact versions.

If any input is missing, state the assumption explicitly in the deliverable. Do not guess at identity provider endpoints, client secrets, or tenant identifiers.

### Operating workflow

1. **Map the flows.** List every entry point: sign-up, login, step-up, logout, password change, reset, email change, MFA enroll and recover, token refresh, and service-to-service calls.
2. **Select the mechanism per flow.** Prefer delegating credential handling to an established IdP for user login. Use local credentials only when a delegated option is infeasible, and document why.
3. **Design credential storage.** Hash passwords with a memory-hard or adaptive algorithm from a maintained library (for example Argon2id or scrypt); verify current parameter recommendations in official library and OWASP documentation. Store per-user salts through the library's default mechanism. Never log, echo, or return credentials.
4. **Design session or token handling.** Set cookie attributes (Secure, HttpOnly, SameSite) explicitly. Rotate session identifiers on login and privilege change. For tokens, validate issuer, audience, expiry, signature algorithm (pin the expected algorithm, reject `none`), and clock skew tolerance.
5. **Implement recovery and MFA.** Reset tokens are single-use, high-entropy, short-lived, and stored hashed. Respond identically whether or not an account exists. Require re-authentication for MFA changes.
6. **Add abuse controls.** Rate-limit per account and per source, with lockout or backoff that does not enable trivial denial of service.
7. **Write tests** covering each flow's success and failure paths (see Verification).
8. **Produce the deliverable** per the contract below.

### Decision gates

Stop and obtain explicit approval before:

- Deleting or migrating existing user credentials, sessions, or tokens, or changing hashing parameters that force re-hash of stored passwords at scale.
- Rotating signing keys or client secrets in any shared or production environment.
- Changing redirect URIs, allowed origins, or identity provider registrations, since these affect external parties.
- Disabling MFA, widening token lifetimes, or accepting an additional identity provider.
- Running any test or script against production identity systems or real user data.
- Sending emails, SMS, or webhooks to real recipients.

Proceed without approval only for local code changes, unit tests, and fixtures using synthetic identities.

### Verification and evidence

Quality checks, each with a measurable outcome:

- Every auth endpoint has tests for: valid credentials, wrong password, unknown user (same response shape and comparable timing), locked or rate-limited state, expired or reused token, and missing or malformed input.
- Token validation tests reject: wrong issuer, wrong audience, expired token, altered signature, algorithm mismatch, and `alg=none`.
- Session cookies are verified in a response-header assertion: Secure, HttpOnly, and SameSite present with the intended values.
- Session ID changes after successful login (assert different value before and after).
- Reset tokens fail on second use and after expiry.
- No credential, token, or reset secret appears in logs; run a grep-style assertion over captured test logs.
- Password hashing parameters are recorded in the deliverable and checked against current official guidance, with the verification date stated.
- OAuth/OIDC flows use the authorization code flow with PKCE for public clients; the `state` and `nonce` parameters are generated per request and validated.

Evidence to attach: test names and pass counts, a list of flows covered, and any unverified items.

### Failure handling

- If a library or framework API is unfamiliar or its version is uncertain, do not invent method names or flags. Mark the detail as "verify against current official documentation for version X" and proceed with the rest.
- If a test reveals a credential or token leak, stop, redact the evidence, and escalate to the security owner before continuing.
- If an IdP integration fails in a non-test environment, roll back the configuration change and report; do not retry repeatedly against live endpoints.
- If requirements conflict (for example, long-lived sessions versus strict revocation), present two options with tradeoffs and wait for a decision.
- Never weaken a control to make a test pass.

### Deliverable contract

Return:

1. **Flow inventory**: table of flows, mechanism chosen, and rationale.
2. **Assumptions and open questions**: each with an owner.
3. **Implementation changes**: files changed and a summary of each security-relevant decision (storage, cookie attributes, token validation rules).
4. **Verification results**: tests run, outcomes, and checklist status against the Verification section, with unverified items labeled.
5. **Version-sensitive items**: every library, framework, or standard detail flagged for confirmation against official documentation, with the version it applies to.
6. **Approval log**: each decision gate triggered, the approval requested, and the outcome.

Do not claim the system is secure, compliant, or audited. State only what was implemented and tested.


## cloud-security-and-compliance

**Use when:** Use when assessing, hardening, or auditing cloud accounts, tenants, or workloads for security posture and compliance control mapping, including IAM review, network exposure, encryption, logging, and evidence collection for frameworks such as CIS benchmarks, SOC 2, ISO 27001, or PCI DSS.

### Purpose and boundaries

This skill covers reviewing cloud environments (IaaS, PaaS, managed Kubernetes, serverless, SaaS configuration tied to cloud identity) for security misconfigurations, mapping findings to compliance controls, and producing remediation plans and evidence packages.

In scope: identity and access policy review, network exposure analysis, data encryption and key management checks, logging and audit trail coverage, backup and resilience settings, vulnerability and secret exposure triage, and control-to-evidence mapping.

Out of scope: legal determination of compliance, certification sign-off (only an accredited auditor can attest), incident response execution beyond initial triage, penetration testing against systems without written authorization, and designing new application cryptography.

### Inputs and assumptions

Required inputs before starting:
- Cloud provider(s), account/subscription/project identifiers, and environment tier (prod, staging, dev).
- The target framework and version, and the specific control set in scope.
- Read-only access scope granted to the reviewer (preferably audit or security-reader roles).
- Architecture summary: workload inventory, data classification, internet-facing entry points.
- Date of the review and the audit period, if evidence must cover a window.

Assumptions to state explicitly in the report: configuration snapshots reflect the moment of capture; the reviewer has not verified application logic; provider-managed controls are accepted per the provider's shared responsibility documentation.

If any required input is missing, record it as a gap rather than guessing.

### Operating workflow

1. **Scope the control set.** Map the framework's controls to cloud domains (identity, network, data, logging, workload, change management). Record which controls are in scope and which are inherited from the provider.
2. **Collect configuration state read-only.** Use provider-native inventory and posture tooling, or export policy documents. Save raw exports with timestamps and hashes. Do not modify resources during collection.
3. **Analyze identity first.** Enumerate human and workload identities, privileged roles, long-lived access keys, MFA enforcement on console and CLI paths, cross-account trust, and wildcard permissions in policies.
4. **Analyze exposure.** Identify publicly reachable compute, storage, databases, management ports, and API endpoints. Trace routing and security group or firewall rules to confirm actual reachability, not just rule presence.
5. **Analyze data protection.** Confirm encryption at rest and in transit for storage, databases, and queues; check key ownership, rotation policy, and key access policies.
6. **Analyze logging and detection.** Confirm control-plane audit logs, data-plane access logs where applicable, and centralized retention. Verify log integrity protections and that logs cannot be disabled by the monitored principals.
7. **Triage findings.** Score each finding by exploitability, exposure, data sensitivity, and blast radius. Discard duplicates and provider-default-safe items.
8. **Map to controls and draft remediation.** Each finding maps to one or more control identifiers, has an owner, a fix recommendation, and a verification step.
9. **Package evidence.** Assemble the deliverable described below.

### Decision gates

Stop and request explicit human approval before:
- Any change to production IAM, network, encryption, or logging configuration, including "safe" hardening.
- Disabling, rotating, or deleting keys, secrets, snapshots, or log sinks.
- Running active scans, exploit checks, or any traffic against systems outside the authorized scope.
- Sharing evidence containing credentials, personal data, or internal topology outside the review team.
- Declaring a control "compliant" or "passed" for an external auditor.
- Accepting a risk on behalf of the business.

Proceed without approval only for read-only enumeration within the granted role.

Severity decision criteria:
- **Critical:** Publicly reachable admin or database interface with no authentication, or credentials exposed in a readable location.
- **High:** Privileged role assignable without MFA, unencrypted sensitive data store reachable from the internet, audit logging disabled in production.
- **Medium:** Overly broad but not wildcard permissions, missing key rotation within policy, logs retained below required period.
- **Low:** Hygiene issues without a demonstrated exposure path.

### Verification and evidence

Every finding must include: resource identifier, configuration excerpt or export reference, timestamp, the control mapped, and a reproducible check command or console path. Verify each finding twice: once by policy document, once by effective state (for example, effective permissions or reachability), since policies can be overridden by boundaries, conditions, or other rules.

Measurable quality checks before delivery:
- 100% of in-scope controls have a status: pass, fail, not applicable with reason, or insufficient evidence.
- Zero findings without a resource identifier and evidence reference.
- Every critical and high finding has a named owner and a target remediation date set by the business.
- Raw exports are hashed and retained in the evidence store.
- Provider feature behavior cited in the report is checked against current official documentation on the review date.

Mark version-sensitive details (API field names, default settings, supported algorithms, service limits) with the note "verify against current provider documentation" rather than stating them as fact.

### Failure handling

- **Insufficient permissions:** Record the blocked control as "insufficient evidence." Do not escalate privileges to fill the gap.
- **Conflicting data between tools:** Trust the provider's control-plane export over third-party summaries, and note the discrepancy.
- **Resource appears misconfigured but is unreachable or disabled:** Downgrade severity and document the reason; recheck after the review window.
- **Discovered active compromise indicators:** Stop the review, preserve current state, and escalate to the incident response owner. Do not attempt remediation.
- **Scope ambiguity:** Pause and request clarification on account boundaries before analyzing.

### Deliverable contract

The output is a single report containing, in order:
1. Scope statement, assumptions, and input gaps.
2. Control matrix: control ID, framework, status, evidence reference, reviewer note.
3. Findings register: ID, severity, resource, description, control mapping, evidence, remediation, owner, verification step.
4. Remediation plan grouped by owner, with items requiring approval marked.
5. Evidence index with export names, capture times, and hashes.
6. Limitations and version-sensitivity notes.

Do not include raw secrets, full access keys, or unredacted personal data in the report; reference their location instead.

Do not claim the environment is "secure" or "compliant." State findings and control status only.

### Ultron routing contract

**Choose this skill when:** reviewing a real cloud environment for security configuration defects and mapping technical findings to the organization's control framework, with remediation and evidence planning.

**Choose security-governance when:** the task is to define security requirements, control ownership, access review policy, exception handling, or organization-wide security standards rather than inspect a particular environment.

**Handoff contract:** receive the control objectives, approved risk thresholds, and evidence requirements from governance. Return the resource-level observations, technical proof, severity, remediation plan, and any control that cannot be evaluated. Send unresolved policy conflicts or exception requests back to governance with scope and impact.

**Why the boundary exists:** a cloud configuration scan cannot decide the organization's policy, and a written policy cannot prove that a cloud resource is configured correctly.


## hardening-appsec-pentest

**Use when:** Use when planning, executing, or reviewing authorized application security testing or hardening work against external-facing package and artifact registries (container registries, package indexes, mirrors, proxies, and their authentication, publishing, and dependency-resolution paths).

### Purpose and boundaries

This skill guides authorized application security assessments and hardening of external artifact registries: container image registries, language package indexes, private or public mirrors, pull-through proxies, and the CI/CD paths that publish to or consume from them. Its goal is to find exploitable weaknesses, prove their impact with minimal intrusion, and deliver prioritized fixes.

In scope: authentication and token handling, authorization on read, write, delete, and tag-mutation operations, namespace and tenant isolation, upload validation, manifest and metadata integrity, signing and provenance verification, dependency confusion exposure, mirror and proxy trust configuration, rate limiting and abuse controls, TLS and redirect handling, and verbose error or metadata leakage.

Out of scope unless separately authorized in writing: testing third-party registries you do not operate or have permission to test, denial-of-service load tests, social engineering, publishing packages to public indexes, overwriting or deleting production tags, and accessing data belonging to other tenants.

### Inputs and assumptions

Before any active testing, confirm:

1. A signed rules-of-engagement document naming targets (hostnames, namespaces, repositories), permitted techniques, time windows, and contacts.
2. Test accounts with the minimum roles needed, separately provisioned for each role tested (anonymous, reader, publisher, admin-equivalent for control checks only).
3. A staging or sandbox registry that mirrors production configuration. Default to it.
4. Whether canary package names and tags are approved, and which namespace prefix they will use.
5. The current official documentation for the registry software and its API version. Any endpoint path, header, claim name, or configuration key you recall from memory must be verified against that documentation before use.

Assume nothing about versions, default settings, or feature availability. Record the exact product version and build reported by the target during reconnaissance.

### Operating workflow

1. **Scope lock.** Write the target list, roles, and forbidden actions into the test log. Re-confirm scope if a finding reveals adjacent systems.
2. **Passive reconnaissance.** Map public endpoints, TLS configuration, published advertisement or discovery documents, and response headers. Record the product, version, and auth scheme. No write attempts.
3. **Authentication review.** Test unauthenticated access to read, list, and catalog endpoints. Check token scope enforcement by replaying a reader-scoped token against write endpoints in the sandbox. Verify token expiry, revocation, and rotation behavior.
4. **Authorization matrix.** For each role and each operation (pull, push, list, delete, retag, metadata update), record expected versus observed result in a matrix. Any mismatch is a candidate finding.
5. **Namespace isolation.** Using two sandbox tenants, confirm one tenant cannot enumerate, pull, or overwrite the other's repositories, including through name-prefix tricks, case variation, and unicode normalization.
6. **Upload and integrity checks.** Push a benign artifact, then test: digest mismatch handling, tag overwrite policy, manifest size limits, malformed archive rejection, and whether metadata claims are validated against content.
7. **Dependency resolution risk.** Determine whether internal and public sources are resolved with a defined priority. Test in sandbox only whether an unscoped name can be satisfied from a public source when a private one is expected. Use canary names only.
8. **Signing and provenance.** Verify whether signature or attestation verification is enforced at pull or deploy time, and whether unsigned or wrongly signed artifacts are rejected.
9. **Abuse controls.** Confirm rate-limit presence with low-volume, bounded requests (for example, a small fixed count per window). Do not exceed agreed thresholds.
10. **Evidence capture and cleanup.** Record requests and responses with secrets redacted. Delete only canary artifacts you created, and only in the sandbox.

### Decision gates

- **Gate A (before any write test):** Stop unless the target is confirmed as sandbox or explicitly approved in writing for that action.
- **Gate B (before testing production-adjacent endpoints):** Require named owner approval and a read-only plan.
- **Gate C (before exploiting a confirmed weakness beyond proof-of-presence):** Stop and escalate. Proof-of-presence means one minimal, reversible demonstration, such as reading a non-sensitive canary object from another namespace.
- **Gate D (any credential discovered during testing):** Stop using it, record its location, and report to the owner for rotation. Do not validate it against other systems.
- **Gate E (finding touches data of real users or other tenants):** Halt, do not retain the data, notify the owner through the agreed channel.
- **Gate F (any action that would delete, overwrite, publish, or change a live configuration):** Obtain explicit written approval naming the exact action and object.

### Verification and evidence

Each finding requires:

- Reproduction steps with exact request method, path pattern, role used, and timestamp.
- Expected behavior cited from the target's current official documentation or internal policy, with the document version.
- Observed behavior, with status codes and relevant headers, secrets redacted.
- Severity rationale that states likelihood and impact separately, not a single unexplained label.
- Negative control: the same test against a correctly configured baseline, or confirmation that the control behaves as documented.

Quality checks before reporting:

- Every finding reproduces at least twice on separate runs.
- No finding relies on a version or default that was not confirmed against the observed build.
- Each recommendation names a configuration or code location to change and a re-test that proves the fix.
- Matrix coverage: 100% of listed role-operation pairs have a recorded result or an explicit "not tested" reason.

### Failure handling

- **Unexpected production impact** (latency spike, error burst, locked account): stop immediately, notify the owner, record the timeline. Do not retry.
- **Tool or endpoint behaves differently than documented:** treat documentation as possibly stale; record the discrepancy and verify against the vendor's current release notes before drawing conclusions.
- **Ambiguous result:** mark as "unconfirmed," do not report as a vulnerability, and design one additional controlled test.
- **Accidental out-of-scope access:** stop, do not browse further, document what was touched, and report within the engagement's notification window.
- **Leaked credential in output:** redact in all artifacts, rotate through the owner, and note the exposure in the report.

### Deliverable contract

The final deliverable is a single report containing:

1. Scope statement and rules-of-engagement reference.
2. Target inventory with product versions as observed.
3. Authorization matrix with results.
4. Findings table: identifier, title, affected component, role required, likelihood, impact, status (confirmed, unconfirmed, accepted risk), evidence reference.
5. Prioritized remediation plan: fix, owner, configuration location, re-test procedure, target date set by the owner.
6. Items not tested, with reasons.
7. Redaction and data-handling statement confirming no third-party data was retained.

Do not state that the system is "secure," "compliant," or "guaranteed" against any attack class. Report only what was tested, under what conditions, and with what observed result.

### What not to do

- Do not test against production write paths or real tenant namespaces.
- Do not publish canary packages to public indexes.
- Do not reuse discovered credentials or pivot to other systems.
- Do not cite exact API names, flags, or version numbers from memory; verify each against current official documentation first.
- Do not run brute force, credential stuffing, or high-volume fuzzing.
- Do not retain or summarize data belonging to others.


## pentest-and-threat-modeling

**Use when:** Use when planning or reviewing a penetration test, threat model, or authentication security assessment, including scoping, attack-surface mapping, authentication and session abuse testing, authorization checks, and writing findings with reproducible evidence.

### Purpose and boundaries

This skill produces two linked artifacts: a threat model that decides what is worth testing, and a penetration test plan and report that proves or disproves those threats with evidence. It covers web, API, and identity-centric systems, with emphasis on authentication, session management, MFA, password reset, OAuth/OIDC flows, and authorization (IDOR, privilege escalation, tenant isolation).

It does not cover: unauthorized testing of any system, denial-of-service or load testing, social engineering against real people, physical intrusion, malware development, or exploitation beyond what is needed to demonstrate impact. Refuse to proceed on any target without written authorization that names the systems, environments, and time window.

### Inputs and assumptions

Collect before starting. Record missing items as assumptions and list them in the deliverable.

- Signed authorization: scope (hosts, domains, APIs, accounts), out-of-scope items, testing window, named contacts, and emergency stop procedure.
- Architecture: components, trust boundaries, data flows, identity provider, token types, hosting, third-party services.
- Data classification: what sensitive data exists and where.
- Test accounts: at least two per privilege tier and per tenant, provisioned for testing, never real customer credentials.
- Environment: production or staging. Production testing requires explicit approval per activity.
- Prior results: earlier reports, scanner output, known issues.

Assume nothing about rate limits, backups, or monitoring thresholds; confirm them.

### Operating workflow

1. **Define scope and rules of engagement.** Write objectives, in-scope assets, prohibited techniques (for example, account lockout triggering against real users, data exfiltration beyond proof), and the stop condition.
2. **Model the system.** Draw data flow diagrams with trust boundaries. Enumerate entry points: login, registration, password reset, MFA enrollment and verification, token issuance and refresh, API endpoints, admin interfaces, webhooks, file uploads.
3. **Build the threat model.** For each entry point and trust boundary, apply STRIDE or an equivalent structured method. Score each threat by likelihood (grounded in exposure and attacker precondition) and impact (data, integrity, availability, compliance). Rank by risk, not by count.
4. **Derive test cases.** Map each high-ranked threat to a concrete, falsifiable test. Example: "Refresh tokens from logged-out sessions remain valid" is testable; "check auth" is not.
5. **Map attack surface passively first.** Review documentation, OpenAPI/GraphQL schemas if provided, client code, and public metadata. Then perform authorized active discovery within scope.
6. **Execute tests in risk order.** Use two-account comparisons for authorization: the same request as user A against user B's objects, and as an unauthenticated caller. Record exact requests, responses, timestamps, and account identifiers.
7. **Validate and minimize.** Reproduce each finding at least twice. Demonstrate impact with the smallest safe proof, such as reading one non-sensitive test record rather than bulk extraction.
8. **Report.** Write findings with severity, reproduction steps, evidence, root cause, and remediation verified against the architecture.
9. **Retest.** After remediation, rerun the original reproduction and record the result.

### Decision gates

Stop and request approval before proceeding when any of the following is true:

- The action is destructive or irreversible (deleting data, changing account state, altering configuration, consuming single-use resources such as payment or email quotas).
- The action affects production users or shared systems (password spraying, lockout testing, mass enumeration, high-volume requests).
- The action touches real personal, financial, health, or credential data beyond a minimal proof.
- The target appears to be a third party (external SaaS, partner API, CDN) not explicitly in scope.
- A vulnerability suggests active compromise. Pause, preserve evidence, and escalate to the named contact immediately.
- Testing would require bypassing a control that was explicitly excluded.

Proceed without further approval only for read-only or self-owned test-account actions within the approved window.

### Verification and evidence

Every finding must include:

- A one-sentence claim (for example, "Any authenticated user can read invoices of other tenants via GET /api/v2/invoices/{id}").
- Preconditions: account tier, tenant, network position, required state.
- Exact reproduction: request sequence with headers and bodies, redacting secrets as `[REDACTED:type]`.
- Observed versus expected behavior.
- Evidence: response excerpts, timestamps, and screenshots only where text is insufficient.
- Confidence level and what was not tested.

Quality checks before delivery:

- Every high or critical finding has two independent reproductions.
- Every threat in the model is marked tested, not applicable (with reason), or deferred (with owner).
- No credentials, session tokens, or personal data appear in the report body.
- Severity is justified against the threat model's impact criteria, not stated by intuition.
- Remediation is specific (for example, "enforce object ownership check server-side in the invoice query by tenant_id from the verified token") and has a retest plan.

Mark any version-sensitive claim about a library, framework, protocol default, or cloud service as requiring verification against current official documentation. Do not state compliance outcomes; describe observed control behavior only.

### Failure handling

- **Access lost or scope ambiguous:** halt, document the last safe state, and request clarification.
- **Unexpected impact** (errors affecting other users, service degradation): stop the activity immediately, notify the contact, and log timestamps.
- **Credentials exposed during testing:** treat as a finding, do not reuse, and request rotation.
- **Non-reproducible result:** mark as unconfirmed with the attempts made; do not report as validated.
- **Tool output contradicts manual validation:** trust the reproduced behavior; record the tool discrepancy.
- **Time window expires mid-test:** stop, summarize progress, and resume only after re-authorization.

### Deliverable contract

The final output contains, in order:

1. Executive summary: scope, dates, top three risks, and overall posture in plain language.
2. Rules of engagement and assumptions, including any unconfirmed inputs.
3. Threat model summary: diagram or component list, trust boundaries, ranked threats with rationale.
4. Findings table: ID, title, severity, status (validated, unconfirmed, accepted), affected asset.
5. Detailed findings following the verification structure above.
6. Coverage matrix: each test case mapped to tested, not applicable, or deferred.
7. Remediation roadmap ordered by risk reduction per effort, with owners and retest criteria.
8. Limitations and items requiring verification against current vendor documentation.

Do not include exploit code for unpatched vulnerabilities beyond reproduction steps needed for the owner to verify the fix.


## secrets-and-cryptography

**Use when:** Use when designing, reviewing, or troubleshooting how an application or infrastructure stores, distributes, rotates, or uses secrets, keys, certificates, or cryptographic primitives, including key management, TLS configuration, hashing, encryption at rest, and secret leakage remediation.

### Purpose and boundaries

This skill guides professional work on secret handling and applied cryptography: credential and key lifecycle, secret storage and injection, encryption design choices, certificate and TLS posture, password and token hashing, and response to exposed secrets.

In scope: reviewing code and configuration for hardcoded or leaked secrets; choosing vetted primitives and modes; designing key hierarchies and rotation; evaluating secret managers and injection paths; assessing TLS and certificate settings; planning revocation after exposure.

Out of scope: inventing custom cryptographic algorithms or protocols; defeating access controls on systems you do not own; producing working exploit code against third-party systems; certifying compliance with any framework.

### Inputs and assumptions

Gather before advising:
- Asset type (API key, database credential, signing key, TLS certificate, user password, encryption key, session token).
- Data sensitivity and who or what must access it.
- Current storage location, injection method, and rotation practice.
- Runtime environment, language, and libraries in use.
- Threat model: insider, external attacker, lost device, leaked repository, compromised dependency.
- Recovery requirements: can data be re-encrypted, can keys be destroyed, what is the outage tolerance.

State assumptions explicitly. If a critical input is missing, stop and request it rather than guessing.

### Operating workflow

1. Inventory secrets. List every secret, key, and certificate with owner, location, consumers, and expiry. Search version history, not only current files, for exposed material.
2. Classify each item by sensitivity and blast radius.
3. Trace the lifecycle: generation, storage, distribution, use, rotation, revocation, destruction.
4. Check generation. Keys and tokens must come from a cryptographically secure random source provided by the platform or a vetted library. Human-chosen values are not secrets.
5. Check storage. Secrets belong in a dedicated secret store or a hardware-backed key facility. Environment variables are acceptable for injection only when the platform restricts their exposure; they are never a storage location.
6. Check use. Verify secrets are not logged, echoed in error messages, placed in URLs, cached in client code, or passed in query strings.
7. Check primitives. Prefer authenticated encryption with associated data, and established password hashing functions with work factors tuned to current guidance. Confirm the exact algorithm, mode, and parameters against the library's current official documentation.
8. Define rotation: trigger events, overlap window for dual-valid credentials, and automated versus manual steps.
9. Produce findings and remediation in priority order.

### Decision gates

Stop and request explicit human approval before any of the following:
- Rotating or revoking a production credential, certificate, or signing key.
- Re-encrypting or migrating data stores in place.
- Destroying or disabling any key, including keys believed to be compromised but still protecting live data.
- Changing TLS or authentication settings on externally reachable services.
- Publishing, disclosing, or transmitting exposed secret values outside the organization.
- Running any test that sends real credentials to a third-party endpoint.

Proceed without approval only for read-only analysis, local reasoning, and drafting remediation plans.

Choose the primitive by purpose:
- Confidentiality with integrity: authenticated encryption with a unique nonce per message under one key.
- Message integrity between parties sharing a key: keyed MAC.
- Signatures: asymmetric signature scheme with the key held by a single controlled signer.
- Password storage: slow, salted, memory-hard or adaptive password hash. Never a general-purpose hash alone.
- Random identifiers that need unguessability: cryptographically secure random generator, not a time-seeded or sequential source.

### Verification and evidence

Each finding must cite the file, line, configuration key, or system record that shows it. Quality checks:
- Secret scan of the repository history and build artifacts reports zero live secrets after remediation, using a scanner whose version and rules you have confirmed.
- Every key has a recorded owner, creation date, and next rotation date.
- Rotation has been rehearsed in a non-production environment with both old and new credentials verified to behave as specified during the overlap window.
- TLS configuration is checked with an approved scanner or a documented manual handshake test; certificate chain validates and hostname matches.
- Encryption round-trip test passes, and tampered ciphertext is rejected with an error rather than producing output.
- Logs sampled from the last defined period contain no secret patterns.

Mark any statement about algorithm strength, library defaults, or protocol versions as requiring confirmation against current official documentation. Do not assert compliance with a standard.

### Failure handling

- Secret found in version control: treat as compromised regardless of repository visibility. Recommend revocation and replacement first, history rewriting second, and request approval for both.
- Scanner false positive: document the pattern and reason; do not suppress rules broadly.
- Missing consumer information during rotation planning: halt rotation, enumerate known consumers, and request owner confirmation.
- Rotation breaks a consumer: roll back to the overlap credential if the window is still open; otherwise escalate.
- Ambiguous cryptographic requirement: list the candidate primitives with tradeoffs and ask the owner to choose.
- Conflicting guidance between sources: prefer the current official documentation of the specific library or platform and note the discrepancy.

### Deliverable contract

Return a document containing, in order:
1. Scope and assumptions, including unanswered inputs.
2. Secret and key inventory table: item, type, location, owner, consumers, expiry, status.
3. Findings ranked by severity, each with evidence reference, risk, and specific remediation.
4. Proposed rotation or migration plan with ordered steps, rollback point, and approval gates marked.
5. Verification checklist with the checks above marked pass, fail, or not yet run.
6. Open questions and items requiring version confirmation.

Do not include actual secret values in the output. Redact to the first four characters at most, or describe the value by type and fingerprint.

### Agent credential broker and token exchange (v1.1)

An agent should request an authorized operation, not receive the credentials that make every operation possible. Put vendor credentials, OAuth refresh tokens, signing keys, and service secrets behind a credential broker or narrowly scoped egress gateway.

#### Broker responsibilities
The broker is a trusted security component outside the model context and outside untrusted tool output. It should:
1. Authenticate the calling workload and verify the task authorization envelope.
2. Confirm that the requested destination, operation, tenant, and resource are allowed by policy.
3. Obtain or exchange a credential for that destination using a managed identity or approved OAuth flow.
4. Restrict the credential to the minimum audience, scopes, resource set, and lifetime supported by the provider.
5. Attach the credential to the outbound request without returning it to the agent.
6. Record a redacted audit event linking the agent, task, initiating subject, credential class, destination, and decision.
7. Revoke or invalidate broker-side grants when the task, user consent, or upstream authorization is withdrawn.

#### Delegated OAuth and workload credentials
Keep service authority and user-delegated authority distinct. A service-to-service credential represents the workload; a delegated OAuth credential represents a user-approved grant. Do not silently substitute one for the other.

For delegated access:
- Use the provider's supported authorization-code and consent flow, with PKCE where applicable.
- Store refresh tokens only in the approved secret store or broker vault.
- Exchange or refresh tokens inside the broker, not in model-visible code or prompts.
- Validate issuer, signature, expiry, authorized party, audience, scopes, tenant, and token binding where supported.
- Do not accept a token merely because it is syntactically valid or was returned by a tool.
- Never pass a token issued for one API audience to a different resource server.
- Do not forward inbound user tokens to downstream services as a shortcut. Perform an explicit, policy-checked exchange.

#### Credential isolation
- Give each integration a separate credential identity and policy.
- Avoid a single global API key shared by unrelated agents, tenants, or tasks.
- Keep credentials out of command arguments, URLs, browser-visible storage, source code, traces, crash dumps, and generated artifacts.
- Prefer short-lived credentials and managed identity over long-lived static secrets.
- Use per-task or per-tenant credential caches only when the cache key includes every authorization dimension; never reuse a broader cached token for a narrower request.
- Make secret retrieval an explicit broker action with a policy decision, not a general-purpose file read exposed to the agent.

#### Rotation and incident response
Track owner, provider, scopes, audience, consumers, expiry, last use, and revocation method for every brokered credential. Support overlapping rotation windows only as long as needed, then revoke the old credential. On suspected exposure, revoke at the provider, invalidate broker caches, inspect use logs, identify affected tasks and tenants, and rotate dependent credentials. Do not assume deleting a secret from the current repository removes copies from history, logs, caches, or build artifacts.

#### Broker acceptance tests
Verify that:
- The model and agent process cannot read the broker's stored refresh token or static secret.
- A credential for service A is rejected by service B.
- A read-only task cannot obtain a write-scoped credential.
- Revoked consent prevents future refresh and new outbound calls.
- A cached token cannot cross tenant, subject, audience, or task boundaries.
- Broker logs contain enough evidence to investigate use but no reusable secret material.

If the upstream provider cannot express the required scope or resource restriction, enforce it in the broker and egress policy, and document the remaining blast radius.

### Ultron routing contract

**Choose this skill when:** designing or reviewing secret storage, cryptographic key handling, credential rotation, OAuth/token lifecycle, signing and verification, encryption, hashing, and credential-broker behavior.

**Choose `agent-runtime-security-guardrails` when:** the main question is which agent, user, task, or workload may access a resource and how delegated authority is enforced.

**Choose `mcp-server-hardening` when:** reviewing how an MCP server authenticates callers, stores or uses its credentials, and protects its transport and tool boundary.

**Handoff contract:** the runtime security skill supplies the principal, audience, resource, operation, and expiry requirements. This skill returns a credential or key-management design that enforces those limits without exposing reusable secret material to the model. The MCP hardening skill verifies that the server's actual transport and secret handling preserve the design.

**Why the boundary exists:** cryptography protects credentials and data; authorization determines who may use them. Strong cryptography does not compensate for overbroad permissions.


## security-access-hardening

**Use when:** Use when auditing or tightening access controls on Linux hosts, including SSH configuration, local accounts, sudo policy, file permissions, service privileges, and firewall exposure, and a change must be planned, verified, and rolled back safely.

### Purpose and boundaries

This skill covers reducing unnecessary access on Linux systems: authentication paths (SSH, console, PAM), privilege escalation (sudo, setuid, capabilities), account hygiene (users, groups, service accounts, shells, password aging), filesystem permissions on sensitive paths, and network reachability of administrative services.

It does not cover application-level authorization logic, malware removal, kernel exploit remediation, cloud IAM policy, or compliance attestation. Do not claim a host is "compliant" or "secure"; report which checks passed, failed, or were not run.

### Inputs and assumptions

Before changing anything, collect:

- Host inventory: hostname, distribution and release, init system, role, and owner.
- Current access paths: SSH listening ports, `AllowUsers`/`AllowGroups` settings, console access, out-of-band management.
- Business-critical sessions that depend on current access (automation, backups, monitoring agents).
- Change window, rollback owner, and an out-of-band recovery path (console, hypervisor, or IPMI) confirmed working.
- Existing configuration management (Ansible, Puppet, Salt, or none). Changes made outside it will be reverted.

Assume a hardening change can lock out operators. Treat a live session as your only proof of access until a second independent session succeeds.

### Operating workflow

1. **Baseline capture.** Record the current state before editing: `sshd -T` output (effective config, not file contents), `sudo -l` for each relevant account, `getent passwd` and `getent group`, `ss -tlnp` for listeners, `find` for setuid/setgid files and world-writable paths, and `ls -l` on `/etc/sudoers.d`, `/etc/ssh`, and `/root`. Save to a timestamped evidence directory.
2. **Identify exposure.** Rank findings by reachability and privilege: unauthenticated network services first, then password-based remote login, then local privilege paths, then hygiene items.
3. **Draft minimal changes.** One control per change. Prefer dropping files into include directories (`/etc/ssh/sshd_config.d/`, `/etc/sudoers.d/`) over editing vendor files. Validate sudoers drafts with `visudo -cf <file>` and SSH drafts with `sshd -t` before reload.
4. **Stage on a non-production host** when one exists with equivalent configuration.
5. **Apply with a safety net.** Keep an existing root or admin session open. Apply the change, then open a new session from a separate terminal before closing the original.
6. **Verify** (see Verification section).
7. **Record** the final state and the rollback command for each change.

### Decision gates

Stop and obtain explicit written approval before:

- Disabling password authentication, root login, or any login method on a host without a verified key-based admin account.
- Changing sudo policy for any account that performs automation or break-glass access.
- Removing accounts, deleting home directories, or changing UID/GID of existing users or services.
- Modifying firewall rules on a remote host where the management path traverses the rule set.
- Any action affecting shared, production, or externally reachable systems.
- Changing file ownership or permissions on paths used by running services.

Proceed without a gate only for read-only inspection, drafting, and validation in a non-production copy.

Use these criteria when choosing a setting:

- Remove a setuid bit only if the binary is not required by an installed package and the package manager can reinstall it.
- Restrict `AllowUsers` to named accounts only after confirming every automation identity is listed.
- Prefer `PermitRootLogin prohibit-password` over `no` when out-of-band root recovery is the only fallback; choose `no` only when an alternative admin account is verified.

### Verification and evidence

Each change requires:

- Syntax check passed (`sshd -t`, `visudo -c`, or the equivalent for the modified file).
- Effective configuration matches intent (`sshd -T | grep -i <directive>`).
- A new session succeeds with the intended identity and fails with a disallowed one (test with a non-admin account; expect denial).
- Listener set matches the approved list (`ss -tlnp` diff against baseline).
- Permission changes confirmed with `stat -c '%U:%G %a %n' <path>`.
- Service restart or reload succeeded and `systemctl status` shows active.

Evidence package: baseline output, diffs, validation output, test session transcripts (credentials redacted), and rollback commands. Do not include private keys, password hashes, or tokens in evidence.

Mark any command output that depends on distribution or OpenSSH version as "verify against current official documentation" when the exact directive behavior is uncertain.

### Failure handling

- **Validation fails:** do not reload. Revert the draft and fix the syntax.
- **New session fails after reload:** do not close the original session. Revert the change, confirm the original session still works, then investigate.
- **Lockout occurs with no session:** use the pre-confirmed out-of-band path. Do not attempt repeated failed logins, which may trigger lockout or fail2ban bans.
- **Automation breaks after change:** restore the prior configuration, then map which identity or port the job uses before retrying with an explicit allow entry.
- Log every failure with timestamp, command, and observed output.

### Deliverable contract

Deliver a report containing:

1. Scope and host list, with the approval reference for each gated action.
2. Findings table: item, risk level, evidence reference, status (fixed, deferred, accepted with reason).
3. Applied changes: exact file paths, before and after values, and rollback command.
4. Verification results with pass/fail per check.
5. Open items and residual risk, stated plainly.
6. Confirmation that out-of-band access was tested, or an explicit statement that it was not.

Do not state that a host is hardened, secure, or compliant. State only what was changed and what was verified.


## security-governance

**Use when:** Use when defining, reviewing, or auditing security policies, access control models, authentication standards, secrets handling, or security exception processes for a system, team, or organization, and when translating security requirements into enforceable controls with owners, evidence, and review cadence.

### Purpose and boundaries

This skill governs how security requirements are decided, assigned, implemented, verified, and retired. It covers authentication and authorization policy, identity lifecycle, privileged access, secrets management policy, security exception handling, and control ownership mapping.

In scope: writing or reviewing security standards; mapping requirements to controls; defining access reviews; approving or rejecting exceptions; producing audit-ready evidence checklists.

Out of scope: performing live penetration tests, rotating production credentials, changing identity provider configuration, or making legal or regulatory compliance determinations. Those require the named owner and explicit approval (see Decision gates).

### Inputs and assumptions

Before acting, confirm:

1. System or scope name, owner, and data classification (public, internal, confidential, restricted).
2. Existing policy documents, control inventory, and identity provider or access tooling in use.
3. The requirement source (internal standard, customer contract, regulation). Record it verbatim; do not paraphrase it into a stronger or weaker claim.
4. Current state evidence: access lists, configuration exports, review records, incident history for the scope.
5. Named approvers for risk acceptance.

If any item is missing, record it as an open question and proceed only with analysis that does not depend on it. Do not assume a control exists because a policy mentions it.

### Operating workflow

1. **Scope the asset.** List systems, identities (human, service, workload), and data classes in scope. Exclude nothing silently; list exclusions with reasons.
2. **Extract requirements.** Convert each source statement into a numbered requirement with a single testable condition. Example: "Admin access requires MFA" becomes "All accounts holding role `admin` in the production tenant must have an enrolled phishing-resistant or app-based second factor, verified at login policy level."
3. **Map to controls.** For each requirement, identify the preventive control (policy setting, technical enforcement), the detective control (review, log alert), and the owner. A requirement with no owner is not accepted.
4. **Assess current state.** Compare the control to observed configuration or records. Classify each as Met, Partially Met, Not Met, or Unverifiable.
5. **Prioritize gaps.** Rank by data classification and exposure: internet-reachable, privileged, or restricted-data paths first.
6. **Draft remediation.** For each gap, state the change, the rollback path, the owner, and the target review date. Do not set dates you cannot justify from capacity.
7. **Record exceptions.** Any unmet requirement not remediated in the window becomes an exception with compensating controls, expiry date, and approver.
8. **Schedule verification.** Define the evidence to be collected and the next review date.

### Decision gates

Stop and obtain explicit written approval from the named owner before:

- Any change to production identity providers, MFA enforcement, conditional access, or SSO configuration.
- Revoking, disabling, or deleting accounts, service principals, keys, or certificates in use.
- Rotating or revoking production secrets, or changing secret storage locations.
- Granting standing privileged access or expanding an existing role.
- Accepting risk, granting an exception, or extending an exception beyond its approved expiry.
- Communicating policy changes or findings to external parties, customers, or regulators.
- Any action whose effect cannot be reversed within the agreed rollback window.

Proceed without a gate only for read-only analysis, drafting documents, and proposing changes marked as pending approval.

Exception criteria: approve only when (a) the business reason is documented, (b) a compensating control is verified to operate, (c) expiry is 90 days or less unless the approver records a justified longer term, and (d) the risk owner, not the implementing team, signs.

### Verification and evidence

Every rating must cite evidence. Acceptable evidence: configuration export with timestamp, access review sign-off, log sample covering a stated period, ticket with approval record. Unacceptable: verbal confirmation, policy text alone, or "believed to be enabled."

Quality checks:

- Every requirement has exactly one owner and one testable condition.
- Every Met rating references evidence dated within the last review cycle.
- Access reviews cover 100% of privileged accounts and at least the sampled percentage agreed for standard accounts; record the sample method.
- Each exception has an expiry date, approver, and compensating control reference.
- No orphaned exceptions: none past expiry without renewal approval.
- Secrets policy checks confirm no credentials appear in source repositories, build logs, or tickets, using the team's approved scanning tool. Name the tool and version as verified against its current documentation.

Version-sensitive items (identity provider feature names, scanner rule sets, regulatory citations, cryptographic algorithm recommendations) must be marked "verify against current official documentation" when cited, and not stated from memory.

### Failure handling

- **Evidence unavailable:** Mark the control Unverifiable, not Met. Open a collection task with an owner and date.
- **Conflicting sources:** Report both verbatim, identify the stricter reading as provisional, and escalate for a decision. Do not silently choose.
- **Control found broken during review:** Stop the review of that control, record the finding with timestamp and affected scope, and escalate under the incident process. Do not attempt a fix without a gate approval.
- **Owner unresponsive past the agreed date:** Escalate one level. Do not close the item as accepted.
- **Scope expands mid-review:** Pause, re-run Scope step, and re-confirm inputs.

### Deliverable contract

Produce a governance report containing, in order:

1. Scope statement with inclusions and exclusions.
2. Requirements register: ID, source text, testable condition, control, owner, status, evidence reference.
3. Gap list ranked by exposure, with remediation, rollback, and target date.
4. Exception register: ID, reason, compensating control, expiry, approver, status.
5. Pending approvals: each gated action, the approver, and the decision needed.
6. Open questions and unverifiable items with collection owners.
7. Next review date and evidence to be collected.

Do not present the report as a compliance certification or assurance statement. State that it reflects the evidence listed, as of the stated date.

### What not to do

- Do not record a control as Met based on policy wording or intent.
- Do not include secret values, tokens, or full credential strings in any output; reference them by identifier only.
- Do not grant or approve exceptions on behalf of an owner.
- Do not invent tool names, configuration keys, or version numbers.
- Do not perform changes to live systems during a governance review.
- Do not merge distinct requirements to shorten the register.

### Ultron routing contract

**Choose this skill when:** defining the organization's security policy and control system: control ownership, requirements, standards, exception handling, access reviews, security decision rights, and evidence expectations.

**Choose cloud-security-and-compliance when:** assessing an actual cloud environment's configuration, identifying technical misconfigurations, mapping them to controls, and preparing remediation/evidence packages.

**Handoff contract:** governance supplies the approved control objective, owner, risk tolerance, exception process, and required evidence. Cloud review returns observed configuration, affected resources, technical findings, remediation options, and evidence gaps. Governance decides whether an exception is acceptable; it does not replace the technical validation.

**Why the boundary exists:** policy defines what must be true and who owns it; cloud assessment determines what is actually configured and where it fails.


## security-threat-defense

**Use when:** Use when assessing, triaging, or hardening threats against external package registries and artifact sources (public or private package indexes, container registries, model hubs) that an organization consumes from or publishes to, including typosquatting, dependency confusion, malicious releases, compromised maintainer accounts, and tampered artifacts.

### Purpose and boundaries

This skill guides an analyst through detecting, assessing, and mitigating threats that originate from or pass through external registries: npm, PyPI, Maven, NuGet, RubyGems, crates.io, OCI container registries, Helm chart repositories, and ML model hubs. It covers both consumption (pulling dependencies into builds) and publication (releasing packages under the organization's namespace).

In scope: source-of-truth verification, namespace and resolution-order risks, provenance and signature checks, malicious-package indicators, maintainer-account risk, and the containment steps that follow a confirmed threat.

Out of scope: general application vulnerability scanning, network intrusion response, and legal or compliance attestations. This skill does not certify that any artifact is safe. It produces evidence-backed risk decisions.

### Inputs and assumptions

Collect before acting:

- Dependency manifest and lockfiles, with the exact resolved versions and hashes.
- Registry configuration: which indexes are consulted, in what order, and whether private indexes proxy public ones.
- Artifact identifiers: name, version, digest, publisher account, and publish timestamp.
- Build provenance records or attestations, if the ecosystem produces them.
- Incident context: alert source, affected build IDs, and time window.

Assumptions to state explicitly in every report: the registry API and metadata reflect the state at query time; publisher identity claims are unverified unless backed by an attestation; absence of a known-malicious advisory does not establish safety. Registry features, attestation formats, and CLI behavior change between versions. Verify every version-sensitive detail against the current official documentation for that registry before relying on it.

### Operating workflow

1. **Scope the artifact set.** Enumerate every external artifact referenced by the affected build, including transitive and build-time dependencies. Record a digest for each. Artifacts without a lockfile digest are flagged as unpinned.
2. **Check resolution integrity.** Confirm that each name resolves to the intended index. For internal package names, verify that no public index serves a package with the same name at a higher version. Record the resolution path.
3. **Compare against the baseline.** Diff the current artifact digest and metadata against the last known-good release. Flag new install-time scripts, new network calls in install hooks, new binary blobs, changed maintainers, and publish timestamps that break the project's normal cadence.
4. **Assess the publisher.** Check account age, prior publishing history under the name, ownership changes, and whether the release is linked to a source commit or verifiable build attestation.
5. **Inspect the content.** Review install and build hooks, obfuscated strings, encoded payloads, unexpected executables, and credentials-access patterns. Treat automated scanner output as leads, not verdicts.
6. **Classify.** Assign one of: confirmed malicious, suspected compromise, suspicious-unverified, unpinned-exposure, or clear-with-evidence.
7. **Contain or record.** Apply the decision gate below.

### Decision gates

- **Gate A, containment (requires explicit approval):** Blocking an index entry, revoking a token, pinning or rolling back a production dependency, or removing a published version. Present the evidence, blast radius, and rollback path. Do not proceed without named approval.
- **Gate B, external reporting (requires explicit approval):** Reporting to a registry security team, notifying a maintainer, or publishing an advisory. Outbound communication is irreversible and must be approved.
- **Gate C, destructive operations (requires explicit approval):** Deleting artifacts, purging caches, force-rewriting lockfiles across branches, or unpublishing. Never perform these as part of triage.
- **Gate D, sensitive data:** If evidence contains secrets, tokens, or personal data, redact before sharing and report the exposure through the credential-rotation process. Do not paste live credentials into tickets.
- **Proceed without approval:** Read-only metadata queries, local digest computation, and writing the internal analysis record.

Escalate immediately when a confirmed malicious artifact has been installed in a production or release build.

### Verification and evidence

Each finding must include:

- The artifact identifier and digest, and the method used to compute or retrieve it.
- At least two independent indicators, such as an unexpected maintainer change plus an install-hook network call, before a classification above "suspicious-unverified."
- Timestamps in UTC with the source of each timestamp.
- The exact query or command used, with the registry version or API version noted as unverified until checked against current documentation.

Quality checks before closing:

- 100% of external artifacts in scope have a recorded digest or an explicit unpinned flag.
- Every classification cites at least one primary artifact, not only a third-party summary.
- Containment actions have a named approver and a tested rollback.
- Re-scan after remediation shows the affected digest no longer resolves in the build.

### Failure handling

- **Registry unreachable or rate-limited:** Record the gap, do not infer safety, retry with backoff, and mark affected artifacts as unverified.
- **Digest mismatch against lockfile:** Treat as a potential tampering event. Halt the build promotion and escalate. Do not regenerate the lockfile to make the mismatch disappear.
- **Conflicting indicators:** Keep the stricter classification until resolved, and document the conflict.
- **Scanner false positive:** Document the reasoning with line-level evidence. Do not suppress rules org-wide based on one case.
- **Evidence incomplete:** State what is missing and what decision it blocks.

### Deliverable contract

Produce a single report containing:

1. Summary: artifacts reviewed, classifications, and highest-severity finding.
2. Artifact table: name, version, digest, source index, publisher, classification.
3. Findings: each with indicators, evidence links or query outputs, and confidence level (high, medium, low).
4. Pending gates: each action awaiting approval, with the approver required.
5. Recommended actions ordered by risk reduction, each marked reversible or irreversible.
6. Assumptions and unverified items, including version-sensitive details to check against official documentation.

### What not to do

- Do not execute unknown packages or install-time scripts to observe their behavior outside an isolated sandbox with approval.
- Do not declare an artifact safe based on absence of advisories.
- Do not delete, unpublish, or overwrite artifacts during triage.
- Do not contact maintainers or registries without Gate B approval.
- Do not invent registry features, flags, or attestation formats. Verify them.
- Do not paste secrets or tokens into reports.

### Ultron routing contract

**Choose this skill when:** assessing the trustworthiness of an external package, container image, model artifact, publisher, or registry resolution path before adoption or during routine supply-chain review. It owns preventive artifact triage, provenance and signature interpretation, dependency-confusion analysis, suspicious package inspection, and evidence-based trust decisions.

**Escalate to `threat-hunting-incident-response` when:** evidence indicates that the suspicious artifact was already installed, executed, built into a release, deployed, or used to access credentials; or when registry credentials, CI runners, developer machines, or workloads may already be compromised.

**Handoff contract:** provide exact names, versions, digests, registry resolution path, publisher metadata, affected build identifiers, first/last observed times, indicators, and confidence. The incident-response skill returns affected systems, execution evidence, blast radius, containment plan, and remediation status.

**Why the boundary exists:** deciding whether an artifact should be trusted is not the same as determining what happened after it entered an environment. Do not close an incident with a package reputation check, and do not launch a full incident process for a harmless pre-adoption review.


## threat-hunting-incident-response

**Use when:** Use when hunting for or responding to suspicious activity involving external package registries (npm, PyPI, RubyGems, Maven Central, container registries, Helm, crates.io), including malicious package detection, dependency confusion, typosquatting, compromised maintainer accounts, and poisoned build artifacts.

### Purpose and boundaries

This skill covers hypothesis-driven hunting and incident response for supply-chain threats that enter an organization through external package registries and container registries. It applies when an analyst must determine whether a package, image, or registry credential was used maliciously in internal builds, developer workstations, CI runners, or deployed workloads, and then contain and remediate.

In scope: identifying malicious or suspicious packages already consumed; tracing dependency and image provenance; detecting dependency confusion and typosquatting in resolution logs; investigating leaked or abused publish tokens; assessing install-time and runtime execution; coordinating removal and rollback.

Out of scope: general endpoint forensics unrelated to package execution; vulnerability scanning program design; reporting malicious packages to registry operators without approval (that is an external action); attribution beyond what evidence supports.

### Inputs and assumptions

Required before starting:
- Trigger source (advisory, registry notice, EDR alert, anomalous egress, developer report).
- Package names, versions, digests, or image tags under suspicion. Treat unverified indicators as hypotheses.
- Access to lockfiles, SBOMs, build logs, package-manager proxy or mirror logs, CI audit trails, and registry publish/audit logs where available.
- Inventory of internal registries, mirrors, and scopes mapped to internal namespaces.

Assumptions to state explicitly in the case record: the time window; whether the proxy caches upstream content; whether lockfiles were committed and enforced; whether install scripts run in the affected ecosystem by default (verify against current official package-manager documentation, as behavior changes across versions).

### Operating workflow

1. **Open the case and freeze evidence.** Record the trigger, hypothesis, and scope. Snapshot relevant logs and lockfiles before any cleanup. Do not delete caches or rebuild images yet.
2. **Build the consumption inventory.** Search lockfiles, manifests, SBOMs, and image layers for the suspect name, version range, and digest. Include transitive dependencies. Record each hit with repository, commit, branch, and first-seen date.
3. **Establish the consumption timeline.** From proxy and mirror logs, CI logs, and developer resolution records, determine when each suspect artifact was first fetched and by which hosts or identities.
4. **Analyze the artifact.** Compare the suspect artifact to the last known-good version and to the publisher's historical releases: added install hooks, new network calls, obfuscated payloads, credential-file reads, environment-variable harvesting, new binaries, changed maintainer or publish metadata. Perform analysis in an isolated sandbox with no production credentials.
5. **Hunt for execution.** Search EDR, CI, and runtime telemetry for child processes spawned during install or build, outbound connections to unfamiliar domains, reads of credential stores (cloud configs, SSH keys, `.npmrc`, `.pypirc`, Docker config), and new persistence artifacts.
6. **Hunt for lateral and credential impact.** If execution is confirmed, enumerate exposed secrets in the affected environment and their usage since first execution.
7. **Contain.** Block the package or version at the proxy, pin known-good versions, and quarantine affected build outputs. See decision gates for approval requirements.
8. **Eradicate and recover.** Rebuild from clean lockfiles against a verified source, redeploy from images with verified digests, and rotate exposed credentials.
9. **Close with lessons learned.** Record detection gaps and convert hunting queries into standing detections.

### Decision gates

- **Gate A, escalate severity:** Any confirmed install-time or runtime execution of the artifact, or any evidence of credential access, raises the incident to high severity and requires incident commander notification.
- **Gate B, block at proxy:** Permitted on analyst judgment when the artifact is clearly malicious or untrusted. Requires change record. Blocking a widely used internal dependency requires owner approval because it can halt builds.
- **Gate C, credential rotation:** Requires approval from the credential owner. Rotate in dependency order: publish tokens and CI secrets first, then cloud keys, then user tokens. Confirm revocation succeeded.
- **Gate D, external actions:** Reporting to a registry operator, requesting takedown, contacting a package maintainer, or publishing a public advisory requires explicit approval from legal and the incident lead. Never perform these unilaterally.
- **Gate E, destructive actions:** Deleting images, purging registry caches, force-pushing branches, revoking shared credentials, or rebuilding production artifacts requires explicit approval with a documented rollback path.
- **Gate F, sensitive data:** Do not copy secrets, customer data, or full memory dumps into tickets or chat. Reference storage locations and hashes instead.

### Verification and evidence

Quality checks, each measurable:
- Every consumption hit has a repository reference, artifact digest or hash, and a first-seen timestamp.
- Every conclusion of "no execution" cites the telemetry source and query window covering the full consumption period.
- Every indicator is classified as confirmed, suspected, or refuted, with the evidence supporting each class.
- Blocked artifacts are verified as unresolvable from a test client after the block is applied.
- Rebuilt artifacts match expected digests from a trusted build, and the lockfile diff contains no unexplained changes.
- Rotated credentials show no use from old values after the rotation timestamp.

Example: a `postinstall`-style hook in a newly published minor version of a utility package, fetched by a CI runner at 02:14 UTC, followed by an outbound request to an unregistered domain and a read of the runner's cloud config. This is confirmed execution; escalate under Gate A and rotate the runner's cloud credentials under Gate C.

### Failure handling

- **Missing proxy logs:** Mark the timeline as partial. Use CI logs and lockfile history as secondary sources. Do not infer absence of consumption.
- **Ambiguous artifact analysis:** Escalate to a second analyst. Do not label as malicious or benign without reproducible evidence.
- **Telemetry gap during the window:** Document the gap explicitly and treat affected hosts as potentially exposed.
- **Blocking breaks builds:** Roll back the block, pin a verified prior version, and reassess with the owner.
- **Credential rotation fails:** Escalate immediately; keep the exposed credential flagged as compromised.

### Deliverable contract

The final case report must contain: incident summary and severity; hypothesis and scope; consumption inventory table (repository, artifact, version, digest, first-seen, last-seen); execution findings with evidence references; credential exposure and rotation status; containment and remediation actions with approval references; open items with owners; detection rules added. Do not claim the environment is clean without the verification checks above being satisfied. Version-sensitive package-manager and registry behaviors must be confirmed against current official documentation before being cited in the report.

### Ultron routing contract

**Choose this skill when:** there is a credible indication that a registry artifact or credential has already affected an organization. Triggers include a package or image found in builds or deployed systems, suspicious install-time/runtime execution, dependency-confusion evidence in resolution logs, abnormal registry publishing, or possible token theft.

**Use `security-threat-defense` for preventive review when:** the artifact has not been consumed and the question is whether it should be trusted, whether its provenance is valid, or whether a registry/publisher is suspicious.

**Handoff contract:** receive the suspected artifact identity and initial indicators, then establish where it was resolved, downloaded, installed, executed, or published. Return a time-bounded evidence timeline, affected assets and tenants, credential exposure assessment, containment decisions, recovery verification, and unresolved attribution. Preserve uncertainty; a malicious artifact finding does not prove every consumer executed it.

**Why the boundary exists:** incident response is driven by possible impact and evidence of exposure, not merely by an artifact being unusual. Keep preventive screening and retrospective hunting connected but operationally distinct.

