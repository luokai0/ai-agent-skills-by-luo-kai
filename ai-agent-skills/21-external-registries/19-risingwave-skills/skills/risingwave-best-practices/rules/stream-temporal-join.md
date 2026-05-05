---
title: Use FOR SYSTEM_TIME AS OF when joining a stream with a CDC table
impact: HIGH
impactDescription: A regular JOIN between a stream and a CDC table produces incorrect results when the CDC table is updated — temporal join ensures point-in-time correctness
tags: temporal-join, cdc, for-system-time-as-of, join, streaming, correctness
---

## Use FOR SYSTEM_TIME AS OF when joining a stream with a CDC table

When joining a streaming source with a CDC-backed table (e.g., enriching events with user profiles), a regular `JOIN` uses the current state of the CDC table. If the CDC table is updated after the event arrived, the join result changes retroactively. `FOR SYSTEM_TIME AS OF` performs a temporal join — it looks up the CDC table at the event's processing time, producing stable, point-in-time-correct results.

**Incorrect (regular JOIN — results change when CDC table is updated):**
```sql
-- Bad: if a customer's tier changes, past order enrichments are retroactively updated
CREATE MATERIALIZED VIEW enriched_orders AS
SELECT
    o.order_id,
    o.total,
    c.tier AS customer_tier
FROM orders o
JOIN customers c ON o.customer_id = c.id;
-- When customers.tier changes, this MV updates ALL historical rows for that customer
```

**Correct (temporal join — point-in-time lookup):**
```sql
-- Good: looks up the customer record as of when the order was processed
CREATE MATERIALIZED VIEW enriched_orders AS
SELECT
    o.order_id,
    o.total,
    c.tier AS customer_tier
FROM orders o
JOIN customers FOR SYSTEM_TIME AS OF PROCTIME() c
ON o.customer_id = c.id;
-- Historical enrichments are frozen at the time of processing
```

**When to use temporal join:**
- Enriching a stream with reference data that changes over time (user profiles, product catalog, exchange rates)
- When historical correctness matters and retroactive updates are undesirable

**When regular JOIN is appropriate:**
- Both sides are CDC tables (static-ish data joined with static-ish data)
- You explicitly want the MV to reflect the latest state of both sides

Reference: [Temporal joins](https://docs.risingwave.com/processing/sql/joins#temporal-join)
