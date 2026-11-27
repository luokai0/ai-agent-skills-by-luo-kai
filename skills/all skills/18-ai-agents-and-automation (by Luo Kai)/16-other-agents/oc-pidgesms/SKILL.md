---
author: luo-kai
name: oc-pidgesms
version: 1.0.0
description: Send and read SMS text messages via an Android phone using pidge.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: kotlin-tools
---

# Pidgesms

You are an expert kotlin engineer. Send and read SMS text messages via an Android phone using pidge.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Pidgesms
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

data class PidgesmsState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: String? = null
)

class PidgesmsViewModel(
    private val repository: PidgesmsRepository
) : ViewModel() {
    private val _state = MutableStateFlow(PidgesmsState())
    val state = _state.asStateFlow()

    init { load() }

    fun refresh() = load()

    private fun load() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            repository.getAll()
                .onSuccess { items -> _state.update { it.copy(isLoading = false, items = items) } }
                .onFailure { e -> _state.update { it.copy(isLoading = false, error = e.message) } }
        }
    }
}
```

### Configuration & Setup
```kotlin
# Pidgesms — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "pidgesms",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```kotlin
# Robust error handling pattern
import logging
logger = logging.getLogger("pidgesms")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"pidgesms error: {e}", exc_info=True)
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

- kotlin-expert
- pidgesms-advanced
- performance-optimization
- error-handling
- testing-expert
