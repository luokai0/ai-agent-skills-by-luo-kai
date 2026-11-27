---
title: Define watermarks at the ingestion point (source or table)
impact: HIGH
impactDescription: Watermarks defined on MVs instead of sources cause incorrect window behavior; watermarks must be set where data enters the system
tags: schema, watermark, event-time, emit-on-window-close, time-window, source, table
---

## Define watermarks at the ingestion point (source or table)

Watermarks declare how far behind event-time can lag before data is considered late. They must be defined on `CREATE SOURCE` or `CREATE TABLE` — the ingestion point — not inside `CREATE MATERIALIZED VIEW`. Watermarks propagate downstream to all MVs that read the source. Without a watermark, `EMIT ON WINDOW CLOSE` produces no output.

**Note:** In RisingWave 2.8+, `WATERMARK` on a `TABLE` requires the table to be `APPEND ONLY`. For mutable tables (CDC, upsert), define the watermark on a `CREATE SOURCE` instead.

**Incorrect (watermark in MV):**
```sql
-- Bad: watermarks cannot be defined inside a materialized view
CREATE MATERIALIZED VIEW hourly_stats AS
SELECT
    window_start, window_end, COUNT(*) AS cnt
FROM TUMBLE(
    sensor_readings,
    ts,  -- ts has no watermark defined → EMIT ON WINDOW CLOSE never fires
    INTERVAL '1 HOUR'
)
GROUP BY window_start, window_end
EMIT ON WINDOW CLOSE;
```

**Correct (watermark on source/table):**
```sql
-- Good: watermark defined at ingestion
CREATE SOURCE sensor_readings (
    sensor_id   INT,
    value       FLOAT,
    ts          TIMESTAMP,
    WATERMARK FOR ts AS ts - INTERVAL '30' SECOND
)
WITH (connector = 'kafka', topic = 'sensors', ...)
FORMAT PLAIN ENCODE JSON;

-- Now EMIT ON WINDOW CLOSE works correctly
CREATE MATERIALIZED VIEW hourly_stats AS
SELECT window_start, window_end, AVG(value) AS avg_value
FROM TUMBLE(sensor_readings, ts, INTERVAL '1 HOUR')
GROUP BY window_start, window_end
EMIT ON WINDOW CLOSE;
```

**Choosing the watermark interval:**
- Small interval (e.g., `5 SECOND`): tighter windows, more data may be considered late
- Large interval (e.g., `5 MINUTE`): tolerates more out-of-order data, windows close later
- Rule of thumb: set to the maximum expected out-of-order delay in your data

Reference: [Watermarks tutorial](https://tutorials.risingwave.com/docs/advanced/watermark/)
