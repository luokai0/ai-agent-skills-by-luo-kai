---
title: Use EMIT ON WINDOW CLOSE for windowed aggregations
impact: CRITICAL
impactDescription: Without EOWC, downstream consumers receive hundreds of partial intermediate results per window; with EOWC, they receive exactly one final result per window
tags: materialized-view, emit-on-window-close, watermark, tumble, hop, time-window, aggregation
---

## Use EMIT ON WINDOW CLOSE for windowed aggregations

> **Note:** `EMIT ON WINDOW CLOSE` is currently an experimental feature. RisingWave will issue a NOTICE when you use it. It is functional but the interface may change in future versions.

By default, RisingWave emits result updates after every checkpoint barrier (typically every 1 second). For a windowed aggregation like `TUMBLE(... INTERVAL '1 HOUR')`, this means a single 1-hour window emits thousands of intermediate partial results. `EMIT ON WINDOW CLOSE` (EOWC) buffers results until the watermark passes the window end, then emits exactly one final, immutable result.

EOWC requires a watermark on the input source or table.

**Incorrect (default emit — floods downstream with partial results):**
```sql
-- Bad: emits a partial count after every checkpoint during the hour
CREATE MATERIALIZED VIEW events_per_hour AS
SELECT
    event_type,
    COUNT(*) AS event_count,
    window_start,
    window_end
FROM TUMBLE(events, event_time, INTERVAL '1 HOUR')
GROUP BY event_type, window_start, window_end;
-- downstream sink/consumer sees: count=1, count=5, count=47, ..., count=9821 for same window
```

**Correct (EMIT ON WINDOW CLOSE — one final result per window):**
```sql
-- Good: one immutable result emitted when watermark passes window_end
CREATE MATERIALIZED VIEW events_per_hour AS
SELECT
    event_type,
    COUNT(*) AS event_count,
    window_start,
    window_end
FROM TUMBLE(events, event_time, INTERVAL '1 HOUR')
GROUP BY event_type, window_start, window_end
EMIT ON WINDOW CLOSE;
-- downstream sink/consumer sees: count=9821 (once, final)
```

**When to use EOWC:**
- Any windowed aggregation (TUMBLE, HOP, SESSION) that feeds a sink or downstream consumer
- Reporting/analytics where partial results would be confusing or cause duplicates
- Iceberg/warehouse sinks where partial results cause data quality issues

**When NOT to use EOWC:**
- Low-latency dashboards that should show live running totals
- Non-windowed aggregations (no window_start/window_end)
- Cases where the source has no watermark (EOWC will never emit)

Reference: [Emit on Window Close](https://docs.risingwave.com/processing/emit-on-window-close)
