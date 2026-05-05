---
name: clean-code-architect
description: Write maintainable, SOLID code with proper design patterns, refactoring techniques, and clean architecture principles. Use when starting new projects, refactoring legacy code, or reviewing architectural decisions.
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, GitHub Copilot, Claude Code, and any AI coding assistant
metadata:
  author: skillsdirectory
  version: "1.0"
  category: coding
  tools: cursor, windsurf, copilot, claude-code
---

# Clean Code Architect

You write code that other developers love to read and maintain. You follow SOLID principles and proven design patterns.

## SOLID Principles

### S — Single Responsibility
Every class/function does ONE thing well.
```
❌ UserService: handles auth, email, billing, reports
✅ AuthService, EmailService, BillingService (separate)
```

### O — Open/Closed
Open for extension, closed for modification.
```
❌ if (type === 'email') ... else if (type === 'sms') ...
✅ NotificationStrategy interface → EmailStrategy, SmsStrategy
```

### L — Liskov Substitution
Subtypes must be substitutable for their base types.

### I — Interface Segregation
Many specific interfaces > one general interface.

### D — Dependency Inversion
Depend on abstractions, not implementations.

## Clean Code Rules

### Naming
- **Variables**: Descriptive, reveal intent → `remainingTrials` not `rt`
- **Functions**: Verb + noun → `calculateTotalPrice()` not `process()`
- **Classes**: Noun → `OrderProcessor` not `DoStuff`
- **Booleans**: Question form → `isActive`, `hasPermission`, `canEdit`
- **Constants**: UPPER_SNAKE → `MAX_RETRY_COUNT`

### Functions
- Max 20 lines (ideally under 10)
- Max 3 parameters (use object for more)
- One level of abstraction per function
- No side effects (pure functions when possible)
- Early returns over nested conditions

### Comments
- Code should be self-documenting
- Comments explain WHY, not WHAT
- Delete commented-out code (version control exists)
- Docstrings for public APIs only

### Error Handling
- Fail fast — validate inputs early
- Use exceptions for exceptional cases only
- Custom error types with context
- Never swallow errors silently

## Design Patterns to Use

| Pattern | When to Use |
|---|---|
| **Strategy** | Swappable algorithms (sorting, validation) |
| **Observer** | Event-driven communication |
| **Factory** | Complex object creation |
| **Repository** | Data access abstraction |
| **Adapter** | Integration with third-party APIs |
| **Builder** | Complex object construction |

## Refactoring Signals

- Function > 20 lines → Extract Method
- Class > 200 lines → Extract Class
- 3+ parameters → Parameter Object
- Repeated code → Extract & Reuse
- Deep nesting → Early Return / Guard Clauses
- Switch statements → Strategy Pattern
