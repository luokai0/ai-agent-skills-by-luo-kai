---
name: multi-agent-team-orchestration
description: Use when decomposing a complex task across multiple cooperating AI agents or sub-agents, assigning roles, routing handoffs, merging outputs, and deciding when to escalate to a human operator.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Multi Agent Team Orchestration

## Purpose and boundaries

This skill governs how a lead agent (the orchestrator) plans work, delegates bounded subtasks to specialist agents, collects their outputs, and integrates them into one verified result. It covers role design, task contracts, handoff protocol, conflict resolution, and quality gating.

It does not cover: training or fine-tuning models, building the underlying tool integrations, or choosing hosting infrastructure. If the task is a single-step problem, do not spawn a team; a team adds coordination cost and failure surface.

## Inputs and assumptions

Before delegating, confirm:

- The end goal in one sentence, and what "done" looks like in observable terms.
- The available agents and their tools, permissions, and context limits. Do not assume a capability that is not listed.
- Hard constraints: deadlines, budget or token ceilings, data-access limits, and forbidden actions.
- Whether any subtask touches external systems, money, personal data, or production state.

If any of these are missing, ask the human operator before dispatching work.

## Operating workflow

1. **Decompose.** Split the goal into subtasks with clear inputs and outputs. Keep a subtask only if it can be verified independently. Target 3 to 6 subtasks; more usually signals poor decomposition.
2. **Map dependencies.** Mark which subtasks can run in parallel and which require another's output. Parallelize only independent, read-only work.
3. **Assign roles.** One specialist per role. Typical roles: researcher (gathers and cites sources), analyst (transforms data), writer (drafts artifacts), checker (adversarially reviews another agent's output). The checker must not be the agent that produced the work.
4. **Issue task contracts.** Each delegation states: objective, inputs with locations, required output format, acceptance criteria, allowed tools, and stop conditions.
5. **Collect and normalize.** Require every agent to return its output in the agreed schema plus a confidence note and a list of unverified claims.
6. **Reconcile.** When outputs conflict, do not average them. Identify the factual basis for each position, re-check the source, and either resolve or escalate.
7. **Integrate and verify.** Assemble the final artifact, then run the verification checks below before presenting it.
8. **Report.** State what each agent contributed, what was verified, and what remains open.

Example: For a quarterly vendor-risk memo, the researcher extracts contract terms from the supplied PDFs, the analyst tabulates renewal dates and spend, the writer drafts the memo, and a checker verifies every figure against the source extraction.

## Decision gates

Stop and request explicit human approval before any of the following:

- Destructive or irreversible actions: deleting or overwriting data, force-pushing, dropping tables, cancelling contracts.
- External-impacting actions: sending email or messages, publishing, posting to third-party systems, submitting filings, making payments.
- Sensitive-data actions: moving personal, health, financial, or credential data across a boundary, or including it in a shared artifact.
- Scope expansion: any subtask that requires a permission not in the original contract.

Escalate to the human (without waiting for approval to continue reading) when:

- Two agents disagree on a material fact and the source cannot resolve it.
- A checker rejects an output twice.
- An agent reports a tool error that changes the feasibility of the plan.

Do not proceed past a gate by inferring approval from silence or from a prior, different request.

## Verification and evidence

Each claim in the final output must trace to a source, a computed result, or an explicit "assumption" label. Apply these measurable checks:

- Coverage: every acceptance criterion in every contract has a matching piece of evidence. Target 100%; list any gaps.
- Traceability: every number, date, and named entity in the deliverable maps to a source location in the evidence log.
- Independence: the checker's verdict was produced without access to the producer's reasoning, only the artifact and sources.
- Consistency: recalculate any totals, dates, and cross-references. Zero mismatches permitted.
- Freshness: for time-sensitive facts, record the access date.

Maintain an evidence log with columns: claim, source, locator, verifier, status (verified, assumed, disputed).

## Failure handling

- **Agent returns malformed output:** re-issue the contract once with the schema restated. If it fails again, complete the subtask yourself or reassign.
- **Agent exceeds scope or stop condition:** discard out-of-scope content, log the event, and do not reuse it without review.
- **Circular dependency or deadlock:** break the cycle by splitting the subtask or accepting a stated assumption, and mark it for human review.
- **Partial results:** deliver the verified portion with a clear list of what is missing. Do not fill gaps with plausible content.
- **Tool or data unavailable:** report the exact blocked item; do not substitute memory-based claims as sourced facts.

## Deliverable contract

The final response contains:

1. A one-paragraph summary of the outcome and its confidence level.
2. The integrated artifact in the requested format.
3. The evidence log, or a link to it if the format permits.
4. A roles-and-contributions table listing each agent, its subtask, and its verification status.
5. An open-items list with owner and required decision for each item.

Do not state that the work is complete if any acceptance criterion lacks evidence. Do not claim that agents were independently validated unless a checker pass was recorded.

## What not to do

- Do not spawn agents for tasks a single agent can complete reliably.
- Do not let an agent check its own output as the sole verification.
- Do not pass sensitive data to agents lacking the required permission.
- Do not average conflicting outputs into a bland synthesis.
- Do not invent tool names, API parameters, version numbers, or performance figures. Where a tool or library detail is version-sensitive, mark it "verify against current official documentation" before relying on it.
- Do not present regulatory or compliance conclusions as guaranteed; state them as the best reading of the supplied sources, pending qualified review.