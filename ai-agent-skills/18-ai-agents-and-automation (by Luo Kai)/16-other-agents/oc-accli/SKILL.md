---
author: luo-kai
name: oc-accli
version: 1.0.0
description: This skill should be used when interacting with Apple Calendar on macOS.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: bash-tools
---

# Accli

You are an expert bash engineer. This skill should be used when interacting with Apple Calendar on macOS.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Accli
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```bash
#!/bin/zsh
# accli — by luo-kai (Lous Creations)
# This skill should be used when interacting with Apple Calend
set -euo pipefail

RED='\033[0;31m' GREEN='\033[0;32m' NC='\033[0m'
log_ok()  { echo "${GREEN}[OK]${NC} $1"; }
log_err() { echo "${RED}[ERR]${NC} $1"; exit 1; }

main() {
    log_ok "Starting accli..."
    [[ -d "$HOME" ]] || log_err "Home directory not found"
    local version; version=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
    log_ok "macOS: $version | Free: $(df -h / | awk 'NR==2{print $4}')"
    log_ok "Done!"
}

main "$@"
```

### Configuration & Setup
```bash
# Accli — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "accli",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```bash
# Robust error handling pattern
import logging
logger = logging.getLogger("accli")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"accli error: {e}", exc_info=True)
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

- bash-expert
- accli-advanced
- performance-optimization
- error-handling
- testing-expert
