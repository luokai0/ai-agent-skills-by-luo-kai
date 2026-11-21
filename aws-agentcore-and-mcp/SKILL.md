---
name: aws-agentcore-and-mcp
description: Use when designing, building, deploying, or troubleshooting AI agents on AWS AgentCore or connecting agents to tools and data through the Model Context Protocol (MCP), including tool server exposure, auth boundaries, runtime configuration, and agent observability.
author: Luo Kai
provenance: original
version: 1.1.0
---

# AWS AgentCore and MCP

## Purpose and boundaries

This skill guides an agent engineer or cloud engineer through two linked tasks: (1) hosting and operating an agent on AWS AgentCore (runtime, identity, gateway, memory, and observability components), and (2) exposing or consuming tools through MCP servers, whether they run inside AgentCore or elsewhere.

In scope: architecture decisions, tool contract design, IAM and credential scoping for agent tools, deployment checklists, smoke tests, and failure diagnosis.

Out of scope: general model selection or prompt tuning, non-AWS agent platforms, unrelated application code, and any change to production accounts without approval. Do not treat this skill as a source of current API names, CLI flags, SDK versions, quotas, or pricing. Those change; verify them against current AWS and MCP specification documentation before use.

## Inputs and assumptions

Collect these before acting:

- Target account, region, and environment (sandbox, staging, production) with owner name.
- Agent purpose in one sentence, plus the list of tools it may call and the data each tool touches.
- Existing MCP servers, their transport (stdio or HTTP-based), and who operates them.
- Identity model: which users or workloads invoke the agent, and whether actions are taken on their behalf.
- Data classification of inputs, tool outputs, and logs.
- Latency and concurrency targets, stated as numbers.

If any item is missing, record it as an open question. Do not assume production scope, and do not assume that a tool is read-only because its name suggests so.

## Operating workflow

1. **Map the tool surface.** List every tool with: name, purpose, parameters, side effects (read, write, delete, send, spend), data sensitivity, and required credential.
2. **Classify each tool** as read-only, reversible write, or irreversible/external. Only read-only tools may be auto-approved.
3. **Design tool contracts.** Each MCP tool needs a precise description, typed input schema with enumerated values where possible, bounded output size, and structured error responses. Ambiguous descriptions cause wrong tool selection; treat them as code.
4. **Scope credentials per tool.** Give each tool server its own least-privilege role. Never share an administrator role between the agent runtime and tool servers. Prefer short-lived credentials and per-user delegation when actions must reflect the requesting user.
5. **Configure the AgentCore components** the design needs (runtime, identity, gateway, memory, observability). Confirm each component's current capabilities and configuration fields in the official documentation before writing templates.
6. **Add guardrails in the agent loop:** maximum tool calls per task, timeouts per call, and a hard stop on repeated identical calls.
7. **Instrument before launch.** Emit trace IDs, tool name, latency, status, and token counts for each step. Redact parameters that contain personal or secret data.
8. **Run staged verification** (see below), then promote one environment at a time.

## Decision gates

Stop and request explicit human approval before:

- Creating, modifying, or deleting any resource in a production account or any shared network, identity provider, or DNS record.
- Enabling any tool that writes, deletes, sends messages, moves money, or changes access.
- Exposing an MCP server or gateway endpoint to a network beyond the agreed boundary, including public internet access.
- Storing or transmitting personal, regulated, or credential data in agent memory, logs, or prompts.
- Changing IAM trust policies or granting wildcard actions or resources.
- Any action that cannot be rolled back within the agreed recovery window.

Proceed without approval only for: reading documentation, drafting configuration files locally, and running read-only checks in a sandbox account the user has designated.

Criteria for choosing a tool-invocation pattern:
- Use direct tool calls for deterministic, low-risk lookups.
- Use a confirmation step (agent proposes, human approves, then executes) for any write.
- Use a per-user delegated credential when results must respect the requester's permissions; use a service role only when the action is genuinely system-level.

## Verification and evidence

Each change must produce evidence in these categories:

- **Schema check:** every tool's input schema validates against a sample of valid and invalid payloads; invalid payloads return a structured error, not a crash.
- **Permission check:** the tool's role can perform its listed actions and nothing else. Record the policy simulation or access test output.
- **Behavioral check:** a fixed set of at least 20 representative tasks, including 5 adversarial ones (ambiguous requests, injected instructions inside tool output, requests for out-of-scope tools). Record pass rate and every failure.
- **Limit check:** confirm the tool-call cap and timeout trigger correctly by forcing them in a test.
- **Observability check:** a single test task produces a trace with every tool call linked to one trace ID, and no secrets appear in logs.
- **Rollback check:** the deployment can be reverted, and the revert was tested in staging.

Report results with counts and the exact commit or configuration version tested. Do not report "works" without numbers.

## Failure handling

- **Wrong tool selected:** tighten the tool description and add negative guidance ("do not use for X"); re-run the behavioral set. Do not add a catch-all tool.
- **Authorization denied:** check the role trust relationship first, then the resource policy, then the token audience and scope. Do not widen permissions to unblock; propose the minimal additional action and seek approval.
- **Timeouts or loops:** lower the call cap, add idempotency keys to write tools, and inspect repeated parameters in traces.
- **Schema mismatch between client and server:** pin the protocol version both sides support, and verify against the current MCP specification.
- **Unexpected external effect:** stop the agent, disable the tool at the gateway or configuration level, and escalate to the owner with the trace IDs. Do not attempt self-correcting writes.

## Deliverable contract

Every completed engagement delivers:

1. A tool inventory table: name, purpose, side-effect class, credential, approval rule.
2. Architecture summary naming each AgentCore component used and its configuration source.
3. Configuration files or infrastructure definitions, with placeholders replaced by real values supplied by the owner.
4. A verification report with the counts and failures described above.
5. A list of version-sensitive items (SDK versions, API parameters, quotas, supported regions) marked "verify against current official documentation," with the date checked.
6. Open risks and the named approver for each deployment stage.

What not to do: do not grant wildcard permissions, do not expose unauthenticated tool endpoints, do not place secrets in tool descriptions or prompts, do not auto-approve writes, do not promote untested configurations, and do not state performance, cost, or compliance outcomes without measured evidence or an authoritative source.

## Ultron routing contract

**Choose this skill when:** the agent runtime or tool deployment specifically uses AWS AgentCore and needs AWS service architecture, IAM/credential scoping, gateway integration, deployment, operations, or AgentCore-specific failure diagnosis.

**Choose mcp-and-agent-tooling when:** the unresolved problem is the portable MCP protocol and tool layer itself: schemas, resources, prompts, client/server interoperability, and tool result contracts across hosting platforms.

**Handoff contract:** this skill maps the portable MCP capability contract onto AWS AgentCore's gateway/runtime/identity model and returns the AWS resource, policy, deployment, and smoke-test evidence. The MCP skill defines protocol-level behavior; this skill owns AWS-specific integration and version-sensitive service configuration.

**Why the boundary exists:** MCP is a cross-platform protocol; AgentCore is a particular hosting and integration environment. Do not present AWS-specific APIs or assumptions as universal MCP behavior.
