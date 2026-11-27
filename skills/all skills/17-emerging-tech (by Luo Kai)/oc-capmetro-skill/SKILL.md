---
author: luo-kai
name: oc-capmetro-skill
version: 1.0.0
description: Austin CapMetro transit — real-time vehicle positions, next arrivals, service alerts, route info, and trip planning for buses and rail.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: typescript-tools
---

# Capmetro Skill

You are an expert typescript engineer. Austin CapMetro transit — real-time vehicle positions, next arrivals, service alerts, route info, and trip planning for buses and rail.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Capmetro Skill
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

interface CapmetroSkillProps {
    className?: string;
    onSelect?: (id: string) => void;
}

export const CapmetroSkill = memo(function CapmetroSkill({ className, onSelect }: CapmetroSkillProps) {
    const [selected, setSelected] = useState<string | null>(null);

    const { data, isLoading, error } = useQuery({
        queryKey: ['capmetro-skill'],
        queryFn: () => fetch('/api/capmetro-skill').then((r) => r.json()),
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
# Capmetro Skill — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "capmetro-skill",
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
logger = logging.getLogger("capmetro-skill")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"capmetro-skill error: {e}", exc_info=True)
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
- capmetro-skill-advanced
- performance-optimization
- error-handling
- testing-expert
