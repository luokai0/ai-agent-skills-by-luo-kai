---
name: llm-app-agents-and-prompts
description: Use when designing, reviewing, or debugging LLM-powered applications that involve prompt templates, tool-calling agents, retrieval context, or multi-step model workflows, and need structured guidance on prompt contracts, agent loops, evaluation, and safe deployment.
author: Luo Kai
provenance: original
version: 1.2.0
---

# LLM App Agents and Prompts

## Purpose and boundaries

This skill guides the design, implementation review, and debugging of LLM-based application components: prompt templates, output schemas, tool-using agent loops, retrieval-augmented context assembly, and evaluation harnesses for these.

In scope: prompt structure and versioning, output contracts, tool definitions and call validation, agent step limits, context budgeting, offline evaluation sets, regression testing of prompts, and failure triage.

Out of scope: model training or fine-tuning, infrastructure procurement, legal or compliance certification, and choosing a model vendor on benchmark claims. Do not present any model's capabilities as guaranteed.

## Inputs and assumptions

Collect before acting:

1. The user-facing task the application performs and its failure cost (cosmetic, financial, safety, legal).
2. Current prompt text, tool schemas, and sample inputs/outputs, including at least five failing examples if debugging.
3. The model identifier and provider in use. Treat any model behavior, context limit, pricing, or parameter name as version-sensitive and verify against current official provider documentation before relying on it.
4. Data classes the prompt will receive (public, internal, personal, regulated).
5. Whether the agent can take actions with side effects (writes, sends, purchases, deletions).

For missing evaluation inputs, disclose the assumption and explain how it limits the result.

## Operating workflow

1. **Map the decision points.** List every place the model chooses: classify, extract, route, call a tool, or produce final text. Each is a separate contract.
2. **Define output contracts first.** For each decision point, specify the allowed output shape (enumerated labels, JSON fields with types, or free text with length bounds). Validate outputs in code, not by trusting the prompt.
3. **Write the prompt in layers.** Order: role and task scope; hard constraints; input data delimited and labeled as untrusted; output schema; two to four worked examples drawn from real cases; the refusal or escalation path.
4. **Constrain tools.** For each tool: name, purpose, typed arguments, read or write classification, and maximum calls per run. Reject calls with unknown names or invalid arguments and return a structured error to the model.
5. **Bound the loop.** Set a maximum step count, a maximum token or cost budget, and a stop condition that requires a final answer or an explicit escalation.
6. **Budget context.** Allocate fixed shares of the context window to instructions, retrieved passages, conversation history, and reserved output. Truncate retrieval by rank, never silently by position.
7. **Build an evaluation set.** Minimum 30 cases spanning typical, edge, adversarial, and empty inputs. Store expected outputs or grading rubrics with the prompt version.
8. **Run and compare.** Evaluate the candidate against the current baseline on the same set, with identical settings.

## Decision gates

- **Gate A, before any tool with write or external effect is enabled:** require explicit human approval of the tool list, argument validation, and a dry-run mode. Obtain approval for any action that is destructive, irreversible, sends data outside the organization, or touches personal or regulated data.
- **Gate B, before shipping a prompt change:** schema-valid rate and task pass rate must meet or exceed the baseline, and no category of previously passing cases may regress by more than 2 percentage points.
- **Gate C, before routing real user data through a new provider or model:** confirm the data-handling terms with the owning team. Do not assert retention or training guarantees from memory.
- **Gate D, when the model's output drives a high-cost decision:** keep a human review step; the model may propose, not commit.

## Verification and evidence

Report each claim with its measurement:

- Schema-valid rate (target: 100% enforced by validator; raw model rate reported separately).
- Task accuracy against the rubric, with the sample size and confidence stated.
- Tool-call precision: proportion of calls with valid arguments and appropriate choice, from a labeled trace sample of at least 20 runs.
- Step-count distribution and percentage of runs hitting the step cap (target: under 2% on the eval set).
- Injection test results: percentage of adversarial inputs where instructions embedded in data were ignored.

Never state benchmark numbers, vendor rankings, or compliance outcomes that were not measured in this context.

## Failure handling

- **Invalid schema:** retry once with the validator error appended; on second failure, route to fallback or escalation. Do not loop.
- **Unknown or invalid tool call:** return a structured error; count it toward the step budget.
- **Step cap reached:** return the partial state and an escalation flag; never return an unverified final answer.
- **Retrieval returns nothing relevant:** instruct the model to say the context is insufficient; do not let it answer from memory for factual claims that require sources.
- **Regression after change:** revert to the prior prompt version, then diagnose using the failing cases before re-attempting.

## Deliverable contract

Every deliverable must include:

1. The prompt text with a version identifier and changelog entry.
2. The output schema and validator rules.
3. Tool definitions with read/write classification and approval status.
4. Loop limits and budget values, with the rationale.
5. The evaluation set description, baseline results, and candidate results, labeled as measured.
6. Listed assumptions, including any version-sensitive items marked for verification against current official documentation.
7. Open risks and the gate status (A through D) for each.

Do not: hardcode secrets in prompts; trust model output as authorization; expand tool permissions without approval; treat examples in the prompt as exhaustive policy; or report unmeasured quality claims.
## Agent application architecture and prompt/runtime boundaries (v1.1)

Keep prompts, agent definitions, tool schemas, runtime policy, and application state as separate versioned artifacts. Instructions describe intended behavior; deterministic application code enforces identity, permissions, budgets, approvals, and side-effect constraints. Never rely on prompt wording as the sole control for a sensitive operation.

Define the agent's role, objective, scope, allowed tools, prohibited actions, expected output schema, escalation conditions, and stopping criteria. Keep specialist instructions narrow and compose them through explicit contracts. Use structured outputs for machine-consumed decisions and validate them before downstream use. Treat model-generated JSON as untrusted input until schema and policy validation pass.

Choose the simplest orchestration that meets the task: a deterministic workflow for fixed sequences, a single agent with tools for bounded work, a manager with specialists when central ownership matters, or handoffs when a specialist should take over. Maintain explicit state across runs and define what context is forwarded to each specialist. Avoid putting secrets, hidden application state, or unrestricted authority in prompts.

Separate model selection from runtime guarantees. Record model identifier, prompt revision, tool versions, policy revision, and evaluation suite for each release. Test prompt injection, ambiguous intent, invalid structured output, tool misuse, refusal behavior, context overflow, handoff loops, and unexpected model changes. Evaluate full trajectories and external postconditions, not only final response quality.

## Ultron routing contract

**Choose this skill when:** implementing the application layer that connects an LLM to prompts, tools, structured outputs, context, memory, retrieval, and a runtime loop. It owns prompt/runtime separation and the application-level behavior of model-powered features.

**Choose `agent-design-patterns` when:** deciding the agent's fundamental coordination pattern, control owner, or single-agent versus multi-agent architecture.

**Choose `agent-tool-architecture` when:** designing the general capability and authorization boundary exposed to the model.

**Choose `rag-and-retrieval-systems` when:** the central problem is evidence ingestion, retrieval/reranking, context grounding, citations, or retrieval-specific evaluation.

**Handoff contract:** provide the chosen agent pattern, model/runtime interface, structured input/output contract, tool inventory, context policy, and acceptance criteria. Specialist skills return versioned implementations and evidence; this skill verifies that the application composes them without allowing prompts or retrieved data to grant permissions.

**Why the boundary exists:** an LLM application composes model-facing behavior, but architecture, tool governance, and retrieval security each require their own explicit contracts.
