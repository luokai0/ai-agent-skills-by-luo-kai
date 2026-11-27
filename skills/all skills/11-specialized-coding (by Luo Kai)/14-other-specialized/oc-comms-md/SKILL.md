---
author: luo-kai
name: oc-comms-md
version: 1.0.0
description: Create a COMMS.md — a structured, queryable document expressing someone's communication preferences for humans.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: typescript-tools
---

# Comms Md

You are an expert typescript engineer. Create a COMMS.md — a structured, queryable document expressing someone's communication preferences for humans.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Comms Md
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
import Fastify from 'fastify';
import { Type, Static } from '@sinclair/typebox';

const app = Fastify({ logger: true });

const Schema = Type.Object({
    id: Type.String(),
    name: Type.String({ minLength: 1 }),
    tags: Type.Array(Type.String()),
});
type Item = Static<typeof Schema>;

const store = new Map<string, Item>();

app.get('/comms-md', {
    schema: { response: { 200: Type.Array(Schema) } },
    handler: async () => [...store.values()],
});

app.post<{ Body: Omit<Item, 'id'> }>('/comms-md', {
    schema: {
        body: Type.Omit(Schema, ['id']),
        response: { 201: Schema },
    },
    handler: async (req, reply) => {
        const item: Item = { id: crypto.randomUUID(), ...req.body };
        store.set(item.id, item);
        return reply.status(201).send(item);
    },
});

app.listen({ port: 3000 }).then(() => {
    console.log('Server: http://localhost:3000');
});
```

### Configuration & Setup
```typescript
# Comms Md — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "comms-md",
    "version": "1.0.0",
    "author": "luo-kai",
    "enabled": True,
    "debug": False,
    "timeout_seconds": 30,
    "max_retries": 3,
}
```

### Error Handling
```typescript
# Robust error handling pattern
import logging
logger = logging.getLogger("comms-md")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"comms-md error: {e}", exc_info=True)
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
- comms-md-advanced
- performance-optimization
- error-handling
- testing-expert
