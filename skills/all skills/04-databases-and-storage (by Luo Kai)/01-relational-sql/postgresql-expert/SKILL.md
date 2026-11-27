---
author: luo-kai
name: postgresql-expert
description: Expert-level PostgreSQL. Use when writing complex SQL queries, designing schemas, working with indexes, CTEs, window functions, JSONB, full-text search, stored procedures, performance tuning, or pg extensions. Also use when the user mentions 'slow query', 'EXPLAIN', 'index', 'migration', 'schema design', 'normalization', 'JOIN', 'window function', 'CTE', or 'JSONB'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# PostgreSQL Expert

You are an expert PostgreSQL database engineer with deep knowledge of query optimization, schema design, indexing strategies, and PostgreSQL internals.

## Before Starting

1. **PostgreSQL version** — 14, 15, 16, 17?
2. **Scale** — thousands or millions of rows?
3. **Access patterns** — read-heavy, write-heavy, or mixed?
4. **ORM in use** — raw SQL, Prisma, SQLAlchemy, Drizzle, GORM?
5. **Problem type** — performance, schema design, query help, or replication?

---

## Core Expertise Areas

- **Query writing**: CTEs, recursive CTEs, window functions, LATERAL joins, FILTER clause, GROUPING SETS
- **Indexing**: B-tree, GIN, GiST, BRIN, partial, covering (INCLUDE), expression indexes
- **Performance**: EXPLAIN ANALYZE, BUFFERS, query planning, autovacuum, pg_stat_statements
- **JSONB**: operators, GIN indexing, jsonb_set, jsonb_agg, jsonb_array_elements
- **Full-text search**: tsvector, tsquery, ts_rank, custom dictionaries, pg_trgm
- **Partitioning**: range, list, hash partitioning, partition pruning, attach/detach
- **PL/pgSQL**: stored functions, triggers, exception handling, dynamic SQL
- **High availability**: streaming replication, logical replication, PgBouncer connection pooling

---

## Key Patterns & Code

### Window Functions
```sql
-- Running total, rank, moving average — all in one query
SELECT
  customer_id,
  order_date,
  amount,

  -- Running total per customer
  SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total,

  -- Rank by amount within each customer
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY amount DESC
  ) AS rank_by_amount,

  -- Previous order amount
  LAG(amount, 1, 0) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
  ) AS prev_amount,

  -- 3-period moving average
  ROUND(AVG(amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ), 2) AS moving_avg_3,

  -- Percentage of customer total
  ROUND(
    amount / SUM(amount) OVER (PARTITION BY customer_id) * 100,
    2
  ) AS pct_of_total

FROM orders
ORDER BY customer_id, order_date;
```

### CTEs & Recursive CTEs
```sql
-- Readable complex queries with CTEs
WITH
  active_users AS (
    SELECT id, email, created_at
    FROM users
    WHERE last_seen > NOW() - INTERVAL '30 days'
      AND deleted_at IS NULL
  ),
  user_revenue AS (
    SELECT
      user_id,
      COUNT(*) AS order_count,
      SUM(total) AS revenue,
      AVG(total) AS avg_order_value
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
      AND status = 'completed'
    GROUP BY user_id
  )
SELECT
  u.email,
  u.created_at,
  COALESCE(r.order_count, 0) AS order_count,
  COALESCE(r.revenue, 0) AS revenue,
  COALESCE(r.avg_order_value, 0) AS avg_order_value
FROM active_users u
LEFT JOIN user_revenue r ON r.user_id = u.id
ORDER BY r.revenue DESC NULLS LAST;

-- Recursive CTE for hierarchical data (org chart, categories, threads)
WITH RECURSIVE category_tree AS (
  -- Base case: root categories
  SELECT
    id,
    name,
    parent_id,
    0 AS depth,
    ARRAY[id] AS path,
    name AS full_path
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: children
  SELECT
    c.id,
    c.name,
    c.parent_id,
    ct.depth + 1,
    ct.path || c.id,
    ct.full_path || ' > ' || c.name
  FROM categories c
  JOIN category_tree ct ON ct.id = c.parent_id
  WHERE ct.depth < 10  -- prevent infinite loops
)
SELECT * FROM category_tree ORDER BY path;
```

### Indexing Strategy
```sql
-- B-tree: default, good for equality and range queries
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Partial index: only index rows you actually query
-- Much smaller, faster than full index
CREATE INDEX idx_orders_pending
  ON orders(created_at)
  WHERE status = 'pending';

CREATE INDEX idx_users_unverified
  ON users(email)
  WHERE email_verified = false;

-- Covering index: include extra columns to enable index-only scans
-- Avoids hitting the heap entirely
CREATE INDEX idx_users_email_covering
  ON users(email)
  INCLUDE (id, name, role);
-- This query now uses index-only scan:
-- SELECT id, name, role FROM users WHERE email = $1;

-- Expression index: index the result of a function
CREATE INDEX idx_users_email_lower
  ON users(LOWER(email));
-- Now this uses the index:
SELECT * FROM users WHERE LOWER(email) = LOWER($1);

-- GIN index for JSONB and full-text search
CREATE INDEX idx_products_attrs
  ON products USING GIN(attributes);

CREATE INDEX idx_articles_fts
  ON articles USING GIN(
    to_tsvector('english', title || ' ' || COALESCE(body, ''))
  );

-- GIN for array contains queries
CREATE INDEX idx_posts_tags
  ON posts USING GIN(tags);
-- SELECT * FROM posts WHERE tags @> ARRAY['postgres', 'sql'];

-- Multi-column index: order matters!
-- Good for: WHERE status = $1 AND created_at > $2
-- Good for: WHERE status = $1 (leftmost prefix)
-- Bad for:  WHERE created_at > $2 (not leftmost)
CREATE INDEX idx_orders_status_date
  ON orders(status, created_at DESC);
```

### EXPLAIN ANALYZE — Reading Query Plans
```sql
-- Always use ANALYZE + BUFFERS for real execution stats
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '90 days'
GROUP BY u.id, u.email
ORDER BY order_count DESC
LIMIT 20;

-- Key things to look for:
-- ❌ Seq Scan on large table   → missing index
-- ❌ Nested Loop with large outer → consider Hash Join
-- ❌ High "Rows Removed by Filter" → bad selectivity, run ANALYZE
-- ❌ Buffers: read=X (large) → data not in cache, I/O bound
-- ✅ Index Scan / Index Only Scan → using index correctly
-- ✅ Buffers: hit=X (large) → data in shared buffer cache

-- After adding an index, run this to update statistics:
ANALYZE users;
ANALYZE orders;
```

### JSONB Operations
```sql
-- Query JSONB fields
SELECT * FROM products
WHERE
  attributes->>'color' = 'red'
  AND (attributes->'price')::numeric < 100
  AND attributes @> '{"in_stock": true}'::jsonb;

-- Update nested JSONB (immutable — creates new value)
UPDATE products
SET attributes = jsonb_set(
  attributes,
  '{specs,weight_kg}',
  '2.5'::jsonb
)
WHERE id = $1;

-- Remove a key from JSONB
UPDATE products
SET attributes = attributes - 'old_field'
WHERE id = $1;

-- Expand JSONB array to rows
SELECT
  p.id,
  p.name,
  tag.value AS tag
FROM products p,
  jsonb_array_elements_text(p.attributes->'tags') AS tag;

-- Aggregate rows into JSONB
SELECT jsonb_agg(
  jsonb_build_object(
    'id', id,
    'name', name,
    'email', email
  )
) AS users_json
FROM users
WHERE active = true;
```

### Full-Text Search
```sql
-- Basic full-text search
SELECT
  id,
  title,
  ts_rank(
    to_tsvector('english', title || ' ' || body),
    to_tsquery('english', 'postgresql & performance')
  ) AS rank
FROM articles
WHERE
  to_tsvector('english', title || ' ' || body)
  @@ to_tsquery('english', 'postgresql & performance')
ORDER BY rank DESC
LIMIT 10;

-- Using stored tsvector column (faster — pre-computed)
ALTER TABLE articles ADD COLUMN search_vector tsvector;

UPDATE articles SET search_vector =
  to_tsvector('english', title || ' ' || COALESCE(body, ''));

CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Keep it updated with a trigger
CREATE FUNCTION update_search_vector() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('english',
    NEW.title || ' ' || COALESCE(NEW.body, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_vector_update
  BEFORE INSERT OR UPDATE ON articles
  FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Fuzzy search with pg_trgm
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING GIN(name gin_trgm_ops);

SELECT name, similarity(name, 'Muhamed') AS sim
FROM users
WHERE name % 'Muhamed'  -- similarity > 0.3
ORDER BY sim DESC
LIMIT 10;
```

### Efficient Upsert & Queue Patterns
```sql
-- Upsert: insert or update on conflict
INSERT INTO users (email, name, updated_at)
VALUES ($1, $2, NOW())
ON CONFLICT (email)
DO UPDATE SET
  name = EXCLUDED.name,
  updated_at = EXCLUDED.updated_at
WHERE users.name IS DISTINCT FROM EXCLUDED.name  -- only update if changed
RETURNING id, (xmax = 0) AS inserted;  -- xmax=0 means it was inserted

-- Bulk upsert from values
INSERT INTO prices (product_id, amount, currency)
VALUES
  (1, 9.99, 'USD'),
  (2, 14.99, 'USD'),
  (3, 4.99, 'USD')
ON CONFLICT (product_id, currency)
DO UPDATE SET
  amount = EXCLUDED.amount,
  updated_at = NOW();

-- Job queue: SKIP LOCKED for concurrent workers
-- No deadlocks, no double processing
BEGIN;
SELECT id, payload, attempts
FROM jobs
WHERE status = 'pending'
  AND run_at <= NOW()
  AND attempts < 3
ORDER BY priority DESC, run_at ASC
LIMIT 5
FOR UPDATE SKIP LOCKED;
-- process jobs...
UPDATE jobs SET status = 'processing', attempts = attempts + 1
WHERE id = ANY($1);
COMMIT;
```

### Schema Design Patterns
```sql
-- Users table with best practices
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  role        TEXT NOT NULL DEFAULT 'user'
                CHECK (role IN ('user', 'admin', 'moderator')),
  metadata    JSONB NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ  -- soft delete
);

-- Auto-update updated_at
CREATE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Audit log table
CREATE TABLE audit_log (
  id          BIGSERIAL PRIMARY KEY,
  table_name  TEXT NOT NULL,
  record_id   UUID NOT NULL,
  operation   TEXT NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
  old_data    JSONB,
  new_data    JSONB,
  changed_by  UUID REFERENCES users(id),
  changed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_log_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_changed_at ON audit_log(changed_at DESC);
```

### Performance Queries
```sql
-- Find slowest queries (requires pg_stat_statements extension)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT
  round(mean_exec_time::numeric, 2) AS avg_ms,
  round(total_exec_time::numeric, 2) AS total_ms,
  calls,
  round(stddev_exec_time::numeric, 2) AS stddev_ms,
  LEFT(query, 100) AS query_snippet
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Find missing indexes (tables with many sequential scans)
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  seq_tup_read / seq_scan AS avg_seq_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Find unused indexes (wasting space and slowing writes)
SELECT
  schemaname,
  tablename,
  indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan AS times_used
FROM pg_stat_user_indexes
JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0
  AND NOT indisprimary
  AND NOT indisunique
ORDER BY pg_relation_size(indexrelid) DESC;

-- Table bloat — when to run VACUUM
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
  n_dead_tup AS dead_tuples,
  n_live_tup AS live_tuples,
  ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_vacuum,
  last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```

---

## Best Practices

- Run `EXPLAIN (ANALYZE, BUFFERS)` on every slow query before adding indexes
- Use `timestamptz` — never plain `timestamp` (always store UTC)
- Use `gen_random_uuid()` for UUID primary keys (pg 13+, no extension needed)
- Always index foreign key columns — PostgreSQL does not do this automatically
- Use `VACUUM ANALYZE` after bulk inserts/deletes
- Enable `pg_stat_statements` from day one — invaluable for performance monitoring
- Use PgBouncer in transaction mode for connection pooling
- Set `work_mem` carefully — too high causes OOM with many concurrent queries
- Use `UNLOGGED` tables for temporary data that can be recreated

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| `SELECT *` | Fetches unused columns, breaks index-only scans | Select only needed columns |
| No FK indexes | Slow JOINs and deletes | Always index foreign keys |
| N+1 queries | 100 rows = 101 queries | Use JOINs or batch with `ANY($1::uuid[])` |
| `timestamp` without tz | Timezone bugs in production | Always use `timestamptz` |
| Long transactions | Table bloat, lock contention, replication lag | Keep transactions as short as possible |
| No LIMIT on large tables | OOM or timeout | Always paginate large result sets |
| Implicit type casts | Index not used due to type mismatch | Match parameter types exactly |
| Missing ANALYZE after bulk load | Planner uses stale statistics | Run `ANALYZE table` after bulk operations |

---

## Related Skills

- **database-design**: For schema design patterns and normalization
- **prisma-expert**: For Prisma ORM on top of PostgreSQL
- **redis-expert**: For caching PostgreSQL query results
- **docker-expert**: For running PostgreSQL in containers
- **data-engineering**: For PostgreSQL in analytical pipelines
