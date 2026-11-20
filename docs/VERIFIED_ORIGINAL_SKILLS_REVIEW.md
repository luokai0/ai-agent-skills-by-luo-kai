# Verified Original Skills Review

**Review date:** 2026-11-20  
**Scope:** The six skills whose frontmatter explicitly identifies Luo Kai as author and marks provenance as original.  
**Result:** No safe consolidation was identified among these six. Keep them separate. All six have now received substantive capability updates and are at version 1.1.0.

## Reviewed skills

| Skill | Version | Primary responsibility | Decision |
|---|---:|---|---|
| [MCP Server Hardening](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/02-mcp-tools/mcp-server-hardening/SKILL.md) | 1.1.0 | Secure MCP servers, tools, resources, transports, authentication, authorization, session lifecycle, and downstream side effects | Keep separate |
| [Agent Observability](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/16-other-agents/agent-observability/SKILL.md) | 1.1.0 | Traces, structured events, runtime quality, latency, cost, privacy-aware telemetry, SLOs, and incident operations | Keep separate |
| [Skill Supply Chain Audit](../ai-agent-skills/06-security-and-auth%20(by%20Luo%20Kai)/05-devsecops/skill-supply-chain-audit/SKILL.md) | 1.1.0 | Pre-install review of provenance, instructions, scripts, dependencies, artifact integrity, permissions, and license risks | Keep separate |
| [Agent Evaluation Design](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/16-other-agents/agent-evaluation-design/SKILL.md) | 1.1.0 | Reproducible agent evaluations, data governance, statistical interpretation, judge calibration, regression checks, and release gates | Keep separate |
| [AI-Generated Change Verification](../ai-agent-skills/07-testing-and-quality%20(by%20Luo%20Kai)/10-ai-assisted-quality/ai-generated-change-verification/SKILL.md) | 1.1.0 | Independent verification of agent-produced code/configuration diffs, binary artifacts, migrations, tests, regressions, and external effects | Keep separate |
| [Prompt Injection Defense](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/03-context-engineering/prompt-injection-defense/SKILL.md) | 1.1.0 | Runtime defenses against direct and indirect prompt injection across user input, multimodal content, retrieval, tools, and memory | Keep separate |

## Why they remain separate

- **MCP hardening vs. prompt-injection defense:** server-side identity, authorization, transport, session, and tool execution controls differ from agent-side instruction/data separation and hostile-content handling.
- **Supply-chain audit vs. prompt-injection defense:** pre-install package inspection differs from runtime protection when an agent reads untrusted content.
- **Observability vs. evaluation design:** production traces, SLOs, and operational signals differ from controlled test sets, scoring, and version comparisons.
- **Evaluation design vs. change verification:** measuring an agent's behavior differs from independently validating a particular code or configuration change before merge.
- **Observability vs. change verification:** runtime monitoring does not replace evidence-based review of a proposed change.
- **Supply-chain audit vs. MCP hardening:** evaluating a package before installation differs from enforcing identity, authorization, and runtime controls on an MCP server.

These skills can reference one another in their workflows, but merging them would blur distinct lifecycle stages and weaken task selection. No skill was deleted. The six updates preserve the prior workflows while adding targeted coverage for gaps identified during review.

## Update summary

- **Agent Evaluation Design:** added evaluation-data governance, leakage prevention, run planning, uncertainty interpretation, judge validation, production feedback, and reproducibility records.
- **Skill Supply Chain Audit:** added artifact integrity and build provenance, dependency inventory/SBOM review, installation/update-path checks, risk-tiered review depth, and reassessment triggers.
- **MCP Server Hardening:** added HTTP authorization/OAuth protections, secure session lifecycle, complete capability inventory, downstream integration controls, and security regression coverage.
- **Agent Observability:** added SLI/SLO design, telemetry cardinality and sampling controls, async tracing, telemetry-failure safety, incident runbooks, and data-access review.
- **Prompt Injection Defense:** added deterministic enforcement boundaries, trust-label propagation, multimodal input handling, retrieval isolation, false-positive handling, and attack-matrix testing.
- **AI-Generated Change Verification:** added binary artifact inspection, data migration review, concurrency/failure recovery, negative security testing, evidence hierarchy, CI/release gate verification, and reviewer independence.

## Repository-wide review boundary

The wider overlap audit found 10,478 catalogued skills. Only six currently carry explicit original-provenance metadata. The remaining entries include third-party material and skills whose ownership has not been verified. Similarity alone is not permission to copy, adapt, remove notices, or claim ownership.

For original-only consolidation, first verify provenance. For adapted or third-party material, preserve the applicable rights and notices. Where rights cannot be established, do not redistribute or adapt the material; independently author a replacement from general knowledge and public documentation instead.

---

Copyright (c) 2026 Luo Kai. All rights reserved for original review text.
