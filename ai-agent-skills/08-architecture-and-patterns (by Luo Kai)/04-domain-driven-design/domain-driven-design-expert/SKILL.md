---
author: luo-kai
name: domain-driven-design
description: Expert-level Domain-Driven Design (DDD). Use when applying DDD principles, identifying bounded contexts, aggregates, entities, value objects, domain events, repositories, application services, or ubiquitous language. Also use when the user mentions 'bounded context', 'aggregate', 'value object', 'domain event', 'ubiquitous language', 'context map', 'DDD', 'domain model', or 'aggregate root'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Domain-Driven Design Expert

You are an expert in Domain-Driven Design with deep knowledge of strategic design, tactical patterns, and applying DDD to real-world software projects.

## Before Starting

1. **Domain complexity** — simple CRUD or complex business rules?
2. **Team context** — single team or multiple teams working on same domain?
3. **Problem type** — strategic design (bounded contexts), tactical (aggregates, entities), or both?
4. **Current state** — greenfield design or refactoring existing code?
5. **Language/framework** — TypeScript, Python, Java, C#?

---

## Core Expertise Areas

- **Strategic design**: bounded contexts, context maps, subdomains, ubiquitous language
- **Tactical design**: aggregates, entities, value objects, domain events, domain services
- **Repositories**: aggregate persistence, unit of work, collection-oriented vs persistence-oriented
- **Application services**: orchestrating use cases, transaction boundaries, command/query separation
- **Domain events**: capturing domain occurrences, eventual consistency, integration events
- **Context mapping**: shared kernel, customer-supplier, conformist, anti-corruption layer
- **Event storming**: collaborative domain discovery workshop technique
- **Anemic vs rich domain model**: recognizing and fixing anemic models

---

## Key Patterns & Code

### Strategic Design — Core Concepts
```
Domain:
  The sphere of knowledge and activity the software is about
  Example: Insurance, Banking, E-commerce, Healthcare

Subdomain types:
  Core domain:       Your competitive advantage — invest most here
                     Example: Recommendation engine for Netflix
  Supporting domain: Necessary but not differentiating
                     Example: User management, notifications
  Generic domain:    Solved problems — buy or use off-the-shelf
                     Example: Authentication, billing, email delivery

Bounded Context:
  A boundary within which a domain model is defined and applicable
  The same word can mean different things in different contexts
  Example: 'Customer' in Sales context vs 'Customer' in Support context

Ubiquitous Language:
  Shared vocabulary between developers and domain experts
  Used in code, documentation, conversations, tests
  No translation between business language and code
  WRONG: user_account, person_record, contact_entry
  RIGHT: Customer, Policy, Claim, Premium (use domain terms)

Rule of thumb:
  One bounded context = one team ownership
  One bounded context = one ubiquitous language
  One bounded context = one deployable unit (microservice or module)
```

### Context Map Patterns
```
Partnership:
  Two teams coordinate changes together
  Use when: teams are closely aligned, mutual success

Shared Kernel:
  Two contexts share a subset of the domain model
  Use when: teams are closely aligned, sharing is worth the coupling
  Risk: changes require coordination between teams

Customer-Supplier:
  Upstream (supplier) provides API for downstream (customer)
  Customer can influence roadmap but supplier decides
  Use when: clear dependency direction, some influence

Conformist:
  Downstream conforms to upstream model without influence
  Use when: upstream does not care about downstream needs
  Example: Using a third-party API, conforming to its model

Anti-Corruption Layer (ACL):
  Downstream creates translation layer to protect its model
  Use when: upstream model is messy or incompatible
  MOST IMPORTANT pattern for keeping domain clean

Open Host Service:
  Provider publishes a protocol for integration
  Use when: many consumers, published API

Published Language:
  Well-documented shared language for integration
  Example: CloudEvents, OpenAPI specs, AsyncAPI
```

### Aggregates — The Core Tactical Pattern
```typescript
// Aggregate: cluster of domain objects treated as a unit
// Aggregate Root: the single entry point to the aggregate
// Rules:
//   1. All access to the aggregate goes through the root
//   2. External objects hold references only to the root
//   3. The aggregate maintains its own invariants
//   4. Aggregate boundaries define transaction scope

// Example: Order aggregate
// OrderItem is INSIDE the Order aggregate
// Customer is OUTSIDE — referenced by ID only

export class Order {  // Aggregate Root
  private readonly _id: OrderId;
  private readonly _customerId: CustomerId;  // reference by ID, not object
  private _items: OrderItem[] = [];
  private _status: OrderStatus;
  private _domainEvents: DomainEvent[] = [];

  private constructor(id: OrderId, customerId: CustomerId) {
    this._id = id;
    this._customerId = customerId;
    this._status = OrderStatus.Draft;
  }

  static create(customerId: CustomerId): Order {
    const order = new Order(OrderId.generate(), customerId);
    order.addDomainEvent(new OrderCreatedEvent(order._id, customerId));
    return order;
  }

  // All business operations go through the aggregate root
  addItem(productId: ProductId, quantity: Quantity, price: Money): void {
    this.guardAgainstConfirmedOrder();

    const existingItem = this._items.find(i => i.productId.equals(productId));
    if (existingItem) {
      existingItem.increaseQuantity(quantity);
    } else {
      this._items.push(OrderItem.create(productId, quantity, price));
    }
  }

  removeItem(productId: ProductId): void {
    this.guardAgainstConfirmedOrder();
    this._items = this._items.filter(i => !i.productId.equals(productId));
  }

  confirm(): void {
    if (this._status !== OrderStatus.Draft) {
      throw new DomainError('Only draft orders can be confirmed');
    }
    if (this._items.length === 0) {
      throw new DomainError('Cannot confirm empty order');
    }
    this._status = OrderStatus.Confirmed;
    this.addDomainEvent(new OrderConfirmedEvent(this._id, this.total()));
  }

  cancel(reason: string): void {
    if (this._status === OrderStatus.Shipped) {
      throw new DomainError('Cannot cancel shipped order');
    }
    this._status = OrderStatus.Cancelled;
    this.addDomainEvent(new OrderCancelledEvent(this._id, reason));
  }

  // Computed value — derived from state
  total(): Money {
    return this._items.reduce(
      (sum, item) => sum.add(item.subtotal()),
      Money.zero('USD')
    );
  }

  // Invariant guard
  private guardAgainstConfirmedOrder(): void {
    if (this._status !== OrderStatus.Draft) {
      throw new DomainError('Cannot modify a confirmed order');
    }
  }

  // Domain events
  private addDomainEvent(event: DomainEvent): void {
    this._domainEvents.push(event);
  }

  pullDomainEvents(): DomainEvent[] {
    const events = [...this._domainEvents];
    this._domainEvents = [];
    return events;
  }

  // Getters
  get id(): OrderId { return this._id; }
  get customerId(): CustomerId { return this._customerId; }
  get status(): OrderStatus { return this._status; }
  get items(): ReadonlyArray<OrderItem> { return this._items; }
}

// OrderItem is INSIDE the Order aggregate
// It cannot be accessed directly from outside
export class OrderItem {
  private _quantity: Quantity;

  private constructor(
    readonly productId: ProductId,
    quantity: Quantity,
    readonly unitPrice: Money,
  ) {
    this._quantity = quantity;
  }

  static create(productId: ProductId, quantity: Quantity, price: Money): OrderItem {
    if (quantity.value <= 0) {
      throw new DomainError('Quantity must be positive');
    }
    return new OrderItem(productId, quantity, price);
  }

  increaseQuantity(by: Quantity): void {
    this._quantity = this._quantity.add(by);
  }

  subtotal(): Money {
    return this.unitPrice.multiply(this._quantity.value);
  }

  get quantity(): Quantity { return this._quantity; }
}
```

### Value Objects
```typescript
// Value Object: defined by its attributes, not identity
// Immutable — no setters, create new instance for changes
// Equality by value, not reference

export class Money {
  private constructor(
    readonly amount: number,   // in cents to avoid float issues
    readonly currency: string,
  ) {
    if (amount < 0) throw new DomainError('Amount cannot be negative');
    if (!currency) throw new DomainError('Currency is required');
  }

  static of(amount: number, currency: string): Money {
    return new Money(Math.round(amount * 100), currency);
  }

  static zero(currency: string): Money {
    return new Money(0, currency);
  }

  add(other: Money): Money {
    this.guardSameCurrency(other);
    return new Money(this.amount + other.amount, this.currency);
  }

  subtract(other: Money): Money {
    this.guardSameCurrency(other);
    const result = this.amount - other.amount;
    if (result < 0) throw new DomainError('Insufficient funds');
    return new Money(result, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(Math.round(this.amount * factor), this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  isGreaterThan(other: Money): boolean {
    this.guardSameCurrency(other);
    return this.amount > other.amount;
  }

  toString(): string {
    return (this.amount / 100).toFixed(2) + ' ' + this.currency;
  }

  private guardSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new DomainError('Cannot operate on different currencies: ' + this.currency + ' vs ' + other.currency);
    }
  }
}

// Strong ID types prevent mixing IDs of different aggregates
export class OrderId {
  private constructor(readonly value: string) {
    if (!value) throw new DomainError('OrderId cannot be empty');
  }

  static generate(): OrderId {
    return new OrderId(crypto.randomUUID());
  }

  static from(value: string): OrderId {
    return new OrderId(value);
  }

  equals(other: OrderId): boolean {
    return this.value === other.value;
  }

  toString(): string { return this.value; }
}

export class Quantity {
  private constructor(readonly value: number) {
    if (!Number.isInteger(value) || value <= 0) {
      throw new DomainError('Quantity must be a positive integer');
    }
  }

  static of(value: number): Quantity { return new Quantity(value); }

  add(other: Quantity): Quantity {
    return new Quantity(this.value + other.value);
  }

  equals(other: Quantity): boolean { return this.value === other.value; }
}
```

### Domain Events
```typescript
// Domain Event: something significant that happened in the domain
// Named in past tense, immutable, carry relevant data

interface DomainEvent {
  readonly eventId: string;
  readonly occurredAt: Date;
  readonly eventType: string;
}

export class OrderCreatedEvent implements DomainEvent {
  readonly eventId = crypto.randomUUID();
  readonly occurredAt = new Date();
  readonly eventType = 'order.created';

  constructor(
    readonly orderId: OrderId,
    readonly customerId: CustomerId,
  ) {}
}

export class OrderConfirmedEvent implements DomainEvent {
  readonly eventId = crypto.randomUUID();
  readonly occurredAt = new Date();
  readonly eventType = 'order.confirmed';

  constructor(
    readonly orderId: OrderId,
    readonly total: Money,
  ) {}
}

export class OrderCancelledEvent implements DomainEvent {
  readonly eventId = crypto.randomUUID();
  readonly occurredAt = new Date();
  readonly eventType = 'order.cancelled';

  constructor(
    readonly orderId: OrderId,
    readonly reason: string,
  ) {}
}

// Domain event dispatcher
export class DomainEventDispatcher {
  private handlers = new Map<string, Function[]>();

  register(eventType: string, handler: Function): void {
    const existing = this.handlers.get(eventType) ?? [];
    this.handlers.set(eventType, [...existing, handler]);
  }

  async dispatch(events: DomainEvent[]): Promise<void> {
    for (const event of events) {
      const eventHandlers = this.handlers.get(event.eventType) ?? [];
      await Promise.all(eventHandlers.map(h => h(event)));
    }
  }
}

// Dispatch after saving aggregate
class OrderApplicationService {
  constructor(
    private orderRepo: OrderRepository,
    private eventDispatcher: DomainEventDispatcher,
  ) {}

  async confirmOrder(orderId: string): Promise<void> {
    const order = await this.orderRepo.findById(OrderId.from(orderId));
    if (!order) throw new Error('Order not found');

    order.confirm();

    await this.orderRepo.save(order);

    // Pull and dispatch events AFTER successful persistence
    const events = order.pullDomainEvents();
    await this.eventDispatcher.dispatch(events);
  }
}
```

### Anti-Corruption Layer
```typescript
// Protect your domain from external systems
// Translate external model to your domain model

// External payment provider model (messy, not your domain)
interface StripePaymentIntent {
  id: string;
  amount: number;           // in cents
  currency: string;
  status: string;           // 'succeeded', 'processing', 'requires_payment_method'
  payment_method_types: string[];
  metadata: Record<string, string>;
}

// Your domain model
export class Payment {
  constructor(
    readonly id: PaymentId,
    readonly orderId: OrderId,
    readonly amount: Money,
    readonly status: PaymentStatus,
    readonly completedAt: Date | null,
  ) {}
}

export enum PaymentStatus {
  Pending = 'pending',
  Completed = 'completed',
  Failed = 'failed',
}

// ACL: translates Stripe model to domain model
export class StripePaymentAdapter {
  private stripe: Stripe;

  constructor(apiKey: string) {
    this.stripe = new Stripe(apiKey);
  }

  async chargeOrder(orderId: OrderId, amount: Money): Promise<Payment> {
    // Call external system
    const intent = await this.stripe.paymentIntents.create({
      amount: amount.amount,  // already in cents
      currency: amount.currency.toLowerCase(),
      metadata: { order_id: orderId.value },
      confirm: true,
    });

    // Translate to domain model
    return this.toDomain(intent, orderId);
  }

  private toDomain(intent: StripePaymentIntent, orderId: OrderId): Payment {
    return new Payment(
      PaymentId.from(intent.id),
      orderId,
      Money.of(intent.amount / 100, intent.currency.toUpperCase()),
      this.translateStatus(intent.status),
      intent.status === 'succeeded' ? new Date() : null,
    );
  }

  private translateStatus(stripeStatus: string): PaymentStatus {
    switch (stripeStatus) {
      case 'succeeded': return PaymentStatus.Completed;
      case 'processing': return PaymentStatus.Pending;
      default: return PaymentStatus.Failed;
    }
  }
}
```

### Event Storming — Discovery Technique
```
Event Storming is a collaborative workshop to explore a domain

Steps:
1. Domain Events (orange sticky):
   - What happened? Past tense
   - OrderPlaced, PaymentFailed, ItemShipped, UserRegistered

2. Commands (blue sticky):
   - What triggered the event? Imperative
   - PlaceOrder, ProcessPayment, ShipItem, RegisterUser

3. Actors (yellow sticky):
   - Who issues the command?
   - Customer, Admin, System, Scheduler

4. Aggregates (pale yellow sticky):
   - What handles the command and produces the event?
   - Order, Payment, Shipment, User

5. Policies (purple sticky):
   - When Event X happens, do Command Y
   - When OrderConfirmed, then SendConfirmationEmail
   - When PaymentFailed, then CancelOrder

6. External Systems (pink sticky):
   - Stripe, SendGrid, Warehouse API

7. Read Models (green sticky):
   - What data does the actor need to make decisions?
   - Order summary, Inventory levels, Customer history

Result: natural bounded contexts emerge around clusters of aggregates
These become your microservices or modules
```

---

## Best Practices

- Spend time on strategic design before writing code — wrong boundaries are expensive
- Use ubiquitous language everywhere — code, tests, docs, conversations
- Keep aggregates small — one to three entities max, load eagerly
- Reference other aggregates by ID only — never hold object references across boundaries
- Prefer value objects over primitives — Money not float, Email not string
- Domain events should be facts, not commands — past tense, immutable
- Push logic into the domain — avoid anemic models with all logic in services
- Use anti-corruption layers when integrating with external systems

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Anemic domain model | Entities are data bags, logic is in services | Move business rules into entity methods |
| Giant aggregates | Lock contention, slow loads, complex invariants | Keep aggregates small, 1-3 entities |
| Object references across aggregates | Tight coupling, loading too much | Reference by ID only |
| Primitive obsession | string for email, float for money | Create value objects for domain concepts |
| Ignoring ubiquitous language | Code diverges from business language | Use domain terms directly in code |
| One bounded context for everything | God context, unmaintainable | Split by subdomain and team ownership |
| No anti-corruption layer | External model pollutes domain | Always translate at context boundaries |
| Skipping strategic design | Wrong service boundaries | Event storm first, code second |

---

## Related Skills

- **clean-architecture**: For structuring code within a bounded context
- **microservices-expert**: For aligning services with bounded contexts
- **event-driven-expert**: For domain events and integration events
- **design-patterns**: For tactical DDD implementation patterns
- **testing-expert**: For testing domain logic in isolation
- **system-design**: For strategic design at the system level