---
title: Use snapshot=false when adding sinks to existing materialized views
impact: HIGH
impactDescription: Without snapshot=false, adding a sink to an existing MV replays all historical MV data into the sink, causing duplicates and overwhelming downstream systems
tags: sink, snapshot, backfill, kafka, iceberg, duplicate-data
---

## Use snapshot=false when adding sinks to existing materialized views

When a sink is created for an existing materialized view, RisingWave by default sends all current MV data to the sink before switching to live streaming (snapshot mode). If the MV has been running for days or months, this means millions of rows are pushed to the sink on creation. For Kafka topics or databases that are already populated, this causes massive duplicates.

`snapshot = false` skips the historical backfill and starts emitting only new changes from the moment the sink is created.

**Incorrect (default — replays all existing MV data):**
```sql
-- Bad: existing MV has 30 days of data; all 50M rows go to Kafka immediately
CREATE SINK fraud_alerts_sink FROM fraud_detection_mv
WITH (
    connector = 'kafka',
    topic = 'fraud-alerts',
    properties.bootstrap.server = 'kafka:9092'
)
FORMAT PLAIN ENCODE JSON;
-- Downstream consumer overwhelmed with 50M duplicate historical records
```

**Correct (snapshot=false — new events only):**
```sql
-- Good: only emits changes that happen after this sink is created
CREATE SINK fraud_alerts_sink FROM fraud_detection_mv
WITH (
    connector = 'kafka',
    topic = 'fraud-alerts',
    properties.bootstrap.server = 'kafka:9092',
    snapshot = false   -- skip historical backfill
)
FORMAT PLAIN ENCODE JSON;
```

**When to omit snapshot=false (i.e., backfill IS desired):**
- Populating a brand-new downstream table/topic that has no data
- Initial load of a data warehouse sink where historical data is needed
- Disaster recovery: rebuilding a downstream system from scratch

**Default behavior:** `snapshot = true` (backfill is ON by default)

Reference: [CREATE SINK](https://docs.risingwave.com/sql/commands/sql-create-sink)
