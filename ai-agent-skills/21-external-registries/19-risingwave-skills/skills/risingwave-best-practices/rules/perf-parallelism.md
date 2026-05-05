---
title: Increase parallelism for high-throughput materialized views
impact: MEDIUM
impactDescription: Default parallelism may saturate a single core on high-volume topics; increasing parallelism distributes processing across cores and nodes linearly
tags: performance, parallelism, throughput, materialized-view, kafka, scaling
---

## Increase parallelism for high-throughput materialized views

RisingWave assigns each streaming job a default parallelism based on the cluster configuration. For high-volume Kafka topics (millions of events/second) or compute-intensive MVs, the default may be insufficient. Setting explicit parallelism distributes the MV's fragments across more CPU cores and worker nodes.

**Incorrect (default parallelism — may bottleneck on high-volume sources):**
```sql
-- Bad: uses cluster default parallelism, may saturate at high event rates
CREATE MATERIALIZED VIEW high_volume_stats AS
SELECT event_type, COUNT(*) AS cnt
FROM high_volume_events
GROUP BY event_type;
```

**Correct (explicit parallelism via session variable):**
```sql
-- Good: set parallelism before CREATE, applies to the next DDL statement
SET streaming_parallelism = 16;

CREATE MATERIALIZED VIEW high_volume_stats AS
SELECT event_type, COUNT(*) AS cnt
FROM high_volume_events
GROUP BY event_type;
```

**How to choose parallelism:**
- Start with the number of Kafka partitions (parallelism > partitions provides no benefit for source reads)
- For CPU-bound MVs (complex aggregations, joins), match the total vCPU count of streaming nodes
- Monitor streaming node CPU via the dashboard at port `5691` or Grafana at port `3001`

**Check current parallelism:**
```sql
SELECT name, parallelism, max_parallelism
FROM rw_catalog.rw_streaming_jobs
WHERE name = 'high_volume_stats';
```

**Alter parallelism on an existing MV:**
```sql
ALTER MATERIALIZED VIEW high_volume_stats SET PARALLELISM = 32;
```

Reference: [Streaming job parallelism](https://docs.risingwave.com/sql/commands/sql-create-mv)
