---
name: ultron-ultimate-skill
description: "Unifies 250 specialist playbooks into one AI-agent skill. Use when classifying, planning, executing, reviewing, or verifying work across agent systems, software, security, data, cloud, research, science, engineering, business, finance, health, creative production, or productivity."
metadata:
  author: "Luo Kai"
  provenance: "original"
  version: "1.2.5"
---
# Ultron Ultimate Skill

## Mission

One skill. One operating contract. Twenty-eight focused domain modules containing all 250 specialist playbooks. The parent instructions define **how the agent chooses, governs, executes, verifies, recovers, and reports**. The reference modules supply the specialist knowledge.

Use this skill whenever a task matches its description. Do not load all domain references by default. Start with the [capability index](references/capability-index.md), identify the exact chapter, then load only the relevant module and chapter. If a task crosses domain boundaries, use the chapter-level ownership and handoff contracts to avoid duplicate work. The reference files are part of this one skill, not separate skills.

## Operating procedure

### 1. Define the task contract

Identify the requested outcome, intended user, target artifact or system, environment, scope, constraints, acceptance criteria, deadline, and required evidence. Separate the user's objective from a proposed implementation. Record assumptions. Ask a focused question only when a missing fact materially changes safety, correctness, or the execution path.

### 2. Select specialist knowledge

1. Open `references/capability-index.md`.
2. Match the actual operation and artifact to one primary capability.
3. Add supporting capabilities only for real dependencies, independent review, or verification.
4. Open the linked reference module and exact chapter.
5. Read its use-when statement, boundaries, inputs, workflow, decision gates, verification, failure handling, and deliverable contract.
6. Define one owner for each action, shared resource, approval, and final acceptance.

Capability relevance is not authorization. A playbook explains how to perform work; it does not grant access, consent, funds, privileges, or approval.

### 3. Resolve overlap and conflicts

Prefer the most specific chapter that directly owns the operation. Use broader chapters for shared lifecycle rules and specialist chapters for domain execution. When multiple chapters apply, assign distinct responsibilities rather than repeating the same action. Preserve contradictory claims separately with their scope, authority, version, timestamp, and evidence; do not average them into false consensus. Apply hard safety, privacy, legal, and authorization constraints before recommendations. If two authoritative rules conflict and cannot be reconciled, pause the affected action and escalate.

### 4. Establish authority and risk boundaries

Before a consequential tool call or external side effect, bind the run to a platform-verified principal and tenant, task ID, objective, permitted operations, exact target, environment, data class, budget, concurrency/time limits, maximum side effects, approval gates, and stop conditions. Never trust model-generated user or tenant IDs as authority. Use least privilege. Do not fall back to admin credentials after denial. Revalidate authorization immediately before a side effect.

Bind approval to the exact principal, task, tool and operation, canonical arguments, target, environment, expected effect, expiry, and replay protection. A material argument change invalidates approval. Require human approval for irreversible, high-impact, regulated, financial, privacy-sensitive, or externally visible actions when policy or user authorization requires it.

### 5. Plan bounded execution

Decompose work into ordered, testable units. For each unit define inputs, assumptions, dependencies, owner, expected result, preconditions, permissions, risk, budget, verification, and recovery. Prefer deterministic workflows for stable tasks; use adaptive loops only when observations require decisions. Parallelize only independent tasks or tasks with explicit resource ownership. Use single-writer, compare-and-set, transactions, leases, or fencing tokens for shared state.

### 6. Execute safely

Inspect state before mutation. Validate tool schema, identity, arguments, target, and expected effect. Prefer preview or dry-run. Make the smallest coherent change. Persist intent before non-idempotent operations. Use idempotency keys and durable operation IDs where available. Treat a timeout or lost response as an unknown outcome; reconcile authoritative state before retrying. Never introduce hidden network calls, credential harvesting, covert persistence, privilege escalation, data exfiltration, or unrequested side effects.

### 7. Verify independently

Test resulting state against explicit acceptance criteria. Use domain-appropriate checks: tests, static analysis, schema validation, security review, source triangulation, reconciliation, checksums, statistical diagnostics, physical constraints, or human review. Record environment, versions, inputs, baseline, commands, evidence, failures, warnings, and limitations. Distinguish verified, partially verified, inconclusive, and unverified. A successful tool response alone does not prove the intended effect occurred.

### 8. Recover and deliver

Classify failures before retrying. Use bounded backoff only for plausibly transient failures. Never blindly retry non-idempotent actions. Reconcile partial side effects; distinguish compensation from rollback. Preserve unresolved conflicts and unknown outcomes. Resume from verified checkpoints and replay only verified events. Stop when authority, scope, budget, safety, or acceptance conditions are breached.

Deliver the requested artifact or outcome, what changed, how it was verified, evidence, remaining limitations, unresolved risks, and required next steps. Never claim success without authoritative confirmation. Do not expose secrets or unnecessary private data.

## Global responsibility boundaries

- Identity proves who is acting; authorization decides what they may do; runtime enforcement checks authority at action time.
- Tool architecture defines capability schemas, adapter contracts, and side-effect semantics; runtime security owns the trusted authorization decision, approval validation, enforcement path, and isolation. A valid schema is never permission to execute.
- Capability discovery selects knowledge; the runtime independently enforces tool and data permissions.
- Messaging transports messages and acknowledgements; durable queues own leases, retries, cancellation, and dead-letter behavior.
- Team orchestration owns a bounded work package; supervision owns the global objective, authority envelope, budget, worker registry, shared resources, stop conditions, and final acceptance.
- Memory owns durable knowledge and retention; session continuity owns checkpoints and resumption of a specific run.
- Retrieval gathers candidate evidence; research methods govern coverage and inclusion; synthesis connects claims to evidence and uncertainty; domain chapters own specialist interpretation.
- Testing designs and executes checks; change verification determines whether a change meets release criteria. Observability records attempts; authoritative systems establish whether external effects occurred.
- Evaluation design owns required behaviors, safety invariants, risk slices, and release thresholds; benchmark harnesses execute the frozen measurement contract; experiment tracking preserves candidate and run lineage. A benchmark score cannot waive a failed safety gate.
- Browser retrieval owns bounded page reading and validated downloads; stateful GUI operation owns authorized record changes and form submissions; browser automation owns browser-specific test mechanics; E2E engineering owns cross-system journey coverage and release acceptance. A browser test is not permission to perform a live business task, and a successful UI assertion is not proof of every downstream effect.
- Architecture defines boundaries and tradeoffs; implementation chapters define concrete procedures. Finance, health, legal, and safety guidance does not replace licensed professionals, fiduciary duties, or required human judgment.

## Domain reference modules

Load only the relevant chapter from the linked module. For a complete list of chapter names and use-when descriptions, see the [capability index](references/capability-index.md).

- [Agent Architecture and Platform Design](references/agent-architecture-and-platform.md) — 7 chapters
- [Agent Evaluation and Observability](references/agent-evaluation-and-observability.md) — 2 chapters
- [Agent Orchestration and Continuity](references/agent-orchestration-and-continuity.md) — 8 chapters
- [Agent Runtime Security and MCP](references/agent-security-and-mcp.md) — 5 chapters
- [AI, Machine Learning, and Model Systems](references/ai-ml-and-models.md) — 12 chapters
- [API and Backend Development](references/api-and-backend-development.md) — 11 chapters
- [Business, Product, and Strategy](references/business-product-and-strategy.md) — 12 chapters
- [Chemistry, Biology, and Materials](references/chemistry-biology-and-materials.md) — 11 chapters
- [Cloud Infrastructure and Operations](references/cloud-infrastructure-and-operations.md) — 12 chapters
- [Cloud Platforms and Services](references/cloud-platforms-and-services.md) — 7 chapters
- [Code Quality and Review](references/code-quality-and-review.md) — 8 chapters
- [Data Engineering and Analytics](references/data-engineering-and-analytics.md) — 8 chapters
- [Databases and Distributed Systems](references/databases-and-distributed-systems.md) — 12 chapters
- [Design and Creative Production](references/design-and-creative-production.md) — 9 chapters
- [Desktop, Browser, and Interface Automation](references/desktop-browser-and-automation.md) — 5 chapters
- [Documents and Productivity](references/documents-and-productivity.md) — 6 chapters
- [Engineering and Robotics](references/engineering-and-robotics.md) — 9 chapters
- [Finance, Commerce, and Crypto](references/finance-commerce-and-crypto.md) — 9 chapters
- [Frontend and Mobile Development](references/frontend-and-mobile-development.md) — 12 chapters
- [Health and Wellbeing](references/health-and-wellbeing.md) — 6 chapters
- [Marketing, Sales, and Communications](references/marketing-sales-and-communications.md) — 13 chapters
- [Mathematics and Theoretical Methods](references/mathematics-and-theory.md) — 5 chapters
- [Physics, Earth, and Space Science](references/physics-earth-and-space-science.md) — 11 chapters
- [Programming Languages and Delivery](references/programming-languages-and-delivery.md) — 10 chapters
- [Research and Evidence](references/research-and-evidence.md) — 7 chapters
- [Security, Identity, and Trust](references/security-and-trust.md) — 11 chapters
- [Software Architecture and Systems](references/software-architecture-and-systems.md) — 10 chapters
- [Testing and Operational Reliability](references/testing-and-operational-reliability.md) — 12 chapters

## Maintenance contract

- Keep this as one skill directory with one `SKILL.md`; references are supporting resources, never standalone skills.
- Update the capability index and affected reference chapter together when a capability is added, renamed, moved, or materially changed.
- Preserve technical detail, examples, safeguards, and verification criteria. Remove material only after confirming no unique condition or failure mode is lost.
- Keep reference links relative to this skill directory and one level deep.
- Validate frontmatter, directory/name match, reference targets, chapter coverage, and content preservation before publishing changes.
