---
author: luo-kai
name: oc-neo-py-memory-optimizer
version: 1.0.0
description: Automatically analyzes Python code and suggests memory usage optimizations for improved performance.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Neo Py Memory Optimizer

You are an expert python engineer. Automatically analyzes Python code and suggests memory usage optimizations for improved performance.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Neo Py Memory Optimizer
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

app = FastAPI(title="NeoPyMemoryOptimizer", version="1.0.0")

class NeoPyMemoryOptimizerItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: Annotated[str, Field(min_length=1, max_length=200)]
    description: str | None = None
    tags: list[str] = []

class NeoPyMemoryOptimizerResponse(NeoPyMemoryOptimizerItem):
    id: str

store: dict[str, NeoPyMemoryOptimizerResponse] = {}

@app.get("/neo-py-memory-optimizer", response_model=list[NeoPyMemoryOptimizerResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[NeoPyMemoryOptimizerResponse]:
    return list(store.values())[skip:skip + limit]

@app.post("/neo-py-memory-optimizer", response_model=NeoPyMemoryOptimizerResponse, status_code=201)
async def create_item(payload: NeoPyMemoryOptimizerItem) -> NeoPyMemoryOptimizerResponse:
    import uuid
    item = NeoPyMemoryOptimizerResponse(id=str(uuid.uuid4()), **payload.model_dump())
    store[item.id] = item
    return item

@app.get("/neo-py-memory-optimizer/{item_id}")
async def get_item(item_id: str) -> NeoPyMemoryOptimizerResponse:
    if item_id not in store:
        raise HTTPException(404, f"Item {item_id!r} not found")
    return store[item_id]
```

### Configuration & Setup
```python
# Neo Py Memory Optimizer — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "neo-py-memory-optimizer",
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
logger = logging.getLogger("neo-py-memory-optimizer")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"neo-py-memory-optimizer error: {e}", exc_info=True)
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
- neo-py-memory-optimizer-advanced
- performance-optimization
- error-handling
- testing-expert
