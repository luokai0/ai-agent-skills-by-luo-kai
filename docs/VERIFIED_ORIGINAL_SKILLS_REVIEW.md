# Verified Original Skills Review

**Review date:** 2026-11-20  
**Scope:** The six skills whose frontmatter explicitly identifies Luo Kai as author and marks provenance as original.  
**Result:** No safe consolidation was identified among these six. Keep them separate.

## Reviewed skills

| Skill | Primary responsibility | Decision |
|---|---|---|
| [MCP Server Hardening](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/02-mcp-tools/mcp-server-hardening/SKILL.md) | Secure MCP servers, tools, resources, transports, authentication, authorization, validation, and audit logging | Keep separate |
| [Agent Observability](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/16-other-agents/agent-observability/SKILL.md) | Traces, structured events, runtime quality, latency, cost, privacy-aware logging, and operational debugging | Keep separate |
| [Skill Supply Chain Audit](../ai-agent-skills/06-security-and-auth%20(by%20Luo%20Kai)/05-devsecops/skill-supply-chain-audit/SKILL.md) | Pre-install review of skill provenance, instructions, scripts, dependencies, permissions, and license risks | Keep separate |
| [Agent Evaluation Design](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/16-other-agents/agent-evaluation-design/SKILL.md) | Reproducible agent evaluations, representative test sets, scoring rubrics, regression checks, and release gates | Keep separate |
| [AI-Generated Change Verification](../ai-agent-skills/07-testing-and-quality%20(by%20Luo%20Kai)/10-ai-assisted-quality/ai-generated-change-verification/SKILL.md) | Independent verification of agent-produced code/configuration diffs, requirements, tests, regressions, and external effects | Keep separate |
| [Prompt Injection Defense](../ai-agent-skills/18-ai-agents-and-automation%20(by%20Luo%20Kai)/03-context-engineering/prompt-injection-defense/SKILL.md) | Runtime defenses against direct and indirect prompt injection across user input, documents, web pages, repositories, tools, and memory | Keep separate |

## Why they remain separate

- **MCP hardening vs. prompt-injection defense:** server-side identity, authorization, transport, and tool execution controls differ from agent-side instruction/data separation and hostile-content handling.
- **Supply-chain audit vs. prompt-injection defense:** pre-install package inspection differs from runtime protection when an agent reads untrusted content.
- **Observability vs. evaluation design:** production traces and operational signals differ from controlled test sets, scoring, and version comparisons.
- **Evaluation design vs. change verification:** measuring an agent's behavior differs from independently validating a particular code or configuration change before merge.
- **Observability vs. change verification:** runtime monitoring does not replace evidence-based review of a proposed change.

These skills can reference one another in their workflows, but merging them would blur distinct lifecycle stages and weaken task selection. No skill was deleted or modified during this review.

## Repository-wide review boundary

The wider overlap audit found 10,478 catalogued skills. Only six currently carry explicit original-provenance metadata. The remaining entries include third-party material and skills whose ownership has not been verified. Similarity alone is not permission to copy, adapt, remove notices, or claim ownership.

For original-only consolidation, first verify provenance. For adapted or third-party material, preserve the applicable rights and notices. Where rights cannot be established, do not redistribute or adapt the material; independently author a replacement from general knowledge and public documentation instead.

---

Copyright (c) 2026 Luo Kai. All rights reserved for original review text.
