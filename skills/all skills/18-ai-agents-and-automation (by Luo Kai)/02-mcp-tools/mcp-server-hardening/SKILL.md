---
name: mcp-server-hardening
description: Designs and reviews secure Model Context Protocol servers, tools, resources, and transports. Use when building, integrating, deploying, or auditing MCP servers, tool authorization, authentication, input validation, output handling, and audit logging.
metadata:
  author: Luo Kai
  provenance: original
  version: "1.1.0"
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

MCP authorization is optional at the protocol level. For HTTP-based MCP deployments that implement authorization, follow the current MCP authorization specification. The specification says stdio implementations should not use the HTTP authorization flow; they should obtain credentials from the environment and protect them according to the local runtime's trust model. Alternative transports must use the security model appropriate to that transport.

For HTTP-based authorization, implement and verify these requirements against the current specification:

- The MCP server MUST expose OAuth 2.0 Protected Resource Metadata (RFC 9728), and the client MUST use it for authorization-server discovery. The server MUST advertise the metadata location through a `WWW-Authenticate` `resource_metadata` parameter on an authorization challenge or through the applicable well-known URI.
- The authorization server MUST provide OAuth 2.0 Authorization Server Metadata (RFC 8414) or OpenID Connect Discovery. Clients must support both discovery mechanisms and validate issuer identity and metadata origins.
- The client MUST include the canonical MCP server URI as the OAuth `resource` parameter in both authorization and token requests, following RFC 8707. The server MUST validate that presented tokens were issued for that MCP resource/audience.
- Clients MUST use authorization code flow with PKCE, use `S256` when capable, and verify PKCE support through authorization-server metadata before proceeding. Do not embed client secrets in distributed public clients.
- Authorization-server endpoints MUST use HTTPS. Redirect URIs must be localhost or HTTPS and must be validated exactly; reject open redirects and untrusted callback destinations.
- Send access tokens in the `Authorization: Bearer` header on every HTTP request. Never put access tokens in query strings. Store tokens securely; public-client refresh tokens must use the rotation behavior required by the applicable specification.
- The MCP server MUST accept only tokens issued by the authorization server for that MCP resource. It MUST NOT accept or transit arbitrary tokens, including tokens intended for downstream services.
- If the MCP server calls an upstream API, obtain a separate credential issued for that API or use a supported token-exchange/delegation design. Never forward the MCP access token as a downstream bearer token.
- Keep authorization state, PKCE verifiers, and tokens protected against cross-session mix-ups, replay, logging, and leakage.

Do not invent an authentication flow when the transport or client does not support it. Document the actual trust model and enforce it server-side. Re-check the normative requirements when the MCP specification changes.

Normative references: [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) and [MCP Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations).

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

Validate at the boundary and again immediately before sensitive execution. A validated request can become unsafe if its target, identity, or authorization context changes later.

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

For local HTTP services, validate the Host and Origin headers against an explicit policy, reject unexpected origins, and defend against DNS rebinding. Do not assume that binding to localhost alone is a complete browser-origin security boundary.

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

## 10. Secure protocol lifecycle and session state

Treat protocol initialization, capability negotiation, session creation, resumption, and termination as security-relevant transitions.

- Validate protocol versions and negotiated capabilities. Do not assume a client supports a feature merely because the server implements it.
- Keep session identifiers unpredictable, scoped, and protected from disclosure. Bind session state to the authenticated principal and tenant.
- Re-authenticate or re-authorize when identity, tenant, credential, or privilege context changes.
- Expire abandoned sessions and bound the number and lifetime of active sessions.
- Reject replayed, stale, malformed, or out-of-order messages where the transport or protocol requires ordering and freshness.
- Handle cancellation and disconnects without leaving background jobs or privileged operations running unintentionally.
- Do not treat a session ID as a bearer credential unless the protocol explicitly defines it as one and it is protected accordingly.

## 11. Review every exposed MCP capability

Maintain an inventory of tools, resources, resource templates, prompts, and any server-initiated or client-mediated capability exposed by the implementation.

For each capability, record its purpose, input and output schema, required identity, authorization rule, data classification, downstream systems, side effects, rate limits, and failure behavior.

- Keep descriptions accurate and avoid broad claims such as “full access” when the server enforces narrower operations.
- Apply access checks to resource templates after URI expansion and before data retrieval.
- Ensure pagination cannot cross tenant or authorization boundaries.
- Treat prompt templates and server-provided content as untrusted data when they incorporate external records.
- If the server supports sampling, elicitation, roots, or other client-mediated capabilities, define which party initiates the request, what data is exposed, and what consent or policy checks apply.
- Disable capabilities that are not required by the deployment.

## 12. Harden downstream integrations and side effects

The MCP server is a policy enforcement point, not a trusted tunnel to every downstream system.

- Use separate credentials and scopes for each downstream service. Never reuse the caller's MCP access token as a downstream bearer token.
- Enforce destination allowlists for outbound requests and prevent user-controlled arguments from selecting arbitrary hosts or protocols.
- Set explicit timeouts, response-size limits, retry ceilings, and idempotency behavior.
- For writes, record the intended target and operation before execution, then verify the resulting state using an authorized read-back where practical.
- Make destructive and externally visible actions explicit. Require an approval signal that is bound to the exact action and target, not a generic “approved” flag.
- Ensure retries cannot duplicate payments, messages, deployments, or other non-idempotent effects.
- Return partial-failure states honestly. Do not report success when the downstream result is unknown.

## 13. Maintain security regression coverage

Keep repeatable tests for authentication and authorization boundaries, tenant isolation, schema validation, output redaction, SSRF defenses, origin checks, session handling, cancellation, and high-impact side effects.

Add a regression test for each confirmed security defect. Run negative tests with synthetic identities and controlled destinations. Review coverage whenever a new tool, resource, transport, or downstream integration is added.

A passing test suite is evidence for the tested cases and revision, not proof that the server is universally secure.
