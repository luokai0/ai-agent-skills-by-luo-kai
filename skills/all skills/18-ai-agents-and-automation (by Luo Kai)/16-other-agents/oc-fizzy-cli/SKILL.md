---
author: luo-kai
name: oc-fizzy-cli
version: 1.0.0
description: Use the fizzy-cli tool to authenticate and manage Fizzy kanban.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Fizzy Cli

You are an expert python engineer. Use the fizzy-cli tool to authenticate and manage Fizzy kanban.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Fizzy Cli
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
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
import re, html, hashlib, secrets

class FizzyCliSecureInput(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: str
    content: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Alphanumeric, _ and - only')
        return v

    @field_validator('content')
    @classmethod
    def sanitize(cls, v: str) -> str:
        return html.escape(v)  # Prevent XSS

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return f"{salt}:{h.hex()}"

def verify_password(password: str, stored: str) -> bool:
    salt, hash_hex = stored.split(':')
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return secrets.compare_digest(h.hex(), hash_hex)

# Safe parameterized DB query (NEVER string interpolation)
async def get_user(conn, user_id: str):
    return await conn.fetchrow(
        "SELECT id, email FROM users WHERE id = $1", user_id
    )
```

### Configuration & Setup
```python
# Fizzy Cli — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "fizzy-cli",
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
logger = logging.getLogger("fizzy-cli")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"fizzy-cli error: {e}", exc_info=True)
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
- fizzy-cli-advanced
- performance-optimization
- error-handling
- testing-expert
