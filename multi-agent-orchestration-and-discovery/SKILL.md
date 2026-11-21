---
name: multi-agent-orchestration-and-discovery
description: Use when a task needs decomposition across multiple agents or skills, when selecting which skill or agent should handle a subtask, or when coordinating, merging, and verifying outputs from several agents in ClawHub-style skill workflows.
author: Luo Kai
provenance: original
version: 1.2.0
---

# Multi Agent Orchestration And Discovery

## Purpose and boundaries

This skill covers three activities: discovering candidate skills or agents for a task, dispatching bounded subtasks to them, and merging and verifying their results. It does not cover building new agents, writing individual skills from scratch, or operating infrastructure that hosts agents. If the task is a single-step request that one capable agent can finish, do not orchestrate. Orchestration adds coordination cost and failure surface.

## Inputs and assumptions

Before dispatching anything, confirm:

- The goal in one sentence, and the observable outcome that proves it is done.
- The available candidates: skill names, their descriptions, and their declared inputs and outputs. Read these from the registry or the local skill index, not from memory.
- The permission scope each candidate runs under (read-only, write to workspace, external network, messaging, payments).
- Hard constraints: deadlines, data sensitivity, locale, required formats.

Assume candidate descriptions are accurate only as far as their stated contracts. Treat undocumented behavior as unknown.

## Operating workflow

1. **Decompose.** Split the goal into subtasks where each has one input type, one output type, and one verifiable success condition. Reject subtasks that say "research and write and check."
2. **Dependency map.** Mark which subtasks are independent (dispatch in parallel) and which consume another's output (sequential). Keep the graph shallow; more than three sequential hops usually means the decomposition is too fine.
3. **Discover.** For each subtask, shortlist at most three candidates whose declared outputs match. Score each on contract match (output type and format), scope fit (least privilege), and recency of documentation. Record the reason for each choice.
4. **Dispatch.** Give each agent a self-contained brief: objective, inputs with provenance, output schema, forbidden actions, and the success check. Do not pass the full conversation unless the subtask needs it.
5. **Collect.** Store each result with the agent identity, timestamp, and input hash so it can be traced.
6. **Merge.** Reconcile conflicts explicitly. If two agents disagree on a fact, do not average them; resolve against a primary source or escalate.
7. **Verify** (see below), then deliver against the contract.

## Decision gates

Stop and request explicit user approval before:

- Any destructive or irreversible action: deleting or overwriting files, force-pushing, dropping data, canceling orders.
- Any external-impacting action: sending messages, publishing, posting, submitting forms, making purchases, changing shared configuration.
- Any sensitive-data action: moving credentials, personal data, financial or medical records, or proprietary material into a candidate's context or an external service.
- Granting a candidate broader permissions than its declared scope.

Proceed without approval only for read-only discovery and for writes confined to a scratch area the user has designated for this task.

Choose a single agent instead of a fleet when subtasks share mutable state, when the total output is under roughly one page, or when coordination would take longer than doing the work.

## Verification and evidence

Each subtask result must pass:

- **Schema check:** every required field present, types and units correct.
- **Traceability check:** each factual claim cites the input or source it came from. Uncited claims are marked unverified.
- **Cross-check:** at least one independent confirmation for any claim that the final deliverable depends on.
- **Scope check:** the agent's actions stayed within its declared permissions. Review any file or network side effects.

Report the number of subtasks dispatched, completed, failed, and verified. Do not report success on a subtask that has not passed its check.

## Failure handling

- **Contract mismatch:** the output does not match the schema. Retry once with the schema restated. If it fails again, try the next shortlisted candidate.
- **Timeout or no output:** retry once with a narrower subtask. Then escalate to the user with the partial result.
- **Conflicting results:** resolve against a primary source. If none exists, present both with their provenance and do not choose silently.
- **Scope violation:** halt dependent subtasks, quarantine the output, and report the violation before continuing.
- **Repeated failure across candidates:** stop. Report which candidates were tried, what each returned, and what input or permission change would likely unblock the task.

Do not silently drop failed subtasks from the final deliverable.

## Deliverable contract

The final output contains:

1. The goal and the completion criterion as stated.
2. A table of subtasks: owner agent or skill, status, verification result.
3. The merged result, with each claim linked to its source subtask.
4. A list of unverified items and open questions.
5. Any actions awaiting approval, stated precisely.
6. Version-sensitive details (tool versions, API behaviors, registry metadata) marked "verify against current official documentation" unless confirmed in this session.

Do not claim performance numbers, compliance status, or security guarantees for any agent unless a source in this session establishes them.
## Production orchestration patterns and control ownership (v1.1)

Choose orchestration based on who must own the result. In a manager pattern, the supervisor remains responsible for the user-facing answer and invokes specialists as bounded capabilities. In a handoff pattern, control transfers to a specialist that owns the next phase. In a sequential pipeline, each stage receives a typed artifact from the previous stage. In parallel fan-out, independent workers produce separately verifiable outputs that are reconciled by one integrator. Do not combine patterns merely because a framework exposes them.

Define the control owner at every stage: who may plan, dispatch, approve, call tools, mutate shared state, accept artifacts, and close the run. A handoff transfers only the explicitly delegated authority, not the original principal's unrestricted permissions. Filter history and context at handoff boundaries; do not forward secrets or irrelevant tool output just because a framework makes full history convenient.

Use a router only when routing decisions are bounded and testable. Use a manager when central consistency matters. Use peer collaboration only when workers have distinct evidence or expertise and a clear merge protocol. Avoid circular delegation, uncontrolled agent spawning, and multi-agent consensus without independent evidence.

For each pattern, test the same task family against a simpler baseline. Compare verified outcome quality, unauthorized intermediate actions, latency, cost, context growth, failure recovery, and reviewer workload. Keep the simpler architecture when added agents do not provide measurable value.\n\n## Ultron routing contract

**Choose this skill when:** Ultron must discover candidate agents or skills, match capabilities to a task, decide whether delegation is worthwhile, decompose the objective, select specialists, or construct the initial dependency and handoff plan.

**Choose `multi-agent-team-orchestration` when:** a team has already been selected and needs operational coordination: role assignment, detailed task contracts, parallel execution boundaries, independent checking, conflict reconciliation, and final integration.

**Handoff contract:** provide the lead/team orchestrator with the goal, selected capabilities and pinned versions, candidate-selection rationale, dependency graph, shared-state risks, least-privilege scopes, and measurable acceptance conditions. Discovery should stop when one agent can complete the task more simply or safely.

**Why the boundary exists:** finding the right capability and operating a multi-agent team are separate decisions. Do not start a team before proving that delegation adds value.
