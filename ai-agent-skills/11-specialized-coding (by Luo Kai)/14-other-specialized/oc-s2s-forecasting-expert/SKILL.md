---
author: luo-kai
name: oc-s2s-forecasting-expert
version: 1.0.0
description: End-to-end builder for AI-based Subseasonal-to-Seasonal (S2S) forecasting systems.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# S2s Forecasting Expert

You are an expert python engineer. End-to-end builder for AI-based Subseasonal-to-Seasonal (S2S) forecasting systems.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for S2s Forecasting Expert
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
#!/usr/bin/env python3
"""
S2sForecastingExpert — by luo-kai (Lous Creations)
End-to-end builder for AI-based Subseasonal-to-Seasonal (S2S) forecasting system
"""
from __future__ import annotations
import logging, sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("s2s-forecasting-expert")

class S2sForecastingExpert:
    """Main implementation of S2sForecastingExpert."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._ready = False

    def setup(self) -> None:
        logger.info("Setting up S2sForecastingExpert...")
        self._ready = True

    def run(self, input_data: Any) -> dict[str, Any]:
        if not self._ready:
            self.setup()
        logger.info("Processing...")
        result = self._process(input_data)
        return {"success": True, "result": result, "author": "luo-kai"}

    def _process(self, data: Any) -> Any:
        return data  # Override with real logic

def main() -> int:
    tool = S2sForecastingExpert()
    try:
        tool.setup()
        result = tool.run(sys.argv[1:])
        print(f"Done: {result['result']}")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Configuration & Setup
```python
# S2s Forecasting Expert — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "s2s-forecasting-expert",
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
logger = logging.getLogger("s2s-forecasting-expert")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"s2s-forecasting-expert error: {e}", exc_info=True)
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
- s2s-forecasting-expert-advanced
- performance-optimization
- error-handling
- testing-expert
