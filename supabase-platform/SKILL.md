---
name: supabase-platform
description: Use when designing, provisioning, migrating, securing, or troubleshooting a Supabase project that combines Postgres schemas, row-level security, auth-linked tables, Storage buckets, or Realtime and Edge Function integrations.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Supabase Platform

## Purpose and boundaries

This skill guides work on a Supabase project's data and storage layer: Postgres schema and migrations, row-level security (RLS), Storage buckets and object policies, auth-linked user data, and the supporting Realtime and Edge Function touchpoints where they affect data access.

In scope: schema design, RLS policy authoring and review, Storage bucket configuration, migration sequencing, key and role hygiene, access-pattern verification, and diagnosing permission or data-access failures.

Out of scope: general Postgres tuning beyond what a Supabase project exposes, frontend client implementation, billing and plan decisions, and any claim about certifications or regulatory compliance. Those require separate review.

## Inputs and assumptions

Before acting, confirm:

1. Target environment (local, staging, production) and the project reference the user intends to change.
2. Current schema source of truth: migration files, dashboard-edited state, or both. Drift between them is a primary failure cause.
3. Access model: which roles call the database (anon, authenticated, service role, direct connections) and which tables hold per-user data.
4. Storage intent: public versus private buckets, expected file sizes, MIME types, and who uploads and reads.
5. Current Supabase CLI and documentation version. Treat exact CLI commands, dashboard labels, and feature availability as version-sensitive; verify them against current official Supabase documentation before issuing them to the user.

If any input is missing and it changes the outcome, ask. Do not assume production.

## Operating workflow

1. **Snapshot current state.** Capture the existing schema, policies, grants, and bucket settings. Record them before any edit.
2. **Map access paths.** For each table and bucket, list every role and operation (select, insert, update, delete, upload, download) that must succeed, and every one that must fail.
3. **Draft changes as migrations.** Express schema, RLS, grants, and bucket configuration as ordered, idempotent migration files. Avoid editing production through the dashboard alone.
4. **Enable RLS with policies in the same migration.** A table with RLS enabled and no policies denies all non-owner access; create policies deliberately, not after the fact.
5. **Scope policies to the authenticated subject.** Compare ownership columns against the authenticated user identifier obtained from the auth context. Index columns referenced by policies.
6. **Validate locally.** Apply migrations to a local or branch database, then run the access matrix from step 2 using each role.
7. **Review diffs.** Confirm that the only changes are the intended ones.
8. **Stage, then promote.** Apply to staging, run the same matrix, then request approval before production.

## Decision gates

Stop and obtain explicit user approval before:

- Dropping, truncating, or renaming tables, columns, policies, buckets, or schemas.
- Running any data-modifying statement against a non-local database.
- Making a bucket public, or loosening any policy so that anon or unauthenticated access expands.
- Rotating or revealing keys, JWT secrets, or database passwords.
- Changing auth provider settings, email templates, or redirect URLs, which affect external users.
- Deleting Storage objects or altering object retention.
- Any operation that cannot be reversed by a down migration or restore.

Proceed without a gate for read-only inspection, writing new migration files, and local validation.

Use the service role key only in trusted server contexts. Never place it in client code, logs, or chat output.

## Verification and evidence

Quality checks are measurable:

- **Access matrix pass rate:** 100% of expected allow and deny outcomes match across every role and operation listed in step 2. Record results as a table: role, operation, target, expected, actual.
- **RLS coverage:** every table in exposed schemas has RLS enabled unless a written justification exists. Query the catalog for tables where row security is off and confirm each exception.
- **Policy completeness:** each operation on each RLS table has an explicit policy or a documented reason for denial.
- **Index check:** every column used in a policy predicate has a supporting index, verified with an execution plan on a representative row count.
- **Storage check:** upload of a disallowed MIME type or oversized file is rejected; download of another user's private object is denied.
- **Migration idempotency:** applying the migration set twice to a fresh database yields an identical schema dump.

Attach evidence (query output, plan excerpts, matrix table) to every completed change.

## Failure handling

- **Permission denied on a query that should succeed:** check the role in use, whether RLS is enabled, whether a matching policy exists for that command, and whether the policy expression evaluates true for the test user. Do not respond by adding a broad `using (true)` policy.
- **Empty results instead of errors:** RLS silently filters rows. Compare results against an elevated context in staging only.
- **Migration drift:** when the dashboard state differs from migration files, stop, capture both, and ask the user which is authoritative. Do not overwrite silently.
- **Failed migration partway:** do not re-run blindly. Inspect applied state, write a corrective migration, and gate it.
- **Storage upload failures:** inspect bucket policy, object path, and MIME configuration before changing anything.

## Deliverable contract

Every deliverable includes:

1. Summary of intended change and affected environments.
2. Migration files or SQL, in apply order, with a matching down or rollback path where feasible.
3. Access matrix with actual results.
4. Explicit list of gated actions requiring approval, and the status of each.
5. Version-sensitive items flagged for verification against current official Supabase documentation.
6. Residual risks and anything not tested.

Do not state that a configuration is secure, compliant, or audit-ready. State only what the matrix and catalog checks demonstrated.