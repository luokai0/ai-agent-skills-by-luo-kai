---
author: luo-kai
name: oc-android-3d-developer
version: 1.0.0
description: Help build and optimize 3D games and interactive experiences on Android, using engines and frameworks.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: kotlin-tools
---

# Android 3d Developer

You are an expert kotlin engineer. Help build and optimize 3D games and interactive experiences on Android, using engines and frameworks.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Android 3d Developer
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

data class Android3dDeveloperState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: String? = null
)

class Android3dDeveloperViewModel(
    private val repository: Android3dDeveloperRepository
) : ViewModel() {
    private val _state = MutableStateFlow(Android3dDeveloperState())
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
# Android 3d Developer — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "android-3d-developer",
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
logger = logging.getLogger("android-3d-developer")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"android-3d-developer error: {e}", exc_info=True)
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
- android-3d-developer-advanced
- performance-optimization
- error-handling
- testing-expert
