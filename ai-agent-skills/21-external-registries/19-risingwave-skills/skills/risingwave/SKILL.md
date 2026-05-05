---
name: risingwave
description: Use when working with RisingWave — streaming SQL database, materialized views, sources, sinks, CDC from PostgreSQL/MySQL, Kafka ingestion, time windows (TUMBLE/HOP/SESSION), watermarks, EMIT ON WINDOW CLOSE, port 4566, risingwave-mcp, event streaming pipeline design, real-time analytics, stream processing
license: Apache-2.0
metadata:
  author: RisingWave Labs
  version: "0.3.1"
  organization: RisingWave Labs
  date: April 2026
  abstract: >
    Comprehensive reference for building stream processing pipelines with RisingWave.
    Covers connection, MCP server setup, the Source→MV→Sink pipeline pattern, CDC ingestion,
    time-windowed aggregations, watermarks, system catalog queries, and common gotchas.
---

# RisingWave

RisingWave is a streaming SQL database implementing the PostgreSQL wire protocol.
The core pipeline is: **Source** (ingest) → **Materialized View** (continuous compute) → **Sink** (output).

## Core Principles

1. **Port 4566, not 5432** — RisingWave listens on `4566` for SQL connections. Dashboard is at `5691`.
2. **SOURCE ≠ TABLE** — `CREATE SOURCE` connects a stream but doesn't persist data. `CREATE TABLE` persists. For CDC (Debezium, Maxwell, Canal), you MUST use `CREATE TABLE ... FROM source`.
3. **Watermarks unlock window closing** — Without `WATERMARK FOR col AS col - INTERVAL '...'`, `EMIT ON WINDOW CLOSE` won't work; use it on the source or table definition. In RisingWave 2.8+, watermarks on `TABLE` require `APPEND ONLY` — use `CREATE SOURCE` for non-append-only streams that need watermarks.
4. **`EMIT ON WINDOW CLOSE` vs default** — Default emit-on-update sends partial results after each checkpoint. Use `EMIT ON WINDOW CLOSE` for final, immutable window results.
5. **Large backfills need `BACKGROUND_DDL`** — Creating an MV over a large table blocks without `SET BACKGROUND_DDL = true`. Monitor with `SELECT * FROM rw_catalog.rw_ddl_progress`.
6. **`snapshot = false` on sinks** — Adding a sink to an existing MV without this flag replays all historical data into the sink.
7. **Verify docs** — RisingWave evolves rapidly. When unsure, check [docs.risingwave.com](https://docs.risingwave.com) or query `SHOW CREATE` on existing objects.

## Connection

```bash
# Default local connection
psql -h localhost -p 4566 -d dev -U root

# Docker (single-node)
docker run -it --pull=always -p 4566:4566 -p 5691:5691 \
  risingwavelabs/risingwave:latest single_node
```

| Parameter | Default |
|-----------|---------|
| Host | `localhost` |
| Port | `4566` |
| Database | `dev` |
| User | `root` |
| Password | (none) |

Connection string: `postgresql://root:@localhost:4566/dev`

Any PostgreSQL-compatible client works: `psql`, JDBC, `psycopg2`, `pgx`, SQLAlchemy, dbt, Grafana.

## MCP Server Setup

RisingWave has an official MCP server with 100+ tools (query execution, schema exploration, streaming job monitoring, CDC progress, Kafka lag, Hummock storage analysis).

```bash
git clone https://github.com/risingwavelabs/risingwave-mcp.git
cd risingwave-mcp && pip install -r requirements.txt
```

Configure via environment variable:
```
RISINGWAVE_CONNECTION_STR=postgresql://root:@localhost:4566/dev
```

Add to your agent's MCP config (Claude Code: `~/.claude/claude_desktop_config.json`, VS Code: `.vscode/mcp.json`):

```json
{
  "mcpServers": {
    "risingwave": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/risingwave-mcp/src/main.py"],
      "env": {
        "RISINGWAVE_CONNECTION_STR": "postgresql://root:@localhost:4566/dev"
      }
    }
  }
}
```

## The Pipeline Pattern

```
Stream data → SOURCE → MATERIALIZED VIEW(s) → SINK(s)
Static/CDC data → TABLE ─────────────────────────────╯
```

### Step 1: Source (streaming, no persistence)

```sql
CREATE SOURCE user_events (
    user_id     INT,
    action      VARCHAR,
    event_time  TIMESTAMP,
    WATERMARK FOR event_time AS event_time - INTERVAL '5 SECOND'
)
WITH (
    connector = 'kafka',
    topic = 'user-events',
    properties.bootstrap.server = 'kafka:9092',
    scan.startup.mode = 'latest'
)
FORMAT PLAIN ENCODE JSON;
```

### Step 2: Materialized View (continuous compute)

```sql
-- Windowed aggregation with final results on window close
CREATE MATERIALIZED VIEW active_users_per_minute AS
SELECT
    action,
    COUNT(DISTINCT user_id) AS unique_users,
    window_start,
    window_end
FROM TUMBLE(user_events, event_time, INTERVAL '1 MINUTE')
GROUP BY action, window_start, window_end
EMIT ON WINDOW CLOSE;

-- Plain aggregation (emit on every update)
CREATE MATERIALIZED VIEW user_action_counts AS
SELECT user_id, action, COUNT(*) AS cnt
FROM user_events
GROUP BY user_id, action;
```

### Step 3: Sink (output)

```sql
CREATE SINK alerts_to_kafka FROM active_users_per_minute
WITH (
    connector = 'kafka',
    topic = 'user-alerts',
    properties.bootstrap.server = 'kafka:9092',
    snapshot = false   -- skip historical backfill
)
FORMAT PLAIN ENCODE JSON;
```

## CDC Pattern (Database Replication)

CDC requires a **two-step setup**: shared connection source + per-table TABLE.

```sql
-- Step 1: shared CDC source connection
CREATE SOURCE pg_cdc WITH (
    connector = 'postgres-cdc',
    hostname = 'postgres-host',
    port = '5432',
    username = 'replicator',
    password = '<your-password>',
    database.name = 'mydb',
    slot.name = 'rw_slot'
);

-- Step 2: per-table ingestion (TABLE, not SOURCE)
CREATE TABLE orders (
    id          INT PRIMARY KEY,
    customer_id INT,
    total       DECIMAL,
    created_at  TIMESTAMP
)
FROM pg_cdc TABLE 'public.orders';
```

## Time Windows

All three window types add `window_start` and `window_end` columns.

```sql
-- TUMBLE: non-overlapping fixed windows
FROM TUMBLE(table, time_col, INTERVAL '5 MINUTES')

-- HOP (sliding): overlapping windows
-- hop_size = slide interval, window_size = total duration
FROM HOP(table, time_col, INTERVAL '1 MINUTE', INTERVAL '5 MINUTES')

```

> **Note:** SESSION windows are only supported in batch mode in RisingWave 2.x. For streaming, use TUMBLE or HOP.

**Pattern:** Always group by `window_start, window_end` and add `EMIT ON WINDOW CLOSE` when using watermarks.

## Useful System Catalog Queries

```sql
-- All materialized views with definitions
SELECT name, definition FROM rw_catalog.rw_materialized_views;

-- DDL progress during MV creation / backfill
SELECT ddl_id, ddl_statement, progress FROM rw_catalog.rw_ddl_progress;

-- Active sources and their connectors
SELECT name, connector FROM rw_catalog.rw_sources;

-- Sink info
SELECT name, sink_type, connector FROM rw_catalog.rw_sinks;

-- CDC backfill progress
SELECT job_id, split_total_count, split_backfilled_count, split_completed_count
FROM rw_catalog.rw_cdc_progress;

-- Cluster nodes
SELECT id, host, type, state FROM rw_catalog.rw_worker_nodes;

-- Inspect object definition
SHOW CREATE MATERIALIZED VIEW my_mv;
SHOW CREATE SOURCE my_source;
SHOW CREATE SINK my_sink;
```

## Useful Session Settings

```sql
-- Large backfills: non-blocking DDL
SET BACKGROUND_DDL = true;

-- Share Kafka source across multiple MVs (v2.1+)
SET streaming_use_shared_source = true;
```

## Troubleshooting

**MCP server not connecting**
- Verify `RISINGWAVE_CONNECTION_STR` is set and RisingWave is running on port 4566
- Test the connection first: `psql -h localhost -p 4566 -d dev -U root`
- Check Python version: `python --version` (requires Python 3.8+)

**`EMIT ON WINDOW CLOSE` produces no output**
- The source or table must have `WATERMARK FOR col AS col - INTERVAL '...'` defined
- Confirm watermark is advancing: insert rows with recent timestamps, not historical data
- Check MV definition: `SHOW CREATE MATERIALIZED VIEW my_mv`

**MV creation hangs / session times out**
- Use `SET BACKGROUND_DDL = true` before `CREATE MATERIALIZED VIEW`
- Monitor progress: `SELECT ddl_id, ddl_statement, progress FROM rw_catalog.rw_ddl_progress`

**CDC table not receiving updates**
- Verify PostgreSQL has `wal_level = logical` and the replication user has `REPLICATION` role
- Check CDC lag: `SELECT * FROM rw_catalog.rw_cdc_progress`
- Ensure `slot.name` in `CREATE SOURCE` is unique and does not already exist on the upstream DB

**Sink sending duplicate historical data**
- Add `snapshot = false` to the sink `WITH` clause to skip backfilling existing MV data

## References

- [Connectors reference](references/connectors.md) — all supported sources and sinks
- [System catalog reference](references/catalog.md) — full `rw_catalog` table listing
- [RisingWave docs](https://docs.risingwave.com)
- [RisingWave MCP server](https://github.com/risingwavelabs/risingwave-mcp)
