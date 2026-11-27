---
author: luo-kai
name: oc-healthkit-sync
version: 1.0.0
description: iOS HealthKit data sync CLI commands and patterns.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: swift-tools
---

# Healthkit Sync

You are an expert swift engineer. iOS HealthKit data sync CLI commands and patterns.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Healthkit Sync
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```swift
import Foundation
import SwiftUI

@Observable
class HealthkitSyncViewModel {
    var isLoading = false
    var items: [Item] = []
    var error: String?

    func load() async {
        isLoading = true
        defer { isLoading = false }
        do {
            let url = URL(string: "https://api.example.com/healthkit-sync")!
            let (data, _) = try await URLSession.shared.data(from: url)
            items = try JSONDecoder().decode([Item].self, from: data)
        } catch {
            error = error.localizedDescription
        }
    }
}

struct HealthkitSyncView: View {
    @State private var vm = HealthkitSyncViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if vm.isLoading { ProgressView() }
                else { List(vm.items) { i in Text(i.name) } }
            }
            .navigationTitle("HealthkitSync")
            .task { await vm.load() }
        }
    }
}
```

### Configuration & Setup
```swift
# Healthkit Sync — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "healthkit-sync",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```swift
# Robust error handling pattern
import logging
logger = logging.getLogger("healthkit-sync")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"healthkit-sync error: {e}", exc_info=True)
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

- swift-expert
- healthkit-sync-advanced
- performance-optimization
- error-handling
- testing-expert
