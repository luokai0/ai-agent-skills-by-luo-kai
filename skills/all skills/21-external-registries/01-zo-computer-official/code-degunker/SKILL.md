---
name: code-degunker
description: |
  Identify and fix AI-generated code anti-patterns: incomplete implementations, TODO placeholders, over-engineering, hallucinated APIs, missing error handling, over-defensive code, security vulnerabilities, performance anti-patterns, code bloat, type workarounds, dead code, magic numbers, inconsistent patterns, and poor architecture. Use when asked to "clean up", "degunk", "deslop", review, audit, or harden code. Also triggers on "is this code any good", "make this production-ready", "this feels AI-generated", "fix the code smell", "remove the slop", or "this code is a mess". Covers 27 anti-patterns across architecture, logic, security, performance, completeness, style, and reliability. Supports full file review and branch diff review modes.
compatibility: Created for Zo Computer
metadata:
  author: skeletorjs
  origin: Adapted from Claude Code skill by same author
---

# Code Degunker: Remove AI Code Anti-Patterns

You are a senior code reviewer that identifies and removes signs of AI-generated code to make it production-ready, maintainable, and actually correct. Based on research from CodeRabbit's AI vs Human Code Report, Augment Code's 8 Failure Patterns, IEEE Spectrum, Veracode, and GitHub's code review guidance.

## Your Task

When given code to degunk:

1. **Scan for anti-patterns** -- Check against every category below
2. **Triage by severity** -- Critical (will break in prod) > Major (will cause pain) > Minor (code smell)
3. **Rewrite problematic sections** -- Don't just flag; fix
4. **Preserve intent** -- Keep what the code is trying to do; fix how it does it
5. **Simplify** -- The best fix is often removing code, not adding it
6. **Do a final "would I ship this?" pass** -- Read the output as if you're on-call tonight and this just got deployed

---

## THE CORE INSIGHT

AI generates code that *looks correct* -- syntactically valid, architecturally plausible, pattern-matching against training data. The failure mode is not "obviously broken." The failure mode is "passes code review, works in staging, breaks at 3am under real load."

Research shows AI-authored PRs produce ~1.7x more issues than human PRs. The issues aren't unique to AI -- humans make the same mistakes -- but AI makes them more often, at larger scale, and with a surface-level polish that makes them harder to catch.

Your job is to see through the polish.

---

## THE NORTH STAR: MATCH THE CODEBASE

Universal rules matter, but the most important standard is *consistency with the existing codebase*. If the file doesn't use try/catch, don't add it. If the project uses terse comments, don't add block docstrings to every function. If the team uses `snake_case`, don't introduce `camelCase` because it's "more standard."

AI doesn't internalize your conventions. It defaults to whatever patterns were most common in its training data. The result is code that looks professional in isolation but feels foreign in context.

Before flagging something as an anti-pattern, ask: **Does the rest of this codebase do it this way?** If the existing code is consistent and the AI-generated code deviates, the AI code is wrong -- even if the AI's pattern is "better" in the abstract. Consistency beats correctness on style. (It never beats correctness on security or logic.)

---

## COMPLETENESS PATTERNS

### 1. TODO Placeholders and Stub Implementations

**Signals:** `// TODO`, `// FIXME`, `// HACK`, `throw new Error('Not implemented')`, `pass # placeholder`, empty function bodies, `console.log('implement me')`, `return null // temporary`

**Problem:** AI generates skeleton code that compiles and runs but doesn't actually do the thing. These stubs survive into production because they don't cause test failures -- the test either doesn't exist or was also generated as a stub.

**Before:**
```javascript
async function processPayment(order) {
  // TODO: implement payment processing
  console.log('Processing payment for order:', order.id);
  return { success: true };
}
```

**After:**
```javascript
async function processPayment(order) {
  if (!order?.id || !order?.amount || order.amount <= 0) {
    throw new PaymentError('Invalid order: missing id or valid amount');
  }

  const response = await stripe.paymentIntents.create({
    amount: Math.round(order.amount * 100),
    currency: order.currency ?? 'usd',
    metadata: { orderId: order.id },
  });

  if (response.status !== 'succeeded') {
    throw new PaymentError(`Payment failed: ${response.status}`, {
      orderId: order.id,
      stripeId: response.id,
    });
  }

  return { success: true, transactionId: response.id };
}
```

---

### 2. Fake Tests

**Signals:** Tests that always pass, tests that assert `true === true`, tests with no assertions, tests that mock everything including the thing being tested, deleted or skipped tests (`xit`, `test.skip`, `@pytest.mark.skip`), tests that only check the happy path

**Problem:** AI generates tests that give the illusion of coverage without testing anything meaningful. A test that mocks the database, mocks the API, and then asserts the mock returned what you told it to return is not a test -- it's a tautology.

**Before:**
```javascript
test('processPayment works', async () => {
  const mockStripe = { paymentIntents: { create: jest.fn().mockResolvedValue({ status: 'succeeded', id: 'pi_123' }) } };
  const result = await processPayment({ id: '1', amount: 50 });
  expect(result).toBeTruthy();
});
```

**After:**
```javascript
describe('processPayment', () => {
  test('rejects orders with missing amount', async () => {
    await expect(processPayment({ id: '1' }))
      .rejects.toThrow('Invalid order');
  });

  test('rejects negative amounts', async () => {
    await expect(processPayment({ id: '1', amount: -5 }))
      .rejects.toThrow('Invalid order');
  });

  test('returns transaction ID on success', async () => {
    const result = await processPayment({
      id: 'order_abc',
      amount: 49.99,
      currency: 'usd',
    });
    expect(result.transactionId).toMatch(/^pi_/);
  });

  test('throws PaymentError on Stripe failure', async () => {
    await expect(processPayment({
      id: 'order_abc',
      amount: 49.99,
      cardToken: 'tok_chargeDeclined',
    })).rejects.toThrow(PaymentError);
  });
});
```

---

### 3. Hallucinated APIs and Phantom Dependencies

**Signals:** Imports of packages that don't exist, method calls that look plausible but aren't real, referencing API properties that were never part of the spec, using deprecated methods as if they're current

**Problem:** AI learns patterns, not facts. It generates imports and method calls that pattern-match against its training data. One in five AI code samples contains references to non-existent libraries. These hallucinations can also enable supply-chain attacks ("slopsquatting") when attackers register the hallucinated package names.

**Before:**
```python
from flask_autovalidate import validate_schema  # doesn't exist
from utils.helpers import sanitize_html  # never defined in this project

@app.route('/submit', methods=['POST'])
@validate_schema(SubmissionSchema)
def submit():
    data = sanitize_html(request.json)
    return process(data)
```

**After:**
```python
from marshmallow import ValidationError
import bleach

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = SubmissionSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    data['body'] = bleach.clean(data.get('body', ''))
    return process(data)
```

**Checklist:** Before accepting any unfamiliar import, verify it exists on npm/PyPI/crates.io. Check the package's last publish date, weekly downloads, and maintainer count. If it was published recently with very low downloads, be suspicious.

---

## ARCHITECTURE PATTERNS

### 4. Over-Engineering and Unnecessary Abstraction

**Signals:** Single-use factory classes, wrapper interfaces around already-abstract types, "strategy pattern" with one strategy, abstract base classes with one child, dependency injection containers for 3-file apps, service layers that just pass through to the repository

**Problem:** AI mimics enterprise architecture patterns from its training data regardless of whether the codebase warrants them. A function that could be 5 lines balloons into a class hierarchy with interfaces, factories, and dependency injection. It looks architecturally sophisticated but just adds indirection without value.

**Before:**
```typescript
// IUserServiceFactory.ts
interface IUserServiceFactory {
  createUserService(): IUserService;
}

// UserServiceFactory.ts
class UserServiceFactory implements IUserServiceFactory {
  createUserService(): IUserService {
    return new UserService(new UserRepository(new DatabaseConnection()));
  }
}

// IUserService.ts
interface IUserService {
  getUserById(id: string): Promise<User | null>;
}

// UserService.ts
class UserService implements IUserService {
  constructor(private readonly repository: IUserRepository) {}

  async getUserById(id: string): Promise<User | null> {
    return this.repository.findById(id);
  }
}

// IUserRepository.ts
interface IUserRepository {
  findById(id: string): Promise<User | null>;
}

// UserRepository.ts
class UserRepository implements IUserRepository {
  constructor(private readonly db: IDatabaseConnection) {}

  async findById(id: string): Promise<User | null> {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}
```

**After:**
```typescript
// users.ts
import { db } from './db';

export async function getUserById(id: string): Promise<User | null> {
  const row = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  return row ?? null;
}
```

**Rule of thumb:** Don't add abstraction until you have a concrete second use case. One implementation behind an interface is not "programming to an interface" -- it's premature complexity.

---

### 5. Context Blindness and Duplicated Logic

**Signals:** Same logic implemented differently in multiple files, re-implementing utility functions that already exist in the project, parallel authentication checks, inconsistent date formatting across modules, copy-pasted code with minor variations

**Problem:** AI has a limited context window. When it runs out, it loses track of existing implementations and creates new ones. You end up with three different approaches to the same problem scattered across the codebase.

**Before:**
```javascript
// auth-middleware.js
function isAuthenticated(req) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return false;
  try {
    jwt.verify(token, process.env.JWT_SECRET);
    return true;
  } catch { return false; }
}

// api/users.js (different file, different approach)
function checkAuth(request) {
  const authHeader = request.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) return null;
  const decoded = jwt.decode(authHeader.substring(7));
  return decoded?.exp > Date.now() / 1000 ? decoded : null;
}
```

**After:**
```javascript
// auth.js -- single source of truth
export function verifyToken(req) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return null;

  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch {
    return null;
  }
}
```

---

### 6. Cargo Cult Patterns

**Signals:** Design patterns applied without a reason, `async/await` on synchronous operations, `.bind(this)` in arrow functions, wrapping simple values in `Optional`/`Maybe` when null checks suffice, creating a pub/sub system for two components that talk directly

**Problem:** AI applies patterns it has seen frequently without understanding *why* those patterns exist. The code works, but the pattern adds cognitive overhead without solving any actual problem.

**Before:**
```python
# Observer pattern for... two things
class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event, callback):
        self._subscribers.setdefault(event, []).append(callback)

    def publish(self, event, data):
        for cb in self._subscribers.get(event, []):
            cb(data)

bus = EventBus()
bus.subscribe('user_created', lambda u: send_welcome_email(u))
bus.subscribe('user_created', lambda u: log_signup(u))
```

**After:**
```python
def create_user(data):
    user = db.users.insert(data)
    send_welcome_email(user)
    log_signup(user)
    return user
```

---

## SECURITY PATTERNS

### 7. Hardcoded Secrets and Insecure Defaults

**Signals:** API keys, passwords, or tokens in source code (even "placeholder" ones), `CORS: '*'`, disabled TLS verification, `chmod 777`, debug endpoints left exposed, `password = 'admin'` in config

**Problem:** AI has seen thousands of committed secrets in its training data and reproduces the pattern. "Test" credentials bleed into production. CORS wildcard gets shipped. Debug routes stay enabled.

**Before:**
```python
app.config['SECRET_KEY'] = 'super-secret-key-change-me'
app.config['DATABASE_URL'] = 'postgresql://admin:password123@localhost/mydb'

@app.route('/debug/users')
def debug_users():
    return jsonify(User.query.all())

CORS(app, origins='*')
```

**After:**
```python
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']

# No debug routes in production

CORS(app, origins=os.environ.get('ALLOWED_ORIGINS', '').split(','))
```

---

### 8. Missing Input Validation and SQL Injection

**Signals:** String concatenation in database queries, `f"SELECT * FROM users WHERE id = {user_id}"`, no request body validation, trusting `req.query` or `req.params` directly, `eval()` or `exec()` on user input, `dangerouslySetInnerHTML` without sanitization

**Problem:** AI optimizes for "code that works" not "code that's secure." 45% of AI-generated code contains security vulnerabilities that pass functional tests but fail under adversarial input.

**Before:**
```python
@app.route('/search')
def search():
    query = request.args.get('q')
    results = db.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    return render_template('results.html', results=results, query=query)
```

**After:**
```python
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query or len(query) > 200:
        return render_template('results.html', results=[], query='')

    results = db.execute(
        "SELECT * FROM products WHERE name LIKE :q",
        {'q': f'%{query}%'}
    )
    return render_template('results.html', results=results, query=escape(query))
```

---

### 9. Broken Authentication Logic

**Signals:** Token validation that only checks expiration but not signature, session management that doesn't invalidate on logout, password comparison with `==` instead of constant-time comparison, missing rate limiting on login endpoints, no CSRF protection

**Problem:** AI-generated auth flows can be convincing and work in the happy path but have hidden bypasses. These are business logic flaws that automated scanners miss.

**Before:**
```javascript
function verifyUser(token) {
  const decoded = jwt.decode(token); // decode, not verify!
  if (decoded.exp > Date.now() / 1000) {
    return decoded;
  }
  return null;
}
```

**After:**
```javascript
function verifyUser(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      maxAge: '1h',
    });
  } catch {
    return null;
  }
}
```

---

## ERROR HANDLING PATTERNS

### 10. Swallowed Errors and Silent Failures

**Signals:** Empty `catch` blocks, `catch (e) { console.log(e) }` in production code, `except: pass`, `try/catch` around entire functions, `.catch(() => {})` on promises, error handling that returns a "success" response

**Problem:** AI generates error handling that prevents crashes but hides failures. The code doesn't blow up, so it looks like it works. But errors are silently swallowed, making debugging impossible and causing data corruption.

**Before:**
```javascript
async function syncInventory(items) {
  for (const item of items) {
    try {
      await api.updateStock(item.id, item.quantity);
    } catch (e) {
      console.log('Error updating stock:', e.message);
    }
  }
  return { success: true, synced: items.length };
}
```

**After:**
```javascript
async function syncInventory(items) {
  const results = { synced: [], failed: [] };

  for (const item of items) {
    try {
      await api.updateStock(item.id, item.quantity);
      results.synced.push(item.id);
    } catch (error) {
      results.failed.push({
        itemId: item.id,
        error: error.message,
        code: error.code ?? 'UNKNOWN',
      });
      logger.warn('Inventory sync failed', { itemId: item.id, error });
    }
  }

  if (results.failed.length > 0) {
    logger.error('Partial inventory sync failure', {
      total: items.length,
      failed: results.failed.length,
    });
  }

  return results;
}
```

---

### 11. Missing Edge Cases

**Signals:** No null/undefined checks, no empty array handling, no bounds checking, assumes network calls always succeed, no handling for concurrent access, ignores timezone differences, doesn't handle Unicode

**Problem:** AI training data over-represents the happy path. The code works with typical inputs but breaks on empty arrays, null values, max integers, Unicode characters, and concurrent requests.

**Before:**
```javascript
function getAverageRating(reviews) {
  const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
  return sum / reviews.length;
}
```

**After:**
```javascript
function getAverageRating(reviews) {
  if (!reviews?.length) return 0;

  const validRatings = reviews
    .map(r => r?.rating)
    .filter(r => typeof r === 'number' && r >= 1 && r <= 5);

  if (validRatings.length === 0) return 0;

  const sum = validRatings.reduce((acc, r) => acc + r, 0);
  return Math.round((sum / validRatings.length) * 10) / 10;
}
```

---

### 12. Over-Defensive Code

**Signals:** Try/catch around every function call, null checks on values that were already validated upstream, defensive copies of immutable data, redundant `if (x !== null && x !== undefined)` checks in typed code where `x` can't be null, error handling on internal helper functions that only receive trusted input

**Problem:** This is the mirror image of patterns 10 and 11. AI wraps everything in defensive armor regardless of context. If a function is only ever called from a middleware that already validated the request, re-validating inside the function is noise.

**Before:**
```typescript
async function getUserPreferences(req: AuthenticatedRequest) {
  try {
    if (!req) throw new Error('Request is required');
    if (!req.user) throw new Error('User is required');
    if (!req.user.id) throw new Error('User ID is required');
    if (typeof req.user.id !== 'string') throw new Error('User ID must be string');

    const prefs = await db.preferences.findUnique({
      where: { userId: req.user.id },
    });

    if (prefs === null || prefs === undefined) {
      return { theme: 'light', language: 'en' };
    }

    return prefs;
  } catch (error) {
    console.error('Error getting preferences:', error);
    return { theme: 'light', language: 'en' };
  }
}
```

**After:**
```typescript
async function getUserPreferences(req: AuthenticatedRequest) {
  const prefs = await db.preferences.findUnique({
    where: { userId: req.user.id },
  });
  return prefs ?? { theme: 'light', language: 'en' };
}
```

**Rule of thumb:** Before adding a defensive check, ask: "Can this value actually be invalid at this point in the call chain?" If the answer is no, the check is noise. Trust your type system. Trust your middleware. Trust your validation layer.

---

## PERFORMANCE PATTERNS

### 13. O(n^2) When O(n) Would Do

**Signals:** Nested loops over the same dataset, `.find()` inside `.map()`, repeated array scans, filtering within a loop that could use a Set or Map, `includes()` in a loop on a large array

**Problem:** AI defaults to the most readable pattern, not the most efficient. For small datasets during testing this doesn't matter. For production data, it causes exponential slowdown.

**Before:**
```javascript
function findMatchingOrders(orders, customers) {
  return orders.map(order => ({
    ...order,
    customer: customers.find(c => c.id === order.customerId),
  }));
}
```

**After:**
```javascript
function findMatchingOrders(orders, customers) {
  const customerMap = new Map(customers.map(c => [c.id, c]));
  return orders.map(order => ({
    ...order,
    customer: customerMap.get(order.customerId) ?? null,
  }));
}
```

---

### 14. N+1 Queries and Excessive I/O

**Signals:** Database queries inside loops, `await` inside `for`/`forEach` that could be batched, individual API calls for each item when a bulk endpoint exists, reading files one line at a time when a bulk read works

**Problem:** Excessive I/O was ~8x more common in AI-authored code. AI favors clarity and simple patterns over efficiency. Individual queries in a loop are easier to read than a JOIN or batch call, so that's what AI generates.

**Before:**
```python
async def get_order_details(order_ids):
    orders = []
    for oid in order_ids:
        order = await db.orders.find_one({'_id': oid})
        customer = await db.customers.find_one({'_id': order['customer_id']})
        items = await db.items.find({'order_id': oid}).to_list()
        orders.append({**order, 'customer': customer, 'items': items})
    return orders
```

**After:**
```python
async def get_order_details(order_ids):
    orders = await db.orders.find({'_id': {'$in': order_ids}}).to_list()
    customer_ids = [o['customer_id'] for o in orders]
    item_lookup = defaultdict(list)

    customers, items = await asyncio.gather(
        db.customers.find({'_id': {'$in': customer_ids}}).to_list(),
        db.items.find({'order_id': {'$in': order_ids}}).to_list(),
    )

    cust_map = {c['_id']: c for c in customers}
    for item in items:
        item_lookup[item['order_id']].append(item)

    return [
        {**o, 'customer': cust_map.get(o['customer_id']), 'items': item_lookup[o['_id']]}
        for o in orders
    ]
```

---

### 15. String Concatenation in Loops

**Signals:** `+=` on strings inside loops, repeated `str()` conversions, building HTML/XML by appending strings, creating CSV output character by character

**Problem:** In many languages, string concatenation in loops creates a new string object on every iteration. For large datasets, this turns linear work into quadratic memory allocation.

**Before:**
```python
def generate_report(records):
    output = ""
    for record in records:
        output += f"{record['name']},{record['value']},{record['date']}\n"
    return output
```

**After:**
```python
def generate_report(records):
    lines = [f"{r['name']},{r['value']},{r['date']}" for r in records]
    return '\n'.join(lines) + '\n'
```

---

## STYLE AND READABILITY PATTERNS

### 16. Generic and Meaningless Names

**Signals:** `data`, `result`, `temp`, `val`, `info`, `item`, `obj`, `handler`, `manager`, `utils`, `helpers`, `stuff`, `thing`, `process()`, `handle()`, `doWork()`, single-letter variables outside of trivial loops

**Problem:** AI uses generic identifiers pulled from statistical frequency rather than domain meaning. When every function returns `data` and every module is called `utils`, the codebase becomes opaque.

**Before:**
```javascript
async function handleData(items) {
  const result = [];
  for (const item of items) {
    const data = await process(item);
    if (data.status === 'ok') {
      result.push(transformData(data));
    }
  }
  return result;
}
```

**After:**
```javascript
async function applyDiscounts(eligibleProducts) {
  const discounted = [];
  for (const product of eligibleProducts) {
    const priceCheck = await fetchCurrentPricing(product);
    if (priceCheck.isEligible) {
      discounted.push(applyTierDiscount(priceCheck));
    }
  }
  return discounted;
}
```

---

### 17. Inconsistent Style Within the Codebase

**Signals:** Mixing `camelCase` and `snake_case`, some files use semicolons and others don't, tabs vs spaces mixed, import ordering varies file to file, some functions return early and others use else chains, inconsistent quote styles

**Problem:** AI doesn't internalize your codebase's conventions -- it defaults to whatever was most common in its training data. The result is style drift: each generated file follows slightly different conventions, increasing cognitive load for reviewers.

**Fix:** Before accepting AI code, compare it against your existing patterns. Adopt and enforce a linter/formatter config (ESLint + Prettier, Black, rustfmt). Generated code should match the repo, not the model's preferences.

---

### 18. Overly Verbose Solutions

**Signals:** 20 lines where 3 would do, manual implementations of standard library functions, recreating `Array.filter` with a for loop, writing a custom date parser instead of using a library, implementing `isOdd` instead of `n % 2 !== 0`

**Problem:** AI tends toward verbosity. It generates long, explicit code that's "safe" and unlikely to be wrong, but makes the codebase harder to scan and maintain.

**Before:**
```javascript
function getActiveUsers(users) {
  const activeUsers = [];
  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    if (user.status !== null && user.status !== undefined) {
      if (user.status === 'active') {
        activeUsers.push(user);
      }
    }
  }
  return activeUsers;
}
```

**After:**
```javascript
function getActiveUsers(users) {
  return users.filter(u => u.status === 'active');
}
```

---

### 19. Comment Noise and Misleading Comments

**Signals:** Comments that restate the code (`// increment i by 1`), comments that describe *what was intended* but not *what the code does*, stale comments from a previous version, zero comments on complex business logic, AI-generated docstrings that describe a different function, block comments on every single function when the existing codebase uses them sparingly

**Problem:** AI generates two kinds of bad comments. *Misleading* comments that describe what the AI intended to write -- which may not match what it actually wrote. And *noise* comments that a human would never add: obvious narration, docstrings on trivial getters, or comment density wildly inconsistent with the rest of the file.

**Before:**
```javascript
// Get the user's name
async function fetchUserData(userId) {
  // Call the API
  const response = await fetch(`/api/users/${userId}/full-profile`);
  // Parse the response as JSON
  const data = await response.json();
  // Return the data
  return data;
}
```

**After:**
```javascript
/**
 * Fetches complete user profile including preferences and org membership.
 * Used by the dashboard to render the sidebar and permission checks.
 */
async function fetchUserProfile(userId) {
  const response = await fetch(`/api/users/${userId}/full-profile`);
  if (!response.ok) {
    throw new ApiError(`Failed to fetch profile for ${userId}`, response.status);
  }
  return response.json();
}
```

**Rule of thumb:** Comments should explain *why*, never *what*. If you need a comment to explain what a line does, the code should be rewritten so the line explains itself. Match the comment density of the surrounding codebase.

---

## RELIABILITY PATTERNS

### 20. Incorrect Async/Concurrency Handling

**Signals:** `await` inside `forEach` (which doesn't actually await), missing `await` on async calls, fire-and-forget promises with no error handling, race conditions in shared state, no timeout on external calls, using `Promise.all` when one failure should not abort the rest

**Problem:** AI gets async patterns subtly wrong. The code appears to work in testing (where operations complete quickly in predictable order) but breaks under real concurrency.

**Before:**
```javascript
async function notifyAllUsers(userIds) {
  userIds.forEach(async (id) => {
    await sendNotification(id); // doesn't actually await!
  });
  console.log('All notifications sent'); // runs immediately
}
```

**After:**
```javascript
async function notifyAllUsers(userIds) {
  const results = await Promise.allSettled(
    userIds.map(id => sendNotification(id))
  );

  const failures = results.filter(r => r.status === 'rejected');
  if (failures.length > 0) {
    logger.warn(`${failures.length}/${userIds.length} notifications failed`);
  }
}
```

---

### 21. Missing Observability

**Signals:** No logging on failures, no metrics on latency or throughput, no request tracing, no alerting hooks, `console.log` as the only logging mechanism, no way to tell if the service is healthy

**Problem:** AI doesn't add observability unless you explicitly ask. When the code breaks in production, you have no visibility into what happened.

**Before:**
```javascript
app.post('/api/orders', async (req, res) => {
  const order = await createOrder(req.body);
  res.json(order);
});
```

**After:**
```javascript
app.post('/api/orders', async (req, res) => {
  const startTime = Date.now();
  const requestId = req.headers['x-request-id'] ?? crypto.randomUUID();

  try {
    const order = await createOrder(req.body);

    logger.info('Order created', {
      requestId,
      orderId: order.id,
      durationMs: Date.now() - startTime,
    });

    res.json(order);
  } catch (error) {
    logger.error('Order creation failed', {
      requestId,
      error: error.message,
      body: sanitize(req.body),
      durationMs: Date.now() - startTime,
    });

    res.status(error.statusCode ?? 500).json({
      error: 'Order creation failed',
      requestId,
    });
  }
});
```

---

## DEPENDENCY PATTERNS

### 22. Unnecessary Dependencies

**Signals:** Importing a full utility library for one function (`lodash` for `_.isEmpty`), using a package for something the standard library does, `is-odd`, `is-even`, `left-pad`, pulling in a 500KB library for a 5-line feature

**Problem:** AI suggests packages it has seen frequently in training data, regardless of whether they're needed. Each dependency is an attack surface, a maintenance burden, and a bundle size increase.

**Before:**
```javascript
import _ from 'lodash';
import moment from 'moment';
import isEmail from 'is-email';

const isEmpty = _.isEmpty(obj);
const formatted = moment().format('YYYY-MM-DD');
const valid = isEmail(addr);
```

**After:**
```javascript
const isEmpty = obj == null || Object.keys(obj).length === 0;
const formatted = new Date().toISOString().split('T')[0];
const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(addr);
```

---

### 23. Outdated and Deprecated Patterns

**Signals:** `var` instead of `let`/`const`, `componentWillMount` in React, `request` library (deprecated), `moment.js` when `date-fns` or `Temporal` is available, `http.createServer` for complex apps instead of a framework, Python 2 syntax

**Problem:** AI training data includes decades of code. It will suggest patterns that were best practice in 2015 but are deprecated or insecure today.

**Fix:** When you see old patterns, update them. Check that libraries are still maintained (last publish date, open issues, download trends). Replace deprecated APIs with their current equivalents.

---

### 24. Type Workarounds and `any` Casting

**Signals:** `as any` in TypeScript, `# type: ignore` in Python, `@SuppressWarnings` on everything, casting to `Object` in Java, `(void*)` in C, using `any` as a function parameter or return type to silence the compiler

**Problem:** When AI encounters a type error, it often takes the shortest path to silence the compiler rather than fixing the underlying type mismatch. Casting to `any` doesn't fix the problem -- it hides it.

**Before:**
```typescript
async function updateUser(id: string, data: any) {
  const user = await db.users.findUnique({ where: { id } }) as any;
  return db.users.update({
    where: { id },
    data: { ...user, ...data } as any,
  });
}
```

**After:**
```typescript
interface UserUpdate {
  name?: string;
  email?: string;
  role?: 'admin' | 'member' | 'viewer';
}

async function updateUser(id: string, data: UserUpdate) {
  const user = await db.users.findUnique({ where: { id } });
  if (!user) throw new NotFoundError(`User ${id} not found`);

  return db.users.update({
    where: { id },
    data,
  });
}
```

**Rule of thumb:** Every `as any` is a bug you're choosing to find later. If the types don't align, fix the types.

---

### 25. Dead Code and Unused Imports

**Signals:** Imported modules that are never referenced, functions that are never called, variables that are assigned but never read, commented-out code blocks, unreachable code after a `return`/`throw`, feature flags for features that shipped months ago, debug logging left behind

**Problem:** AI generates code iteratively. When it changes approach mid-generation, it often leaves behind artifacts from the previous attempt. Over time this accumulates into "lava flow" -- dead code that nobody dares touch because nobody knows if it's actually dead.

**Before:**
```javascript
import { format, parse, addDays, subDays, isValid } from 'date-fns';
import _ from 'lodash';

// Old approach - keeping for reference
// function legacyFormat(date) {
//   return date.toISOString().split('T')[0];
// }

function formatDate(date) {
  return format(date, 'yyyy-MM-dd');
}

function unusedHelper(items) {
  return _.uniqBy(items, 'id');
}
```

**After:**
```javascript
import { format } from 'date-fns';

function formatDate(date) {
  return format(date, 'yyyy-MM-dd');
}
```

**Rule of thumb:** Delete it. If you need it later, git has your back.

---

### 26. Magic Numbers and Hardcoded Values

**Signals:** Numeric literals in conditionals (`if (retries > 3)`), string literals repeated across files, timeout values without explanation (`setTimeout(fn, 86400000)`), array indices used as field accessors (`row[4]`), status codes without context

**Problem:** AI generates hardcoded values inline because that's the simplest way to make code work. But `3`, `86400000`, and `'active'` mean nothing to the next developer.

**Before:**
```javascript
async function retryRequest(url) {
  for (let i = 0; i < 3; i++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
      if (res.status === 429) {
        await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
        continue;
      }
      return res;
    } catch { continue; }
  }
  throw new Error('Request failed');
}
```

**After:**
```javascript
const MAX_RETRIES = 3;
const REQUEST_TIMEOUT_MS = 5_000;
const RETRY_BASE_MS = 1_000;

async function retryRequest(url) {
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS) });
      if (res.status === 429) {
        await new Promise(r => setTimeout(r, RETRY_BASE_MS * Math.pow(2, attempt)));
        continue;
      }
      return res;
    } catch { continue; }
  }
  throw new Error(`Request to ${url} failed after ${MAX_RETRIES} attempts`);
}
```

---

### 27. Misplaced Imports

**Signals:** `import` or `from x import y` statements inside function bodies (Python), `require()` inside conditionals or loops (Node.js), dynamic imports used for static dependencies, import order that doesn't match the rest of the file

**Problem:** AI sometimes places imports inside functions rather than at the top of the file. Usually just sloppy placement, not intentional lazy loading.

**Before:**
```python
def process_upload(file_path):
    import pandas as pd
    from pathlib import Path
    import json

    data = pd.read_csv(Path(file_path))
    return json.dumps(data.to_dict())
```

**After:**
```python
import json
from pathlib import Path

import pandas as pd


def process_upload(file_path):
    data = pd.read_csv(Path(file_path))
    return json.dumps(data.to_dict())
```

**Exception:** Inline imports are legitimate when breaking circular dependencies or lazy-loading expensive modules.

---

## WHEN NOT TO DEGUNK

Not every review calls for a full audit. Restraint is as important as thoroughness.

**Don't refactor code that wasn't changed.** If you're reviewing a branch, focus on the diff.

**Don't "improve" working code that matches the codebase style.** Style crusades belong in separate PRs with team buy-in.

**Don't add abstraction preemptively.** Wait for the second use case.

**Don't gold-plate a prototype.** Match the effort to the lifespan of the code.

**Scale the review to the risk.** Auth, payment processing, and data mutations get the full checklist. A utility function that formats a date gets a glance.

---

## Process

### Full Review Mode (reviewing a file or module)

1. Read the code carefully -- understand what it's supposed to do before judging how it does it
2. Run a completeness check first -- are there TODOs, stubs, or missing implementations?
3. Check imports -- do all dependencies exist? Are they necessary? Are they current?
4. Audit security -- input validation, auth logic, secrets management, CORS
5. Review error handling -- are errors caught, reported, and recoverable? Or swallowed?
6. Check edge cases -- null, empty, boundary values, concurrent access
7. Evaluate performance -- nested loops, N+1 queries, string concat, unnecessary I/O
8. Assess architecture -- is the abstraction level appropriate? Any cargo cult patterns?
9. Read for consistency -- does the style match the rest of the codebase?
10. Final pass -- would you ship this? Would you be comfortable being on-call tonight?

### Branch Review Mode (cleaning up a diff)

Use this when reviewing AI-generated changes against a base branch. The goal is to remove slop introduced in the diff without touching unrelated code.

1. Get the diff: `git diff main...HEAD`
2. For each changed file, compare the AI's additions against the file's existing style
3. Remove comment noise -- extra comments inconsistent with the rest of the file
4. Remove over-defensive code -- try/catch and null checks that are abnormal for that area of the codebase
5. Fix type workarounds -- replace `as any` casts with proper types
6. Move misplaced imports to the top of the file
7. Remove dead code -- unused imports, unreachable branches, commented-out blocks
8. Verify consistency -- naming, formatting, error handling patterns should match the existing file
9. Report a brief summary (1-3 sentences) of what changed

## Output Format

Provide:
1. **Severity summary** -- How many critical / major / minor issues found
2. **Findings** -- Each issue with its category, the problematic code, why it's a problem, and the fix
3. **Rewritten code** -- The complete corrected version (not just patches)
4. **Remaining risks** -- Anything you can't fix without more context

Adapt the depth to what you're given. If someone pastes a 10-line function, don't produce a 500-line audit. If someone pastes a full module, be thorough.

---

## Quick Reference: The Degunk Checklist

**Will it break?**
- [ ] All TODOs and stubs replaced with real implementations
- [ ] All imports verified as real, maintained packages
- [ ] Input validation on all external data
- [ ] Auth logic verifies (not just decodes) tokens
- [ ] No hardcoded secrets
- [ ] Error handling reports failures, not hides them
- [ ] Edge cases handled (null, empty, max values, Unicode)
- [ ] No `as any` or type-suppression hacks hiding real mismatches

**Will it hurt?**
- [ ] No N+1 queries or loops-within-loops on large data
- [ ] No string concatenation in loops
- [ ] Async patterns are correct (no `forEach` with `await`)
- [ ] Tests actually test meaningful behavior
- [ ] Concurrency-safe where needed
- [ ] No magic numbers -- constants are named and explained
- [ ] No dead code, unused imports, or commented-out blocks

**Will it annoy?**
- [ ] No unnecessary abstractions or single-use factories
- [ ] No cargo cult patterns
- [ ] No over-defensive checks on already-validated data
- [ ] Names mean something in the domain
- [ ] Style is consistent with the existing codebase
- [ ] No unnecessary dependencies
- [ ] Comments explain why, not what -- and match the file's comment density
- [ ] No deprecated patterns or APIs
- [ ] Imports are at the top of the file (unless lazy-loading for a reason)
