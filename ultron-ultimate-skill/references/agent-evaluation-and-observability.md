# Agent Evaluation and Observability

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## agent-evaluation-design

**Use when:** Use when designing, reviewing, or extending evaluations (evals) for LLM-based agents or automation workflows, including task suites, graders, trajectory checks, regression baselines, and release gates.

### Purpose and boundaries

Use this skill to turn an agent's intended behavior into a measurable evaluation suite that can gate changes to prompts, tools, models, or orchestration logic. It covers task-level outcome checks, intermediate trajectory checks (tool calls, arguments, ordering, budget), safety and policy checks, and regression tracking.

In scope: eval case design, grader selection (deterministic, rubric-based, model-graded, human review), sampling, baselines, statistical reporting, and pass/fail thresholds.

Out of scope: building the agent itself, general model training, unit testing of non-agent code, and certifying regulatory compliance. Do not claim that a passing suite guarantees safety, correctness, or compliance.

### Inputs and assumptions

Collect before designing anything:

1. Agent purpose statement: what it does, for whom, and what counts as success.
2. Tool inventory: each tool's name, side effects (read-only, write, external send, payment), and required arguments.
3. Environment: sandbox, staging, or production data. Assume production unless told otherwise, and treat it as sensitive.
4. Failure costs: which errors are cosmetic, costly, or harmful.
5. Existing traces or logs, if any, for sampling realistic inputs.
6. Model and framework identifiers, with the note that version-specific behavior (context limits, tool-calling formats, grader model availability) must be verified against current official documentation before relying on it.

If any of items 1–4 is missing, stop and request it. Do not invent success criteria.

### Operating workflow

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

### Decision gates

- **Gate A (scope):** Proceed only if every outcome has an observable success signal. If not, rewrite the outcome or drop it.
- **Gate B (grader validity):** A model-graded check may gate releases only if its agreement with human labels is at least 85% and the disagreement cases are reviewed. Otherwise downgrade it to advisory.
- **Gate C (sample size):** Do not report a pass rate difference smaller than the baseline run-to-run spread as a real improvement.
- **Gate D (data sensitivity):** Before copying any production trace into the suite, confirm anonymization and that the owner has approved its use. Mark any case containing personal, financial, or credential data as restricted.
- **Gate E (side effects):** Any eval that triggers writes, sends messages, spends money, or calls external systems must run in a sandbox or mock. Running it against live systems requires explicit written approval from the system owner.

### Verification and evidence

- Each case records: input, expected outcome check, allowed tools, budget, grader ID, and expected-failure label if known.
- Report pass rate with a confidence interval (for example, Wilson interval for proportions) and the baseline spread from three runs.
- Report per-category results (typical, edge, adversarial) separately. A high overall score cannot hide adversarial failures.
- Include at least 5 failed traces per release candidate in the review, with the first wrong step identified.
- Check grader determinism: rerun 10% of model-graded cases and report flip rate. A flip rate above 10% makes that grader advisory.
- Record model, prompt, tool schema, and suite versions for every run. Verify model identifiers and any tool-calling interface details against current official documentation.

### Failure handling

- **Flaky case** (different results across identical runs): mark it, investigate environment nondeterminism first, then the grader. Do not silently retry until it passes.
- **Grader disagreement:** sample 10 disagreements, decide the correct label, update the rubric, and recalibrate.
- **Suite-wide regression:** halt the release candidate, bisect across prompt, tool, and model changes one variable at a time.
- **Unexpected side effect during eval:** stop the run, report the exact action and environment, and escalate. Do not continue to rerun.
- **Insufficient data for a category:** report it as "insufficient evidence" rather than a percentage.

### Deliverable contract

The final evaluation package must contain:

1. Suite manifest: version, date, agent configuration identifiers, case count per category.
2. Outcome list with mapped failure modes.
3. Case table: ID, category, input summary, checks, grader, budget, sensitivity flag.
4. Grader calibration report: sample size, agreement, flip rate, and disposition (gating or advisory).
5. Results: per-category pass rates with intervals, baseline spread, and trajectory violations.
6. Gate decision: pass, fail, or hold, with the specific gate that drove it.
7. Open risks: untested tools, untested languages or user segments, and any version-sensitive assumptions still awaiting verification.

### What not to do

- Do not write success criteria that a human cannot check from the output or environment state.
- Do not use the agent's own output as the sole judge of its correctness without calibration.
- Do not tune cases to a failing agent so the score improves; fix the agent or document the failure.
- Do not run evals against live systems or real customers without explicit approval.
- Do not report a single run as a benchmark result.
- Do not state that an eval score demonstrates safety, legal compliance, or fitness for regulated use.
### Continuous agent evaluation and release engineering (v1.1)

An evaluation suite is a versioned product artifact. Track separate versions for instructions, model, tool schemas, policy bundle, memory schema, runtime, and test suite. Every result must identify the complete configuration.

Layer evaluations: unit checks for schemas and deterministic adapters; component checks for retrieval, memory, routing, and tools; trajectory checks for ordering, arguments, approvals, retries, and stopping; outcome checks against external postconditions; adversarial checks for injection, permission denial, isolation, malformed tool output, and budget abuse; operational checks for latency, cost, timeout recovery, concurrency, and checkpoint resumption; and human review for high-impact judgments.

Build cases from anonymized failures, support escalations, near misses, tool errors, and user corrections. Each case declares preconditions, allowed tools, prohibited actions, expected state transitions, observable postconditions, grader, budget, and severity. Keep an unseen holdout set to reduce overfitting.

A correct final answer does not excuse an unauthorized intermediate action. Score goal completion, grounding, tool selection, argument validity, policy adherence, side-effect correctness, efficiency, and recovery separately. Record the first trajectory divergence and whether it caused an external effect. Include negative assertions such as "no message sent" or "no cross-tenant record returned."

Run frozen suites against candidate and baseline in equivalent environments. Repeat stochastic cases to estimate variance; report per-case outcomes and category counts. Gate safety-critical failures independently of aggregate scores. Require human review for unexplained shifts, new permissions, model or policy changes, and memory migrations. Preserve a rollback artifact and known-good configuration.

Keep grader prompts and holdout labels separate from the agent. Calibrate model graders against human labels and publish disagreements. Version case changes with reasons; do not remove a hard case merely because it fails. A green suite means only that tested behaviors passed under recorded conditions.

### Evaluation integrity and deployment-stage gates (v1.2)

An agent benchmark can overstate capability when the test set, harness, tools, or retrieval environment leak the expected answers. Treat evaluation integrity as part of the system under test.

#### Prevent contamination and harness leakage
- Keep final holdout tasks and labels inaccessible to the agent, prompt author, and routine optimization loop.
- Separate development, validation, and holdout datasets. Record who can access each and when.
- Inspect prompts, tool descriptions, scaffold code, retrieval indexes, examples, and cached responses for benchmark-specific answer leakage.
- Test whether web search, APIs, or connected tools can retrieve the benchmark answer during evaluation when the benchmark intends to test unaided capability.
- Rotate or refresh exposed holdouts. Report known overlap and prior use rather than treating a public benchmark as secret.
- Inspect full trajectories for answer memorization, hard-coded task branches, unauthorized evaluator access, and other harness-level shortcuts.
- Use clean evaluation environments with pinned agent, model, skill, tool, and dataset versions.

#### Measure generalization, not only aggregate score
Stratify results by task family, difficulty, ambiguity, language, tenant, data quality, tool availability, and risk class. Report sample counts and confidence or uncertainty intervals where meaningful. Preserve per-case outcomes and representative failures; an aggregate score must not conceal a critical failure in a small but high-risk slice.

For stochastic tasks, repeat enough trials to estimate variance and record seeds or replay conditions where available. Separate model variance from environment, tool, and evaluator variance. Do not compare versions using materially different budgets or access to tools without explicitly labeling the comparison.

#### Evaluator quality
For model-based graders:
- Define a rubric with observable criteria and examples of borderline outcomes.
- Calibrate against independent human labels on a stratified sample.
- Track agreement, disagreement categories, and grader drift by version.
- Use pairwise or structured judgments where absolute scoring is unstable.
- Keep grader prompts and hidden reference answers inaccessible to the evaluated agent.
- Escalate ambiguous or high-impact outcomes to qualified human review.

An LLM judge is a measurement instrument with its own error rate, not ground truth.

#### Release gates
Use separate gates for safety, task success, reliability, and operations. Do not let high task success compensate for an unauthorized action or failed safety invariant.

A cautious deployment sequence is:
1. Offline evaluation against frozen development and holdout suites.
2. Shadow execution with no user-visible side effects.
3. Limited canary with strict traffic, cost, and action limits.
4. Staged expansion only after slice-level metrics and safety probes remain within policy.
5. Continuous monitoring with a tested kill switch and rollback path.

Define minimum sample counts, guardrail thresholds, and observation windows before rollout. If evidence is insufficient, hold the release rather than interpreting missing data as a pass.

#### Evaluation report contract
Record the candidate and baseline digests, test-set versions, holdout access policy, environment, model and tool versions, budgets, per-slice outcomes, evaluator calibration, safety failures, and deployment decision. Include known contamination risks and tests that were not run. Never describe benchmark performance as proof of general intelligence or universal reliability.

### Ultron routing contract

**Choose this skill when:** defining what an agent must prove before release and how its behavior should be evaluated over time: evaluation layers, safety gates, trajectory correctness, outcome verification, holdouts, regression policy, and release thresholds.

**Choose `llm-benchmark-harness` when:** implementing the actual test runner, frozen case set, controlled environment, graders, and scoring pipeline.

**Choose `experiment-tracking` when:** organizing multiple controlled runs and comparing model, prompt, tool, or routing variants under a stable measurement setup.

**Choose `ai-change-verification` when:** the evaluation result is being used to approve a concrete AI-generated code/configuration change and must be tied to a reproducible change artifact and rollback evidence.

**Handoff contract:** this skill defines the acceptance policy and risk thresholds; specialist tools return versioned cases, raw outcomes, per-slice scores, grader calibration, and change provenance. Never let a high aggregate score override a failed safety invariant.

**Why the boundary exists:** deciding what counts as acceptable behavior is separate from running a benchmark or approving one particular change.


### Statistical validity for stochastic agent comparisons (v1.4)

Treat the evaluation task, not each repeated execution, as the primary independent sampling unit when tasks are sampled from a broader task population. Repeated runs of one task estimate that task's execution variability; they do not create new independent task examples. Report both the number of distinct tasks and the number of executions per task.

When comparing a candidate with a baseline, run both configurations on the same task set under equivalent permissions, tools, budgets, environment state, and grader conditions. Preserve task pairing in the analysis. Report per-task outcomes and paired differences, including ties and regressions; do not infer an improvement from two unpaired aggregate pass rates when a paired design is feasible.

Before running the comparison, define the primary metric, minimum practically important effect, acceptable false-positive risk, target power where a formal test is appropriate, sampling plan, exclusions, and stopping rule. Estimate the number of independent tasks from pilot variance or historical task-level differences. If the available task set is fixed, report the minimum detectable effect rather than pretending the suite can establish smaller changes. Do not keep adding tasks or rerunning until a favorable result appears.

For repeated stochastic executions, preserve the task grouping and report within-task variability separately from between-task variability. Choose repeat counts based on the decision: additional distinct tasks usually improve generalization evidence, while repeats help characterize flaky tasks and execution reliability. State the randomization or replay controls used and whether the environment was reset consistently.

For multiple candidate variants, metrics, slices, or repeated interim looks, predefine the primary comparison and control multiplicity or label secondary findings exploratory. Do not select the best-looking metric after observing results. Report effect sizes and uncertainty intervals, not only p-values or a binary significance label. Use a task-clustered bootstrap or a suitable paired method when its assumptions fit; explain the sampling unit and method.

Audit grader error as part of comparison validity. Validate false-pass and false-fail rates against human-labeled examples across relevant task categories and candidate systems. Check whether grader error differs by model family, response style, answer length, language, or task type. For pairwise judges, counterbalance presentation order and test position bias. If grader quality differs materially between candidates or categories, do not treat the raw score gap as an unbiased estimate; recalibrate, use a more reliable grader, or downgrade the conclusion.

A release decision must consider newly failing high-severity tasks, safety invariants, and task slices in addition to the mean score. Keep the complete per-task result table and representative regressions with the report. If the suite is too small or noisy to resolve the practical effect, record the result as inconclusive and gather better evidence rather than declaring a winner.

#### Statistical comparison checklist

- [ ] Distinct task count and executions-per-task count are both reported.
- [ ] Candidate and baseline were tested on the same tasks under comparable conditions.
- [ ] Pairing and task-level differences are preserved in the analysis.
- [ ] Primary metric, practical effect threshold, sample plan, and stopping rule were fixed before the run.
- [ ] Repeated runs are not misrepresented as independent tasks.
- [ ] Grader calibration includes category- and candidate-specific error checks.
- [ ] Multiple comparisons and interim looks are controlled or clearly exploratory.
- [ ] Effect size, uncertainty, regressions, and critical failures are visible.
- [ ] Insufficient evidence is reported as inconclusive, not as a pass.


### Cross-skill routing, conflict, and handoff evaluation (v1.5)

A skill system must be evaluated as a coordinated decision system, not only as 250 isolated documents. Build a dedicated evaluation slice that measures whether the agent selects the right capability, respects ownership boundaries, preserves unresolved conflicts, and transfers work without losing constraints or evidence.

#### Define observable routing outcomes

For each scenario, specify:
- User goal and task scope, including explicit exclusions.
- Candidate skills and their pinned versions, including near-neighbor skills that should not own the task.
- The expected primary skill, optional supporting skills, and skills that must not be invoked for the stated scope.
- Required handoff fields, evidence references, and receiving-skill acceptance conditions.
- Policy and authority constraints that remain independently enforced regardless of routing.
- Observable completion and negative assertions, such as no unauthorized tool call, no duplicate execution, and no approval reuse for a changed target.

Do not grade a route solely by matching one exact skill name when multiple valid decompositions exist. Define an acceptable capability set and the responsibilities each selected skill must perform. Penalize missing owners, unnecessary duplication, and incompatible parallel execution.

#### Required scenario families

Include at least these families in the routing and handoff suite:
1. **Near-neighbor discrimination:** distinguish context compaction from durable memory and session recovery; workflow planning from queue execution; tool integration from server hardening; evaluation policy from benchmark implementation.
2. **Authority conflict:** a general recommendation conflicts with a scoped hard constraint; a stale approval conflicts with current policy; two same-authority sources differ and no explicit supersession is present.
3. **Untrusted instruction:** retrieved content or a tool result attempts to override the task, grant permissions, or redirect a handoff.
4. **Incomplete handoff:** missing target, artifact digest, tenant, policy revision, approval binding, or postcondition must produce rejection or a non-executable hold.
5. **Stale handoff:** skill digest, dependency, environment, policy, target, or task revision changes after sender preparation and before receiver acceptance.
6. **Duplicate and concurrent delivery:** repeated message, lost acknowledgement, delayed sender, competing worker, or duplicate child result must not create two logical side effects.
7. **Partial conflict:** one branch is blocked by a disputed constraint while independent branches can safely continue with separate ownership.
8. **Recovery and compaction:** compressed state preserves exact blockers, provenance, completed effects, approvals, and next safe action after restart.

#### Score the full trajectory

Record separate measures for primary-skill selection, supporting-skill precision, missed required capability, boundary violations, conflict detection, authority classification, conflict disposition, handoff schema validity, receiver acceptance, provenance retention, approval binding, duplicate-effect prevention, and postcondition verification. Record the first incorrect decision and whether it caused a side effect.

Use deterministic graders for schemas, version pins, tool-call permissions, state transitions, artifact digests, duplicate execution, and forbidden actions. Use calibrated rubric graders only for semantic quality such as whether a boundary explanation is adequate. Human review is required when the correct authority or policy interpretation is itself disputed. A model grader must not adjudicate the same safety conflict whose resolution is under test.

#### Dataset construction and anti-shortcut controls

Create cases from realistic multi-skill tasks, anonymized failures, routing disagreements, stale handoffs, and recovery incidents. Include paraphrased requests, multilingual phrasing where relevant, missing fields, misleading descriptions, and adversarial instructions in retrieved content. Keep hidden cases and expected routes unavailable to the routing model and routine prompt optimization loop. Pin the skill catalog, policy, runtime, and test harness for each evaluation run.

Use paired baseline/candidate runs on the same cases and comparable tool access. Report distinct scenario count separately from repeated stochastic executions. Preserve per-case trajectories and stratify by task family, risk, ambiguity, and language. A high routing score cannot compensate for a single critical authorization bypass or duplicate irreversible action.

#### Release gate

Hold release if the agent executes a blocked handoff, treats routing as authorization, drops a material unresolved conflict during compaction, reuses approval after a material action change, or creates duplicate external effects. For non-critical routing errors, require an owner and corrective action, then rerun the frozen regression slice. If the expected skill set is genuinely ambiguous, label the case ambiguous and define acceptable decompositions rather than forcing a false single answer.

**Routing boundary:** this section defines evaluation requirements and acceptance criteria. Use llm-benchmark-harness to implement the runner and experiment-tracking to organize controlled comparisons; do not let the evaluation skill become the runtime conflict resolver.


## agent-tracing-observability

**Use when:** Use when instrumenting, debugging, or auditing LLM agent runs (tool calls, model calls, retrievals, sub-agent handoffs) and you need traces, spans, token and cost accounting, or evidence of what an agent actually did.

### Purpose and boundaries

This skill designs and reviews tracing for autonomous or semi-autonomous agent systems: capturing a structured record of each run so engineers can reconstruct decisions, diagnose failures, measure cost and latency, and verify behavior against expectations.

In scope: trace data model design, span boundaries, attribute schemas, redaction rules, sampling policy, cost and token attribution, trace-based evaluation, and incident reconstruction.

Out of scope: model selection, prompt authoring quality, general application APM unrelated to agent steps, and any claim that tracing guarantees safety or regulatory compliance.

### Inputs and assumptions

Gather before designing:
- Agent topology: single loop, planner/executor, multi-agent handoffs, or workflow graph.
- Step types: model calls, tool invocations, retrievals, memory reads/writes, human approvals, sub-agent calls.
- Data sensitivity: what prompts, tool arguments, and outputs may contain (personal data, credentials, customer records).
- Storage and retention constraints, and who may read traces.
- Existing telemetry stack. If you rely on a specific tracing standard or SDK, verify current attribute names and semantic conventions against its official documentation; they change between versions.

Assume nothing about provider token counting or pricing; use the values the provider returns and mark any price table as version-sensitive.

### Operating workflow

1. **Map the run.** Draw the actual execution graph from logs or code, not the intended design. Identify every point where control leaves the agent (tool, API, file write, message send).
2. **Define spans.** One root span per user-visible task or job. Child spans for each model call, tool call, retrieval, and handoff. Avoid spans for trivial in-memory string operations.
3. **Set the attribute schema.** For each span record: run ID, parent ID, step index, span kind, model or tool name, version identifier, start and end time, status, input and output size, token counts (input, output, cached if reported), and error class.
4. **Apply redaction before export.** Hash or drop secrets, credentials, and personal identifiers at the instrumentation point, not in the backend.
5. **Choose sampling.** Keep 100% of error and policy-flagged runs; sample successful high-volume runs. Record the sampling decision on the root span so analyses can correct for it.
6. **Attribute cost.** Sum token usage per run and per step. Compute cost only with a dated, versioned price table recorded alongside the data.
7. **Link to evaluation.** Store the expected outcome or rubric reference on the root span when one exists, so trace review can be scored.
8. **Validate with a replay.** Run a known task end to end and confirm the trace reconstructs the sequence, arguments, and results.

### Decision gates

Stop and request explicit approval before:
- Enabling capture of full prompts, tool arguments, or model outputs in any environment that holds real customer or personal data.
- Exporting traces to a third-party service or outside the current data boundary.
- Changing retention periods, deleting existing traces, or purging audit records.
- Turning on tracing in production for a system that performs writes, payments, messages, or other external actions, if the change alters runtime behavior or adds latency on the critical path.
- Adding any tool that lets the agent read its own traces, since this can create feedback loops and data exposure.

Proceed without a gate for: local development traces with synthetic data, span naming changes in a non-production branch, and dashboard construction on already-approved fields.

### Verification and evidence

Check each of the following and record results:
- **Completeness:** for a replayed run of N known steps, the trace contains N step spans with correct parent-child links. Target: zero missing or orphaned spans.
- **Ordering:** timestamps are monotonic within each parent; child spans fall inside parent intervals.
- **Token accounting:** sum of per-step tokens equals the run total within the provider's reported figures. Any discrepancy is logged, not averaged away.
- **Redaction:** a seeded canary string placed in a test input must not appear in any exported attribute. Zero occurrences required.
- **Error fidelity:** an injected tool failure appears as an error status with a classified error type, and the agent's subsequent step is linked to it.
- **Overhead:** measure added latency with and without instrumentation on the same workload; report the median and p95 difference. Do not claim a figure you have not measured.

### Failure handling

- **Missing spans:** check async context propagation first; spans created in detached tasks or callbacks often lose parent links.
- **Duplicated spans:** typically retries re-emitting spans. Give each attempt its own span with an attempt counter rather than suppressing it.
- **Oversized payloads:** store large inputs or outputs by reference (content hash plus a secured store) and record byte size inline.
- **Redaction false negatives:** treat any leaked sensitive value as a severity incident. Halt export, identify affected records, and request approval before deletion.
- **Clock skew across services:** record both local timestamps and the sequence index; do not reorder by timestamp alone.

### Deliverable contract

Deliver:
1. A span tree diagram for the agent's main flow.
2. An attribute table with field name, type, source, redaction class, and whether it is required.
3. Sampling and retention policy with the approval status of each setting.
4. Verification results from the checks above, with actual counts and measured values.
5. A list of open items, each marked as requiring verification against current official documentation where a version-specific detail applies.

Do not deliver a trace design that has not been replayed, claims tracing makes an agent correct or compliant, or contains unredacted sensitive fields in examples.
### End-to-end agent run evidence (v1.1)

Instrument the entire run, not just model calls. Connect the user request, run contract, plan revision, policy decisions, model turns, tool invocations, approvals, worker tasks, checkpoints, artifacts, and final verification. Use stable correlation identifiers for run, task, step, tool call, approval, and external operation.

Capture structured events for run creation and contract revisions; plan generation, validation, and rejection; policy decisions with policy version and reason; approval request, grant, denial, expiry, or invalidation; tool request, authorization, execution, retry, reconciliation, and verification; worker dispatch and acceptance; checkpoint save and restore; artifact digest; and terminal status.

Record timestamps plus a monotonic sequence number. Distinguish model intention from gateway authorization and downstream execution. Store large payloads by protected reference and digest; traces must not become a second database of sensitive content.

Measure verified task completion, tool error rate by class, approval wait time, duplicate suppression, retries per operation, recovery success, policy denials, injection detections, checkpoint restore success, and cost/latency per completed task. Segment by agent version, tool version, task family, and risk class. Faster execution achieved by skipping verification is a regression.

Alert on repeated denials, unusual tool sequences, unexpected privilege use, excessive retries, runaway spend, cross-tenant attempts, missing approval receipts, and abnormal side-effect volume. Define an owner, severity, response window, and disable action for each alert. Preserve security-critical events even when ordinary spans are sampled out.

For consequential workflows, maintain an append-only event ledger with hash-linked records or another suitable tamper-evident mechanism. Record hashes and references rather than raw sensitive payloads. Protect ledger access separately from the runtime. Define retention, access, export, and deletion rules before launch; immutability must not be used to evade retention or deletion requirements.

### Telemetry privacy, audit integrity, and evidence boundaries (v1.2)

Metrics, traces, logs, and audit records answer different questions. Do not treat them as interchangeable evidence.

#### Signal responsibilities
- **Metrics** describe aggregate behavior such as latency, error classes, token use, tool-call rates, cost, and policy-denial rates. Use bounded dimensions and avoid request content or high-cardinality identifiers as metric labels.
- **Traces** connect stages of a request and help locate latency or failure across model calls, retrieval, policy checks, and tools. Sampling, missing instrumentation, and best-effort exporters mean a trace is not a complete audit ledger.
- **Operational logs** capture bounded diagnostic events and service errors. Prefer normalized error categories over raw provider messages that may contain user content or credentials.
- **Audit evidence** records attributable decisions and consequential actions for investigation. It requires explicit delivery, access, integrity, and retention guarantees beyond ordinary telemetry.

#### Privacy-by-design capture
Before enabling content-bearing telemetry, define the purpose, data owner, approved fields, access roles, retention period, residency constraints, and redaction method. Default to metadata and digests rather than raw prompts, completions, tool arguments, documents, or retrieved passages.

Never emit passwords, API keys, bearer tokens, refresh tokens, private keys, session cookies, or authentication headers. Treat user identifiers, tenant identifiers, file paths, and correlation metadata as potentially sensitive even when message content is absent. Restrict access and retention accordingly.

Use allowlisted structured fields rather than serializing arbitrary request objects. Apply redaction before data leaves the process, not only in a downstream dashboard. Test redaction against nested errors, retries, exception traces, and malformed tool responses.

#### Correlation and attribution
Use server-generated run and span identifiers. Treat caller-supplied correlation IDs as untrusted metadata, not identity or authorization. Preserve distinct fields for requested model, served model, agent version, skill digest, tool version, policy version, initiating subject, and task identity when available and permitted.

Record both admission and completion evidence for consequential operations:
- Admission: caller and task identity, policy version, action classification, normalized destination, decision, and approval reference.
- Completion: downstream operation identifier, outcome, postcondition verification, retries or reconciliation, and artifact digest where relevant.

A successful admission does not prove the action completed. A tool response does not prove the intended external state changed. Verify the postcondition through an authoritative read path.

#### Durable audit delivery
For actions requiring durable evidence, use an append-only or tamper-evident store with explicit acknowledgement, access separation, retention, and export controls. Track dropped, delayed, duplicated, and rejected audit events. Define whether an action must fail closed when audit persistence is unavailable; do not imply that guarantee exists unless the execution path enforces it.

Keep audit integrity controls separate from the agent runtime so an agent cannot rewrite or erase its own evidence. Hash chaining can help detect alteration, but it does not by itself prove event completeness, truthful event generation, or correct retention.

#### Verification tests
Test that:
- Secrets and personal content are absent from metrics, traces, logs, and error paths.
- Metric dimensions remain bounded under high-cardinality traffic.
- A sampled-out trace does not remove required audit evidence.
- Missing audit acknowledgement triggers the documented policy behavior.
- Correlation IDs cannot be used to impersonate another task or subject.
- Admission and completion records can be joined without exposing raw sensitive payloads.
- An agent runtime cannot modify or delete the durable audit record.

Report telemetry coverage, known blind spots, retention, redaction tests, and delivery guarantees separately. Do not claim compliance or complete forensic reconstruction from instrumentation alone.

### Ultron routing contract

**Choose this skill when:** instrumenting agent-specific execution: model turns, tool calls, handoffs, approvals, memory access, queue events, checkpoints, artifacts, and verified task outcomes.

**Choose `sre-observability-and-incidents` when:** the work concerns general service/platform telemetry, infrastructure health, SLOs, on-call alerting, or incident response across services rather than agent-run semantics.

**Choose `threat-hunting-incident-response` or the relevant security response skill when:** telemetry indicates a security incident that needs investigation and containment, not merely an observability dashboard.

**Handoff contract:** agent tracing emits bounded, privacy-reviewed run and action evidence with stable identifiers and policy/version context. The platform SRE skill consumes service-level signals and owns operational response. Security incident response consumes attributable events and owns investigation. Keep metrics, sampled traces, logs, and durable audit records distinct.

**Why the boundary exists:** agent behavior needs semantic traces, but platform reliability and security incident management require different owners, retention, and response guarantees.


### Trace integrity, asynchronous causality, and content minimization (v1.4)

A trace is an evidence record of instrumented execution, not a complete or automatically truthful transcript. Document what is instrumented, what is sampled, what is omitted, and which execution paths can bypass instrumentation. Never infer that an action did not occur merely because its span is absent unless instrumentation coverage and failure behavior make that absence meaningful.

#### Preserve causality across boundaries
- Propagate trace context across process, service, agent, tool, and queue boundaries using the supported context-propagation mechanism for each transport. Do not assume an HTTP request span captures every message or operation inside a long-lived stream.
- For asynchronous work, retain the originating run/task identifier and use parent-child relationships or span links according to the actual causal relationship. A queued task that executes later should not be represented as if it were synchronous work inside the original request.
- Record stable, non-secret identifiers for run, task, attempt, tool call, approval, and artifact version. Distinguish logical operation IDs from retry/attempt IDs.
- Record state transitions and external-effect receipts at the boundary where the effect is attempted and where its outcome is reconciled. A successful tool-call span alone does not prove the intended external postcondition.
- When clocks or services are not synchronized, avoid deriving strict event order from wall-clock timestamps alone. Preserve causal links and monotonic duration measurements where available.

#### Make capture policy explicit
- Default to metadata-only traces. Treat prompts, completions, tool arguments/results, retrieved documents, memory content, and exception messages as potentially sensitive.
- If content capture is justified, require a documented purpose, data classification, approved audience, retention period, deletion path, and access audit. Prefer storing approved content in a separately governed artifact store and placing only opaque references and integrity metadata in traces.
- Apply minimization and redaction before data leaves the originating trust boundary. Downstream collector filters are defense in depth, not permission to export raw secrets or personal data first.
- Inspect actual exported payloads from every enabled instrumentation and exporter. A global capture flag does not guarantee that custom spans, framework instrumentation, logs, baggage, or vendor exporters follow the same policy.
- Keep high-cardinality or sensitive values out of metric labels. Use bounded dimensions for metrics and access-controlled trace attributes for detailed diagnosis.
- Treat baggage and propagated context as untrusted input. Allowlist keys, constrain size, prevent identity or tenant spoofing, and never propagate credentials or authorization tokens.

#### Sampling and evidence completeness
- State the sampling policy and its effect on conclusions. Preserve 100% of defined high-severity failures or security-relevant events where feasible, while documenting any unavoidable loss.
- If sampling is probabilistic, record the sampling decision and policy version. Use sampling-aware analysis when estimating population rates; do not treat a sampled trace set as a census.
- Record dropped-span, exporter-failure, queue-overflow, and collector-loss indicators where available. Distinguish an absent event from an event that could not be observed.
- Maintain a separate durable audit record for security-sensitive or regulated actions when trace sampling, retention, or mutability cannot meet the required evidence guarantee.
- Validate trace completeness with synthetic canary runs that exercise tool calls, retries, handoffs, asynchronous callbacks, failures, and approval pauses.

#### Trace review contract
For an incident or disputed action, reconstruct the causal sequence from trace IDs, task/attempt identifiers, policy and configuration versions, tool call IDs, and external system receipts. Mark each conclusion as directly observed, inferred from linked events, or unavailable. State instrumentation gaps and sampling limitations. Do not claim that traces prove intent, correctness, or absence of uninstrumented actions.

