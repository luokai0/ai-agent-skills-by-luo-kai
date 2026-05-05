---
title: Use force_compaction to reduce output volume for upsert sinks
impact: MEDIUM
impactDescription: Without force_compaction, high-cardinality upsert sinks emit multiple intermediate updates per key per second; force_compaction deduplicates to at most one per barrier
tags: sink, force-compaction, upsert, kafka, performance, output-volume
---

## Use force_compaction to reduce output volume for upsert sinks

RisingWave processes streaming changes in barrier intervals (typically 1 second). For a high-activity key (e.g., a user's running total), multiple updates may be emitted within a single barrier. For upsert sinks (Kafka compacted topics, Redis, databases), downstream systems must process all intermediate states even though only the final state matters.

`force_compaction = true` merges multiple updates for the same key within a barrier into a single output message — the most recent state only.

**Incorrect (multiple updates per key per barrier):**
```sql
-- Bad: user_id=123 may emit 50 partial updates per second if highly active
CREATE SINK user_stats_redis FROM user_stats_mv
WITH (
    connector = 'redis',
    redis.url = 'redis://localhost:6379',
    primary_key = 'user_id'
)
FORMAT UPSERT ENCODE JSON;
-- Redis receives: {user_id:123, score:1}, {user_id:123, score:2}, ..., {user_id:123, score:50}
-- 49 unnecessary writes, all but last are overwritten immediately
```

**Correct (force_compaction — one update per key per barrier):**
```sql
-- Good: at most one Redis write per user_id per barrier interval
CREATE SINK user_stats_redis FROM user_stats_mv
WITH (
    connector = 'redis',
    redis.url = 'redis://localhost:6379',
    primary_key = 'user_id',
    force_compaction = true
)
FORMAT UPSERT ENCODE JSON;
-- Redis receives: {user_id:123, score:50} (once per barrier)
```

**When to use `force_compaction = true`:**
- Upsert sinks where only the latest state per key matters
- Redis, Elasticsearch, database UPSERT sinks
- Kafka compacted topics
- Any sink where downstream processes all messages (not just latest)

**When NOT to use:**
- Append-only sinks (FORMAT PLAIN) where every event is distinct
- Audit log sinks where intermediate states must be preserved
- CDC pipelines where every change event has semantic meaning

Reference: [CREATE SINK options](https://docs.risingwave.com/sql/commands/sql-create-sink)
