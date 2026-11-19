---
name: mcp-server-hardening
description: Designs and reviews secure Model Context Protocol servers, tools, resources, and transports. Use when building, integrating, deploying, or auditing MCP servers, tool authorization, authentication, input validation, output handling, and audit logging.
license: Proprietary. See repository LICENSE
metadata:
  author: Luo Kai
  provenance: original
  version: "1.0.0"
---

# MCP Server Hardening

## Objective

Make every MCP capability explicit, authenticated where required, authorized per caller, bounded in scope, and observable. A tool description is not an access-control system.

## 1. Map the trust boundaries

Document the client, agent runtime, MCP server, downstream service, and data-store boundaries; transport and TLS termination; user, service, and tenant identities; exposed tools and resources; data classifications; and every system each capability can reach.

Draw a data-flow diagram before implementation. Mark where untrusted text becomes a tool argument, query, URL, path, or command.

## 2. Authentication and identity

- Use a supported, standard authentication mechanism appropriate to the transport and deployment.
- Validate issuer, audience, expiry, signature, and intended scope for tokens.
- Do not accept credentials in tool arguments, URLs, prompts, logs, or source files.
- Do not treat a client-supplied user ID or tenant ID as proof of identity.
- Keep service credentials separate from user-delegated credentials.
- Rotate credentials and support revocation.
- Fail closed when identity validation is unavailable.

For local processes, document the operating-system identity and local trust assumptions. For remote services, require TLS and verify the peer.

## 3. Authorize each capability

Create a policy matrix mapping principals to tools, resources, operations, tenants, and data classes.

- Default to deny.
- Authorize every call on the server, not only in the agent's instructions.
- Apply tenant checks to every object lookup and mutation.
- Separate read, write, delete, publish, and administrative capabilities.
- Use narrow scopes and short-lived delegated credentials.
- Require confirmation for destructive, financial, external-publication, or production actions.
- Re-check authorization after resolving aliases, resource URIs, or indirect identifiers.

A hidden or renamed tool is not protected. Tool descriptions must match actual server-side enforcement.

## 4. Validate inputs and constrain execution

- Validate argument types, lengths, formats, enumerations, and required fields against a strict schema.
- Reject unknown fields unless forward compatibility explicitly requires them.
- Normalize paths and URLs before checking policy.
- Prevent path traversal, command injection, SQL injection, template injection, and unsafe deserialization.
- Apply timeouts, payload limits, pagination limits, and concurrency bounds.
- Avoid passing untrusted arguments through a shell. Prefer direct library calls and argument arrays.
- Restrict file operations to explicit workspace roots; resolve symlinks and verify the final target remains inside the allowed root.
- For URL-fetching tools, block loopback, link-local, private, and cloud-metadata destinations unless specifically required and safely constrained. Re-check after DNS resolution and redirects to reduce SSRF risk.

## 5. Treat outputs as untrusted

Tool output may contain prompt injection, forged instructions, hostile markup, or data belonging to another tenant.

- Return data with clear provenance and structured fields.
- Delimit retrieved content as data, not instructions.
- Escape or sanitize content for the consuming format.
- Avoid returning secrets, internal stack traces, access tokens, or unrelated records.
- Enforce response-size limits and redact sensitive fields.
- Never let a tool result expand the caller's permissions.

## 6. Protect the transport and runtime

- Prefer authenticated TLS for remote transports.
- Bind local-only services to loopback unless remote access is explicitly intended.
- Avoid wildcard CORS and broad origin allowlists.
- Apply request-size limits, rate limits, connection limits, and idle timeouts.
- Keep dependencies patched and lock versions.
- Run with a dedicated low-privilege identity and a read-only filesystem where possible.
- Isolate tools that need shell, browser, or filesystem access.
- Do not expose debugging endpoints or development credentials in production.

## 7. Audit and monitor

Log the authenticated principal, tenant, tool name, authorization decision, request ID, timestamp, outcome, latency, and safe error category.

Do not log raw secrets, full authorization headers, private user content, or unredacted tool arguments by default. Use correlation IDs to connect client, server, and downstream events.

Alert on repeated authorization failures, unusual tool-call volume, unexpected destinations, high-risk actions, cross-tenant access attempts, and privilege changes.

## 8. Test the security boundaries

Test missing, expired, malformed, wrong-audience, and revoked credentials; cross-tenant object access; extra fields and oversized values; path traversal, symlinks, SSRF, redirects, and DNS rebinding; prompt injection in tool output; rate limits, timeouts, cancellation, and partial failure; destructive actions without approval; and secret redaction.

Use synthetic identities and data. Never test with production credentials in a public or untrusted environment.

## 9. Release gate

Before deployment, verify that the capability inventory, permission matrix, threat model, tests, dependency review, logging policy, and rollback procedure are complete. Record accepted risks and the exact release revision.

If identity or authorization cannot be established, fail closed. Do not silently fall back to anonymous or administrator access.
