# Rule Sections

| Priority | Category | Impact | Prefix | Description |
|----------|----------|--------|--------|-------------|
| 1 | Schema Design | CRITICAL | `schema-` | Source vs Table selection, append-only, watermarks |
| 2 | Materialized Views | CRITICAL/HIGH | `mv-` | Emit semantics, DDL for large tables |
| 3 | Streaming SQL | CRITICAL/HIGH | `stream-` | CDC pattern, time window functions |
| 4 | Sink Configuration | HIGH/MEDIUM | `sink-` | Snapshot behavior, output compaction |
| 5 | Performance | HIGH/MEDIUM | `perf-` | Shared source, MV indexing |
