---
author: luo-kai
name: sql-analytics
description: Expert-level SQL for analytics and business intelligence. Use when writing complex analytical SQL, window functions, CTEs, cohort analysis, funnel queries, time-series analysis, or working with BI tools (Looker, Metabase, Superset). Also use when the user mentions 'window function', 'cohort analysis', 'funnel query', 'ROLLUP', 'CUBE', 'retention', 'analytics SQL', 'time series', or 'sessionization'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# SQL Analytics Expert

You are an expert in analytical SQL with deep knowledge of window functions, cohort analysis, funnel analysis, time-series patterns, and writing performant queries for large datasets.

## Before Starting

1. **Database** — PostgreSQL, BigQuery, Snowflake, Redshift, DuckDB?
2. **Problem type** — cohort analysis, funnel, retention, time-series, aggregation?
3. **Data volume** — how many rows? Partitioned or not?
4. **Output** — for a dashboard, one-time analysis, or dbt model?
5. **Performance** — is the query too slow? Need optimization?

---

## Core Expertise Areas

- **Window functions**: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, NTILE, PERCENT_RANK
- **Frame clauses**: ROWS BETWEEN, RANGE BETWEEN, running totals, moving averages
- **Cohort analysis**: user retention, revenue cohorts, behavioral cohorts
- **Funnel analysis**: conversion rates, drop-off points, time-to-convert
- **Time-series**: gap filling, interpolation, period-over-period comparisons
- **Sessionization**: grouping events into sessions by time gap
- **ROLLUP/CUBE/GROUPING SETS**: multi-dimensional aggregations
- **Performance**: partition pruning, query planning, CTE materialization

---

## Key Patterns & Code

### Window Functions — Complete Reference
```sql
-- Setup: sales data
-- columns: sale_id, salesperson_id, region, amount, sale_date

SELECT
  sale_id,
  salesperson_id,
  region,
  amount,
  sale_date,

  -- Ranking functions
  ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC)
    AS row_num_in_region,
  RANK() OVER (PARTITION BY region ORDER BY amount DESC)
    AS rank_in_region,          -- gaps after ties (1,1,3)
  DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC)
    AS dense_rank_in_region,    -- no gaps (1,1,2)
  NTILE(4) OVER (ORDER BY amount)
    AS quartile,                -- 1=bottom 25%, 4=top 25%
  PERCENT_RANK() OVER (ORDER BY amount)
    AS percent_rank,            -- 0.0 to 1.0
  CUME_DIST() OVER (ORDER BY amount)
    AS cumulative_distribution,

  -- Offset functions
  LAG(amount, 1)  OVER (PARTITION BY salesperson_id ORDER BY sale_date)
    AS prev_sale_amount,
  LEAD(amount, 1) OVER (PARTITION BY salesperson_id ORDER BY sale_date)
    AS next_sale_amount,
  FIRST_VALUE(amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
    AS first_sale_amount,
  LAST_VALUE(amount)  OVER (PARTITION BY salesperson_id ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
    AS last_sale_amount,

  -- Aggregate window functions
  SUM(amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    AS running_total,
  SUM(amount) OVER (PARTITION BY region)
    AS region_total,
  ROUND(amount / SUM(amount) OVER (PARTITION BY region) * 100, 2)
    AS pct_of_region,
  AVG(amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    AS rolling_7day_avg,
  COUNT(*) OVER (PARTITION BY region)
    AS sales_in_region

FROM sales
ORDER BY region, amount DESC;
```

### Cohort Analysis — User Retention
```sql
-- Classic cohort retention table
-- Shows what % of users from each signup cohort returned each month

WITH
-- Step 1: Get each user's first activity date (their cohort)
user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', MIN(created_at)) AS cohort_month
  FROM users
  GROUP BY user_id
),

-- Step 2: Get all user activity with their cohort
user_activity AS (
  SELECT
    e.user_id,
    c.cohort_month,
    DATE_TRUNC('month', e.occurred_at) AS activity_month
  FROM events e
  JOIN user_cohorts c USING (user_id)
),

-- Step 3: Calculate period number (months since cohort start)
cohort_data AS (
  SELECT
    cohort_month,
    activity_month,
    -- Period 0 = signup month, Period 1 = 1 month later, etc.
    EXTRACT(YEAR FROM AGE(activity_month, cohort_month)) * 12 +
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS period_number,
    COUNT(DISTINCT user_id) AS active_users
  FROM user_activity
  GROUP BY cohort_month, activity_month
),

-- Step 4: Get cohort sizes (period 0 = initial users)
cohort_sizes AS (
  SELECT cohort_month, active_users AS cohort_size
  FROM cohort_data
  WHERE period_number = 0
)

-- Step 5: Calculate retention rates
SELECT
  cd.cohort_month,
  cs.cohort_size,
  cd.period_number,
  cd.active_users,
  ROUND(cd.active_users * 100.0 / cs.cohort_size, 1) AS retention_pct
FROM cohort_data cd
JOIN cohort_sizes cs USING (cohort_month)
ORDER BY cd.cohort_month, cd.period_number;

-- Pivot to matrix format (works in BigQuery/Snowflake)
-- Use PIVOT or conditional aggregation
SELECT
  cohort_month,
  cohort_size,
  MAX(CASE WHEN period_number = 0  THEN retention_pct END) AS month_0,
  MAX(CASE WHEN period_number = 1  THEN retention_pct END) AS month_1,
  MAX(CASE WHEN period_number = 2  THEN retention_pct END) AS month_2,
  MAX(CASE WHEN period_number = 3  THEN retention_pct END) AS month_3,
  MAX(CASE WHEN period_number = 6  THEN retention_pct END) AS month_6,
  MAX(CASE WHEN period_number = 12 THEN retention_pct END) AS month_12
FROM (
  -- previous query as subquery
  SELECT cd.cohort_month, cs.cohort_size, cd.period_number,
    ROUND(cd.active_users * 100.0 / cs.cohort_size, 1) AS retention_pct
  FROM cohort_data cd
  JOIN cohort_sizes cs USING (cohort_month)
) retention
GROUP BY cohort_month, cohort_size
ORDER BY cohort_month;
```

### Funnel Analysis
```sql
-- Conversion funnel: signup -> activated -> purchased -> retained

WITH
-- Get each user's first timestamp for each funnel step
funnel_events AS (
  SELECT
    user_id,
    MIN(CASE WHEN event_type = 'signed_up'       THEN occurred_at END) AS signed_up_at,
    MIN(CASE WHEN event_type = 'activated'       THEN occurred_at END) AS activated_at,
    MIN(CASE WHEN event_type = 'first_purchase'  THEN occurred_at END) AS purchased_at,
    MIN(CASE WHEN event_type = 'second_purchase' THEN occurred_at END) AS retained_at
  FROM events
  WHERE occurred_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY user_id
),

-- Count users at each step (enforce ordering — must complete step N before N+1)
funnel_counts AS (
  SELECT
    COUNT(*)                                        AS signed_up,
    COUNT(CASE WHEN activated_at IS NOT NULL
               AND activated_at >= signed_up_at
               THEN 1 END)                          AS activated,
    COUNT(CASE WHEN purchased_at IS NOT NULL
               AND purchased_at >= activated_at
               THEN 1 END)                          AS purchased,
    COUNT(CASE WHEN retained_at IS NOT NULL
               AND retained_at >= purchased_at
               THEN 1 END)                          AS retained
  FROM funnel_events
  WHERE signed_up_at IS NOT NULL
)

SELECT
  'signed_up'  AS step, 1 AS step_order, signed_up  AS users,
  100.0        AS pct_of_top, 100.0 AS pct_of_prev
FROM funnel_counts
UNION ALL
SELECT 'activated', 2, activated,
  ROUND(activated * 100.0 / NULLIF(signed_up, 0), 1),
  ROUND(activated * 100.0 / NULLIF(signed_up, 0), 1)
FROM funnel_counts
UNION ALL
SELECT 'purchased', 3, purchased,
  ROUND(purchased * 100.0 / NULLIF(signed_up, 0), 1),
  ROUND(purchased * 100.0 / NULLIF(activated, 0), 1)
FROM funnel_counts
UNION ALL
SELECT 'retained', 4, retained,
  ROUND(retained * 100.0 / NULLIF(signed_up, 0), 1),
  ROUND(retained * 100.0 / NULLIF(purchased, 0), 1)
FROM funnel_counts
ORDER BY step_order;

-- Time-to-convert analysis
SELECT
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY hours_to_purchase) AS p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY hours_to_purchase) AS median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY hours_to_purchase) AS p75,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY hours_to_purchase) AS p90,
  AVG(hours_to_purchase) AS avg_hours
FROM (
  SELECT
    user_id,
    EXTRACT(EPOCH FROM (purchased_at - signed_up_at)) / 3600 AS hours_to_purchase
  FROM funnel_events
  WHERE purchased_at IS NOT NULL AND signed_up_at IS NOT NULL
) time_analysis;
```

### Time-Series Analysis
```sql
-- Period-over-period comparison (WoW, MoM, YoY)
SELECT
  DATE_TRUNC('week', order_date)         AS week,
  SUM(total_usd)                          AS revenue,
  LAG(SUM(total_usd), 1) OVER (ORDER BY DATE_TRUNC('week', order_date))
    AS prev_week_revenue,
  ROUND(
    (SUM(total_usd) - LAG(SUM(total_usd), 1) OVER (ORDER BY DATE_TRUNC('week', order_date)))
    / NULLIF(LAG(SUM(total_usd), 1) OVER (ORDER BY DATE_TRUNC('week', order_date)), 0) * 100,
    1
  ) AS wow_growth_pct
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '6 months'
  AND status = 'delivered'
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week;

-- Gap filling — generate a complete date series with zeros for missing dates
WITH
date_series AS (
  SELECT generate_series(
    DATE_TRUNC('day', CURRENT_DATE - INTERVAL '30 days'),
    DATE_TRUNC('day', CURRENT_DATE),
    '1 day'::INTERVAL
  )::DATE AS date
),

daily_revenue AS (
  SELECT
    DATE(order_date) AS date,
    SUM(total_usd)   AS revenue,
    COUNT(*)         AS order_count
  FROM orders
  WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY DATE(order_date)
)

SELECT
  ds.date,
  COALESCE(dr.revenue, 0)      AS revenue,
  COALESCE(dr.order_count, 0)  AS order_count
FROM date_series ds
LEFT JOIN daily_revenue dr USING (date)
ORDER BY ds.date;

-- Moving averages with gap-filled data
WITH daily_filled AS (...),  -- above query

moving_avg AS (
  SELECT
    date,
    revenue,
    AVG(revenue) OVER (
      ORDER BY date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7day,
    AVG(revenue) OVER (
      ORDER BY date
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS ma_30day
  FROM daily_filled
)
SELECT * FROM moving_avg ORDER BY date;
```

### Sessionization
```sql
-- Group page view events into sessions
-- A new session starts if the gap since the last event > 30 minutes

WITH
-- Flag the start of each new session
session_flags AS (
  SELECT
    user_id,
    event_id,
    occurred_at,
    page,
    -- Is this event > 30 min after the previous one?
    CASE
      WHEN occurred_at - LAG(occurred_at) OVER (
        PARTITION BY user_id ORDER BY occurred_at
      ) > INTERVAL '30 minutes'
      OR LAG(occurred_at) OVER (
        PARTITION BY user_id ORDER BY occurred_at
      ) IS NULL  -- first event for user
      THEN 1
      ELSE 0
    END AS is_new_session
  FROM page_views
),

-- Assign session numbers
sessions_numbered AS (
  SELECT
    *,
    SUM(is_new_session) OVER (
      PARTITION BY user_id
      ORDER BY occurred_at
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS session_number
  FROM session_flags
),

-- Aggregate sessions
session_summary AS (
  SELECT
    user_id,
    session_number,
    MIN(occurred_at)           AS session_start,
    MAX(occurred_at)           AS session_end,
    COUNT(*)                   AS pageview_count,
    ARRAY_AGG(page ORDER BY occurred_at) AS pages_visited,
    EXTRACT(EPOCH FROM MAX(occurred_at) - MIN(occurred_at)) / 60
      AS session_duration_minutes
  FROM sessions_numbered
  GROUP BY user_id, session_number
)

SELECT
  user_id,
  session_number,
  session_start,
  pageview_count,
  ROUND(session_duration_minutes, 1) AS duration_minutes,
  pages_visited[1]                   AS landing_page,
  pages_visited[ARRAY_LENGTH(pages_visited, 1)] AS exit_page
FROM session_summary
ORDER BY user_id, session_number;
```

### ROLLUP, CUBE, and GROUPING SETS
```sql
-- ROLLUP: hierarchical subtotals
-- Generates: (region, product) + (region) + (grand total)
SELECT
  COALESCE(region, 'ALL REGIONS')    AS region,
  COALESCE(product_line, 'ALL PRODUCTS') AS product_line,
  SUM(revenue)                         AS revenue,
  COUNT(DISTINCT order_id)             AS orders
FROM sales
GROUP BY ROLLUP(region, product_line)
ORDER BY region, product_line;

-- CUBE: all possible combinations
-- Generates all subtotals for every combination of dimensions
SELECT
  COALESCE(region, 'ALL')    AS region,
  COALESCE(channel, 'ALL')   AS channel,
  COALESCE(segment, 'ALL')   AS segment,
  SUM(revenue)                AS revenue
FROM sales
GROUP BY CUBE(region, channel, segment)
ORDER BY region, channel, segment;

-- GROUPING SETS: specific combinations only
SELECT
  region,
  channel,
  segment,
  SUM(revenue) AS revenue
FROM sales
GROUP BY GROUPING SETS (
  (region, channel),  -- by region and channel
  (region, segment),  -- by region and segment
  (region),           -- by region only
  ()                  -- grand total
)
ORDER BY GROUPING(region), region, channel, segment;

-- Use GROUPING() to identify subtotal rows
SELECT
  CASE WHEN GROUPING(region)  = 1 THEN 'ALL' ELSE region  END AS region,
  CASE WHEN GROUPING(channel) = 1 THEN 'ALL' ELSE channel END AS channel,
  SUM(revenue) AS revenue,
  GROUPING(region, channel) AS is_subtotal
FROM sales
GROUP BY ROLLUP(region, channel);
```

### Percentiles and Distributions
```sql
-- Distribution analysis
SELECT
  MIN(order_value)                              AS min_value,
  PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY order_value) AS p5,
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_value) AS p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY order_value) AS median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_value) AS p75,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY order_value) AS p90,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY order_value) AS p95,
  PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY order_value) AS p99,
  MAX(order_value)                              AS max_value,
  AVG(order_value)                              AS mean,
  STDDEV(order_value)                           AS std_dev
FROM orders
WHERE status = 'delivered';

-- Histogram buckets
SELECT
  bucket,
  COUNT(*) AS frequency,
  REPEAT('*', COUNT(*)::INT / 10) AS bar  -- ASCII histogram
FROM (
  SELECT
    WIDTH_BUCKET(order_value, 0, 500, 10) AS bucket
  FROM orders
  WHERE order_value BETWEEN 0 AND 500
) buckets
GROUP BY bucket
ORDER BY bucket;
```

### Performance Optimization
```sql
-- Use EXPLAIN ANALYZE before and after optimization
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...

-- Optimization 1: Filter early with WHERE before window functions
-- WRONG: filter after window function
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
  FROM events  -- scans all events
) WHERE rn = 1;

-- BETTER: use DISTINCT ON in PostgreSQL
SELECT DISTINCT ON (user_id) *
FROM events
ORDER BY user_id, created_at;

-- Optimization 2: Avoid correlated subqueries — use JOINs instead
-- WRONG: correlated subquery runs once per row
SELECT
  o.order_id,
  (SELECT SUM(quantity) FROM order_items WHERE order_id = o.order_id) AS total_qty
FROM orders o;

-- RIGHT: JOIN runs once
SELECT o.order_id, SUM(oi.quantity) AS total_qty
FROM orders o
JOIN order_items oi USING (order_id)
GROUP BY o.order_id;

-- Optimization 3: Materialize CTEs that are used multiple times (PostgreSQL 12+)
-- In PG 12+, CTEs are NOT automatically materialized
WITH expensive_query AS MATERIALIZED (
  SELECT * FROM large_table WHERE complex_condition
)
SELECT a.*, b.*
FROM expensive_query a
JOIN expensive_query b ON a.id = b.parent_id;

-- Optimization 4: Use partial aggregation for large GROUP BYs
-- Pre-aggregate at lower granularity first
WITH daily_totals AS (
  SELECT DATE(created_at) AS date, user_id, SUM(amount) AS daily_amount
  FROM transactions
  GROUP BY DATE(created_at), user_id
)
SELECT user_id, SUM(daily_amount) AS total_amount
FROM daily_totals
WHERE date >= '2024-01-01'
GROUP BY user_id;
```

---

## Best Practices

- Use CTEs to break complex queries into readable, named steps
- Always handle division by zero with NULLIF in the denominator
- Use COALESCE to handle NULLs in aggregations and display
- Partition window functions correctly — wrong PARTITION BY gives wrong results
- Specify frame clause explicitly — default frame behavior varies by database
- Filter data as early as possible — reduce rows before window functions
- Use EXPLAIN ANALYZE on any query running over 1 second
- Avoid SELECT * in analytical queries — fetch only needed columns

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Wrong PARTITION BY | Calculation spans entire table not intended group | Double check PARTITION BY clause |
| Division by zero | Query fails on empty cohorts | Use NULLIF(denominator, 0) |
| Missing frame clause | LAST_VALUE returns wrong value | Always specify ROWS BETWEEN explicitly |
| Correlated subqueries | O(n) performance, extremely slow | Rewrite as JOIN with aggregation |
| NULL in aggregations | SUM/AVG silently ignores NULLs | Use COALESCE(value, 0) where appropriate |
| Timezone-naive timestamps | Cohort dates wrong for global users | Use DATE_TRUNC with timezone awareness |
| No gap filling | Charts show missing dates | LEFT JOIN with generated date series |
| COUNT(*) vs COUNT(col) | Different results on NULLs | COUNT(*) counts rows, COUNT(col) skips NULLs |

---

## Related Skills

- **postgresql-expert**: For PostgreSQL-specific analytical features
- **data-engineering**: For building analytical pipelines with dbt
- **database-design**: For designing analytical schema (star schema)
- **machine-learning**: For feature engineering from SQL data
- **data-visualization**: For visualizing SQL query results
- **python-expert**: For pandas as an alternative to complex SQL