---
author: luo-kai
name: oc-comonyx-admin
version: 1.0.0
description: Admin skill to sign into Cosmonyx, fetch companies, filter/export (PDF or Excel), optionally email the export.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: typescript-tools
---

# Comonyx Admin

You are an expert typescript engineer. Admin skill to sign into Cosmonyx, fetch companies, filter/export (PDF or Excel), optionally email the export.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Comonyx Admin
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```tsx
import React from 'react';
import { View, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { SafeAreaView } from 'react-native-safe-area-context';

type Item = { id: string; title: string };

async function fetchComonyxAdmin(): Promise<Item[]> {
    const res = await fetch('https://api.example.com/comonyx-admin');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

export function ComonyxAdminScreen() {
    const { data, isLoading, refetch } = useQuery({
        queryKey: ['comonyx-admin'],
        queryFn: fetchComonyxAdmin,
        staleTime: 5 * 60_000,
    });

    if (isLoading) return <ActivityIndicator style={styles.center} size="large" />;

    return (
        <SafeAreaView style={styles.container}>
            <FlatList
                data={data}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <View style={styles.row}>
                        {/* item.title */}
                    </View>
                )}
                onRefresh={refetch}
                refreshing={isLoading}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
    row: { padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee' },
});
```

### Configuration & Setup
```tsx
# Comonyx Admin — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "comonyx-admin",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```tsx
# Robust error handling pattern
import logging
logger = logging.getLogger("comonyx-admin")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"comonyx-admin error: {e}", exc_info=True)
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

- typescript-expert
- comonyx-admin-advanced
- performance-optimization
- error-handling
- testing-expert
