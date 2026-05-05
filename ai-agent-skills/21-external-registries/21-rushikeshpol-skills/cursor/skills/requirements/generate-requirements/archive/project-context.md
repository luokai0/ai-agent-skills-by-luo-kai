# Project Context: [Project Name]

> **Persistent project memory for the generate-requirements skill.**
> This file is read automatically at the start of every requirements session.
> Update it as the project evolves — add new integrations, refine personas, lock in conventions.
> Keep it factual. Mark unknowns as [TBD]. Never fabricate.

**Project:** [Name]
**Type:** [Web App / Mobile App / API / Platform / Internal Tool]
**Team:** [Team name]
**Last updated:** [YYYY-MM-DD]

---

## 1. Project Overview

**What it does:** [1–2 sentences — what the product does and for whom]

**Current phase:** [MVP / Beta / Production / Legacy]

**Key product goals:**
- [Goal 1]
- [Goal 2]

---

## 2. Tech Stack

### Frontend
- **Framework:** [e.g., React 18, Next.js 14, Vue 3]
- **Language:** [TypeScript / JavaScript]
- **UI Library:** [e.g., Ant Design, MUI, Tailwind]
- **State management:** [e.g., Redux, Zustand, React Context]
- **HTTP client:** [e.g., Axios, React Query, Fetch]

### Backend
- **Framework:** [e.g., .NET Core 8, Node/Express, Django, Rails]
- **Language:** [C# / TypeScript / Python / Ruby]
- **Database:** [e.g., PostgreSQL 15, MySQL, MongoDB]
- **Cache:** [e.g., Redis, N/A]
- **Queue:** [e.g., RabbitMQ, SQS, N/A]

### Infrastructure
- **Cloud:** [AWS / GCP / Azure / On-prem]
- **Deployment:** [e.g., Docker + ECS, Kubernetes, Heroku]
- **CI/CD:** [e.g., GitHub Actions, CircleCI]

---

## 3. API Conventions

> These patterns override generic REST best practices in every requirements session.

### Authentication
- **Method:** [Bearer Token (JWT) / OAuth 2.0 / API Key]
- **Header:** `Authorization: Bearer {token}`
- **Token expiry:** [e.g., 1 hour]
- **Refresh:** [e.g., via /auth/refresh endpoint]

### Naming Conventions
- **Field names:** [camelCase / snake_case / PascalCase]
- **Path naming:** [e.g., plural nouns: /users, /reports]
- **Path pattern:** [e.g., /api/v1/{resource} or /api/{resource}]
- **Date format:** [ISO 8601: YYYY-MM-DD / Unix timestamp]
- **Datetime format:** [ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ]

### Error Response Shape
```json
{
  "error": "[Type string]",
  "message": "[User-friendly message]",
  "field": "[field name — validation errors only]",
  "requestId": "[UUID — server errors only]"
}
```
*(Update this with your actual error shape)*

### HTTP Status Codes Used
| Situation | Code |
|-----------|------|
| Success | 200 |
| Created | 201 |
| Validation failed | 422 |
| Bad request | 400 |
| Unauthorized | 401 |
| Forbidden | 403 |
| Not found | 404 |
| Internal error | 500 |
| Service down | 503 |
| Timeout | 504 |

### Pagination
- **Style:** [offset+limit / page+pageSize / cursor-based / none]
- **Default page size:** [e.g., 20]
- **Max page size:** [e.g., 100]
- **Response envelope:**
```json
{
  "data": [...],
  "pagination": {
    "currentPage": 1,
    "pageSize": 20,
    "totalRecords": 100,
    "totalPages": 5
  }
}
```

### Response Envelope
- **Wrapped:** `{"data": {...}, "meta": {...}}` / **Bare:** `{...}` *(choose one)*

---

## 4. Personas

> Locked persona definitions. Used in every feature's User Context without re-asking.

### Primary Personas

**[Persona 1 Name] — [Role Title]**
- **Demographics:** [Experience level, company size, tech proficiency]
- **Goals:** [What they want to achieve using the product]
- **Pain points:** [Current frustrations]
- **Usage context:** [How often, what device, what environment]
- **Representative quote:** *"[Quote capturing their core need]"*
- **Source:** [User research / interviews / assumed — flag if assumed]

---

**[Persona 2 Name] — [Role Title]**
- **Demographics:** [...]
- **Goals:** [...]
- **Pain points:** [...]
- **Usage context:** [...]
- **Quote:** *"[...]"*
- **Source:** [...]

---

### Secondary Personas
- **[Name/Role]:** [Brief description — goals and context]

---

## 5. System Architecture

### Core Components

| Component | Purpose | Owner | Technology | Notes |
|-----------|---------|-------|------------|-------|
| [Frontend App] | [User interface] | [Team] | [Tech] | |
| [API Server] | [Orchestration] | [Team] | [Tech] | |
| [Database] | [Primary data store] | [Team] | [Tech] | |
| [Data Warehouse] | [Reporting data] | [Team] | [Tech] | |

### Architecture Diagram (ASCII)
```
[Frontend] → [API] → [Database]
                ↓
          [Data Warehouse]
                ↓
          [External Service]
```

---

## 6. Existing Integrations

> Pre-populated for every feature — only feature-specific integrations need adding.

| System | Interface | Auth | Purpose | Owner | SLA | Notes |
|--------|-----------|------|---------|-------|-----|-------|
| [System 1] | [API/DB] | [method] | [purpose] | [team] | [uptime] | |
| [System 2] | [API/DB] | [method] | [purpose] | [team] | [uptime] | |

---

## 7. Compliance Baseline

> Applied to every feature unless explicitly noted as N/A for a specific feature.

- **Regulatory:** [GDPR / HIPAA / SOC2 / PCI-DSS / None]
- **Security standard:** [Auth requirements, encryption, data handling]
- **Accessibility:** [WCAG 2.1 Level AA / Level A / Not required]
- **Data retention:** [Policy — e.g., 7 years, 90 days, N/A]
- **Audit logging:** [Required / Not required / Feature-specific]

---

## 8. Browser & Device Support

| Platform | Browsers | Minimum Version |
|----------|---------|-----------------|
| Desktop | Chrome, Firefox, Safari, Edge | [versions] |
| Mobile | iOS Safari, Android Chrome | [versions] |
| Tablet | iOS Safari, Android Chrome | [versions] |

**Responsive breakpoints:**
- Mobile: [e.g., 375px+]
- Tablet: [e.g., 768px+]
- Desktop: [e.g., 1280px+]

---

## 9. Out of Scope (Project-Wide)

> These items are never in scope for any feature unless explicitly overridden.

- [Item 1 — e.g., "PDF export (use CSV only)"]
- [Item 2 — e.g., "Email notifications (not yet supported)"]
- [Item 3]

---

## 10. Glossary

> Project-specific terms. Use these consistently in all requirement documents.

| Term | Definition |
|------|------------|
| [Term 1] | [Definition — e.g., "Account: a top-level organization in the system"] |
| [Term 2] | [Definition] |
| [Term 3] | [Definition] |

---

## 11. Change Log

> Track significant updates so the team knows what changed.

| Date | Change | Updated By |
|------|--------|------------|
| [YYYY-MM-DD] | Initial project context created | [Name] |
| [YYYY-MM-DD] | Added [System X] integration | [Name] |
