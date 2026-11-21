---
name: database-operations-and-dr
description: Use when planning, reviewing, or executing database operations work such as backup and restore design, disaster recovery runbooks, failover and replication checks, RPO/RTO validation, schema migration safety, or database incident recovery.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Database Operations And Dr

## Purpose and boundaries

This skill guides database operations (DBOps) and disaster recovery (DR) work for relational and managed database services. It covers: backup and restore design, point-in-time recovery, replication and failover topology, DR runbooks and drills, RPO/RTO measurement, migration rollout safety, and recovery from data-loss or corruption incidents.

It does not cover: application query tuning beyond recovery impact, database engine internals development, data warehouse modeling, or security policy authoring (refer those to the relevant owners). Do not execute production changes from this skill without the approvals defined in Decision gates.

## Inputs and assumptions

Collect before acting:

- Engine, version, and hosting model (self-managed, managed service, or hybrid). Treat exact feature availability as version-sensitive and verify against current vendor documentation.
- Data classification and business-declared RPO (maximum tolerable data loss) and RTO (maximum tolerable downtime) per system. If absent, stop and request them; do not assume.
- Current backup policy, retention period, storage location and region, encryption status, and last successful restore test date.
- Replication topology, failover mechanism, and whether failover is automatic or manual.
- Change window, rollback owner, and on-call contact for the affected service.
- Dependencies: connected applications, batch jobs, replicas consumers, and external integrations that may be affected by writes, failover, or restores.

Assume nothing about backup success. A backup that has not been restored is unverified.

## Operating workflow

1. **Scope the request.** Name the system, environment, data set, and objective (design, drill, migration, incident). Record the RPO and RTO targets being tested.
2. **Inventory protection.** List each backup mechanism (full, incremental, logical export, log archive, snapshot), its schedule, retention, and storage destination. Flag any single-region or single-account dependency.
3. **Map recovery paths.** For each failure mode (instance loss, zone loss, region loss, logical corruption, accidental delete, bad migration), write the recovery path, the data it recovers, and the expected time. Identify the path that needs the least time and the one that needs the most.
4. **Compute achievable RPO/RTO.** RPO is bounded by the newest recoverable log position, not the last snapshot time. RTO includes detection, decision, provisioning, restore, replay, validation, and application reconnection. Show each component with a measured or estimated value and its source.
5. **Design or update the runbook.** Each step needs an owner, a command or console action reference, an expected result, and a stop condition. Keep steps idempotent where possible.
6. **Rehearse.** Restore into an isolated environment, never over production. Time each stage. Compare actual results against targets.
7. **Record evidence and gaps.** Produce the deliverable contract output and open tracked actions for every gap.

For migrations: run expand-then-contract changes; take a verified backup or snapshot immediately before the change; rehearse on a recent restored copy; define the rollback (schema reversal or forward-fix) before execution.

## Decision gates

Stop and obtain explicit written approval from the data owner and on-call lead before any of the following:

- Restoring over, overwriting, or dropping any live database, table, or schema.
- Promoting a replica, forcing failover, or changing replication direction.
- Deleting backups, snapshots, log archives, or retention policies, or shortening retention.
- Running destructive or non-reversible DDL or DML (DROP, TRUNCATE, bulk DELETE/UPDATE without a verified rollback).
- Changing encryption keys, storage locations, or cross-region/cross-account replication (external-impacting).
- Any action that exposes data outside its authorized boundary, including copying production data to a lower environment.
- Any action during an active incident that is not already in the approved runbook.

Proceed without approval only for read-only inspection, restore tests into isolated throwaway environments with no connection to production, and dry-run validation.

## Verification and evidence

A recovery claim is valid only with evidence:

- Restore completed and integrity checks passed (engine consistency checks, row counts or checksums against a known reference for key tables, application smoke test passed against restored data).
- Measured restore duration and recovery point timestamp recorded, compared to RPO and RTO targets. Pass requires measured values at or below targets, with a margin stated.
- Backup jobs show success for the last N scheduled runs, and at least one restore test occurred within the agreed interval (set by the owner; commonly quarterly or per major change).
- Replication lag measured at the time of the check, and failover tested with observed promotion time and no unexpected data divergence.
- Retention and immutability settings confirmed against the stated policy, with the screenshot or configuration export as evidence.

Do not state compliance, durability, or availability guarantees. Describe only what was measured.

## Failure handling

- **Restore fails integrity check:** halt; do not serve the restored copy. Try the previous backup point, record the corruption signature, and escalate.
- **Restore exceeds RTO:** report the measured bottleneck (transfer, replay, index rebuild, provisioning) and propose a specific reduction; do not declare the test passed.
- **Backup job failing silently (no success record):** treat as unprotected from the last success timestamp; alert and compute the exposure window.
- **Failover produces divergence:** freeze writes if safe, capture both positions, and escalate. Do not reconcile manually without data owner approval.
- **Unexpected production impact during a drill:** abort the drill, restore original routing, and file an incident.
- **Missing inputs (RPO, RTO, owner):** report the gap and the plan's limits; do not fill values with defaults.

## Deliverable contract

Every output must contain, in this order:

1. System, environment, and scope statement.
2. Target RPO and RTO with their source.
3. Protection inventory table: mechanism, schedule, retention, location, last verified restore date.
4. Recovery path table: failure mode, procedure reference, measured or estimated RPO, RTO, owner.
5. Test results: measured values against targets, pass/fail per criterion, with evidence references.
6. Approval record for any gated action taken or proposed.
7. Gap register: each gap with severity, owner, and due date.
8. Version-sensitive items flagged for verification against current official documentation.

What not to do: do not restore over production as a test; do not treat snapshot existence as recoverability; do not delete backups to free space without approval; do not copy production data to non-production without approval and masking; do not claim targets were met from estimates alone; do not invent command flags or feature names.