---
author: luo-kai
name: microservices-expert
description: Expert-level microservices architecture. Use when designing microservices, service boundaries, inter-service communication, saga pattern, CQRS, event sourcing, service mesh, API gateways, or managing distributed systems complexity. Also use when the user mentions 'microservices', 'service boundary', 'saga pattern', 'service mesh', 'CQRS', 'event sourcing', 'API gateway', 'distributed transaction', or 'service decomposition'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Microservices Expert

You are an expert in microservices architecture with deep knowledge of service decomposition, inter-service communication, distributed data management, and operational patterns.

## Before Starting

1. **Current state** — monolith being split, or designing from scratch?
2. **Team structure** — how many teams? Conway's Law applies
3. **Scale** — what are the scalability requirements driving the decision?
4. **Problem type** — service design, communication pattern, data consistency, deployment?
5. **Tech stack** — language, message broker, service mesh, cloud provider?

---

## Core Expertise Areas

- **Service decomposition**: bounded contexts, DDD, single responsibility, team ownership
- **Communication**: sync (REST, gRPC) vs async (Kafka, SQS), choreography vs orchestration
- **Data management**: database per service, eventual consistency, CQRS, event sourcing
- **Saga pattern**: distributed transactions without 2PC, compensating transactions
- **Resilience**: circuit breakers, retries, timeouts, bulkheads, graceful degradation
- **Service mesh**: Istio, Linkerd — traffic management, mTLS, observability
- **API gateway**: routing, auth, rate limiting, request aggregation
- **Testing**: consumer-driven contracts, component tests, integration tests

---

## Key Patterns & Code

### When to Use Microservices
```
Use microservices when:
  - Multiple teams working on the same codebase causing conflicts
  - Different parts of the system have very different scaling needs
  - Different parts need different technology stacks
  - Independent deployment is critical for business velocity
  - Team size exceeds 'two pizza rule' (8-10 people per service)

Do NOT use microservices when:
  - Team is small (< 10 engineers total)
  - Domain is not well understood yet (premature decomposition is painful)
  - No operational maturity (CI/CD, monitoring, containers)
  - Starting a new product — start with a modular monolith

Conway's Law:
  'Organizations design systems that mirror their communication structure'
  Your service boundaries WILL follow your team boundaries
  Design teams first, then services — not the other way around

Rule of thumb:
  A service should be ownable by ONE team
  A team can own MULTIPLE services
  No service should require changes from multiple teams for a single feature
```

### Service Decomposition — Bounded Contexts
```
Example: E-commerce platform decomposition

Monolith modules → Microservices:

  Order Management     → order-service
    - Create order
    - Cancel order
    - Order history

  Inventory            → inventory-service
    - Check stock
    - Reserve items
    - Restock

  Payment              → payment-service
    - Process payment
    - Refund
    - Payment history

  User Accounts        → user-service
    - Registration
    - Authentication
    - Profile

  Notifications        → notification-service
    - Email
    - SMS
    - Push notifications

  Search               → search-service
    - Product search
    - Autocomplete
    - Faceted filters

Anti-patterns to avoid:
  - Nanoservices: too fine-grained, chatty, high overhead
  - Shared database: defeats data isolation purpose
  - Distributed monolith: all services deploy together, tightly coupled
  - Chatty services: hundreds of sync calls per user request
```

### Inter-Service Communication
```python
# Synchronous: REST — use for queries and commands that need immediate response
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class InventoryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(5.0),  # always set timeout
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def check_stock(self, product_id: str, quantity: int) -> bool:
        response = await self.client.get(
            '/api/inventory/' + product_id,
            params={'quantity': quantity},
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return response.json()['available']

    async def reserve_stock(self, product_id: str, quantity: int, order_id: str) -> str:
        response = await self.client.post(
            '/api/inventory/' + product_id + '/reserve',
            json={'quantity': quantity, 'order_id': order_id},
        )
        response.raise_for_status()
        return response.json()['reservation_id']

# Asynchronous: Events via Kafka — use for commands that can be processed later
from confluent_kafka import Producer, Consumer
import json

class EventPublisher:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def publish(self, topic: str, event_type: str, payload: dict, key: str = None):
        event = {
            'event_type': event_type,
            'payload': payload,
            'metadata': {
                'service': 'order-service',
                'version': '1.0',
                'timestamp': datetime.utcnow().isoformat(),
                'event_id': str(uuid.uuid4()),
            }
        }
        self.producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(event).encode(),
            callback=self._delivery_report,
        )
        self.producer.flush()

    def _delivery_report(self, err, msg):
        if err:
            logging.error('Failed to deliver message: ' + str(err))

# Usage in order service
class OrderService:
    def __init__(self, db, events: EventPublisher, inventory: InventoryClient):
        self.db = db
        self.events = events
        self.inventory = inventory

    async def create_order(self, user_id: str, items: list) -> Order:
        # Sync: check inventory (needs immediate answer)
        for item in items:
            if not await self.inventory.check_stock(item.product_id, item.quantity):
                raise InsufficientStockError(item.product_id)

        # Create order in DB
        order = await self.db.orders.create(user_id=user_id, items=items, status='pending')

        # Async: publish event (other services react independently)
        self.events.publish(
            topic='orders',
            event_type='order.created',
            payload={'order_id': order.id, 'user_id': user_id, 'items': items},
            key=order.id,
        )

        return order
```

### Saga Pattern — Choreography
```python
# Choreography: each service listens to events and reacts
# No central coordinator — services are fully decoupled
# Good for: simple workflows, high scalability
# Bad for: complex workflows, hard to track state

# Order Service: publishes order.created
# Inventory Service: listens, reserves stock, publishes stock.reserved
# Payment Service: listens, charges card, publishes payment.completed
# Notification Service: listens to payment.completed, sends confirmation

# If payment fails:
# Payment Service publishes payment.failed
# Inventory Service listens, releases reservation
# Order Service listens, marks order as failed
# Notification Service listens, sends failure email

class InventoryEventHandler:
    def __init__(self, db, events: EventPublisher):
        self.db = db
        self.events = events

    async def handle(self, event: dict):
        event_type = event['event_type']

        if event_type == 'order.created':
            await self._handle_order_created(event['payload'])
        elif event_type == 'payment.failed':
            await self._handle_payment_failed(event['payload'])

    async def _handle_order_created(self, payload: dict):
        order_id = payload['order_id']
        items = payload['items']

        try:
            # Reserve all items atomically
            reservation_ids = []
            for item in items:
                res_id = await self.db.reservations.create(
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    order_id=order_id,
                )
                reservation_ids.append(res_id)

            self.events.publish(
                topic='inventory',
                event_type='stock.reserved',
                payload={'order_id': order_id, 'reservation_ids': reservation_ids},
                key=order_id,
            )
        except InsufficientStockError as e:
            # Compensating transaction — trigger saga rollback
            self.events.publish(
                topic='inventory',
                event_type='stock.reservation.failed',
                payload={'order_id': order_id, 'reason': str(e)},
                key=order_id,
            )

    async def _handle_payment_failed(self, payload: dict):
        # Compensating transaction: release reservations
        await self.db.reservations.release_by_order(payload['order_id'])
```

### Saga Pattern — Orchestration
```python
# Orchestration: central coordinator manages the workflow
# Good for: complex workflows, easy to track state, easier to debug
# Bad for: coordinator is a bottleneck, tight coupling to coordinator

class CreateOrderSaga:
    def __init__(self, inventory: InventoryClient, payment: PaymentClient, db):
        self.inventory = inventory
        self.payment = payment
        self.db = db

    async def execute(self, order_data: dict) -> dict:
        saga_state = SagaState(order_id=order_data['order_id'])

        # Step 1: Reserve inventory
        try:
            reservation_id = await self.inventory.reserve(
                items=order_data['items'],
                order_id=order_data['order_id'],
            )
            saga_state.reservation_id = reservation_id
        except Exception as e:
            await self._fail(saga_state, 'inventory_reservation_failed', str(e))
            raise

        # Step 2: Process payment
        try:
            payment_id = await self.payment.charge(
                amount=order_data['total'],
                user_id=order_data['user_id'],
                order_id=order_data['order_id'],
            )
            saga_state.payment_id = payment_id
        except Exception as e:
            # Compensate: release reservation
            await self.inventory.release(saga_state.reservation_id)
            await self._fail(saga_state, 'payment_failed', str(e))
            raise

        # Step 3: Confirm order
        order = await self.db.orders.confirm(
            order_id=order_data['order_id'],
            payment_id=saga_state.payment_id,
        )

        await self._complete(saga_state)
        return order

    async def _fail(self, state, reason, detail):
        await self.db.saga_log.record(
            order_id=state.order_id,
            status='failed',
            reason=reason,
            detail=detail,
        )

    async def _complete(self, state):
        await self.db.saga_log.record(
            order_id=state.order_id,
            status='completed',
        )
```

### Circuit Breaker
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED    = 'closed'     # normal — requests flow through
    OPEN      = 'open'       # failing — requests fail fast
    HALF_OPEN = 'half_open'  # testing — let a few through

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError('Circuit breaker is open')

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.success_count = 0

# Usage
inventory_breaker = CircuitBreaker(failure_threshold=5, timeout=30)

async def check_stock_safe(product_id: str) -> bool:
    try:
        return await inventory_breaker.call(inventory_client.check_stock, product_id)
    except CircuitOpenError:
        # Graceful degradation — assume in stock when circuit is open
        logging.warning('Inventory circuit open — assuming in stock')
        return True
```

### Outbox Pattern — Reliable Event Publishing
```python
# Problem: writing to DB and publishing event are not atomic
# If DB write succeeds but Kafka publish fails = data inconsistency

# Solution: Outbox pattern
# 1. Write business data AND event to DB in same transaction
# 2. Separate process reads outbox and publishes to Kafka
# 3. Mark as published after successful delivery

async def create_order_with_outbox(order_data: dict, db):
    async with db.transaction():
        # Write order
        order = await db.orders.create(order_data)

        # Write event to outbox (same transaction)
        await db.outbox.create({
            'aggregate_type': 'Order',
            'aggregate_id': order.id,
            'event_type': 'order.created',
            'payload': json.dumps({'order_id': order.id, 'user_id': order.user_id}),
            'created_at': datetime.utcnow(),
            'published': False,
        })

    return order

# Outbox publisher (runs as separate process or background task)
async def publish_outbox_events(db, publisher: EventPublisher):
    while True:
        # Fetch unpublished events
        events = await db.outbox.find_unpublished(limit=100)

        for event in events:
            try:
                publisher.publish(
                    topic=event.aggregate_type.lower() + 's',
                    event_type=event.event_type,
                    payload=json.loads(event.payload),
                    key=event.aggregate_id,
                )
                await db.outbox.mark_published(event.id)
            except Exception as e:
                logging.error('Failed to publish event ' + str(event.id) + ': ' + str(e))

        await asyncio.sleep(1)
```

### CQRS — Command Query Responsibility Segregation
```python
# Separate read and write models
# Write side: normalized, consistent, handles commands
# Read side: denormalized, optimized for queries, may be eventually consistent

# Command handler (write side)
class CreateOrderHandler:
    def __init__(self, db, events: EventPublisher):
        self.db = db
        self.events = events

    async def handle(self, command: CreateOrderCommand) -> str:
        # Validate
        if not command.items:
            raise ValueError('Order must have at least one item')

        # Write to normalized DB
        order = await self.db.orders.create({
            'id': str(uuid.uuid4()),
            'user_id': command.user_id,
            'status': 'pending',
            'created_at': datetime.utcnow(),
        })
        for item in command.items:
            await self.db.order_items.create({
                'order_id': order.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': item.price,
            })

        # Publish event for read side to update
        self.events.publish(
            topic='orders',
            event_type='order.created',
            payload={
                'order_id': order.id,
                'user_id': command.user_id,
                'items': [i.__dict__ for i in command.items],
            },
        )
        return order.id

# Read model updater (updates denormalized read DB from events)
class OrderReadModelUpdater:
    def __init__(self, read_db):
        self.read_db = read_db

    async def handle_order_created(self, event: dict):
        payload = event['payload']
        # Upsert into denormalized read model
        await self.read_db.order_summaries.upsert({
            'order_id': payload['order_id'],
            'user_id': payload['user_id'],
            'item_count': len(payload['items']),
            'total': sum(i['price'] * i['quantity'] for i in payload['items']),
            'status': 'pending',
            'created_at': event['metadata']['timestamp'],
        })

# Query handler (read side) — fast, simple queries
class OrderQueryHandler:
    def __init__(self, read_db):
        self.read_db = read_db

    async def get_user_orders(self, user_id: str, page: int = 1) -> list:
        # Simple query on denormalized read model
        return await self.read_db.order_summaries.find(
            {'user_id': user_id},
            sort=[('created_at', -1)],
            limit=20,
            skip=(page - 1) * 20,
        )
```

---

## Best Practices

- Start with a modular monolith — extract services only when you have clear boundaries
- Design services around business capabilities, not technical layers
- Each service must own its data — no shared databases
- Prefer async communication for operations that do not need immediate response
- Design for failure — any service can be slow or unavailable at any time
- Implement idempotency for all event handlers — events may be delivered more than once
- Use the outbox pattern for reliable event publishing
- Version your APIs and events — never break consumers without notice
- Invest in observability before going to production — distributed tracing is essential

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Shared database | Services tightly coupled, cannot deploy independently | Each service owns its DB schema |
| Distributed monolith | Services deploy together, call each other synchronously | Async communication, independent deployments |
| No idempotency | Duplicate events cause duplicate side effects | Add idempotency key to all handlers |
| Chatty services | Hundreds of sync calls per user request = high latency | Coarsen service boundaries or use async |
| No circuit breakers | One slow service cascades to bring down all services | Circuit breakers on all external calls |
| 2PC distributed transactions | Locks across services, availability nightmare | Use saga pattern instead |
| Premature decomposition | Wrong boundaries, expensive to change | Start with monolith, extract when boundaries are clear |
| No contract testing | Service changes break consumers silently | Implement consumer-driven contract testing with Pact |

---

## Related Skills

- **event-driven-expert**: For Kafka and event-driven patterns
- **domain-driven-design**: For identifying correct service boundaries
- **docker-expert**: For containerizing microservices
- **kubernetes-expert**: For orchestrating microservices
- **monitoring-expert**: For distributed tracing and observability
- **api-design-expert**: For designing service APIs