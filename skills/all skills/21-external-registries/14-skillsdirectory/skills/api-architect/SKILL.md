---
name: api-architect
description: Design and build production-grade RESTful and GraphQL APIs with proper authentication, error handling, rate limiting, and documentation. Use when designing APIs, creating API specifications, or reviewing API architecture.
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, GitHub Copilot, Claude Code, and any AI coding assistant
metadata:
  author: skillsdirectory
  version: "1.0"
  category: web-development
  tools: cursor, windsurf, copilot, claude-code
---

# API Architecture Expert

You design and build APIs that are consistent, well-documented, and a joy to consume.

## RESTful API Design

### URL Convention
```
GET    /api/v1/users          → List users
GET    /api/v1/users/:id      → Get single user
POST   /api/v1/users          → Create user
PUT    /api/v1/users/:id      → Full update
PATCH  /api/v1/users/:id      → Partial update
DELETE /api/v1/users/:id      → Delete user

# Nested resources
GET    /api/v1/users/:id/orders    → User's orders
POST   /api/v1/users/:id/orders    → Create order for user
```

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Error Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ]
  }
}
```

### HTTP Status Codes
| Code | When |
|---|---|
| `200` | Success |
| `201` | Created |
| `204` | No Content (delete success) |
| `400` | Bad request / validation error |
| `401` | Not authenticated |
| `403` | Not authorized |
| `404` | Not found |
| `409` | Conflict (duplicate) |
| `422` | Unprocessable entity |
| `429` | Rate limited |
| `500` | Server error |

## Security
- HTTPS only
- Bearer token authentication (JWT / API keys)
- Rate limiting per endpoint
- Input validation and sanitization
- CORS properly configured
- No sensitive data in URLs
- Request/response logging (without secrets)

## Pagination
```
GET /api/v1/users?page=2&per_page=20
GET /api/v1/users?cursor=abc123&limit=20  # Cursor-based
```

## Versioning
- URL path: `/api/v1/users` (recommended)
- Header: `Accept: application/vnd.api+json;version=1`

## Documentation
- OpenAPI/Swagger spec for every API
- Request/response examples
- Authentication guide
- Rate limit documentation
- Error code reference
