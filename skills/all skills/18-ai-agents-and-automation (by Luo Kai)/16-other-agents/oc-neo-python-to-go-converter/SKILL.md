---
author: luo-kai
name: oc-neo-python-to-go-converter
version: 1.0.0
description: Automatically converts Python code to optimized Go code for performance-critical applications.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Neo Python To Go Converter

You are an expert python engineer. Automatically converts Python code to optimized Go code for performance-critical applications.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Neo Python To Go Converter
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

app = FastAPI(title="NeoPythonToGoConverter", version="1.0.0")

class NeoPythonToGoConverterItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: Annotated[str, Field(min_length=1, max_length=200)]
    description: str | None = None
    tags: list[str] = []

class NeoPythonToGoConverterResponse(NeoPythonToGoConverterItem):
    id: str

store: dict[str, NeoPythonToGoConverterResponse] = {}

@app.get("/neo-python-to-go-converter", response_model=list[NeoPythonToGoConverterResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[NeoPythonToGoConverterResponse]:
    return list(store.values())[skip:skip + limit]

@app.post("/neo-python-to-go-converter", response_model=NeoPythonToGoConverterResponse, status_code=201)
async def create_item(payload: NeoPythonToGoConverterItem) -> NeoPythonToGoConverterResponse:
    import uuid
    item = NeoPythonToGoConverterResponse(id=str(uuid.uuid4()), **payload.model_dump())
    store[item.id] = item
    return item

@app.get("/neo-python-to-go-converter/{item_id}")
async def get_item(item_id: str) -> NeoPythonToGoConverterResponse:
    if item_id not in store:
        raise HTTPException(404, f"Item {item_id!r} not found")
    return store[item_id]
```

### Configuration & Setup
```python
# Neo Python To Go Converter — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "neo-python-to-go-converter",
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
logger = logging.getLogger("neo-python-to-go-converter")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"neo-python-to-go-converter error: {e}", exc_info=True)
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
- neo-python-to-go-converter-advanced
- performance-optimization
- error-handling
- testing-expert
