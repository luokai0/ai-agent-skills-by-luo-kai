---
author: luo-kai
name: oc-george
version: 1.0.0
description: Automate George online banking (Erste Bank / Sparkasse Austria)
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# George

You are an expert python engineer. Automate George online banking (Erste Bank / Sparkasse Austria)

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for George
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```python
import polars as pl
from pathlib import Path
import logging

logger = logging.getLogger("george")

def extract(source: str) -> pl.DataFrame:
    logger.info(f"Extracting from {source}")
    return pl.read_parquet(source)

def transform(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .filter(pl.col("id").is_not_null())
        .with_columns([
            pl.col("name").str.strip_chars().str.to_lowercase(),
            pl.col("created_at").cast(pl.Datetime("us")),
        ])
        .unique(subset=["id"], keep="last")
        .sort("created_at", descending=True)
    )

def load(df: pl.DataFrame, dest: str) -> None:
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(dest, compression="zstd", statistics=True)
    logger.info(f"Wrote {len(df)} rows to {dest}")

def run_george(source: str, dest: str) -> dict:
    raw = extract(source)
    clean = transform(raw)
    load(clean, dest)
    return {"input": len(raw), "output": len(clean),
             "dropped": len(raw) - len(clean)}
```

### Configuration & Setup
```python
# George — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "george",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```python
# Robust error handling pattern
import logging
logger = logging.getLogger("george")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"george error: {e}", exc_info=True)
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

- python-expert
- george-advanced
- performance-optimization
- error-handling
- testing-expert
