---
name: agent-evaluation-design
description: Use when designing, reviewing, or extending evaluations (evals) for LLM-based agents or automation workflows, including task suites, graders, trajectory checks, regression baselines, and release gates.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Agent Evaluation Design

## Purpose and boundaries

Use this skill to turn an agent's intended behavior into a measurable evaluation suite that can gate changes to prompts, tools, models, or orchestration logic. It covers task-level outcome checks, intermediate trajectory checks (tool calls, arguments, ordering, budget), safety and policy checks, and regression tracking.

In scope: eval case design, grader selection (deterministic, rubric-based, model-graded, human review), sampling, baselines, statistical reporting, and pass/fail thresholds.

Out of scope: building the agent itself, general model training, unit testing of non-agent code, and certifying regulatory compliance. Do not claim that a passing suite guarantees safety, correctness, or compliance.

## Inputs and assumptions

Collect before designing anything:

1. Agent purpose statement: what it does, for whom, and what counts as success.
2. Tool inventory: each tool's name, side effects (read-only, write, external send, payment), and required arguments.
3. Environment: sandbox, staging, or production data. Assume production unless told otherwise, and treat it as sensitive.
4. Failure costs: which errors are cosmetic, costly, or harmful.
5. Existing traces or logs, if any, for sampling realistic inputs.
6. Model and framework identifiers, with the note that version-specific behavior (context limits, tool-calling formats, grader model availability) must be verified against current official documentation before relying on it.

If any of items 1–4 is missing, stop and request it. Do not invent success criteria.

## Operating workflow

1. **Define outcomes.** Write 3–7 outcome statements in the form "Given [input state], the agent must produce [observable result] without [forbidden action]." Each must be checkable from the environment state or final output.
2. **Map failure modes.** For each outcome, list at least three ways it can fail: wrong tool, wrong arguments, premature termination, hallucinated data, unauthorized action, excessive steps.
3. **Build the case set.** Target 30–50 cases for a first suite, distributed as: 50% typical, 30% edge (missing fields, ambiguous requests, conflicting instructions), 20% adversarial (injection in tool output, out-of-scope requests, permission boundaries). Derive typical cases from anonymized real traces where possible.
4. **Assign graders per check.** Use the cheapest reliable grader:
   - Deterministic: exact state diffs, schema validation, tool-call sequence assertions, forbidden-tool absence.
   - Rubric/model-graded: summary faithfulness, tone, completeness. Calibrate against at least 30 human-labeled examples and report agreement.
   - Human: any policy, safety, or financial judgment.
5. **Specify trajectory rules.** Define allowed tool sets per case, maximum step and token budgets, and required confirmation steps before writes.
6. **Set baselines.** Run the current production configuration 3 times on the suite to measure variance before setting any threshold.
7. **Write the report template** (see Deliverable contract) and freeze the suite version.

## Decision gates

- **Gate A (scope):** Proceed only if every outcome has an observable success signal. If not, rewrite the outcome or drop it.
- **Gate B (grader validity):** A model-graded check may gate releases only if its agreement with human labels is at least 85% and the disagreement cases are reviewed. Otherwise downgrade it to advisory.
- **Gate C (sample size):** Do not report a pass rate difference smaller than the baseline run-to-run spread as a real improvement.
- **Gate D (data sensitivity):** Before copying any production trace into the suite, confirm anonymization and that the owner has approved its use. Mark any case containing personal, financial, or credential data as restricted.
- **Gate E (side effects):** Any eval that triggers writes, sends messages, spends money, or calls external systems must run in a sandbox or mock. Running it against live systems requires explicit written approval from the system owner.

## Verification and evidence

- Each case records: input, expected outcome check, allowed tools, budget, grader ID, and expected-failure label if known.
- Report pass rate with a confidence interval (for example, Wilson interval for proportions) and the baseline spread from three runs.
- Report per-category results (typical, edge, adversarial) separately. A high overall score cannot hide adversarial failures.
- Include at least 5 failed traces per release candidate in the review, with the first wrong step identified.
- Check grader determinism: rerun 10% of model-graded cases and report flip rate. A flip rate above 10% makes that grader advisory.
- Record model, prompt, tool schema, and suite versions for every run. Verify model identifiers and any tool-calling interface details against current official documentation.

## Failure handling

- **Flaky case** (different results across identical runs): mark it, investigate environment nondeterminism first, then the grader. Do not silently retry until it passes.
- **Grader disagreement:** sample 10 disagreements, decide the correct label, update the rubric, and recalibrate.
- **Suite-wide regression:** halt the release candidate, bisect across prompt, tool, and model changes one variable at a time.
- **Unexpected side effect during eval:** stop the run, report the exact action and environment, and escalate. Do not continue to rerun.
- **Insufficient data for a category:** report it as "insufficient evidence" rather than a percentage.

## Deliverable contract

The final evaluation package must contain:

1. Suite manifest: version, date, agent configuration identifiers, case count per category.
2. Outcome list with mapped failure modes.
3. Case table: ID, category, input summary, checks, grader, budget, sensitivity flag.
4. Grader calibration report: sample size, agreement, flip rate, and disposition (gating or advisory).
5. Results: per-category pass rates with intervals, baseline spread, and trajectory violations.
6. Gate decision: pass, fail, or hold, with the specific gate that drove it.
7. Open risks: untested tools, untested languages or user segments, and any version-sensitive assumptions still awaiting verification.

## What not to do

- Do not write success criteria that a human cannot check from the output or environment state.
- Do not use the agent's own output as the sole judge of its correctness without calibration.
- Do not tune cases to a failing agent so the score improves; fix the agent or document the failure.
- Do not run evals against live systems or real customers without explicit approval.
- Do not report a single run as a benchmark result.
- Do not state that an eval score demonstrates safety, legal compliance, or fitness for regulated use.
## Continuous agent evaluation and release engineering (v1.1)

An evaluation suite is a versioned product artifact. Track separate versions for instructions, model, tool schemas, policy bundle, memory schema, runtime, and test suite. Every result must identify the complete configuration.

Layer evaluations: unit checks for schemas and deterministic adapters; component checks for retrieval, memory, routing, and tools; trajectory checks for ordering, arguments, approvals, retries, and stopping; outcome checks against external postconditions; adversarial checks for injection, permission denial, isolation, malformed tool output, and budget abuse; operational checks for latency, cost, timeout recovery, concurrency, and checkpoint resumption; and human review for high-impact judgments.

Build cases from anonymized failures, support escalations, near misses, tool errors, and user corrections. Each case declares preconditions, allowed tools, prohibited actions, expected state transitions, observable postconditions, grader, budget, and severity. Keep an unseen holdout set to reduce overfitting.

A correct final answer does not excuse an unauthorized intermediate action. Score goal completion, grounding, tool selection, argument validity, policy adherence, side-effect correctness, efficiency, and recovery separately. Record the first trajectory divergence and whether it caused an external effect. Include negative assertions such as "no message sent" or "no cross-tenant record returned."

Run frozen suites against candidate and baseline in equivalent environments. Repeat stochastic cases to estimate variance; report per-case outcomes and category counts. Gate safety-critical failures independently of aggregate scores. Require human review for unexplained shifts, new permissions, model or policy changes, and memory migrations. Preserve a rollback artifact and known-good configuration.

Keep grader prompts and holdout labels separate from the agent. Calibrate model graders against human labels and publish disagreements. Version case changes with reasons; do not remove a hard case merely because it fails. A green suite means only that tested behaviors passed under recorded conditions.

