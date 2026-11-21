---
name: mcp-server-hardening
description: Use when reviewing, securing, or deploying a Model Context Protocol (MCP) server that exposes tools, resources, or prompts to AI agents, and you need to reduce its attack surface, constrain tool permissions, and verify its behavior before or after exposure.
author: Luo Kai
provenance: original
version: 1.0.0
---

# MCP Server Hardening

## Purpose and boundaries

This skill covers hardening an MCP server: the process that receives tool calls, resource reads, and prompt requests from an AI client and executes them against local or remote systems. It applies to servers you own or are authorized to modify and test.

In scope: tool inventory and risk classification, input validation, authorization and scoping, transport and authentication review, secret handling, output sanitization against prompt injection, logging, and pre-release verification.

Out of scope: building a new MCP server from scratch, choosing an agent framework, general application pentesting of systems the server calls (only the server's exposure to them), and legal or compliance certification. Do not present hardening as a compliance guarantee.

## Inputs and assumptions

Collect before starting:

1. Server source or configuration, with the exact commit or version under review.
2. Full tool, resource, and prompt list, including descriptions and input schemas.
3. Each backend the server touches (filesystem paths, databases, SaaS APIs, shells, cloud accounts) and the credentials it holds.
4. Transport in use (for example stdio for local subprocess, or a network transport) and how clients authenticate.
5. Intended clients and the users on whose behalf calls run.
6. Deployment environment: developer workstation, shared host, container, or cloud.

Assumptions to state explicitly if information is missing: treat the model as untrusted input producer; treat tool descriptions and returned content as potentially adversarial; assume any credential the server holds can be misused if a tool is coerced.

Verify SDK-specific behavior, transport options, and authentication features against the current official MCP specification and the SDK's documentation for the version in use. Do not rely on memory for those details.

## Operating workflow

1. **Inventory.** List every tool, resource, and prompt. For each, record: side effects (read, write, delete, execute, network egress), backend, credential used, and whether it accepts free-form strings that reach a shell, query, path, or URL.
2. **Classify risk.** Assign each item one level:
   - Low: read-only, bounded, non-sensitive data.
   - Medium: read of sensitive data or write within a bounded scope.
   - High: destructive, financial, credential-bearing, arbitrary code or command execution, outbound network to arbitrary hosts.
3. **Reduce surface.** Remove tools not needed by any stated use case. Split multi-purpose tools (for example a generic "run query" tool) into narrow operations. Replace arbitrary-command tools with fixed operations where possible.
4. **Validate inputs.** Enforce schemas server-side, not only in the descriptor. Reject unknown fields. Constrain strings by length and pattern. Resolve filesystem paths to canonical form and confirm they fall under an allowlisted root after symlink resolution. Use parameterized queries. Never concatenate input into shell strings; pass argument arrays. Allowlist outbound hosts and schemes.
5. **Scope authorization.** Each tool call must run with the least privilege for the requesting user and task. Separate read and write credentials. Prefer short-lived, narrowly scoped tokens. Do not let a single server-wide admin credential back all tools.
6. **Harden transport and identity.** For network transports, require authentication on every request, bind to specific interfaces, enforce TLS where the transport supports it, and validate Origin or equivalent headers where the spec or SDK requires it. Confirm current requirements in official documentation.
7. **Protect secrets.** Load credentials from a secret store or environment injection, never from tool arguments or returned content. Redact secrets from logs, errors, and tool outputs.
8. **Sanitize outputs.** Treat returned content as data. Truncate large outputs, strip control characters, and label untrusted fetched content so the client is not instructed by it. Do not return raw stack traces or credentials in errors.
9. **Log for audit.** Record tool name, caller identity, arguments with sensitive fields masked, result status, and timestamp. Do not log secret values or full file contents by default.
10. **Verify** (see Verification section).

## Decision gates

Stop and obtain explicit user approval before proceeding if any of the following applies:

- A High-risk tool is to be enabled, widened, or left exposed to untrusted clients.
- A change would delete, overwrite, or rotate production data, credentials, or configuration.
- A step would contact external services with real data, send messages, make payments, or alter shared infrastructure.
- Testing would run against production backends rather than a sandbox or fixture.
- A credential with broader scope than required is needed to complete the work.
- Hardening would remove a tool that users currently depend on.

Proceed without approval only for read-only analysis, local code edits in a working copy, and tests against local fixtures with synthetic data.

## Verification and evidence

Provide evidence for each claim:

- Schema tests: send malformed, oversized, and unknown-field inputs to every tool; expect rejection with no backend call. Target: 100% of crafted invalid inputs rejected, verified by backend call counters.
- Path tests: attempt traversal (`../`), absolute paths outside root, and symlinks pointing outside root; expect denial.
- Injection tests: include instruction-like text in fixture data returned by read tools; confirm it is labeled and that no write or High-risk tool fires without the gate defined above.
- Permission tests: call each tool with a low-privilege identity; confirm denial where expected.
- Secret tests: grep logs and error outputs from test runs for known canary secrets; expect zero matches.
- Transport tests: confirm unauthenticated requests fail on network transports.
- Inventory diff: compare the tool list before and after hardening and record every removed or narrowed item with justification.

Report results as counts (passed/failed per test class) with the commit hash and SDK version. Mark any version-dependent behavior as "verify against current docs" if you did not confirm it in this session.

## Failure handling

- If a validation test passes an input that reaches a backend, treat it as a blocking defect. Fix, then rerun the full class of tests, not only the failing case.
- If a required credential cannot be scoped down, stop and escalate; do not proceed with a broader credential silently.
- If documentation for the transport or auth feature is unavailable or ambiguous, record the gap and do not assume behavior.
- If removing a tool breaks a known workflow, restore it behind a gate rather than deleting the workflow silently.
- If a secret is found in logs or history, stop, report, and request approval for rotation. Do not rotate or delete logs without approval.

## Deliverable contract

Produce:

1. Tool inventory table: name, description, side effects, backend, credential, risk level, action taken.
2. Change list with file paths and rationale for each change.
3. Test results by class, with commands used, counts, commit hash, and SDK version.
4. Open items: unverified version-specific behaviors, pending approvals, residual risks ranked by severity.
5. Operator notes: required environment variables or secret references (names only, never values), and rollback steps.

Do not include: secret values, claims of compliance or certification, invented flags or API names, or benchmark figures not produced by your own tests.