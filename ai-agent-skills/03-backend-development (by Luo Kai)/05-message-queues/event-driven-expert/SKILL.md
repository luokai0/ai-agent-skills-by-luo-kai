---
author: luo-kai
name: event-driven-expert
description: Expert-level event-driven architecture. Use when designing event-driven systems, working with Kafka, RabbitMQ, AWS SQS/SNS, event sourcing, CQRS, pub/sub patterns, event schema design, or async workflows. Also use when the user mentions 'event-driven', 'Kafka', 'message queue', 'event sourcing', 'outbox pattern', 'pub/sub', 'consumer group', 'dead letter queue', or 'async workflow'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Event-Driven Architecture Expert

You are an expert in event-driven architecture with deep knowledge of Kafka, RabbitMQ, SQS/SNS, event design, delivery guarantees, and building reliable async systems.

## Before Starting

1. **Message broker** — Kafka, RabbitMQ, AWS SQS/SNS, EventBridge, Redis Streams?
2. **Use case** — async processing, event sourcing, CQRS, microservice communication?
3. **Delivery guarantee** — at-most-once, at-least-once, or exactly-once?
4. **Scale** — messages/second, consumer count, retention requirements?
5. **Problem type** — design, implementation, debugging lag, ordering issues?

---

## Core Expertise Areas

- **Event design**: CloudEvents spec, schema design, versioning, event vs command vs query
- **Kafka**: topics, partitions, consumer groups, offsets, retention, compaction
- **Delivery guarantees**: at-most-once, at-least-once, exactly-once semantics
- **Idempotent consumers**: deduplication, idempotency keys, at-least-once safe processing
- **Dead letter queues**: poison message handling, retry strategies, alerting
- **Outbox pattern**: reliable publishing with database transactions
- **Event sourcing**: append-only event log, projections, snapshots, rebuilding state
- **Schema evolution**: backward/forward compatibility, Avro, Schema Registry

---

## Key Patterns & Code

### Event vs Command vs Query
```
Event:   Something that HAPPENED in the past
         - Immutable fact — cannot be undone
         - Named in past tense: OrderCreated, PaymentFailed, UserRegistered
         - Publisher does not care who listens
         - Multiple consumers can react independently
         Example: { type: 'order.created', order_id: '123', user_id: '456' }

Command: Request to DO something
         - Has a single intended recipient
         - Named in imperative: CreateOrder, SendEmail, ChargePayment
         - Can be rejected
         - Sender usually wants a response
         Example: { type: 'send_email', to: 'alice@example.com', subject: 'Welcome' }

Query:   Request to READ something
         - Has a single intended recipient
         - Named as question: GetUser, FindOrders, SearchProducts
         - No side effects
         - Always gets a response

Rule of thumb:
  Use events for: things that happened, notifying other services
  Use commands for: requesting action from a specific service
  Use queries for: reading data from a specific service
  Topic names should reflect events: orders, payments, inventory (noun-plural)
  NOT: createOrder, processPayment (those are commands)
```

### Event Schema Design
```python
# CloudEvents spec — industry standard envelope
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any
import json

@dataclass
class CloudEvent:
    # Required CloudEvents attributes
    specversion: str = '1.0'
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ''           # URI of the event producer
    type: str = ''             # Reverse-DNS namespaced event type
    time: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    datacontenttype: str = 'application/json'
    data: Any = None

    # Custom extension attributes
    correlationid: str = ''    # trace ID for distributed tracing
    causationid: str = ''      # ID of the event that caused this one
    version: str = '1'         # schema version for evolution

    def to_dict(self) -> dict:
        return {
            'specversion': self.specversion,
            'id': self.id,
            'source': self.source,
            'type': self.type,
            'time': self.time,
            'datacontenttype': self.datacontenttype,
            'data': self.data,
            'correlationid': self.correlationid,
            'causationid': self.causationid,
            'version': self.version,
        }

# Event factory
def create_event(event_type: str, data: dict, correlation_id: str = None, causation_id: str = None) -> CloudEvent:
    return CloudEvent(
        source='https://myapp.com/order-service',
        type='com.myapp.' + event_type,
        data=data,
        correlationid=correlation_id or str(uuid.uuid4()),
        causationid=causation_id or '',
    )

# Example events
order_created = create_event(
    'order.created',
    {
        'order_id': 'ord_123',
        'user_id': 'usr_456',
        'items': [{'product_id': 'p1', 'quantity': 2, 'price': 9.99}],
        'total': 19.98,
        'currency': 'USD',
    }
)

payment_failed = create_event(
    'payment.failed',
    {
        'order_id': 'ord_123',
        'reason': 'insufficient_funds',
        'amount': 19.98,
    },
    causation_id=order_created.id,
    correlation_id=order_created.correlationid,
)
```

### Kafka — Producer & Consumer
```python
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json
import logging

# Producer with reliability settings
def create_producer(bootstrap_servers: str) -> Producer:
    return Producer({
        'bootstrap.servers': bootstrap_servers,
        'acks': 'all',                  # wait for all replicas to acknowledge
        'retries': 5,                   # retry on transient failures
        'retry.backoff.ms': 300,
        'enable.idempotence': True,     # exactly-once producer semantics
        'max.in.flight.requests.per.connection': 5,
        'compression.type': 'snappy',   # compress messages
        'linger.ms': 5,                 # batch messages for 5ms
        'batch.size': 16384,            # 16KB batch size
    })

def publish_event(producer: Producer, topic: str, event: CloudEvent, key: str = None):
    def delivery_report(err, msg):
        if err:
            logging.error('Failed to deliver to ' + msg.topic() + ': ' + str(err))
        else:
            logging.debug('Delivered to ' + msg.topic() + ' [' + str(msg.partition()) + '] @ ' + str(msg.offset()))

    producer.produce(
        topic=topic,
        key=key.encode() if key else None,
        value=json.dumps(event.to_dict()).encode(),
        headers={
            'event-type': event.type,
            'event-id': event.id,
            'correlation-id': event.correlationid,
        },
        callback=delivery_report,
    )

# Consumer with at-least-once semantics
def create_consumer(bootstrap_servers: str, group_id: str) -> Consumer:
    return Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,    # manual commit for reliability
        'max.poll.interval.ms': 300000, # 5 min max processing time
        'session.timeout.ms': 30000,
        'heartbeat.interval.ms': 10000,
    })

def consume_events(consumer: Consumer, topics: list[str], handler, batch_size: int = 100):
    consumer.subscribe(topics)
    try:
        while True:
            messages = consumer.consume(num_messages=batch_size, timeout=1.0)
            if not messages:
                continue

            for msg in messages:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    raise KafkaException(msg.error())

                try:
                    event = json.loads(msg.value().decode())
                    handler(event)
                except Exception as e:
                    logging.error('Failed to process message: ' + str(e))
                    # Send to DLQ instead of blocking
                    send_to_dlq(msg, str(e))

            # Commit after processing entire batch
            consumer.commit(asynchronous=False)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
```

### Idempotent Consumer
```python
import redis
from datetime import timedelta

class IdempotentEventHandler:
    def __init__(self, redis_client: redis.Redis, handler_name: str):
        self.redis = redis_client
        self.handler_name = handler_name
        self.ttl = timedelta(days=7)  # keep dedup keys for 7 days

    def handle(self, event: dict):
        event_id = event.get('id') or event.get('event_id')
        if not event_id:
            raise ValueError('Event must have an id for idempotency')

        # Dedup key per handler — same event can be processed by different handlers
        dedup_key = 'processed:' + self.handler_name + ':' + event_id

        # Atomic check-and-set
        was_set = self.redis.set(dedup_key, '1', nx=True, ex=int(self.ttl.total_seconds()))

        if not was_set:
            logging.info('Skipping duplicate event ' + event_id)
            return  # already processed

        try:
            self._process(event)
        except Exception:
            # Remove dedup key on failure so event can be retried
            self.redis.delete(dedup_key)
            raise

    def _process(self, event: dict):
        raise NotImplementedError

# Usage
class OrderCreatedHandler(IdempotentEventHandler):
    def __init__(self, redis_client, db, email_service):
        super().__init__(redis_client, 'order-confirmation-email')
        self.db = db
        self.email_service = email_service

    def _process(self, event: dict):
        order_id = event['data']['order_id']
        user_id = event['data']['user_id']

        user = self.db.users.find_by_id(user_id)
        order = self.db.orders.find_by_id(order_id)

        self.email_service.send_order_confirmation(
            to=user.email,
            order=order,
        )
        logging.info('Sent confirmation email for order ' + order_id)
```

### Dead Letter Queue Pattern
```python
import json
import traceback
from datetime import datetime

class DLQHandler:
    def __init__(self, producer, dlq_topic: str = 'dlq'):
        self.producer = producer
        self.dlq_topic = dlq_topic

    def send_to_dlq(self, original_message, error: Exception, attempt: int = 1):
        dlq_event = {
            'original_topic': original_message.topic(),
            'original_partition': original_message.partition(),
            'original_offset': original_message.offset(),
            'original_key': original_message.key().decode() if original_message.key() else None,
            'original_value': original_message.value().decode(),
            'error_message': str(error),
            'error_type': type(error).__name__,
            'error_traceback': traceback.format_exc(),
            'failed_at': datetime.utcnow().isoformat(),
            'attempt': attempt,
        }

        self.producer.produce(
            topic=self.dlq_topic,
            key=original_message.key(),
            value=json.dumps(dlq_event).encode(),
        )
        self.producer.flush()
        logging.error('Sent to DLQ: ' + str(error))

# Retry with exponential backoff before DLQ
class RetryHandler:
    def __init__(self, handler, dlq: DLQHandler, max_retries: int = 3):
        self.handler = handler
        self.dlq = dlq
        self.max_retries = max_retries

    def handle(self, message, event: dict):
        for attempt in range(1, self.max_retries + 1):
            try:
                self.handler(event)
                return  # success
            except Exception as e:
                if attempt == self.max_retries:
                    logging.error('Max retries exceeded, sending to DLQ')
                    self.dlq.send_to_dlq(message, e, attempt)
                    return
                wait = 2 ** attempt
                logging.warning('Attempt ' + str(attempt) + ' failed, retrying in ' + str(wait) + 's')
                time.sleep(wait)
```

### Event Sourcing
```python
from dataclasses import dataclass, field
from typing import List
import json

# Events are the source of truth
@dataclass
class OrderEvent:
    event_id: str
    aggregate_id: str
    event_type: str
    data: dict
    version: int
    occurred_at: str

# Aggregate rebuilds state from events
@dataclass
class Order:
    id: str = ''
    user_id: str = ''
    status: str = ''
    items: list = field(default_factory=list)
    total: float = 0.0
    version: int = 0

    @classmethod
    def from_events(cls, events: List[OrderEvent]) -> 'Order':
        order = cls()
        for event in events:
            order.apply(event)
        return order

    def apply(self, event: OrderEvent):
        if event.event_type == 'order.created':
            self.id = event.aggregate_id
            self.user_id = event.data['user_id']
            self.items = event.data['items']
            self.total = event.data['total']
            self.status = 'pending'

        elif event.event_type == 'order.confirmed':
            self.status = 'confirmed'

        elif event.event_type == 'order.cancelled':
            self.status = 'cancelled'

        elif event.event_type == 'order.item_added':
            self.items.append(event.data['item'])
            self.total += event.data['item']['price'] * event.data['item']['quantity']

        self.version = event.version

# Event store
class EventStore:
    def __init__(self, db):
        self.db = db

    async def append(self, aggregate_id: str, events: List[OrderEvent], expected_version: int):
        # Optimistic concurrency control
        current_version = await self.db.events.get_version(aggregate_id)
        if current_version != expected_version:
            raise ConcurrencyError('Expected version ' + str(expected_version) + ', got ' + str(current_version))

        for event in events:
            await self.db.events.insert(event)

    async def load(self, aggregate_id: str, from_version: int = 0) -> List[OrderEvent]:
        return await self.db.events.find(
            {'aggregate_id': aggregate_id, 'version': {'$gte': from_version}},
            sort=[('version', 1)]
        )

# Projection — builds read model from events
class OrderSummaryProjection:
    def __init__(self, read_db):
        self.read_db = read_db

    async def handle(self, event: OrderEvent):
        if event.event_type == 'order.created':
            await self.read_db.order_summaries.upsert(
                {'order_id': event.aggregate_id},
                {
                    'order_id': event.aggregate_id,
                    'user_id': event.data['user_id'],
                    'total': event.data['total'],
                    'status': 'pending',
                    'item_count': len(event.data['items']),
                    'created_at': event.occurred_at,
                }
            )
        elif event.event_type == 'order.confirmed':
            await self.read_db.order_summaries.update(
                {'order_id': event.aggregate_id},
                {'status': 'confirmed'},
            )
```

### Schema Evolution with Avro
```python
# Schema Registry ensures backward/forward compatibility

# v1 schema
order_created_v1 = {
    'type': 'record',
    'name': 'OrderCreated',
    'namespace': 'com.myapp.orders',
    'fields': [
        {'name': 'order_id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string'},
        {'name': 'total', 'type': 'double'},
    ]
}

# v2 schema — backward compatible changes only:
# - Add optional fields with defaults
# - Remove fields (forward compat, not backward)
# - Rename fields using aliases
order_created_v2 = {
    'type': 'record',
    'name': 'OrderCreated',
    'namespace': 'com.myapp.orders',
    'fields': [
        {'name': 'order_id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string'},
        {'name': 'total', 'type': 'double'},
        # New optional field with default — backward compatible
        {'name': 'currency', 'type': 'string', 'default': 'USD'},
        # New optional field — backward compatible
        {'name': 'coupon_code', 'type': ['null', 'string'], 'default': None},
    ]
}

# NEVER do these — breaking changes:
# - Remove required field
# - Change field type
# - Rename field without alias
# - Change field from optional to required
```

### AWS SQS/SNS Pattern
```python
import boto3
import json
from typing import Callable

# SNS fan-out to multiple SQS queues
# SNS topic -> SQS queue per consumer

class SQSConsumer:
    def __init__(self, queue_url: str, region: str = 'us-east-1'):
        self.sqs = boto3.client('sqs', region_name=region)
        self.queue_url = queue_url

    def consume(self, handler: Callable, batch_size: int = 10):
        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=batch_size,
                WaitTimeSeconds=20,  # long polling — cheaper
                MessageAttributeNames=['All'],
                AttributeNames=['All'],
            )

            messages = response.get('Messages', [])
            if not messages:
                continue

            for message in messages:
                try:
                    # SNS wraps the message in an envelope
                    body = json.loads(message['Body'])
                    if 'Message' in body:
                        # Message came via SNS
                        event = json.loads(body['Message'])
                    else:
                        # Direct SQS message
                        event = body

                    handler(event)

                    # Delete on success
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle'],
                    )
                except Exception as e:
                    logging.error('Failed to process SQS message: ' + str(e))
                    # Do NOT delete — message will become visible again after visibility timeout
                    # After maxReceiveCount it goes to DLQ automatically

class SNSPublisher:
    def __init__(self, topic_arn: str, region: str = 'us-east-1'):
        self.sns = boto3.client('sns', region_name=region)
        self.topic_arn = topic_arn

    def publish(self, event_type: str, payload: dict, group_id: str = None):
        params = {
            'TopicArn': self.topic_arn,
            'Message': json.dumps(payload),
            'MessageAttributes': {
                'event_type': {
                    'DataType': 'String',
                    'StringValue': event_type,
                }
            }
        }
        # For FIFO topics
        if group_id:
            params['MessageGroupId'] = group_id

        self.sns.publish(**params)
```

---

## Best Practices

- Name events in past tense — they represent facts that already happened
- Always include event ID, timestamp, and source in every event
- Design for idempotency — events WILL be delivered more than once
- Use the outbox pattern for reliable publishing — never publish without DB transaction
- Set up dead letter queues from day one — poison messages WILL happen
- Use schema registry for Avro/Protobuf — prevents breaking schema changes
- Choose partition key carefully in Kafka — determines ordering and parallelism
- Monitor consumer lag — it is the most important metric for async systems
- Include correlation ID in every event for distributed tracing

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Non-idempotent handlers | Duplicate events cause duplicate side effects | Implement deduplication with Redis or DB |
| Publishing without transaction | Event published but DB write fails | Use outbox pattern |
| No DLQ | Poison messages block entire consumer | Always configure DLQ |
| Wrong partition key | Hot partition, ordering broken | Choose key that distributes evenly |
| Storing commands as events | Event log polluted with commands | Keep events and commands separate |
| Breaking schema changes | Consumers crash on deployment | Use schema registry, only additive changes |
| Ignoring consumer lag | Queue grows unbounded | Monitor lag, alert when it exceeds threshold |
| Tight coupling via events | Service A knows about Service B internals | Events should be domain facts not service calls |

---

## Related Skills

- **microservices-expert**: For microservice communication patterns
- **apache-kafka-expert**: For deep Kafka internals and tuning
- **aws-expert**: For SQS, SNS, and EventBridge patterns
- **monitoring-expert**: For consumer lag and event pipeline observability
- **database-design**: For event store and outbox table design
- **domain-driven-design**: For event naming and bounded context design