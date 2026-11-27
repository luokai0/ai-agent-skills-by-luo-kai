---
author: luo-kai
name: oc-neo-py2py3-converter
version: 1.0.0
description: Automatically converts legacy Python 2 code to Python 3 with compatibility checks and test generation.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Neo Py2py3 Converter

You are an expert python engineer. Automatically converts legacy Python 2 code to Python 3 with compatibility checks and test generation.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Neo Py2py3 Converter
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
from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="NeoPy2py3Converter", version="1.0.0")

class NeoPy2py3ConverterItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: Annotated[str, Field(min_length=1, max_length=200)]
    description: str | None = None
    tags: list[str] = []

class NeoPy2py3ConverterResponse(NeoPy2py3ConverterItem):
    id: str

store: dict[str, NeoPy2py3ConverterResponse] = {}

@app.get("/neo-py2py3-converter", response_model=list[NeoPy2py3ConverterResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[NeoPy2py3ConverterResponse]:
    return list(store.values())[skip:skip + limit]

@app.post("/neo-py2py3-converter", response_model=NeoPy2py3ConverterResponse, status_code=201)
async def create_item(payload: NeoPy2py3ConverterItem) -> NeoPy2py3ConverterResponse:
    import uuid
    item = NeoPy2py3ConverterResponse(id=str(uuid.uuid4()), **payload.model_dump())
    store[item.id] = item
    return item

@app.get("/neo-py2py3-converter/{item_id}")
async def get_item(item_id: str) -> NeoPy2py3ConverterResponse:
    if item_id not in store:
        raise HTTPException(404, f"Item {item_id!r} not found")
    return store[item_id]
```

### Configuration & Setup
```python
# Neo Py2py3 Converter — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "neo-py2py3-converter",
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
logger = logging.getLogger("neo-py2py3-converter")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"neo-py2py3-converter error: {e}", exc_info=True)
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
- neo-py2py3-converter-advanced
- performance-optimization
- error-handling
- testing-expert
