---
name: ai-system-architecture
description: Use when designing, reviewing, or documenting the architecture of an AI-enabled system, including choosing between prompting, retrieval-augmented generation, fine-tuning, and agentic workflows, or defining data flows, evaluation harnesses, and deployment boundaries for LLM or ML components.
author: Luo Kai
provenance: original
version: 1.1.0
---

# AI System Architecture

## Purpose and boundaries

Produce an architecture decision record and component design for a system that uses machine learning or large language model (LLM) components. Cover problem framing, approach selection, component decomposition, data flow, evaluation, observability, cost and latency budgets, and security boundaries.

Out of scope: training novel model architectures, performing research-grade benchmarking, and issuing legal or compliance certifications. Flag those needs and route them to specialists.

## Inputs and assumptions

Collect before designing:
- Task definition: inputs, outputs, success criteria, and the cost of each error type (false positive versus false negative).
- Data: sources, volume, freshness requirements, sensitivity classification, licensing, and retention rules.
- Constraints: p95 latency, cost per request ceiling, throughput, availability target, and deployment environment.
- Users and trust level: internal staff, customers, or automated consumers.

State every unverified assumption explicitly in the deliverable. Do not guess numbers that drive decisions.

## Operating workflow

1. **Frame the task.** Write one sentence stating the input, the output, and the decision the output supports. If it cannot be written, stop and clarify.
2. **Establish a baseline.** Define a non-AI or simple heuristic baseline and its measured performance on a labeled sample. Any AI approach must beat it by a margin that justifies its cost.
3. **Select the minimal approach.** Apply the ladder in order, stopping at the first rung that meets the success criteria:
   - Deterministic rules or classical ML.
   - Single prompted model call with structured output.
   - Retrieval-augmented generation (RAG) over a versioned corpus.
   - Fine-tuning, only when prompting and retrieval fail on a measured error category and sufficient labeled data exists.
   - Multi-step agent with tool use, only when the task requires dynamic branching that a fixed pipeline cannot express.
4. **Decompose components.** Define separate units for ingestion, retrieval, generation, validation, tool execution, and feedback capture. Each unit gets an explicit input and output schema.
5. **Design the data path.** Specify where sensitive data is redacted, where logs are stored, and which components may see raw inputs.
6. **Design evaluation.** Build a versioned golden set, define per-component metrics (retrieval recall@k, answer faithfulness, schema validity, tool-call success), and set release thresholds.
7. **Design observability.** Log prompt version, model identifier, retrieval document IDs, token counts, latency per stage, and validation outcomes, with sensitive fields masked.
8. **Document failure modes** and their handling (see Failure handling).

## Decision gates

Stop and obtain explicit approval before proceeding when any of these apply:
- The design sends personal, regulated, or confidential data to an external model provider.
- The system takes actions with external effects: sending messages, moving money, modifying records, or deploying code.
- Fine-tuning would use data whose rights or consent status is unconfirmed.
- The design requires deleting, overwriting, or migrating existing data stores.
- Projected cost exceeds the stated budget by more than 20 percent.

Proceed without a gate only for read-only analysis and drafting of documents.

## Verification and evidence

Each claim in the design must link to evidence:
- Retrieval recall@k and answer faithfulness measured on the golden set, with set size and date stated.
- Latency and cost estimates derived from measured token counts and provider price sheets, with the price source and date cited.
- Structured output validity rate above a stated threshold (for example, 99 percent on the golden set) with failures enumerated.
- Human review agreement on a sampled subset, with sample size and rater protocol stated.

Mark any provider API behavior, model context limits, pricing, SDK function names, or version-specific features as **verify against current official documentation** before implementation. Do not present them as settled facts.

## Failure handling

- **Model refusal or malformed output:** retry once with the same input, then route to a deterministic fallback or human queue. Log the failure category.
- **Retrieval returns nothing relevant:** return an explicit "insufficient information" result. Never let the generator answer from parametric memory on a factual task without flagging it.
- **Tool call fails or times out:** make the action idempotent, record the attempt, and halt the chain instead of retrying side-effecting calls automatically.
- **Evaluation regression:** block release and report the metric delta, the affected slice, and the prompt or model change responsible.
- **Cost or latency breach:** degrade to the cheaper rung of the approach ladder, not to silent truncation.

## Deliverable contract

Produce a single document containing, in order:
1. Problem statement and success criteria.
2. Baseline results and the selected approach with justification against the ladder.
3. Component diagram in text form, with input and output schemas per component.
4. Data classification, flow, retention, and redaction points.
5. Evaluation plan: golden set description, metrics, thresholds, and release gate.
6. Observability fields and alert conditions.
7. Failure modes table: trigger, detection, handling, owner.
8. Open assumptions, unverified details flagged for official-documentation checks, and approval gates requiring sign-off.

Do not include: unmeasured accuracy claims, vendor marketing comparisons, invented benchmark figures, or statements that the system is compliant with any regulation.

## Architecture selection and boundary engineering (v1.1)

### Convert requirements into an architecture scorecard

Before selecting a model or agent pattern, create a scorecard with task success threshold, unacceptable error classes, p50/p95 latency, throughput, cost per completed task, freshness requirement, privacy boundary, auditability, recovery objective, and human intervention rate. Mark each value as measured, contractual, estimated, or unknown. Do not allow an unmeasured estimate to masquerade as a release requirement.

Evaluate candidates against the same representative task set. Reject a candidate that violates a hard safety, privacy, latency, or cost constraint even if its average score is highest. For viable candidates, compare total operating cost, including retrieval, tool execution, retries, human review, monitoring, and failure recovery.

### Choose orchestration by control ownership

Use a fixed pipeline when stages and transitions are known. Use a single agent with tools when the model chooses among bounded actions but one owner can retain control. Use a manager with specialists when a central component must synthesize results and retain responsibility for the final answer. Use a handoff when a specialist should own the next interaction or task branch. Use parallel fan-out only when subtasks are independent, bounded, and have an explicit merge rule.

For every multi-agent design, define one owner for each mutable resource and one owner for the final user-facing result. Specify whether specialists return proposals, evidence, or authoritative state changes. Do not let multiple agents independently perform the same irreversible action. If multiple agents cannot be justified over a simpler pipeline, start with the simpler design.

### Define contracts at every boundary

For each component, specify input schema, output schema, allowed side effects, data classification, timeout, retry policy, idempotency key, error taxonomy, and evidence emitted. A component that returns a confident answer without source IDs, validation status, or execution evidence is not verified merely because it returned successfully.

Separate the **control plane** (policy, routing, approvals, budgets, identity, and run state) from the **execution plane** (model calls, retrieval, tools, and specialist work). A model may propose a route or action; deterministic policy code decides whether it is permitted. Keep authorization out of natural-language prompt instructions alone.

### Plan for change and rollback

Record replaceable seams: model provider, embedding model, vector store, tool transport, orchestration runtime, and state store. Define compatibility tests before swapping any seam. Version prompts, schemas, retrieval indexes, model identifiers, tool definitions, and evaluation datasets independently so regressions can be attributed.

Define rollback triggers before launch: hard safety violation, unauthorized side effect, schema incompatibility, sustained quality regression, budget breach, or recovery failure. A rollback plan must identify last known-good versions and state reconciliation; reverting code alone may not undo external side effects or data migrations.

### Architecture review questions

1. Can a deterministic baseline meet the required quality and latency?
2. Does retrieval solve a freshness or grounding problem prompting alone cannot solve?
3. Is fine-tuning supported by a measured error category and lawful, representative data?
4. Does agentic branching improve completion or merely add failure points?
5. Which component can cause an external side effect, and where is authorization enforced?
6. Can important results be traced to source data, model/prompt versions, tool outcomes, and validation?
7. Can the system stop safely, resume without duplicate actions, and recover from partial completion?
8. What is the smallest architecture that satisfies the hard constraints?

## Ultron routing contract

**Choose this skill when:** selecting and documenting the overall architecture of an AI-enabled product or system, including prompting, retrieval, fine-tuning, fixed workflows, agent orchestration, and boundaries for trust, state, evaluation, and deployment.

**Choose agent-design-patterns when:** the architecture direction is established and the task is to select or implement a concrete agent pattern, loop, handoff, manager, or specialist composition.

**Choose rag-and-retrieval-systems when:** the main problem is retrieval quality, corpus preparation, indexing, ranking, grounding, or retrieval evaluation rather than whole-application architecture.

**Choose llm-app-agents-and-prompts when:** implementing the application-level prompt, structured output, tool interaction, or agent integration contract within an already selected architecture.

**Handoff contract:** pass the problem statement, scorecard, baseline evidence, candidate comparison, trust/data-flow diagram, component contracts, side-effect inventory, evaluation gates, and unresolved assumptions. The implementation skill must preserve hard constraints and return infeasible requirements as explicit design conflicts rather than silently weakening them.

**Why the boundary exists:** this skill owns system-level trade-offs and component boundaries; specialist skills own detailed implementation and validation of a selected subsystem.
