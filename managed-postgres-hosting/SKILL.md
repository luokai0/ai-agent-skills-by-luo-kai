---
name: managed-postgres-hosting
description: Use when selecting, provisioning, configuring, migrating to, or operating PostgreSQL on a managed cloud or vendor service, including instance sizing, high availability, backups and point-in-time recovery, connection pooling, extensions, upgrades, and cost or access-control review.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Managed Postgres Hosting

## Purpose and boundaries

This skill guides an agent through decisions and work for PostgreSQL running on a managed service (a cloud provider's database offering or a vendor platform). The provider operates the host OS, storage, and base engine; the team still owns schema, queries, roles, data retention, and recovery readiness.

In scope: vendor/tier selection, sizing, networking and private access, HA and failover design, backup and restore validation, pooling, parameter tuning within vendor limits, extension availability, major and minor upgrades, migration cutover planning, and cost review.

Out of scope: self-managed Postgres on VMs or Kubernetes operators (use a separate skill), application ORM design, and data warehouse engines.

## Inputs and assumptions

Collect before acting:
- Engine major version currently in use and target version.
- Workload profile: read/write ratio, peak connections, p95 query latency target, data size and monthly growth, largest tables.
- Recovery objectives: RPO and RTO stated in minutes, plus the retention period required by policy.
- Required extensions and whether each is available on the candidate service.
- Network model: public endpoint allowed or not, peering or private link requirements, client locations.
- Data classification of stored data (personal, financial, regulated). Do not assume a compliance certification applies; confirm it from vendor documentation.

If any of these are missing, record the assumption explicitly in the plan and flag it for the approver.

## Operating workflow

1. **Inventory current state.** Capture version, extensions, parameter overrides, connection counts (peak and steady), replication topology, backup schedule, and top 20 queries by total time from existing statistics.
2. **Map requirements to tier.** Compare CPU, memory, storage IOPS and throughput, max connections, and HA options against measured peaks with at least 40% headroom. Use vendor pricing and limits pages, verified on the day of decision.
3. **Design networking.** Prefer private connectivity. Restrict allowed source ranges to known egress points. Enforce TLS with certificate verification for all clients.
4. **Design pooling.** If peak client connections exceed what the instance supports comfortably, place a pooler in transaction mode in front of the database. Note that transaction pooling breaks session-level features (session `SET`, advisory session locks, prepared statements unless the pooler supports them). Verify application compatibility before cutover.
5. **Plan recovery.** Enable automated backups and point-in-time recovery. Document the restore path. Schedule a restore into a separate instance and run row-count and checksum comparisons against a known table set.
6. **Plan migration (if applicable).** Use logical replication or the vendor's managed migration tooling for near-zero-downtime moves; use dump and restore for small databases with an agreed maintenance window. Rehearse on a copy at production size.
7. **Stage and cut over.** Lower DNS TTL in advance, freeze schema changes, confirm replication lag is near zero, switch connection strings through a single config mechanism, and keep the source read-only for a fallback window.
8. **Operate.** Monitor replication lag, bloat, autovacuum activity, connection saturation, storage growth, and slow query rates. Review monthly.

## Decision gates

Stop and obtain explicit approval before:
- Deleting, downsizing, or detaching any instance, replica, backup, or snapshot.
- Changing retention periods in a way that shortens recoverability.
- Making a database publicly reachable or widening an allowlist to broad ranges.
- Performing a major version upgrade or any cutover that redirects production traffic.
- Enabling an extension that requires superuser-equivalent rights or that the vendor marks as restricted.
- Creating or rotating credentials that other systems depend on.
- Incurring recurring spend above the approved budget, or accepting a commitment term.
- Sharing data outside the approved environment, including to vendor support.

Proceed without approval only for read-only inspection, metrics queries, and dry-run plans.

## Verification and evidence

- **Restore test:** a restore completes within the stated RTO, and sampled tables match source row counts and aggregate checksums (for example, a sum over a numeric key plus a count per partition).
- **Failover test:** in a non-production environment, forced failover completes within target time, and the application reconnects without manual intervention. Record observed downtime.
- **Performance:** p95 latency on the top 20 queries is within 10% of baseline after migration, or differences are explained.
- **Capacity:** peak CPU under 70%, connection utilization under 75% of limit, storage projected to remain under 80% for six months.
- **Config drift:** parameters differ from the documented baseline only where justified in the change record.
- **Access:** every role has a named owner; no shared superuser login is used by applications.

Store evidence (command output, metrics screenshots exported as data, restore logs) with the change ticket.

## Failure handling

- **Replication lag grows during migration:** pause non-essential batch writes, check for long-running transactions and large unindexed updates, and do not cut over until lag is stable at near zero for at least 15 minutes.
- **Restore checksum mismatch:** halt, identify the first mismatched table, and check whether source writes occurred after the restore point before assuming corruption.
- **Connection exhaustion:** identify the client pools responsible, reduce pool sizes, and add a pooler before resizing. Resizing is a gated action.
- **Pooler incompatibility:** revert the affected service to direct connections and file the specific feature dependency.
- **Vendor limit reached (IOPS, storage, connections):** report the limit and the observed value; do not work around it by disabling safeguards.
- **Unexpected behavior from documentation:** treat the live service as authoritative and record the discrepancy.

## Deliverable contract

Every engagement returns:
1. A requirements summary with stated assumptions and open questions.
2. A tier and configuration recommendation with the sizing calculation shown.
3. An ordered runbook with rollback steps for each stage.
4. Gate list: each approval required, the requester, and the status.
5. Evidence bundle: restore test results, failover results, performance comparison, and capacity projection.
6. Version-sensitive items list: any vendor limit, parameter name, extension version, or pricing figure that must be re-checked against current official documentation before execution.

## Ultron routing contract

**Choose this skill when:** the database is managed PostgreSQL and the task depends on provider-specific choices or operations: tier/sizing, networking, extensions, pooling, parameters, HA/failover, backup/restore, upgrades, migration cutover, or cost.

**Choose `database-operations-and-dr` when:** the central objective is cross-engine or organization-wide recovery strategy, RPO/RTO design, DR governance, corruption response, or recovery drill acceptance.

**Handoff contract:** receive the required RPO/RTO, data integrity expectations, failover posture, retention, and recovery drill plan. Return the provider's actual backup/PITR limits, restore procedure, failover behavior, extension and version constraints, and measured recovery evidence. Never assume a managed-service backup feature is equivalent to a tested recovery plan.

**Why the boundary exists:** managed PostgreSQL operations require provider-specific expertise, while DR governance must remain consistent across all database platforms.
