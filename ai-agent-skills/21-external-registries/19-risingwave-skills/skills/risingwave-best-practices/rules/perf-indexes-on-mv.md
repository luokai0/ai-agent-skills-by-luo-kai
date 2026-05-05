---
title: Create indexes on materialized view columns used in point lookups
impact: MEDIUM
impactDescription: Full table scans on MVs with millions of rows add 10-100ms per query; indexes reduce point lookups to sub-millisecond
tags: performance, index, materialized-view, query, serving, latency
---

## Create indexes on materialized view columns used in point lookups

RisingWave materializes query results as a serving layer. When application code queries an MV using `WHERE customer_id = ?` or joins on a column, RisingWave performs a full scan unless an index exists on that column. For large MVs serving real-time application queries, this causes unnecessary latency.

**Incorrect (no index — full scan on MV):**
```sql
-- MV stores one row per customer
CREATE MATERIALIZED VIEW customer_stats AS
SELECT
    customer_id,
    COUNT(*)        AS order_count,
    SUM(total)      AS lifetime_value,
    MAX(created_at) AS last_order_at
FROM orders
GROUP BY customer_id;

-- Application query: full scan on every lookup
SELECT * FROM customer_stats WHERE customer_id = 12345;
-- Scans all rows to find customer 12345
```

**Correct (index on lookup column):**
```sql
CREATE MATERIALIZED VIEW customer_stats AS
SELECT
    customer_id,
    COUNT(*)        AS order_count,
    SUM(total)      AS lifetime_value,
    MAX(created_at) AS last_order_at
FROM orders
GROUP BY customer_id;

-- Create index on the serving column
CREATE INDEX idx_customer_stats_customer_id ON customer_stats (customer_id);

-- Now point lookup is O(log n) instead of O(n)
SELECT * FROM customer_stats WHERE customer_id = 12345;
```

**When indexes help most:**
- Application-facing MVs serving point lookups (`WHERE id = ?`)
- MVs used as the "right side" of a JOIN in another query
- High-QPS serving patterns (100+ queries/second to same MV)

**When indexes are NOT needed:**
- MVs read by sinks only (no direct queries)
- MVs queried with full scans intentionally (analytics dashboards)
- Small MVs (< 100k rows) where full scan is fast enough

**Verify index usage:**
```sql
EXPLAIN SELECT * FROM customer_stats WHERE customer_id = 12345;
-- Look for scan_ranges: [customer_id = ...] in the output — indicates index lookup
-- Without index: BatchScan with no scan_ranges (full table scan)
```

Reference: [CREATE INDEX](https://docs.risingwave.com/sql/commands/sql-create-index)
