---
author: luo-kai
name: oc-sql-query-generator
version: 1.0.0
description: Generate secure SQL queries with validation, pagination helpers, risk analysis, and audit-focused safeguards.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: sql-tools
---

# Sql Query Generator

You are an expert sql engineer. Generate secure SQL queries with validation, pagination helpers, risk analysis, and audit-focused safeguards.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Sql Query Generator
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```sql
-- sql-query-generator schema — author: luo-kai
CREATE TABLE sql_query_generator (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 200),
    description TEXT,
    metadata    JSONB NOT NULL DEFAULT '{}'::jsonb,
    tags        TEXT[] NOT NULL DEFAULT '{}',
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'inactive', 'archived')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_sql_query_generator_status ON sql_query_generator(status) WHERE status != 'archived';
CREATE INDEX idx_sql_query_generator_tags   ON sql_query_generator USING GIN(tags);
CREATE INDEX idx_sql_query_generator_meta   ON sql_query_generator USING GIN(metadata);
CREATE INDEX idx_sql_query_generator_ts     ON sql_query_generator(created_at DESC);

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_ts()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$;
CREATE TRIGGER trg_sql_query_generator_ts BEFORE UPDATE ON sql_query_generator
    FOR EACH ROW EXECUTE FUNCTION update_ts();

ALTER TABLE sql_query_generator ENABLE ROW LEVEL SECURITY;
```

### Configuration & Setup
```sql
# Sql Query Generator — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "sql-query-generator",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```sql
# Robust error handling pattern
import logging
logger = logging.getLogger("sql-query-generator")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"sql-query-generator error: {e}", exc_info=True)
        raise
```

---

## Best Practices

- **Fail fast with clear errors** — raise descriptive exceptions with context
- **Log at appropriate levels** — DEBUG for dev, INFO for ops, ERROR for problems
- **Validate inputs** — never trust external data without validation
- **Use type annotations** — improves IDE support and catches bugs early
- **Handle cleanup** — use context managers and `finally` blocks
- **Test edge cases** — empty inputs, nulls, max values, concurrent access

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| No error handling | Silent failures in production | Wrap with try/except + logging |
| Hardcoded values | Not portable across environments | Use config/env vars |
| Missing timeouts | Hangs indefinitely | Always set timeout values |
| No retry logic | Single failure = broken workflow | Add exponential backoff |
| No cleanup on exit | Resource leaks | Use context managers |

---

## Related Skills

- sql-expert
- sql-query-generator-advanced
- performance-optimization
- error-handling
- testing-expert
