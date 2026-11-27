---
title: Use BACKGROUND_DDL for creating MVs over large tables
impact: HIGH
impactDescription: Without BACKGROUND_DDL, creating an MV over a 100M+ row table blocks the session for hours; with it, the backfill runs asynchronously
tags: materialized-view, ddl, background-ddl, backfill, performance, large-table
---

## Use BACKGROUND_DDL for creating MVs over large tables

When `CREATE MATERIALIZED VIEW` is executed over a large upstream table or source, RisingWave must backfill all historical data. Without `BACKGROUND_DDL`, this operation blocks the SQL session for the entire duration of the backfill. With `SET BACKGROUND_DDL = true`, the DDL returns immediately and the backfill runs asynchronously.

**Incorrect (blocking DDL on large table):**
```sql
-- Bad: this statement blocks for hours on a 500M-row orders table
CREATE MATERIALIZED VIEW order_stats AS
SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS lifetime_value
FROM orders
GROUP BY customer_id;
-- Session hangs... timeout or lost connection
```

**Correct (non-blocking background DDL):**
```sql
-- Good: DDL returns immediately, backfill runs in background
SET BACKGROUND_DDL = true;

CREATE MATERIALIZED VIEW order_stats AS
SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS lifetime_value
FROM orders
GROUP BY customer_id;
-- Returns immediately: "CREATE MATERIALIZED VIEW"

-- Monitor backfill progress
SELECT ddl_id, ddl_statement, progress
FROM rw_catalog.rw_ddl_progress;

-- Per-fragment progress (more granular)
SELECT *
FROM rw_catalog.rw_fragment_backfill_progress;
```

**When to use:**
- Any MV creation over a table with more than ~10M rows
- Production environments where session timeouts are possible
- When starting a large backfill and continuing other work

**Note:** `SET BACKGROUND_DDL` is session-scoped. The setting resets when the session ends. To limit backfill resource usage:
```sql
-- Throttle backfill to 1000 rows/sec per source
CREATE MATERIALIZED VIEW order_stats
WITH (source_rate_limit = 1000)
AS SELECT ...;
```

Reference: [CREATE MATERIALIZED VIEW](https://docs.risingwave.com/sql/commands/sql-create-mv)
