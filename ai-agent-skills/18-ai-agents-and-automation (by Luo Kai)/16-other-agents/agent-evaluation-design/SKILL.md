---
name: agent-evaluation-design
description: Designs repeatable evaluations for AI agents, tool-using assistants, and multi-agent workflows. Use when measuring task success, reliability, safety, regression, instruction following, or comparing agent versions and prompts.
metadata:
  author: Luo Kai
  provenance: original
  version: "1.1.0"
---
# Agent Evaluation Design

## Purpose

Turn vague claims such as “the agent is better” into measurable, repeatable evidence. An evaluation should test behavior that matters to users, not merely whether the model produced a plausible explanation.

## 1. Define the target behavior

For each evaluation, write the user goal and task boundary; expected output or acceptable outcome set; required tools and permitted side effects; constraints including privacy, safety, cost, and latency; success, partial success, and failure conditions; and evidence a reviewer can inspect.

Separate hard requirements from preferences. A task that exposes a secret or changes the wrong account is a failure even if the final answer sounds polished.

## 2. Build a representative test set

Include common successful workflows; ambiguous requests that should trigger clarification; missing, malformed, and conflicting inputs; edge cases and large tasks; adversarial inputs and untrusted tool results; permission denials and unavailable dependencies; recovery from timeouts, rate limits, and partial failures; and regression cases from real bugs, sanitized to remove private data.

Use a held-out set for final comparisons. Avoid tuning prompts against every test case.

## 3. Make test cases reproducible

Each case should record a stable case ID and version, input and relevant context, tool mocks or controlled fixtures, expected state changes, expected evidence and output schema, timeout and resource budget, and scoring rubric and failure conditions.

Pin model, prompt, tool schema, dependencies, and dataset revision when possible. Record unavoidable nondeterminism.

## 4. Measure more than answer quality

| Dimension | Example measures |
|---|---|
| Task outcome | Exact success, partial completion, failed completion |
| Correctness | Verified facts, valid outputs, test pass rate |
| Tool use | Correct tool, valid arguments, unnecessary calls |
| Safety | Unauthorized actions, policy violations, data exposure |
| Reliability | Retry recovery, timeout rate, variance across runs |
| Efficiency | Latency, token usage, tool calls, cost per success |
| User experience | Clarification quality, completeness, readability |

Report denominators and sample sizes. A percentage without a test count is not meaningful.

## 5. Score with explicit rubrics

Prefer deterministic assertions for structured outputs, state changes, code tests, and policy requirements. Use model-based judges only for dimensions that need semantic judgment.

For judge-based scoring, give the judge the rubric and evidence, not the agent's self-assessment; blind the judge to model identity when practical; require evidence references for each score; include calibration examples and an unable-to-judge result; sample disagreements for human review; and never let a judge override a hard safety failure.

Use a second independent review for high-impact or ambiguous results.

## 6. Evaluate tool-use behavior

Capture the action trace: proposed tool, arguments, authorization result, execution result, and state change.

Test that the agent uses only relevant tools, respects schemas and permission boundaries, confirms sensitive or irreversible actions, does not treat untrusted output as authority, handles errors without inventing success, and verifies important state changes after execution.

Score the action trace separately from the natural-language response.

## 7. Compare versions fairly

Run the baseline and candidate on the same cases and environment. Use repeated trials for nondeterministic tasks. Compare paired results where possible and report confidence intervals or uncertainty rather than overstating small differences.

Track regressions by category. Do not hide a serious safety regression behind an average quality improvement.

## 8. Set release gates

Define gates before running the candidate:

- Zero tolerance for confirmed unauthorized side effects or secret exposure.
- Required minimum task success on critical cases.
- No unacceptable regression in core workflows.
- Bounded latency and cost.
- All critical test failures explained and resolved.
- Human approval for risk acceptance.

If a test is flaky, quarantine it with an owner and reason; do not silently delete it.

## 9. Produce an evaluation report

Include version identifiers, dataset revision, environment, run count, pass/fail counts, metrics, regressions, representative traces, judge calibration, known limitations, and release decision.

A benchmark result describes performance on a defined test set. It does not prove general intelligence, universal safety, or production readiness.

## 10. Protect evaluation data and prevent leakage

- Keep training, prompt-development, validation, and final test sets distinct. Restrict access to held-out cases and record who or what can read them.
- Remove secrets, direct identifiers, and unnecessary personal or customer data before creating fixtures. Use synthetic or consented data for sensitive workflows.
- Track dataset origin, collection date, permitted use, transformation steps, retention, and deletion requirements.
- Detect duplicate and near-duplicate cases across splits. Prevent benchmark answers, expected outputs, and judge rubrics from leaking into agent context.
- Version datasets immutably. A changed case, expected result, or scoring rule creates a new dataset revision.
- If a case becomes public or is used repeatedly for prompt tuning, move it out of the held-out set and replace it with a fresh case.

## 11. Plan runs and interpret uncertainty

Choose the number of cases and repeated trials before comparing candidates. Base the plan on expected effect size, task variability, evaluation cost, and the impact of a wrong release decision.

For each metric:

1. State the unit of analysis: task, conversation, tool call, user, or session.
2. Report numerator, denominator, exclusions, and missing observations.
3. Use paired comparisons when both versions can run against the same cases and fixtures.
4. Report confidence intervals or another suitable uncertainty estimate for important differences.
5. Avoid treating repeated runs of the same case as independent users or independent tasks.
6. Separate statistical uncertainty from practical significance. A tiny measurable gain may not justify added cost or risk.

For rare but severe failures, ordinary average scores are insufficient. Add targeted adversarial cases, boundary tests, and explicit zero-tolerance release gates.

## 12. Validate evaluators and model-based judges

Treat the evaluator as software that can be wrong.

- Test scoring code with known pass, fail, boundary, malformed, and missing-evidence examples.
- Check that judges follow the rubric on a calibration set reviewed by humans.
- Measure judge agreement with human reviewers and inspect disagreements by category.
- Test for position, verbosity, style, and model-identity bias. Randomize candidate order where practical.
- Require a judge to abstain when evidence is insufficient.
- Keep judge prompts and versions fixed during a comparison, or record the change as an evaluation-method change.
- Never use a model judge as the sole check for authorization, secret exposure, destructive side effects, or other objectively testable safety requirements.

## 13. Add production feedback without corrupting the benchmark

Use production signals to discover new failure modes, not to silently rewrite the benchmark.

- Sample real workflows under an approved privacy and retention policy; minimize or redact user content.
- Track task completion, user corrections, retries, escalation, tool failures, and confirmed safety incidents.
- Distinguish user dissatisfaction from verified task failure, and investigate both.
- Convert confirmed incidents and recurring failure patterns into sanitized regression cases.
- Keep online experiments behind controlled rollout, monitoring, and rollback gates.
- Do not infer causal improvement from before-and-after metrics when traffic, users, model versions, or task mix changed materially.

## 14. Preserve the evaluation record

Store the evaluation plan, case and dataset revisions, model and prompt identifiers, tool schemas, dependency versions, environment, random seeds where supported, raw scores, traces, judge version, analysis code, and release decision.

Restrict access to raw traces and sensitive fixtures. Retain only what is necessary for reproducibility and approved audit requirements. A report without enough artifacts to reproduce its key claims is an assertion, not reliable evidence.
