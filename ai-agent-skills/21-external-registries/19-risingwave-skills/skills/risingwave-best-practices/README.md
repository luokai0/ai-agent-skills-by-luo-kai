# risingwave-best-practices skill

14 best-practice rules for RisingWave, organized by category and prioritized by impact. Covers schema design, materialized view patterns, CDC setup, sink configuration, and performance optimization.

**For agents:** This skill activates automatically when designing schemas, writing materialized views, configuring CDC, setting up sinks, or reviewing a RisingWave pipeline.

**For humans:** See [SKILL.md](./SKILL.md) for an overview, or browse the individual rules in [rules/](./rules/).

## Rules

| Rule | Impact |
|------|--------|
| [schema-source-vs-table](rules/schema-source-vs-table.md) | CRITICAL |
| [schema-append-only](rules/schema-append-only.md) | HIGH |
| [schema-watermark](rules/schema-watermark.md) | HIGH |
| [mv-emit-on-window-close](rules/mv-emit-on-window-close.md) | CRITICAL |
| [mv-background-ddl](rules/mv-background-ddl.md) | HIGH |
| [mv-no-order-by](rules/mv-no-order-by.md) | MEDIUM |
| [stream-tumble-windows](rules/stream-tumble-windows.md) | HIGH |
| [stream-cdc-pattern](rules/stream-cdc-pattern.md) | CRITICAL |
| [stream-temporal-join](rules/stream-temporal-join.md) | HIGH |
| [sink-snapshot-false](rules/sink-snapshot-false.md) | HIGH |
| [sink-force-compaction](rules/sink-force-compaction.md) | MEDIUM |
| [perf-shared-source](rules/perf-shared-source.md) | HIGH |
| [perf-indexes-on-mv](rules/perf-indexes-on-mv.md) | MEDIUM |
| [perf-parallelism](rules/perf-parallelism.md) | MEDIUM |

## Installation

```bash
npx skills add risingwavelabs/agent-skills --skill risingwave-best-practices
```
