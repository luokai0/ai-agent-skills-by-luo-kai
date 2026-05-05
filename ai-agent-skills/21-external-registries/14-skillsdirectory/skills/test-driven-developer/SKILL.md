---
name: test-driven-developer
description: Write bulletproof code using Test-Driven Development (TDD) with proper unit tests, integration tests, mocking, and test architecture. Use when implementing features test-first or improving test coverage.
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, GitHub Copilot, Claude Code, and any AI coding assistant
metadata:
  author: skillsdirectory
  version: "1.0"
  category: coding
  tools: cursor, windsurf, copilot, claude-code
---

# Test-Driven Developer

You write tests first, then code. Every feature starts with a failing test.

## TDD Cycle (Red-Green-Refactor)

```
1. 🔴 RED    → Write a failing test
2. 🟢 GREEN  → Write minimal code to pass
3. 🔵 REFACTOR → Clean up without breaking tests
4. ↩️ REPEAT
```

## Test Types

### Unit Tests (Fast, Isolated)
```typescript
// Test ONE function/method in isolation
describe('calculateDiscount', () => {
  it('should apply 10% discount for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(15)
  })
  
  it('should return 0 for orders under $100', () => {
    expect(calculateDiscount(50)).toBe(0)
  })
  
  it('should throw for negative amounts', () => {
    expect(() => calculateDiscount(-10)).toThrow('Invalid amount')
  })
})
```

### Integration Tests (Components Working Together)
```typescript
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' })
    
    expect(response.status).toBe(201)
    expect(response.body.data.name).toBe('John')
  })
})
```

### E2E Tests (Full User Flows)
```typescript
test('user can sign up and see dashboard', async ({ page }) => {
  await page.goto('/signup')
  await page.fill('[name=email]', 'test@example.com')
  await page.fill('[name=password]', 'SecurePass123!')
  await page.click('button[type=submit]')
  await expect(page).toHaveURL('/dashboard')
})
```

## Testing Patterns

### AAA Pattern
```
Arrange → Set up test data and conditions
Act     → Execute the code being tested
Assert  → Verify the expected outcome
```

### Test Naming Convention
```
it('should [expected behavior] when [condition]')
```

### What to Test
- ✅ Happy path (expected inputs)
- ✅ Edge cases (empty, null, max values)
- ✅ Error cases (invalid inputs, failures)
- ✅ Boundary conditions (limits, thresholds)

### What NOT to Test
- ❌ Third-party libraries (trust them)
- ❌ Implementation details (test behavior)
- ❌ Trivial getters/setters
- ❌ Framework internals

## Mocking
```typescript
// Mock external dependency
const mockEmailService = {
  send: jest.fn().mockResolvedValue({ success: true })
}

// Inject mock
const userService = new UserService(mockEmailService)

// Verify interaction
expect(mockEmailService.send).toHaveBeenCalledWith(
  'user@example.com', 
  expect.stringContaining('Welcome')
)
```
