---
author: luo-kai
name: api-design-expert
description: Expert-level API design and developer experience. Use when designing REST APIs, versioning, backward compatibility, SDK design, error handling conventions, API documentation, or API governance. Also use when the user mentions 'API design', 'versioning', 'backward compatible', 'OpenAPI', 'SDK design', 'error format', 'pagination', 'rate limiting', 'API governance', or 'REST conventions'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# API Design Expert

You are an expert in API design with deep knowledge of REST conventions, OpenAPI, versioning strategies, developer experience, and building APIs that stand the test of time.

## Before Starting

1. **API type** — public, internal, partner, mobile backend?
2. **Protocol** — REST, GraphQL, gRPC, or hybrid?
3. **Problem type** — designing from scratch, reviewing existing API, versioning strategy?
4. **Consumers** — web frontend, mobile, third-party developers, other services?
5. **Constraints** — backward compatibility requirements, existing clients, standards?

---

## Core Expertise Areas

- **Resource design**: naming, hierarchy, granularity, relationships
- **HTTP semantics**: methods, status codes, idempotency, cacheability
- **Request/response design**: consistent envelopes, field naming, data types
- **Error handling**: RFC 7807 Problem Details, error codes, actionable messages
- **Pagination**: cursor-based, offset-based, keyset — when to use each
- **Versioning**: URI, header, query param strategies and trade-offs
- **OpenAPI 3.1**: writing specs, schema design, documentation
- **Breaking changes**: what is breaking, how to evolve APIs safely

---

## Key Patterns & Code

### REST Resource Design
```
Naming conventions:
  Use nouns, not verbs — resources are things, not actions
  Use plural nouns for collections
  Use lowercase with hyphens for multi-word resources

  WRONG:  GET /getUser, POST /createOrder, DELETE /removeItem
  RIGHT:  GET /users, POST /orders, DELETE /cart/items/{itemId}

Resource hierarchy:
  /users                      collection of users
  /users/{userId}             specific user
  /users/{userId}/orders      orders belonging to user
  /users/{userId}/orders/{orderId}  specific order of user

  Keep nesting shallow — max 2-3 levels deep
  WRONG: /users/{id}/orders/{id}/items/{id}/reviews/{id}
  RIGHT: /order-items/{id}/reviews  (flatten when it makes sense)

HTTP Methods:
  GET     Read resource — safe and idempotent
  POST    Create new resource or trigger action
  PUT     Replace entire resource — idempotent
  PATCH   Partial update — not necessarily idempotent
  DELETE  Remove resource — idempotent

Actions that do not map to CRUD:
  POST /orders/{id}/cancel     (action as sub-resource)
  POST /orders/{id}/confirm
  POST /payments/{id}/refund
  POST /users/{id}/password-reset
```

### HTTP Status Codes
```
2xx Success:
  200 OK              — GET, PUT, PATCH success
  201 Created         — POST created a new resource, include Location header
  202 Accepted        — request accepted for async processing
  204 No Content      — DELETE success, no body

3xx Redirection:
  301 Moved Permanently  — URL changed permanently
  304 Not Modified       — cache is still valid (ETag/If-None-Match)

4xx Client Errors:
  400 Bad Request        — malformed request, validation failed
  401 Unauthorized       — not authenticated (needs to log in)
  403 Forbidden          — authenticated but not authorized
  404 Not Found          — resource does not exist
  405 Method Not Allowed — HTTP method not supported
  409 Conflict           — state conflict (duplicate, wrong status)
  410 Gone               — resource permanently deleted
  422 Unprocessable      — validation failed (semantic errors)
  429 Too Many Requests  — rate limit exceeded

5xx Server Errors:
  500 Internal Server Error  — unexpected server error
  502 Bad Gateway            — upstream service failed
  503 Service Unavailable    — temporarily overloaded or maintenance
  504 Gateway Timeout        — upstream service timed out

Common mistakes:
  WRONG: 200 OK with { error: 'User not found' } in body
  RIGHT: 404 Not Found with error body

  WRONG: 403 for unauthenticated request
  RIGHT: 401 for unauthenticated, 403 for unauthorized

  WRONG: 500 for validation errors
  RIGHT: 400 or 422 for client-side errors
```

### Error Response Format — RFC 7807
```typescript
// RFC 7807 Problem Details — the industry standard error format
// https://tools.ietf.org/html/rfc7807

interface ProblemDetails {
  type: string;        // URI identifying the problem type
  title: string;       // Short human-readable summary
  status: number;      // HTTP status code
  detail?: string;     // Human-readable explanation of THIS occurrence
  instance?: string;   // URI of the specific occurrence
  // Additional fields for your specific error types
  [key: string]: any;
}

// Examples:

// Validation error
const validationError = {
  type: 'https://api.example.com/errors/validation-failed',
  title: 'Validation Failed',
  status: 422,
  detail: 'The request body contains invalid fields.',
  instance: '/orders/create#request-body',
  errors: [
    { field: 'email', code: 'INVALID_FORMAT', message: 'Must be a valid email address' },
    { field: 'quantity', code: 'OUT_OF_RANGE', message: 'Must be between 1 and 100' },
  ]
};

// Not found error
const notFoundError = {
  type: 'https://api.example.com/errors/resource-not-found',
  title: 'Resource Not Found',
  status: 404,
  detail: 'Order ord_123 was not found.',
  instance: '/orders/ord_123',
};

// Rate limit error
const rateLimitError = {
  type: 'https://api.example.com/errors/rate-limit-exceeded',
  title: 'Rate Limit Exceeded',
  status: 429,
  detail: 'You have exceeded 1000 requests per hour.',
  retryAfter: 3600,
  limit: 1000,
  remaining: 0,
  resetAt: '2024-01-01T13:00:00Z',
};

// Error middleware
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof ValidationError) {
    return res.status(422)
      .type('application/problem+json')
      .json({
        type: 'https://api.example.com/errors/validation-failed',
        title: 'Validation Failed',
        status: 422,
        detail: err.message,
        errors: err.fieldErrors,
      });
  }
  if (err instanceof NotFoundError) {
    return res.status(404)
      .type('application/problem+json')
      .json({
        type: 'https://api.example.com/errors/not-found',
        title: 'Not Found',
        status: 404,
        detail: err.message,
      });
  }
  // Default 500
  console.error(err);
  res.status(500)
    .type('application/problem+json')
    .json({
      type: 'https://api.example.com/errors/internal-error',
      title: 'Internal Server Error',
      status: 500,
      detail: 'An unexpected error occurred.',
    });
}
```

### Pagination Patterns
```typescript
// Offset pagination — simple but has issues at scale
// GET /users?page=2&per_page=20
// Problem: pages shift when items are added/deleted during pagination
interface OffsetPaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
  };
}

// Cursor pagination — preferred for large datasets and real-time data
// GET /users?cursor=eyJpZCI6IjEyMyJ9&limit=20
// Stable: new items do not affect pages already fetched
interface CursorPaginatedResponse<T> {
  data: T[];
  pagination: {
    nextCursor: string | null;   // null means no more pages
    prevCursor: string | null;
    hasMore: boolean;
    limit: number;
  };
}

// Cursor implementation
async function getUsers(cursor: string | null, limit: number = 20) {
  const decodedCursor = cursor ? JSON.parse(Buffer.from(cursor, 'base64url').toString()) : null;

  const users = await db.users.findMany({
    take: limit + 1,  // fetch one extra to check if there are more
    where: decodedCursor ? { id: { gt: decodedCursor.id } } : {},
    orderBy: { id: 'asc' },
  });

  const hasMore = users.length > limit;
  const data = users.slice(0, limit);

  const nextCursor = hasMore
    ? Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64url')
    : null;

  return {
    data,
    pagination: { nextCursor, hasMore, limit },
  };
}

// Use cursor pagination when: large datasets, real-time data, infinite scroll
// Use offset pagination when: small datasets, need jump to page, admin interfaces
```

### API Versioning Strategies
```
Option 1: URI Versioning — most common, most explicit
  /v1/users
  /v2/users
  Pros: obvious, easy to test in browser, cacheable
  Cons: 'dirty' URLs, clients must update base URL

Option 2: Header Versioning
  Accept: application/vnd.myapi.v2+json
  API-Version: 2
  Pros: clean URLs, REST purists prefer it
  Cons: harder to test, not visible in URL, less common

Option 3: Query Parameter
  /users?version=2
  Pros: easy to test
  Cons: pollutes query params, can conflict with filters

Recommendation: URI versioning for public APIs
  Explicit, widely understood, easy to route
  Run multiple versions simultaneously
  Deprecate with sunset dates, not immediate removal

Deprecation headers:
  Deprecation: true
  Sunset: Sat, 31 Dec 2024 23:59:59 GMT
  Link: <https://api.example.com/v2/users>; rel='successor-version'
```

### Breaking vs Non-Breaking Changes
```
NON-BREAKING (safe to deploy without version bump):
  + Add new optional field to response
  + Add new optional request parameter
  + Add new endpoint
  + Add new enum value (if consumers handle unknown values gracefully)
  + Make previously required field optional
  + Relax validation (accept more values)

BREAKING (requires new version):
  - Remove field from response
  - Rename field in response or request
  - Change field type (string to number, etc.)
  - Change URL structure
  - Change HTTP method for an endpoint
  - Add required field to request
  - Tighten validation (reject values previously accepted)
  - Change error response format
  - Change authentication mechanism
  - Change pagination format

Forward compatibility pattern:
  Clients should IGNORE unknown fields in responses
  This allows you to add fields without breaking old clients
  Enforce this in client SDKs with lenient deserialization
```

### Idempotency
```typescript
// Idempotency keys prevent duplicate operations on retries
// Critical for: payments, order creation, email sending

// Client sends unique idempotency key
// POST /payments
// Idempotency-Key: a8098c1a-f86e-11da-bd1a-00112444be1e

async function processPayment(req: Request, res: Response) {
  const idempotencyKey = req.headers['idempotency-key'] as string;

  if (!idempotencyKey) {
    return res.status(400).json({
      type: 'https://api.example.com/errors/missing-idempotency-key',
      title: 'Idempotency Key Required',
      status: 400,
      detail: 'Idempotency-Key header is required for payment operations.',
    });
  }

  // Check if already processed
  const existing = await redis.get('idempotency:' + idempotencyKey);
  if (existing) {
    const cached = JSON.parse(existing);
    return res.status(cached.status).json(cached.body);
  }

  // Process the payment
  const payment = await paymentService.charge(req.body);

  const responseBody = { paymentId: payment.id, status: payment.status };

  // Cache result with TTL
  await redis.setex(
    'idempotency:' + idempotencyKey,
    24 * 60 * 60,  // 24 hours
    JSON.stringify({ status: 201, body: responseBody })
  );

  res.status(201).json(responseBody);
}
```

### OpenAPI 3.1 Spec
```yaml
openapi: 3.1.0
info:
  title: Orders API
  version: 1.0.0
  description: API for managing customer orders
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /orders:
    post:
      summary: Create a new order
      operationId: createOrder
      tags: [Orders]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              ref: '#/components/schemas/CreateOrderRequest'
            example:
              customerId: cust_123
              items:
                - productId: prod_456
                  quantity: 2
      responses:
        '201':
          description: Order created
          headers:
            Location:
              description: URL of the created order
              schema:
                type: string
          content:
            application/json:
              schema:
                ref: '#/components/schemas/Order'
        '422':
          description: Validation failed
          content:
            application/problem+json:
              schema:
                ref: '#/components/schemas/ProblemDetails'

components:
  schemas:
    CreateOrderRequest:
      type: object
      required: [customerId, items]
      properties:
        customerId:
          type: string
          description: ID of the customer placing the order
          example: cust_123
        items:
          type: array
          minItems: 1
          items:
            ref: '#/components/schemas/OrderItem'

    ProblemDetails:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Response Envelope Design
```typescript
// Consistent response structure across all endpoints

// Single resource
interface ResourceResponse<T> {
  data: T;
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

// Collection
interface CollectionResponse<T> {
  data: T[];
  pagination: {
    nextCursor: string | null;
    hasMore: boolean;
    limit: number;
    total?: number;  // optional — expensive to compute
  };
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

// Field naming conventions
const good = {
  userId: 'usr_123',          // camelCase for all fields
  createdAt: '2024-01-01T...',// ISO 8601 for all dates
  amountCents: 9999,           // include unit in numeric field names
  isActive: true,              // boolean with is/has prefix
};

const bad = {
  user_id: 'usr_123',          // snake_case inconsistency
  created: '01/01/2024',       // ambiguous date format
  amount: 99.99,               // float — use cents instead
  active: true,                // missing is/has prefix
};

// Always use string IDs with prefix
// Prefix makes IDs self-describing and prevents mixing
const ids = {
  userId: 'usr_abc123',
  orderId: 'ord_xyz456',
  productId: 'prod_def789',
};
```

---

## Best Practices

- Design APIs for the consumer, not the implementation
- Be consistent — same patterns across all endpoints in the API
- Use RFC 7807 Problem Details for all error responses
- Require idempotency keys for all non-idempotent operations
- Prefer cursor pagination for collections — offset has problems at scale
- Never return 200 with an error body — use correct HTTP status codes
- Version APIs from day one — retrofitting versioning is painful
- Deprecate with Sunset headers and migration guides, not silent removal
- Write OpenAPI spec first — use it as contract before coding

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Verbs in URLs | /getUser, /createOrder | Use nouns: /users, /orders |
| Wrong status codes | 200 with error body | Use 4xx/5xx with problem details |
| No idempotency | Duplicate payments on retry | Require Idempotency-Key header |
| Offset pagination | Rows skip or duplicate on concurrent inserts | Use cursor-based pagination |
| Inconsistent naming | snake_case and camelCase mixed | Pick one convention, enforce with linting |
| Floating point for money | 0.1 + 0.2 = 0.30000000000000004 | Use integer cents, return as string |
| Breaking changes without versioning | Existing clients break silently | Version API, use Sunset header |
| Exposing internal IDs | Sequential IDs leak business data | Use prefixed UUIDs or opaque tokens |

---

## Related Skills

- **rest-api-expert**: For REST implementation patterns
- **graphql-expert**: For GraphQL API design
- **grpc-expert**: For gRPC service design
- **openapi-expert**: For OpenAPI specification writing
- **auth-expert**: For API authentication patterns
- **appsec-expert**: For API security design