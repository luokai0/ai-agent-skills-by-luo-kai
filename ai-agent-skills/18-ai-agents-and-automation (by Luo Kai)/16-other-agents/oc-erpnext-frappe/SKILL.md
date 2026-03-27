---
author: luo-kai
name: oc-erpnext-frappe
version: 1.0.0
description: High-level business workflows that combine multiple MCP tools into reusable, executable skills for ERPNext.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: typescript-tools
---

# Erpnext Frappe

You are an expert typescript engineer. High-level business workflows that combine multiple MCP tools into reusable, executable skills for ERPNext.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Erpnext Frappe
- **Error handling** — robust error recovery and logging
- **Performance** — optimized patterns for production use
- **Testing** — unit and integration test strategies
- **Configuration** — environment-specific setup and tuning
- **Security** — secure coding patterns and best practices
- **Documentation** — clear API and usage documentation

---

## Key Patterns & Code

### Core Implementation

```typescript
import { useState, useCallback, memo } from 'react';
import { useQuery } from '@tanstack/react-query';

interface ErpnextFrappeProps {
    className?: string;
    onSelect?: (id: string) => void;
}

export const ErpnextFrappe = memo(function ErpnextFrappe({ className, onSelect }: ErpnextFrappeProps) {
    const [selected, setSelected] = useState<string | null>(null);

    const { data, isLoading, error } = useQuery({
        queryKey: ['erpnext-frappe'],
        queryFn: () => fetch('/api/erpnext-frappe').then((r) => r.json()),
        staleTime: 30_000,
    });

    const handleSelect = useCallback((id: string) => {
        setSelected(id);
        onSelect?.(id);
    }, [onSelect]);

    if (isLoading) return <div className="animate-pulse">Loading...</div>;
    if (error) return <div className="text-red-500">Error loading data</div>;

    return (
        <div className={`space-y-2 ${className ?? ''}`}>
            {data?.map((item: { id: string; name: string }) => (
                <button
                    key={item.id}
                    onClick={() => handleSelect(item.id)}
                    className={`p-3 rounded border ${
                        selected === item.id
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                    }`}
                >
                    {item.name}
                </button>
            ))}
        </div>
    );
});
```

### Configuration & Setup
```tsx
# Erpnext Frappe — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "erpnext-frappe",
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
logger = logging.getLogger("erpnext-frappe")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"erpnext-frappe error: {e}", exc_info=True)
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
- erpnext-frappe-advanced
- performance-optimization
- error-handling
- testing-expert
