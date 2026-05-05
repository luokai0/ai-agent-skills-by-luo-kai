# API Contract: [Feature Name]

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Owner:** [Team]
**Status:** [Draft / In Review / Approved]

> **Audience:** Backend developers, Frontend developers, QA engineers
> **Naming rule:** Follow existing codebase patterns if Swagger was provided. Mark unknowns as [TBD — confirm with Engineering].
> **No implementation details** — no code, SQL, class names, or internal logic.

---

## 1. API Overview

### Summary
[2–3 sentences: what these APIs enable and who uses them]

### Endpoints Summary

| Endpoint | Method | Purpose | Auth Required | EXISTING/NEW |
|----------|--------|---------|---------------|--------------|
| `/api/[resource]` | POST | [purpose] | Yes/No | NEW |
| `/api/[resource]/{id}` | GET | [purpose] | Yes | EXISTING |

---

## 2. Authentication & Authorization

### Authentication
- **Type:** [Bearer Token / JWT / OAuth2 / API Key]
- **Header:** `Authorization: Bearer {access_token}`
- **Token source:** [How to obtain — e.g., `/auth/login` endpoint]
- **Token expiry:** [Duration]

### Authorization Rules
- [Role/permission required: e.g., "user must have `reports:read` permission"]
- [Access control rule: e.g., "user can only access data within their account"]
- [Cross-context rule: e.g., "no cross-account data access"]

---

## 3. Endpoints

---

### [Endpoint 1 Name]

**`[METHOD] /api/[path]`** — EXISTING / NEW

**Purpose:** [What this does and when to use it]

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Query Parameters:**

| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `param1` | string | Yes | [description] | [rules] |

**Request Body:**

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `field1` | string | Yes | [description] | [rules, e.g., max 100 chars] |
| `field2` | integer | No | [description] | [rules, e.g., min 1, max 90] |

---

#### Responses

**200 OK — Success (with data)**
- Content-Type: `[application/json or text/csv]`
- Body: `[structure or "See example below"]`

**200 OK — Success (no data)**
- Body: `{"message": "[message text]", ...}`

**422 Unprocessable Entity — Validation Error**

Standard error shape:
```json
{
  "error": "[Error type description]",
  "message": "[User-friendly message]",
  "field": "[field name]"
}
```

| Error Message | Field | Condition |
|---------------|-------|-----------|
| "[error text]" | `[field]` | [when this occurs] |

**401 Unauthorized** — Missing or invalid token
**403 Forbidden** — User lacks permission
**500 Internal Server Error** — Unexpected error (include `requestId`)
**503 Service Unavailable** — Dependent service down
**504 Gateway Timeout** — Processing exceeded timeout

---

#### Performance

- **Timeout:** [X] minutes (frontend) / [Y] minutes (backend processing)
- **Rate limiting:** [X] requests per minute per user
- **Expected response time:**
  - Small dataset: [time]
  - Large dataset: [time]

---

#### Example Request (cURL)
```bash
curl -X [METHOD] "https://api.example.com/api/[path]" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value1"}'
```

---

### [Endpoint 2 Name]
*(Repeat structure above)*

---

## 4. Data Models

### [Model Name]

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | integer | Unique identifier | PK, auto-generated |
| `field1` | string | [description] | Max [N] chars, required |
| `createdAt` | ISO 8601 datetime | Creation timestamp | UTC, auto-set |

---

## 5. Error Handling

### Standard Error Response Shape
```json
{
  "error": "[Type — e.g., 'Validation Error']",
  "message": "[User-friendly message]",
  "field": "[field name — validation errors only]",
  "requestId": "[UUID — server errors only, for support]"
}
```

### HTTP Status Code Reference

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful request |
| 201 | Created | Resource created |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Business validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected error |
| 503 | Service Unavailable | Dependent service down |
| 504 | Gateway Timeout | Processing exceeded limit |

### Retry Strategy
- **Retryable:** 503, 504, 429
- **Non-retryable:** 400, 401, 403, 404, 422, 500
- **Client retry logic:** Wait 5s → retry → wait 15s → retry → wait 30s → fail after 3 attempts

---

## 6. Security

### Input Validation
- All input sanitized (parameterized queries, no raw SQL)
- Strict format validation (dates, enums, types)
- Array length limits enforced

### Data Protection
- HTTPS only (TLS 1.2+)
- Tokens encrypted in transit
- User access limited to authorized data scope

### Rate Limiting
- **Limit:** [X] requests per [timeframe]
- **Response:** HTTP 429 `{"error": "Rate Limit Exceeded", "retryAfter": [seconds]}`

---

## 7. Performance

### Expected Load
- Peak concurrent requests: [N] — [TBD if unknown]
- Average requests per day: [N]
- Max payload size: [X] MB

### Performance Benchmarks

| Scenario | Expected Time | Maximum Acceptable |
|----------|---------------|-------------------|
| Small ([description]) | [X] seconds | [Y] seconds |
| Large ([description]) | [X] minutes | [Y] minutes |

---

## 8. Testing

### Test Scenarios

| Scenario | Input | Expected Response |
|----------|-------|-------------------|
| Happy path | Valid request | 200 OK |
| Validation error | Invalid field | 422 with field detail |
| Missing auth | No token | 401 |
| Unauthorized resource | Wrong entity | 403 |
| Service down | [simulated] | 503 |
| Timeout | Large dataset | 504 |

---

## 9. Notes

### Assumptions
- [Assumption 1]

### Known Limitations
- [Limitation 1]

### Future Enhancements
- [Enhancement 1]

---

## 10. Related Documents

| Document | Location |
|----------|----------|
| Feature Requirements | [path to finalized Feature Requirements document] |
| Swagger/OpenAPI | [path] |
| [Other related docs] | [path or URL] |

---

## 11. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial API contract |
