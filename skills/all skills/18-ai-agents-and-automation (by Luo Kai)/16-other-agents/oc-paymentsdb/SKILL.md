---
author: luo-kai
name: oc-paymentsdb
version: 1.0.0
description: Query Stripe customer and billing data from a synced PostgreSQL database.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: sql-tools
---

# Paymentsdb

You are an expert sql engineer. Query Stripe customer and billing data from a synced PostgreSQL database.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Paymentsdb
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
-- paymentsdb schema — author: luo-kai
CREATE TABLE paymentsdb (
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

CREATE INDEX idx_paymentsdb_status ON paymentsdb(status) WHERE status != 'archived';
CREATE INDEX idx_paymentsdb_tags   ON paymentsdb USING GIN(tags);
CREATE INDEX idx_paymentsdb_meta   ON paymentsdb USING GIN(metadata);
CREATE INDEX idx_paymentsdb_ts     ON paymentsdb(created_at DESC);

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION update_ts()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$;
CREATE TRIGGER trg_paymentsdb_ts BEFORE UPDATE ON paymentsdb
    FOR EACH ROW EXECUTE FUNCTION update_ts();

ALTER TABLE paymentsdb ENABLE ROW LEVEL SECURITY;
```

### Configuration & Setup
```sql
# Paymentsdb — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "paymentsdb",
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
logger = logging.getLogger("paymentsdb")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"paymentsdb error: {e}", exc_info=True)
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
- paymentsdb-advanced
- performance-optimization
- error-handling
- testing-expert
