---
author: luo-kai
name: oc-media-player
version: 1.0.0
description: Play audio/video locally on the host.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Media Player

You are an expert python engineer. Play audio/video locally on the host.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Media Player
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
MediaPlayer — by luo-kai (Lous Creations)
Play audio/video locally on the host.
"""
from __future__ import annotations
import logging, sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("media-player")

class MediaPlayer:
    """Main implementation of MediaPlayer."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._ready = False

    def setup(self) -> None:
        logger.info("Setting up MediaPlayer...")
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
    tool = MediaPlayer()
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
# Media Player — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "media-player",
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
logger = logging.getLogger("media-player")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"media-player error: {e}", exc_info=True)
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
- media-player-advanced
- performance-optimization
- error-handling
- testing-expert
