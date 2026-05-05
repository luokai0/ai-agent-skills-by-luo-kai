---
title: Use shared source when multiple MVs read the same Kafka topic
impact: HIGH
impactDescription: Without shared source, each MV spawns a separate Kafka consumer — N MVs = N consumers, N times the network bandwidth and broker load; shared source uses one consumer for all
tags: performance, kafka, shared-source, streaming_use_shared_source, consumer, parallelism
---

## Use shared source when multiple MVs read the same Kafka topic

By default, each materialized view that reads from the same Kafka source spawns its own independent `SourceExecutor`. For a topic with 3 MVs, this means 3 separate consumer groups reading the same partitions, tripling Kafka broker load and network bandwidth. The shared source feature (v2.1+) allows a single `SourceExecutor` to fan out to multiple downstream MVs.

**Incorrect (separate consumer per MV — default behavior):**
```sql
-- Bad: 3 separate Kafka consumers for the same topic
CREATE MATERIALIZED VIEW mv_counts AS
SELECT event_type, COUNT(*) FROM user_events GROUP BY event_type;

CREATE MATERIALIZED VIEW mv_hourly AS
SELECT window_start, COUNT(*) FROM TUMBLE(user_events, ts, INTERVAL '1 HOUR')
GROUP BY window_start, window_end EMIT ON WINDOW CLOSE;

CREATE MATERIALIZED VIEW mv_users AS
SELECT user_id, MAX(ts) AS last_seen FROM user_events GROUP BY user_id;
-- 3 Kafka consumer groups, 3x bandwidth, 3x broker CPU
```

**Correct (shared source — one consumer, fan-out to all MVs):**
```sql
-- Good: enable shared source before creating MVs
SET streaming_use_shared_source = true;

-- Now all MVs from user_events share one SourceExecutor
CREATE MATERIALIZED VIEW mv_counts AS
SELECT event_type, COUNT(*) FROM user_events GROUP BY event_type;

CREATE MATERIALIZED VIEW mv_hourly AS
SELECT window_start, COUNT(*) FROM TUMBLE(user_events, ts, INTERVAL '1 HOUR')
GROUP BY window_start, window_end EMIT ON WINDOW CLOSE;

CREATE MATERIALIZED VIEW mv_users AS
SELECT user_id, MAX(ts) AS last_seen FROM user_events GROUP BY user_id;
-- 1 Kafka consumer group, 1x bandwidth
```

**Important:**
- `SET streaming_use_shared_source` is **session-scoped** — set it before each `CREATE MATERIALIZED VIEW`
- Existing MVs created without shared source are not automatically migrated
- Check if a source is shared: `SELECT name, is_shared FROM rw_catalog.rw_sources`

Reference: [Shared source](https://docs.risingwave.com/sql/commands/sql-create-source)
