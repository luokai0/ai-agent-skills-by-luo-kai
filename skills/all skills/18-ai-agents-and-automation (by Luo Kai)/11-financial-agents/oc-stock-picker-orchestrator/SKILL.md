---
author: luo-kai
name: oc-stock-picker-orchestrator
version: 1.0.0
description: Acts as a meta-orchestrator that routes stock-analysis requests across data, macro/news, and valuation skills.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: python-tools
---

# Stock Picker Orchestrator

You are an expert python engineer. Acts as a meta-orchestrator that routes stock-analysis requests across data, macro/news, and valuation skills.

## Before Starting

1. **Goal** — what specific outcome do you need?
2. **Environment** — versions, platform, existing setup?
3. **Constraints** — performance, security, compatibility requirements?
4. **Integration** — what systems does this connect to?
5. **Output format** — code, config, script, or documentation?

---

## Core Expertise Areas

- **Core implementation** — full working code for Stock Picker Orchestrator
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
import anthropic
import json

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "search",
        "description": "Search for information on a topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]

def handle_tool(name: str, inputs: dict) -> str:
    if name == "search":
        return f"Search results for: {inputs['query']}"
    return f"Unknown tool: {name}"

def run_stock_picker_orchestrator(task: str, max_turns: int = 10) -> str:
    messages = [{"role": "user", "content": task}]
    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, 'text')), "")
        if response.stop_reason == "tool_use":
            results = [
                {"type": "tool_result", "tool_use_id": b.id,
                  "content": handle_tool(b.name, b.input)}
                for b in response.content if b.type == "tool_use"
            ]
            messages.append({"role": "user", "content": results})
    return "Max turns reached"

if __name__ == "__main__":
    result = run_stock_picker_orchestrator("StockPickerOrchestrator task: analyze and report")
    print(result)
```

### Configuration & Setup
```python
# Stock Picker Orchestrator — Configuration
# Author: luo-kai (Lous Creations)

config = {
    "name": "stock-picker-orchestrator",
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
logger = logging.getLogger("stock-picker-orchestrator")

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"stock-picker-orchestrator error: {e}", exc_info=True)
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
- stock-picker-orchestrator-advanced
- performance-optimization
- error-handling
- testing-expert
