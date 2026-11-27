---
title: Use the two-step pattern for CDC ingestion
impact: CRITICAL
impactDescription: Single-step CDC setup fails at runtime or silently drops updates; two-step pattern (shared source + TABLE) is the only supported CDC approach
tags: cdc, postgres-cdc, mysql-cdc, debezium, create-table, create-source, replication
---

## Use the two-step pattern for CDC ingestion

CDC (Change Data Capture) from PostgreSQL, MySQL, or other databases requires a two-step setup in RisingWave:
1. `CREATE SOURCE` — defines the shared database connection (no schema, no FORMAT/ENCODE)
2. `CREATE TABLE ... FROM source TABLE '...'` — creates a per-table ingestion with persistence

Attempting to create a single CDC source with schema and FORMAT fails. Attempting to use `CREATE SOURCE` (without TABLE) for CDC silently drops updates and deletes.

**Incorrect (single-step — fails):**
```sql
-- Bad: CDC cannot be done in a single CREATE SOURCE with schema
CREATE SOURCE orders_cdc (
    id INT PRIMARY KEY,
    status VARCHAR
)
WITH (
    connector = 'postgres-cdc',
    hostname = 'pg',
    ...
)
FORMAT DEBEZIUM ENCODE JSON;  -- ERROR: "CDC source cannot define columns and constraints"
```

**Correct (two-step CDC):**
```sql
-- Step 1: shared CDC connection (no schema, no FORMAT/ENCODE)
CREATE SOURCE pg_mydb WITH (
    connector = 'postgres-cdc',
    hostname = 'postgres-host',
    port = '5432',
    username = 'replicator',  -- must have REPLICATION role
    password = '<your-password>',
    database.name = 'mydb',
    slot.name = 'rw_cdc_slot'  -- unique replication slot name
);

-- Step 2: per-table TABLE (persistent, supports update/delete)
CREATE TABLE orders (
    id          INT PRIMARY KEY,
    customer_id INT,
    total       DECIMAL,
    status      VARCHAR,
    updated_at  TIMESTAMP
)
FROM pg_mydb TABLE 'public.orders';

-- Multiple tables from the same connection
CREATE TABLE customers (
    id INT PRIMARY KEY, name VARCHAR, tier VARCHAR
)
FROM pg_mydb TABLE 'public.customers';
```

**PostgreSQL prerequisite setup:**
```sql
-- On the upstream PostgreSQL database:
ALTER SYSTEM SET wal_level = logical;
CREATE ROLE replicator REPLICATION LOGIN;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO replicator;
-- Reload configuration
SELECT pg_reload_conf();
```

**Monitor CDC backfill progress:**
```sql
SELECT job_id, split_total_count, split_backfilled_count, split_completed_count
FROM rw_catalog.rw_cdc_progress;
```

Reference: [PostgreSQL CDC](https://docs.risingwave.com/integrations/sources/postgresql-cdc)
