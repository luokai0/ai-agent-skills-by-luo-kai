---
title: Use TUMBLE/HOP/SESSION for time windows, not date_trunc
impact: HIGH
impactDescription: date_trunc in a streaming MV is treated as a non-temporal expression — late data handling, watermarks, and EMIT ON WINDOW CLOSE all require proper window table functions
tags: streaming, time-window, tumble, hop, session, date-trunc, aggregation, watermark
---

## Use TUMBLE/HOP/SESSION for time windows, not date_trunc

`date_trunc` is a scalar function that truncates a timestamp — it has no concept of window boundaries, watermarks, or late data. In streaming, RisingWave treats it as a regular column transform. Time window table functions (`TUMBLE`, `HOP`, `SESSION`) are recognized by the streaming planner and integrate with watermarks and `EMIT ON WINDOW CLOSE`.

**Incorrect (date_trunc — no window semantics):**
```sql
-- Bad: can't use EMIT ON WINDOW CLOSE, no watermark integration
CREATE MATERIALIZED VIEW events_per_minute AS
SELECT
    date_trunc('minute', event_time) AS minute_bucket,
    COUNT(*) AS cnt
FROM user_events
GROUP BY date_trunc('minute', event_time);
```

**Correct (TUMBLE — proper streaming window):**
```sql
-- Good: integrates with watermarks, supports EMIT ON WINDOW CLOSE
CREATE MATERIALIZED VIEW events_per_minute AS
SELECT
    window_start,
    window_end,
    COUNT(*) AS cnt
FROM TUMBLE(user_events, event_time, INTERVAL '1 MINUTE')
GROUP BY window_start, window_end
EMIT ON WINDOW CLOSE;
```

**Window function reference:**

| Function | Pattern | Use case |
|----------|---------|----------|
| `TUMBLE(t, col, size)` | `TUMBLE(events, ts, INTERVAL '5 MIN')` | Non-overlapping fixed windows |
| `HOP(t, col, hop, size)` | `HOP(events, ts, INTERVAL '1 MIN', INTERVAL '5 MIN')` | Sliding windows; each row appears in `size/hop` windows |
| `SESSION(col, gap)` | batch mode only (not supported in streaming in 2.x) | Event-gap based grouping |

**Always include `window_start` and `window_end` in GROUP BY** — these are the window identity columns.

**`EMIT ON WINDOW CLOSE` requires `window_start, window_end` in GROUP BY** and a watermark on the source.

Reference: [Time Windows](https://docs.risingwave.com/processing/sql/time-windows)
