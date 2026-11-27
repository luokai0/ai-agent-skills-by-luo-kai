---
name: database-systems-expert
version: 1.0.0
description: Expert-level database systems theory covering relational model, query processing and optimization, transaction management, concurrency control, recovery, and NoSQL systems.
author: luo-kai
tags: [databases, SQL, transactions, ACID, query optimization, NoSQL]
---

# Database Systems Expert

## Before Starting
1. Relational or NoSQL?
2. OLTP or OLAP workload?
3. Theory or implementation focus?

## Core Expertise Areas

### Relational Model
Relations: tables with rows and columns, schema defines types.
Keys: superkey, candidate key, primary key, foreign key.
Relational algebra: select, project, join, union, difference, rename.
Normalization: 1NF, 2NF, 3NF, BCNF — eliminate redundancy and anomalies.
Functional dependencies: X -> Y means X determines Y.

### Query Processing
Query parsing: SQL to parse tree to logical plan.
Query optimization: logical to physical plan, cost-based optimizer.
Join algorithms: nested loop, hash join, sort-merge join.
Index types: B-tree (range queries), hash index (equality), bitmap (low cardinality).
Query plan: EXPLAIN output, seek vs scan, index usage.

### Transaction Management
ACID: atomicity, consistency, isolation, durability.
Isolation levels: read uncommitted, read committed, repeatable read, serializable.
Anomalies: dirty read, non-repeatable read, phantom read.
MVCC: multi-version concurrency control — readers do not block writers.

### Concurrency Control
Two-phase locking: growing phase acquires locks, shrinking releases.
Deadlock: detection via waits-for graph, prevention via ordering.
Optimistic concurrency: read, validate, write — no locks during read.
Timestamp ordering: each transaction gets timestamp, conflicts resolved by order.

### Recovery
Write-ahead logging: log record before data page — guarantee durability.
ARIES algorithm: analysis, redo, undo phases after crash.
Checkpoints: reduce recovery time by limiting log replay.
Shadow paging: copy-on-write alternative to logging.

## Best Practices
- Always analyze query plans before deploying to production
- Choose isolation level based on actual consistency requirements
- Index foreign keys to avoid full table scans on joins
- Monitor long-running transactions and lock waits

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| N+1 query problem | Use joins or eager loading |
| Missing index on join column | Always index foreign keys |
| Using serializable isolation unnecessarily | Profile and choose appropriate level |
| Not handling transaction rollback | Always handle errors and rollback explicitly |

## Related Skills
- postgresql-expert
- distributed-systems-cs-expert
- sql-analytics-expert
