---
title: Declare APPEND ONLY for immutable event streams
impact: HIGH
impactDescription: APPEND ONLY enables storage and compute optimizations; RisingWave can skip deletion tracking and use more efficient data structures
tags: schema, append-only, table, performance, immutable, events
---

## Declare APPEND ONLY for immutable event streams

> **Note:** `APPEND ONLY` is currently an experimental feature. RisingWave will issue a NOTICE when you use it. It is functional but the interface may change in future versions.

RisingWave tables default to supporting updates and deletes, which requires tracking row versions and maintaining tombstones in storage. For immutable event data (logs, transactions, sensor readings), declaring `APPEND ONLY` allows RisingWave to skip this overhead, improving throughput and reducing storage.

**Incorrect (mutable table for append-only data):**
```sql
-- Bad: default table supports updates/deletes, adding overhead for immutable data
CREATE TABLE page_views (
    session_id  BIGINT,
    page_url    VARCHAR,
    view_time   TIMESTAMP,
    user_agent  VARCHAR
);
```

**Correct (APPEND ONLY with watermark):**
```sql
-- Good: APPEND ONLY tells RisingWave no UPDATE/DELETE will occur
CREATE TABLE page_views (
    session_id  BIGINT,
    page_url    VARCHAR,
    view_time   TIMESTAMP,
    user_agent  VARCHAR,
    WATERMARK FOR view_time AS view_time - INTERVAL '10' SECOND
) APPEND ONLY;
```

**When to use APPEND ONLY:**
- Event streams (clickstream, logs, metrics, sensor readings)
- Immutable transaction records
- Any data where rows are only ever inserted, never modified

**When NOT to use APPEND ONLY:**
- CDC tables (require UPDATE/DELETE support)
- Reference data that gets updated (user profiles, product catalog)
- Any table where application code may issue UPDATE or DELETE statements

Reference: [CREATE TABLE](https://docs.risingwave.com/sql/commands/sql-create-table)
