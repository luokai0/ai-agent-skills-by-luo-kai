---
author: luo-kai
name: oc-db-readonly
version: 1.0.0
description: Run safe read-only queries against MySQL or PostgreSQL for data inspection, reporting, and troubleshooting.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: sql-tools
---

# Db Readonly

You are an expert sql engineer. Run safe read-only queries against MySQL or PostgreSQL for data inspection, reporting, and troubleshooting.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Db Readonly
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
-- db-readonly schema — author: luo-kai
CREATE TABLE db_readonly (
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

CREATE INDEX idx_db_readonly_status ON db_readonly(status) WHERE status != 'archived';
CREATE INDEX idx_db_readonly_tags   ON db_readonly USING GIN(tags);
CREATE INDEX idx_db_readonly_meta   ON db_readonly USING GIN(metadata);
CREATE INDEX idx_db_readonly_ts     ON db_readonly(created_at DESC);

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_ts()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$;
CREATE TRIGGER trg_db_readonly_ts BEFORE UPDATE ON db_readonly
    FOR EACH ROW EXECUTE FUNCTION update_ts();

ALTER TABLE db_readonly ENABLE ROW LEVEL SECURITY;
```

### Configuration & Setup
```sql
# Db Readonly — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "db-readonly",
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
logger = logging.getLogger("db-readonly")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"db-readonly error: {e}", exc_info=True)
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
- db-readonly-advanced
- performance-optimization
- error-handling
- testing-expert
