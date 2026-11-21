---
name: ai-system-architecture
description: Use when designing, reviewing, or documenting the architecture of an AI-enabled system, including choosing between prompting, retrieval-augmented generation, fine-tuning, and agentic workflows, or defining data flows, evaluation harnesses, and deployment boundaries for LLM or ML components.
author: Luo Kai
provenance: original
version: 1.0.0
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