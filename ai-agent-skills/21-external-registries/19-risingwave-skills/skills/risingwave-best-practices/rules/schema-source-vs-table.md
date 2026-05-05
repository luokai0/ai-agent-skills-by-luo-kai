---
title: Use TABLE for CDC, SOURCE for append-only streams
impact: CRITICAL
impactDescription: Using CREATE SOURCE for CDC silently drops updates and deletes; data diverges from the upstream database
tags: schema, source, table, cdc, debezium, postgres-cdc, mysql-cdc
---

## Use TABLE for CDC, SOURCE for append-only streams

`CREATE SOURCE` creates a connection without persisting data — it's for append-only streams (Kafka events, logs). `CREATE TABLE` persists data and supports CDC formats (Debezium, Maxwell, Canal) that deliver inserts, updates, and deletes. Using `CREATE SOURCE` with a CDC connector silently discards all update/delete messages.

**Incorrect (CDC source with CREATE SOURCE):**
```sql
-- Bad: UPDATE and DELETE events from Debezium are silently discarded
CREATE SOURCE orders_cdc (
    id INT, customer_id INT, total DECIMAL, status VARCHAR
)
WITH (
    connector = 'postgres-cdc',
    hostname = 'pg-host',
    port = '5432',
    username = 'repl',
    password = '<your-password>',
    database.name = 'mydb'
)
FORMAT DEBEZIUM ENCODE JSON;
-- This fails: "CDC source cannot define columns and constraints"
-- CDC sources are connection-only; column definitions must go in CREATE TABLE
```

**Correct (two-step CDC with TABLE):**
```sql
-- Step 1: shared connection source (no schema, no FORMAT)
CREATE SOURCE pg_cdc WITH (
    connector = 'postgres-cdc',
    hostname = 'pg-host',
    port = '5432',
    username = 'repl',
    password = '<your-password>',
    database.name = 'mydb',
    slot.name = 'rw_slot'
);

-- Step 2: per-table ingestion as TABLE (persisted, supports updates/deletes)
CREATE TABLE orders (
    id          INT PRIMARY KEY,
    customer_id INT,
    total       DECIMAL,
    status      VARCHAR
)
FROM pg_cdc TABLE 'public.orders';
```

| Feature | `CREATE SOURCE` | `CREATE TABLE` |
|---------|----------------|----------------|
| Persists data | No | Yes |
| CDC formats (Debezium etc.) | Not supported | Required |
| NOT NULL constraints | Not supported | Supported |
| Primary key enforcement | No | Yes |
| UPDATE/DELETE support | No | Yes |
| Watermark + TTL cleanup | No | Yes |

Reference: [Source, Table, MV, and Sink](https://docs.risingwave.com/get-started/source-table-mv-sink)
