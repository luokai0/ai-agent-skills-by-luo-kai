---
name: graphql-api-design
description: Use when designing, reviewing, or evolving a GraphQL schema, resolver layer, or GraphQL API contract for a backend service, including schema modeling, pagination, error handling, authorization placement, and breaking-change management.
author: Luo Kai
provenance: original
version: 1.0.0
---

# GraphQL API Design

## Purpose and boundaries

Use this skill to produce or review GraphQL schemas and their backend contracts: type modeling, field design, pagination, mutations, error semantics, authorization placement, N+1 prevention, and schema evolution.

In scope: SDL design, resolver responsibilities, DataLoader-style batching, input and mutation design, error modeling, deprecation and evolution policy, and schema checks in CI.

Out of scope: client UI code, database schema migrations, infrastructure sizing, and REST or gRPC design except where a GraphQL field wraps them. Do not use this skill to approve a production schema change without the owning team's review.

## Inputs and assumptions

Collect before designing:
- Consumers: each client application, its primary screens or workflows, and its release cadence.
- Domain entities, their identifiers, ownership boundaries, and existing REST or database shapes.
- Read/write access patterns and expected list sizes.
- Authentication mechanism and the authorization rules per entity.
- Current schema file, if any, and the list of deployed clients that query it.
- Target GraphQL specification and server library. Treat their specific directives, features, and tooling flags as version-sensitive: verify against current official documentation before relying on them.

If any of these are missing, state the assumption explicitly in the deliverable. Do not invent consumer needs.

## Operating workflow

1. **Map the domain.** List entities, relationships, and the queries clients actually run. Model from consumer use cases, not database tables.
2. **Draft types as nouns, operations as verbs.** Use object types for entities, enums for closed sets, and input types for mutation arguments. Prefer `Order.status: OrderStatus` over string fields.
3. **Design identifiers.** Use a single opaque `ID` scalar for global identity. Do not expose internal auto-increment keys as the only identity.
4. **Design connections for every list that can grow.** Use cursor-based connections (`edges`, `node`, `cursor`, `pageInfo`). Plain lists are acceptable only for bounded collections with a documented maximum.
5. **Design mutations as payload-returning operations.** Each mutation takes one input object and returns a payload type containing the changed entity and a `userErrors`-style list (or a typed union, see decision gates).
6. **Place authorization in resolvers or a service layer, never only in the client.** Hide unauthorized fields by returning a defined error, not by omitting fields silently.
7. **Plan batching.** For every object field that loads related data, identify its loader key and batch window. Confirm the resolver does not query per parent item.
8. **Define evolution rules.** Mark fields as deprecated with a reason and replacement before removal. Record the removal date and the consumer sign-off.
9. **Write the contract tests** described under Verification.

## Decision gates

- **Nullable or non-null:** Mark a field non-null only if the server guarantees a value for every object that can be returned. Making a field non-null later is a breaking change for clients that handle null, so default to nullable for fields derived from external services.
- **Expose a field or not:** Expose only fields that at least one named consumer uses or is committed to using. Speculative fields are a schema commitment.
- **Errors as payload fields vs. GraphQL errors:** Use payload-level user errors for validation and business rule failures the client can act on. Reserve top-level GraphQL `errors` for unexpected system failures and authorization failures on whole operations.
- **Union result vs. error list:** Use a union (e.g., `CreateOrderResult = Order | ValidationError`) when the failure shape differs materially from success. Use an error list when a single payload type suffices. Document the choice per mutation.
- **Custom scalars:** Introduce a scalar (e.g., `DateTime`, `Money`) only with a documented serialization format and parsing rule.
- **Breaking change:** Adding a nullable field, optional argument with default, or new enum value that clients can ignore is non-breaking. Removing or renaming fields, changing types, making a nullable field non-null, or changing enum meaning is breaking. Breaking changes require a deprecation cycle and approval from the consuming teams.
- **Depth and complexity limits:** Require a query depth and complexity policy for any public endpoint. Values must be chosen from observed query data, not guessed.

## Verification and evidence

Each deliverable must include:
- **Schema lint** passing against the team's chosen linter, with the rule set named.
- **Schema diff** against the last released schema, classified as breaking or non-breaking, with the diff output attached.
- **N+1 check:** a test or trace showing query count stays constant (or bounded by batch count) as list size grows, for at least the three largest connection fields. Report measured counts, not estimates.
- **Authorization matrix:** a table of entity × role × operation with expected allowed/denied outcome, each backed by a test.
- **Pagination tests:** forward and backward traversal, empty page, last page, and invalid cursor handling.
- **Example operations:** at least one real query per consumer use case, executed against a test environment, with results recorded.

Do not claim performance improvements or compliance properties without measured evidence.

## Failure handling

- If a consumer use case cannot be served without an N+1 pattern, stop and propose a batching or denormalization option with its trade-offs; do not ship the naive resolver.
- If the schema diff shows an unintended breaking change, revert the change and reintroduce it as an additive field with deprecation of the old one.
- If authorization rules are ambiguous for an entity, mark the field as restricted and request a decision from the domain owner. Do not default to allow.
- If the version of the GraphQL specification or server library behaves differently from documented expectations, record the observed behavior and the version, and verify against current official documentation before proceeding.

## Safety and approval controls

Obtain explicit human approval before:
- Removing, renaming, or changing the type of any field or argument in a published schema.
- Deploying a schema change to production or to any environment consumed by external partners.
- Exposing a new field that returns personal, financial, or credential data.
- Changing authorization rules, including loosening them.
- Enabling introspection or disabling depth or complexity limits on a public endpoint.

## Deliverable contract

Return:
1. The SDL for changed or new types, with comments on non-obvious nullability and error decisions.
2. A decision log: each gate applied, the choice made, and the rationale.
3. Schema diff classification (breaking / non-breaking) with the affected consumers.
4. Verification results: lint, N+1 counts, authorization matrix, pagination test outcomes.
5. Open assumptions and items requiring approval, listed explicitly.

Do not include unsupported claims, unverified version-specific behavior presented as fact, or unresolved sample fields.