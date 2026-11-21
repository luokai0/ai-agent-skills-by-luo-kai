---
name: app-data-layer-integration
description: Use when connecting an application to a database or storage backend, adding or changing a data access layer, repository, ORM mapping, connection handling, or migration path, and the work must preserve correctness, transactions, and operational safety.
author: Luo Kai
provenance: original
version: 1.0.0
---

# App Data Layer Integration

## Purpose and boundaries

Use this skill to design, implement, and verify the seam between application code and a persistent store (relational database, document store, key-value cache of record, or object storage). It covers: access-layer structure, connection and pool configuration, query and transaction boundaries, schema-to-model mapping, error translation, and rollout of data-access changes.

Out of scope: choosing a database vendor from scratch, tuning cluster hardware, designing analytics warehouses, and writing business logic unrelated to persistence.

## Inputs and assumptions

Collect before editing:

- Store type, engine name, and exact server version. Record it; do not assume.
- Current access pattern: ORM, query builder, raw SQL, or driver calls.
- Existing transaction semantics and isolation level in use.
- Expected load: reads/writes per second, largest table row counts, p95 latency target.
- Schema ownership: who runs migrations, and whether a migration tool already exists.
- Environments available for testing (local, staging, production-like snapshot).

If any of these is unknown, state the assumption explicitly in the change summary.

## Operating workflow

1. **Map the current surface.** List every module that opens connections, builds queries, or starts transactions. Use search across the codebase, not memory.
2. **Define the boundary.** Place all persistence calls behind repository or data-access interfaces. Business code receives domain objects, never driver rows or ORM entities that leak lazy-loading behavior.
3. **Centralize configuration.** One place sets pool size, timeouts, statement timeouts, and TLS. Read credentials from the secret store, never from source or logs.
4. **Make transactions explicit.** Each unit of work opens and closes one transaction at the service layer. Repositories accept a transaction handle rather than opening their own.
5. **Translate errors.** Map driver errors to domain errors: unique violation, foreign key violation, serialization failure, timeout, connection loss. Retry only idempotent operations and only on transient classes.
6. **Write queries with bound parameters only.** Never concatenate user input into SQL. Keep queries reviewable as text.
7. **Plan the schema change separately.** Additive migrations first (new nullable column, new table), code that writes both shapes, backfill in batches, then switch reads, then remove the old shape in a later release.
8. **Test against a real engine.** Use the same engine family and version as production. In-memory substitutes do not validate SQL semantics.

## Decision gates

- **Gate A: ORM versus raw SQL.** Use the ORM for standard CRUD. Use explicit SQL for multi-table reporting, bulk updates, or queries where the plan matters. Document each raw query with the reason.
- **Gate B: Retry or fail.** Retry only on serialization conflicts and transient connection errors, with bounded attempts and jittered backoff, and only if the whole transaction is re-executed. Otherwise fail fast.
- **Gate C: Migration safety.** If a migration locks a table longer than the agreed window, or rewrites a large table, stop and request a review of the lock strategy and an approved maintenance window.
- **Gate D: Isolation changes.** Changing isolation level or adding locks requires a concurrency test that reproduces the anomaly being addressed.
- **Gate E: Data movement.** Any copy, export, or deletion of production data requires explicit human approval naming the dataset, the destination, and the retention rule.

## Verification and evidence

- Integration tests run against the target engine version and cover: create, read, update, delete, unique constraint violation, rollback on failure, and concurrent update conflict.
- Query plans checked with the engine's explain facility for any query touching tables above the agreed row threshold. Record the plan summary in the change notes.
- Pool behavior verified under load: no connection leak after a 10-minute soak at target concurrency; pool wait time stays under the agreed budget.
- Migration rehearsed on a production-sized snapshot; record duration and lock observations.
- Confirm that no secret, full row payload, or personal data appears in logs at the chosen log level.
- Version-sensitive settings (driver option names, default isolation levels, pool parameters) must be checked against current official documentation for the exact versions in use. Mark any unverified item as unverified.

Do not report performance numbers without a reproducible measurement method and recorded environment.

## Failure handling

- **Connection refused or timeout:** verify credentials source, network path, and TLS settings; do not raise pool size as a first response.
- **Deadlock or serialization error:** capture the statements and lock order; fix ordering in code before adding retries.
- **Migration fails midway:** stop, do not re-run blindly. Confirm the migration tool's recorded state, then apply the documented recovery path. Obtain approval before any manual repair.
- **Test passes locally, fails in staging:** compare engine version, collation, timezone setting, and isolation defaults first.
- **Unexpected data mismatch after rollout:** disable the new read path via the existing flag, preserve evidence, and escalate. Do not write corrective updates without approval.

## Deliverable contract

Deliver:

1. Changed files list with one-line purpose each.
2. Access-layer interface summary: operations exposed, transaction handling, error mapping.
3. Schema change description with the staged migration plan and rollback path.
4. Test results: engine and version, commands run, pass/fail counts, and any skipped checks with reasons.
5. Query plan notes for flagged queries.
6. Open risks and unverified version-specific settings.
7. Explicit list of actions awaiting approval (destructive, irreversible, external, or sensitive).

What not to do:

- Do not open transactions inside repositories that are called from within another transaction.
- Do not catch and swallow database exceptions.
- Do not run destructive DDL (drop, truncate, column removal) in the same release as the code that stops using it.
- Do not invent driver options, pool parameters, or benchmark figures; verify them.
- Do not connect to production data stores for experiments.
- Do not store credentials, connection strings with passwords, or raw personal data in code, fixtures, or logs.