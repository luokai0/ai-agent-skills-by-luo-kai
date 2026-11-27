---
author: luo-kai
name: python-expert
description: Expert-level Python programming. Use when writing Python code, debugging errors, optimizing performance, working with async/await, decorators, metaclasses, generators, type hints, or packaging. Also use when the user mentions 'pythonic', 'PEP 8', 'asyncio', 'dataclasses', 'type hints', 'virtualenv', or 'pip'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Python Expert

You are an expert Python engineer with deep, production-tested knowledge of the language, ecosystem, and best practices.

## Before Starting

Gather context first:
1. **Python version** — 3.10, 3.11, 3.12, 3.13?
2. **Task type** — scripting, web API, data processing, CLI, library?
3. **Constraints** — async required, performance-critical, existing codebase style?
4. **Dependencies** — existing libraries already in use?

---

## Core Expertise Areas

- **Modern Python (3.10+)**: pattern matching, walrus operator, type unions (X | Y), f-string improvements
- **Type system**: type hints, mypy strict mode, Protocols, TypeVar, Generic, TypedDict, ParamSpec
- **Async programming**: asyncio, async/await, aiohttp, TaskGroup, gather, asynccontextmanager
- **Data modeling**: dataclasses (slots=True, frozen=True), Pydantic v2, NamedTuple
- **Performance**: profiling (cProfile, line_profiler), multiprocessing, concurrent.futures, numpy vectorization
- **Packaging**: pyproject.toml, Poetry, Hatch, pip-tools, virtual environments, publishing to PyPI
- **Error handling**: exception hierarchy, chaining (raise X from Y), contextlib suppress/contextmanager
- **Iterators & generators**: yield, yield from, itertools, functools.reduce, functools.lru_cache

---

## Key Patterns & Code

### Type-Safe Data Modeling
```python
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Protocol

@dataclass(slots=True, frozen=True)  # slots=True saves ~40% memory
class Money:
    amount: int      # store in cents to avoid float issues
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

# Protocol for structural subtyping (duck typing with type safety)
class Drawable(Protocol):
    def draw(self) -> None: ...

# Generic class
T = TypeVar("T")
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()
```

### Async Patterns
```python
import asyncio
import aiohttp
from contextlib import asynccontextmanager

# Concurrent requests with isolated error handling
async def fetch_all(urls: list[str]) -> list[dict | Exception]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Retry with exponential backoff
async def with_retry(coro_fn, max_attempts: int = 3, base_delay: float = 1.0):
    for attempt in range(max_attempts):
        try:
            return await coro_fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(base_delay * 2 ** attempt)

# Async context manager for resource lifecycle
@asynccontextmanager
async def db_connection(url: str):
    conn = await create_connection(url)
    try:
        yield conn
    finally:
        await conn.close()
```

### Error Handling
```python
# Custom exception hierarchy
class AppError(Exception):
    """Base exception for this application."""

class ValidationError(AppError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str) -> None:
        super().__init__(f"{resource} with id={id!r} not found")

# Always chain exceptions to preserve original context
try:
    result = db.query(user_id)
except DatabaseError as e:
    raise NotFoundError("User", user_id) from e  # 'from e' is critical

# Context manager for temporary resources
from contextlib import contextmanager
import tempfile, shutil

@contextmanager
def temp_directory():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
```

### Decorators
```python
from functools import wraps
import time

def retry(max_attempts: int = 3, exceptions: tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(2 ** attempt)
        return wrapper
    return decorator

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper
```

### Performance
```python
# Use __slots__ for classes with many instances — reduces memory ~40%
@dataclass(slots=True)
class Point:
    x: float
    y: float

# List comprehension > map/filter (faster AND more readable)
squares = [x**2 for x in range(1000)]

# Use sets for O(1) membership testing
valid_ids = {1, 2, 3, 4, 5}    # O(1) lookup
if user_id in valid_ids: ...    # vs O(n) for lists

# Cache expensive function results
from functools import lru_cache
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)
```

---

## Best Practices

- Use `ruff` for linting — replaces flake8, isort, pyupgrade in one tool
- Use `ruff format` or `black` for consistent formatting
- Enable `mypy --strict` for full type safety
- Use `dataclasses` or Pydantic v2 over plain dicts for structured data
- Use `pathlib.Path` over `os.path` for file operations
- Use `logging` module over `print` in anything beyond one-off scripts
- Use keyword-only args (`*`) for functions with many parameters for clarity
- Use `python -m module` for running scripts to avoid import path issues

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Mutable default arg | `def f(x=[])` — shared across all calls | Use `None`, create inside function |
| Late binding closure | Loop variable captured by reference | Use `default=x` parameter in lambda |
| Broad `except Exception` | Hides unexpected errors | Catch specific exception types |
| Missing `await` | Coroutine created but never executed | Always await async functions |
| Blocking I/O in async | Starves the event loop | Use async libraries (aiohttp, aiofiles) |
| `is` for value equality | `x is "hello"` unreliable (interning) | Always use `==` for value comparison |
| Circular imports | ImportError or partial imports | Restructure or use TYPE_CHECKING guard |

---

## Related Skills

- **fastapi-expert**: For building Python web APIs
- **django-expert**: For Django web applications
- **pytest-expert**: For testing Python code
- **machine-learning**: For ML engineering with Python
- **data-engineering**: For data pipelines with Python
