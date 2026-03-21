---
name: design-patterns
description: Expert-level software design patterns. Use when implementing Gang of Four patterns (Factory, Singleton, Observer, Strategy, Decorator, Command, etc.), architectural patterns, or recognizing when and how patterns apply. Also use when the user mentions 'Factory pattern', 'Observer', 'Strategy', 'Decorator', 'Singleton', 'design pattern', 'GoF', 'pattern recognition', or 'refactoring to patterns'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Design Patterns Expert

You are an expert in software design patterns with deep knowledge of GoF patterns, when to apply them, and when NOT to apply them.

## Before Starting

1. **Language** — TypeScript, Python, Java, Go, C#?
2. **Problem type** — recognizing a pattern, implementing one, refactoring to one?
3. **Context** — what problem are you trying to solve?
4. **Experience level** — learning patterns or reviewing architecture?
5. **OOP or functional** — some patterns have FP equivalents

---

## Core Expertise Areas

- **Creational**: Factory Method, Abstract Factory, Builder, Singleton, Prototype
- **Structural**: Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight
- **Behavioral**: Observer, Strategy, Command, Iterator, State, Template Method, Chain of Responsibility, Mediator
- **Architectural**: Repository, Unit of Work, CQRS, Event Sourcing, Specification
- **Pattern recognition**: identifying when a pattern applies from code smells
- **Functional alternatives**: higher-order functions instead of Strategy, closures instead of Command
- **When NOT to use**: over-engineering with patterns is a common mistake

---

## Key Patterns & Code

### Creational Patterns
```typescript
// ── Factory Method ──────────────────────────────────────────────────────────
// Define an interface for creating objects, let subclasses decide which to create
// Use when: you do not know ahead of time what class to instantiate

interface Notification {
  send(message: string): void;
}

class EmailNotification implements Notification {
  constructor(private email: string) {}
  send(message: string) { console.log('Email to ' + this.email + ': ' + message); }
}

class SMSNotification implements Notification {
  constructor(private phone: string) {}
  send(message: string) { console.log('SMS to ' + this.phone + ': ' + message); }
}

class PushNotification implements Notification {
  constructor(private deviceId: string) {}
  send(message: string) { console.log('Push to ' + this.deviceId + ': ' + message); }
}

// Factory — centralizes creation logic
class NotificationFactory {
  static create(type: 'email' | 'sms' | 'push', target: string): Notification {
    switch (type) {
      case 'email': return new EmailNotification(target);
      case 'sms':   return new SMSNotification(target);
      case 'push':  return new PushNotification(target);
    }
  }
}

// Usage — caller does not know which class it gets
const notification = NotificationFactory.create('email', 'alice@example.com');
notification.send('Your order is confirmed!');

// ── Builder ──────────────────────────────────────────────────────────────────
// Construct complex objects step by step
// Use when: object has many optional parameters, construction is complex

class QueryBuilder {
  private table = '';
  private conditions: string[] = [];
  private columns: string[] = ['*'];
  private limitValue: number | null = null;
  private orderByValue = '';

  from(table: string): this {
    this.table = table;
    return this;
  }

  select(...columns: string[]): this {
    this.columns = columns;
    return this;
  }

  where(condition: string): this {
    this.conditions.push(condition);
    return this;
  }

  limit(n: number): this {
    this.limitValue = n;
    return this;
  }

  orderBy(column: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.orderByValue = column + ' ' + direction;
    return this;
  }

  build(): string {
    if (!this.table) throw new Error('Table is required');
    let query = 'SELECT ' + this.columns.join(', ') + ' FROM ' + this.table;
    if (this.conditions.length > 0) query += ' WHERE ' + this.conditions.join(' AND ');
    if (this.orderByValue) query += ' ORDER BY ' + this.orderByValue;
    if (this.limitValue !== null) query += ' LIMIT ' + this.limitValue;
    return query;
  }
}

const query = new QueryBuilder()
  .from('users')
  .select('id', 'email', 'name')
  .where('active = true')
  .where('age >= 18')
  .orderBy('created_at', 'DESC')
  .limit(20)
  .build();
// SELECT id, email, name FROM users WHERE active = true AND age >= 18 ORDER BY created_at DESC LIMIT 20
```

### Structural Patterns
```typescript
// ── Adapter ──────────────────────────────────────────────────────────────────
// Convert interface of a class into another interface clients expect
// Use when: integrating incompatible interfaces, wrapping legacy code

// New interface your code expects
interface PaymentProcessor {
  charge(amountCents: number, currency: string): Promise<string>;
  refund(transactionId: string): Promise<void>;
}

// Legacy/external payment library with different interface
class LegacyPaymentLibrary {
  processPayment(amount: number, curr: string, callback: (err: any, id: string) => void): void {
    // legacy callback-based API
    callback(null, 'legacy_' + Date.now());
  }
  cancelPayment(txId: string, callback: (err: any) => void): void {
    callback(null);
  }
}

// Adapter wraps legacy library to match new interface
class LegacyPaymentAdapter implements PaymentProcessor {
  constructor(private legacy: LegacyPaymentLibrary) {}

  charge(amountCents: number, currency: string): Promise<string> {
    return new Promise((resolve, reject) => {
      this.legacy.processPayment(amountCents / 100, currency, (err, id) => {
        if (err) reject(err);
        else resolve(id);
      });
    });
  }

  refund(transactionId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.legacy.cancelPayment(transactionId, (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }
}

// ── Decorator ────────────────────────────────────────────────────────────────
// Add behavior to objects dynamically without changing their class
// Use when: adding features to objects without subclassing

interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(message);
  }
}

class TimestampLoggerDecorator implements Logger {
  constructor(private wrapped: Logger) {}
  log(message: string): void {
    this.wrapped.log('[' + new Date().toISOString() + '] ' + message);
  }
}

class PrefixLoggerDecorator implements Logger {
  constructor(private wrapped: Logger, private prefix: string) {}
  log(message: string): void {
    this.wrapped.log('[' + this.prefix + '] ' + message);
  }
}

class SamplingLoggerDecorator implements Logger {
  constructor(private wrapped: Logger, private sampleRate: number) {}
  log(message: string): void {
    if (Math.random() < this.sampleRate) {
      this.wrapped.log(message);
    }
  }
}

// Compose decorators
const logger: Logger = new SamplingLoggerDecorator(
  new TimestampLoggerDecorator(
    new PrefixLoggerDecorator(
      new ConsoleLogger(),
      'INFO'
    )
  ),
  0.1  // only log 10% of messages
);

// ── Facade ───────────────────────────────────────────────────────────────────
// Provide simplified interface to complex subsystem
// Use when: simplifying complex library, creating layered architecture

class OrderFacade {
  constructor(
    private inventory: InventoryService,
    private payment: PaymentService,
    private shipping: ShippingService,
    private notification: NotificationService,
  ) {}

  // Simple interface hides all the complexity
  async placeOrder(userId: string, items: CartItem[], paymentInfo: PaymentInfo): Promise<string> {
    await this.inventory.reserve(items);
    const orderId = await this.payment.charge(paymentInfo, this.calculateTotal(items));
    await this.shipping.schedule(orderId, userId);
    await this.notification.sendConfirmation(userId, orderId);
    return orderId;
  }

  private calculateTotal(items: CartItem[]): number {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }
}

// ── Proxy ────────────────────────────────────────────────────────────────────
// Provide surrogate that controls access to another object
// Use when: lazy loading, caching, access control, logging

interface UserService {
  getUser(id: string): Promise<User>;
}

class CachingUserServiceProxy implements UserService {
  private cache = new Map<string, { user: User; expiresAt: number }>();
  private readonly TTL = 5 * 60 * 1000; // 5 minutes

  constructor(private real: UserService) {}

  async getUser(id: string): Promise<User> {
    const cached = this.cache.get(id);
    if (cached && Date.now() < cached.expiresAt) {
      return cached.user;
    }
    const user = await this.real.getUser(id);
    this.cache.set(id, { user, expiresAt: Date.now() + this.TTL });
    return user;
  }
}
```

### Behavioral Patterns
```typescript
// ── Observer ─────────────────────────────────────────────────────────────────
// Define one-to-many dependency so when one object changes, dependents are notified
// Use when: event systems, decoupled communication between objects

type EventMap = {
  'order.created': { orderId: string; total: number };
  'user.registered': { userId: string; email: string };
  'payment.failed': { orderId: string; reason: string };
}

class TypedEventEmitter<T extends Record<string, any>> {
  private handlers = new Map<keyof T, Set<Function>>();

  on<K extends keyof T>(event: K, handler: (data: T[K]) => void): () => void {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler); // unsubscribe
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.handlers.get(event)?.forEach(h => h(data));
  }
}

const events = new TypedEventEmitter<EventMap>();

const unsubscribe = events.on('order.created', ({ orderId, total }) => {
  console.log('Order ' + orderId + ' created for ' + total);
});

events.emit('order.created', { orderId: 'ord_123', total: 99.99 });
unsubscribe(); // clean up when done

// ── Strategy ─────────────────────────────────────────────────────────────────
// Define family of algorithms, encapsulate each, make them interchangeable
// Use when: multiple algorithms for a task, want to switch at runtime

interface SortStrategy<T> {
  sort(items: T[]): T[];
}

class QuickSortStrategy<T> implements SortStrategy<T> {
  sort(items: T[]): T[] {
    if (items.length <= 1) return items;
    const pivot = items[Math.floor(items.length / 2)];
    const left  = items.filter(x => x < pivot);
    const mid   = items.filter(x => x === pivot);
    const right = items.filter(x => x > pivot);
    return [...this.sort(left), ...mid, ...this.sort(right)];
  }
}

class BubbleSortStrategy<T> implements SortStrategy<T> {
  sort(items: T[]): T[] {
    const arr = [...items];
    for (let i = 0; i < arr.length; i++)
      for (let j = 0; j < arr.length - i - 1; j++)
        if (arr[j] > arr[j+1]) [arr[j], arr[j+1]] = [arr[j+1], arr[j]];
    return arr;
  }
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(items: T[]): T[] {
    return this.strategy.sort(items);
  }
}

// ── Command ──────────────────────────────────────────────────────────────────
// Encapsulate a request as an object, allowing undo/redo, queuing, logging
// Use when: implementing undo/redo, task queuing, transactional behavior

interface Command {
  execute(): void;
  undo(): void;
}

class TextEditor {
  private text = '';
  private history: Command[] = [];

  executeCommand(command: Command): void {
    command.execute();
    this.history.push(command);
  }

  undoLastCommand(): void {
    const command = this.history.pop();
    command?.undo();
  }

  getText(): string { return this.text; }
  setText(text: string): void { this.text = text; }
}

class InsertTextCommand implements Command {
  private previousText = '';

  constructor(
    private editor: TextEditor,
    private textToInsert: string,
    private position: number,
  ) {}

  execute(): void {
    this.previousText = this.editor.getText();
    const text = this.editor.getText();
    this.editor.setText(
      text.slice(0, this.position) + this.textToInsert + text.slice(this.position)
    );
  }

  undo(): void {
    this.editor.setText(this.previousText);
  }
}

// ── State ────────────────────────────────────────────────────────────────────
// Allow object to alter behavior when internal state changes
// Use when: object has many states with different behavior, lots of conditionals

interface TrafficLightState {
  getColor(): string;
  next(light: TrafficLight): void;
}

class RedState implements TrafficLightState {
  getColor(): string { return 'RED'; }
  next(light: TrafficLight): void { light.setState(new GreenState()); }
}

class GreenState implements TrafficLightState {
  getColor(): string { return 'GREEN'; }
  next(light: TrafficLight): void { light.setState(new YellowState()); }
}

class YellowState implements TrafficLightState {
  getColor(): string { return 'YELLOW'; }
  next(light: TrafficLight): void { light.setState(new RedState()); }
}

class TrafficLight {
  private state: TrafficLightState = new RedState();

  setState(state: TrafficLightState): void { this.state = state; }
  getColor(): string { return this.state.getColor(); }
  next(): void { this.state.next(this); }
}

// ── Template Method ──────────────────────────────────────────────────────────
// Define skeleton of algorithm in base class, let subclasses fill in steps
// Use when: multiple classes share same algorithm structure with different steps

abstract class DataExporter {
  // Template method — defines the algorithm skeleton
  export(data: any[]): string {
    const filtered = this.filterData(data);
    const transformed = this.transformData(filtered);
    const formatted = this.formatData(transformed);
    return this.addHeader() + formatted + this.addFooter();
  }

  // Default implementations (can be overridden)
  protected filterData(data: any[]): any[] { return data; }
  protected transformData(data: any[]): any[] { return data; }
  protected addHeader(): string { return ''; }
  protected addFooter(): string { return ''; }

  // Abstract steps — must be implemented by subclasses
  protected abstract formatData(data: any[]): string;
}

class CSVExporter extends DataExporter {
  protected addHeader(): string { return 'id,name,email\n'; }
  protected formatData(data: any[]): string {
    return data.map(row => Object.values(row).join(',')).join('\n');
  }
}

class JSONExporter extends DataExporter {
  protected formatData(data: any[]): string {
    return JSON.stringify(data, null, 2);
  }
}

// ── Chain of Responsibility ───────────────────────────────────────────────────
// Pass request along chain of handlers until one handles it
// Use when: multiple handlers may handle request, handler not known a priori

abstract class RequestHandler {
  private nextHandler: RequestHandler | null = null;

  setNext(handler: RequestHandler): RequestHandler {
    this.nextHandler = handler;
    return handler;
  }

  handle(request: Request): Response | null {
    if (this.nextHandler) return this.nextHandler.handle(request);
    return null;
  }
}

class AuthHandler extends RequestHandler {
  handle(request: Request): Response | null {
    if (!request.headers.authorization) {
      return new Response(401, 'Unauthorized');
    }
    return super.handle(request);
  }
}

class RateLimitHandler extends RequestHandler {
  private counts = new Map<string, number>();

  handle(request: Request): Response | null {
    const ip = request.ip;
    const count = (this.counts.get(ip) ?? 0) + 1;
    this.counts.set(ip, count);
    if (count > 100) return new Response(429, 'Too Many Requests');
    return super.handle(request);
  }
}

class ValidationHandler extends RequestHandler {
  handle(request: Request): Response | null {
    if (!request.body) return new Response(400, 'Body required');
    return super.handle(request);
  }
}

// Build chain
const auth = new AuthHandler();
const rateLimit = new RateLimitHandler();
const validation = new ValidationHandler();
auth.setNext(rateLimit).setNext(validation);

const result = auth.handle(request);
```

### Pattern Recognition Guide
```
Problem: Creating objects without specifying exact class
  Solution: Factory Method or Abstract Factory

Problem: Building complex objects step by step
  Solution: Builder

Problem: Ensure only one instance exists
  Solution: Singleton (but prefer dependency injection)

Problem: Adding behavior without changing class
  Solution: Decorator

Problem: Incompatible interfaces need to work together
  Solution: Adapter

Problem: Simplify complex subsystem
  Solution: Facade

Problem: One change requires changing many classes
  Solution: Observer (decouple with events)

Problem: Multiple algorithms, want to switch at runtime
  Solution: Strategy

Problem: Need undo/redo or action queuing
  Solution: Command

Problem: Object behavior changes based on state, lots of if/else
  Solution: State

Problem: Multiple handlers may process a request
  Solution: Chain of Responsibility

Problem: Same algorithm skeleton, different steps
  Solution: Template Method

Problem: Tree structure, treat individual and composite uniformly
  Solution: Composite
```

### When NOT to Use Patterns
```
Over-engineering warning signs:
  - You are applying a pattern before you have the problem it solves
  - Adding a pattern makes code harder to understand
  - You added 3 new classes to solve a 10-line problem
  - You cannot explain WHY the pattern helps here

Simple code beats clever code:
  if (type === 'email') sendEmail(...);
  if (type === 'sms')   sendSMS(...);
  // This is fine for 2 cases
  // Only extract to Factory when you have 5+ cases or need runtime switching

YAGNI — You Ain't Gonna Need It
  Do not add patterns for future flexibility that may never materialize
  Wait until you feel the pain, then refactor

Patterns that are often overused:
  Singleton:          Usually a sign of global state problem — use DI instead
  Abstract Factory:   Often unnecessary unless supporting multiple product families
  Visitor:            Complex, hard to understand — consider simpler alternatives
```

---

## Best Practices

- Learn patterns by the PROBLEM they solve, not by their structure
- Apply patterns reactively — wait until you feel the pain, then refactor
- Patterns are a shared vocabulary — use their names in code reviews and discussions
- Most patterns are workarounds for missing language features — know your language
- Functional languages have different patterns: monads, functors, currying, composition
- The best code is the simplest code that solves the problem
- Patterns should make code MORE readable, not less

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Pattern hunting | Applying patterns before having the problem | Wait for pain, then refactor |
| Singleton overuse | Global mutable state, hard to test | Use dependency injection instead |
| Over-abstraction | 5 interfaces for a 2-case problem | Start simple, abstract when needed |
| Pattern for pattern sake | Complex code with no benefit | Always ask: does this make code clearer? |
| Ignoring language features | Java patterns in Python | Use language idioms first |
| Missing observer cleanup | Memory leaks from forgotten subscriptions | Always return and call unsubscribe |
| Deep decorator chains | Hard to debug, stack traces nightmare | Keep decorator chains shallow |
| Visitor complexity | Hard to add new element types | Consider simpler double-dispatch or match |

---

## Related Skills

- **clean-architecture**: For architectural patterns
- **domain-driven-design**: For domain modeling patterns
- **typescript-expert**: For type-safe pattern implementation
- **code-review-expert**: For recognizing patterns in code reviews
- **refactoring-expert**: For refactoring toward patterns
- **functional-programming**: For FP alternatives to OOP patterns