---
title: Do not rely on ORDER BY in materialized views for ongoing ordering
impact: MEDIUM
impactDescription: ORDER BY in a materialized view is silently ignored for streaming results — downstream consumers relying on it receive unordered data
tags: materialized-view, order-by, ordering, streaming, serving
---

## Do not rely on ORDER BY in materialized views for ongoing ordering

`ORDER BY` in a `CREATE MATERIALIZED VIEW` statement affects the physical storage clustering of the MV — RisingWave will issue a NOTICE: "ORDER BY on creating materialized view is not supported by streaming mode." It does **not** guarantee that query results will be returned in that order. Downstream consumers relying on it will see unordered data.

**Incorrect (ORDER BY in MV — no ordering guarantee on query results):**
```sql
-- Bad: RisingWave issues a NOTICE and ORDER BY only influences storage layout, not result order
CREATE MATERIALIZED VIEW recent_orders AS
SELECT order_id, customer_id, total, created_at
FROM orders
ORDER BY created_at DESC;
-- Querying recent_orders returns rows in arbitrary order
```

**Correct (order at query time or use a sink):**
```sql
-- Good: create the MV without ORDER BY
CREATE MATERIALIZED VIEW recent_orders AS
SELECT order_id, customer_id, total, created_at
FROM orders;

-- Apply ORDER BY at query time when serving
SELECT order_id, customer_id, total, created_at
FROM recent_orders
ORDER BY created_at DESC
LIMIT 100;
```

**If ordered output to a sink is required**, use a windowed MV with `EMIT ON WINDOW CLOSE` and sort in the downstream consumer, or use a batch export job.

Reference: [CREATE MATERIALIZED VIEW](https://docs.risingwave.com/sql/commands/sql-create-mv)
