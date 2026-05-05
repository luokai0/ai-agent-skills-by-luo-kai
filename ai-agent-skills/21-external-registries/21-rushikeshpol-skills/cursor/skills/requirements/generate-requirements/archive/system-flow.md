# System Flow: [Feature Name]

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Owner:** [Team]
**Status:** [Draft / In Review / Approved]

> **Audience:** Backend developers, architects, QA engineers
> **Rule:** Describe WHAT happens and WHO is involved — not HOW it's implemented.

---

## 1. Overview

### Summary
[2–3 sentences: end-to-end flow, what triggers it, what it produces]

### Systems Involved

| System | Role | Owner | Technology |
|--------|------|-------|------------|
| [System A] | [Purpose — e.g., "User interface"] | [Team] | [Tech] |
| [System B] | [Purpose — e.g., "API orchestration"] | [Team] | [Tech] |
| [System C] | [Purpose — e.g., "Data warehouse"] | [Team] | [Tech] |

---

## 2. High-Level Flow

```
[User] → [System A] → [System B] → [System C] → [Output]
```

**Detailed diagram:**
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  User    │─1→ │ System A │─2→ │ System B │─3→ │ Output   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                      │
                                      4↓
                               ┌──────────┐
                               │ System C │
                               └──────────┘
```

---

## 3. Step-by-Step Flow (Happy Path)

### Step 1: [Action Name]

**Actor:** [User / System A / System B]
**Trigger:** [What initiates this step]

**Actions:**
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Output:** [What is produced / what happens next]
**Success condition:** [When this step is considered complete]

---

### Step 2: [Action Name]

**System:** [Which system]

**Actions:**
1. [Action 1 — e.g., "Validate auth token"]
2. [Action 2 — e.g., "Check user permissions against entity IDs"]
3. [Action 3 — e.g., "Forward request to data layer"]

**Output:** [Result]

---

### Step 3: [Action Name]

**System:** [Which system]

**Actions:**
1. **[Sub-action A]:** [Brief description]
2. **[Sub-action B]:** [Brief description]
3. **[Sub-action C]:** [Brief description]

**Output:** [Result or next step reference]

---

### Step 4: [Data Processing]

**System:** [Which system]

**Actions:**
1. Query data source with validated parameters
2. Apply business rules to data
3. Transform data to output format

**Output:** [Processed data structure]
**Performance note:** [Expected time for this step]

---

### Step 5: [Return / Response]

**System:** [Which system]

**Actions:**
1. [Generate final output — e.g., build CSV, generate JSON]
2. [Save metadata — if applicable]
3. [Return result to caller]

**Output:** [Final result delivered to user]

---

## 4. Alternative Flows

### Alt Flow 1: No Data Scenario

**Trigger:** Data source returns 0 results

**Difference from happy path (Step 4):**
1. Query returns empty dataset
2. Skip output generation
3. Return informational message `{"message": "[No data message]"}`
4. No metadata saved

**User experience:** [Info message, form preserved, no download]

---

### Alt Flow 2: Timeout

**Trigger:** Processing exceeds [N]-minute threshold

**Handling:**
1. Backend timeout fires at [N] minutes
2. System logs timeout event with requestId
3. Return 504 response
4. Frontend displays retry suggestion

---

### Alt Flow 3: Dependent Service Unavailable

**Trigger:** [External system] returns error or is unreachable

**Handling:**
1. [Service] connection attempt fails
2. System catches exception
3. Log error with context
4. Return 503 response
5. Frontend displays "Try again later" message

---

## 5. Error Handling

### Error Scenarios

| Error | Cause | System Response | User Experience | Recovery |
|-------|-------|-----------------|-----------------|----------|
| Validation failure | Invalid input | 422 + field detail | Form error message | Fix and resubmit |
| Auth failure | Expired token | 401 | Redirect to login | Re-authenticate |
| Permission denied | Unauthorized data | 403 | Access denied message | Contact admin |
| Service down | [System] unavailable | 503 | Retry suggestion | Retry later |
| Timeout | [Step N] exceeded limit | 504 | Reduce scope suggestion | Retry with smaller request |
| Internal error | Unexpected exception | 500 + requestId | Contact support | Support team investigation |

### Retry Strategy

**Client retry (for 503, 504):**
1. Wait 5 seconds → retry
2. Wait 15 seconds → retry
3. Wait 30 seconds → fail and show persistent error

**Server retry:**
- [External system] queries: [N] retry with [backoff]

---

## 6. Security & Data Protection

### Authentication Checkpoints
1. **[Point 1]:** [What is validated — e.g., "Bearer token at API gateway"]
2. **[Point 2]:** [What is validated — e.g., "Entity IDs against user's authorized list"]

### Data in Transit
- HTTPS only (TLS 1.2+)
- Auth tokens in headers (never in URL)

### Data at Rest
- [Storage encryption details or N/A]
- [Retention policy]

### Access Controls
- [Who can access what — role-based rules]

---

## 7. Integration Points

### [External System 1]

| Attribute | Value |
|-----------|-------|
| **Interface** | [API / SDK / ODBC / Database view] |
| **Authentication** | [Service account / API key / OAuth] |
| **Data accessed** | [What data this system provides] |
| **SLA** | [Uptime %, response time] |
| **Owner** | [Team / Contact] |
| **Failure behavior** | [How system handles [External System 1] being unavailable] |

---

### [External System 2]
*(Repeat structure above)*

---

## 8. Data Transformations

### [Source System] → [Destination System]

| Source Field | Destination Field | Transformation Rule |
|--------------|-------------------|---------------------|
| `source_field_name` | `destFieldName` | [e.g., "Concatenate first + last name"] |
| `raw_date` | `formattedDate` | [e.g., "ISO 8601 to 'MMM DD, YYYY'"] |

---

## 9. Performance

### Expected Load
- Peak concurrent requests: [N]
- Average daily requests: [N]
- Max data size per request: [X] MB / [N] rows

### Performance Benchmarks

| Scenario | Expected Time | Bottleneck | Mitigation |
|----------|---------------|------------|------------|
| Small ([description]) | [X] seconds | [Component] | [Approach] |
| Large ([description]) | [X] minutes | [Component] | [Approach] |

### Bottleneck Analysis
- **[Step N]** accounts for ~[X]% of total time because [reason]
- **Mitigation:** [Proposed approach — e.g., indexing, caching, query optimization]

---

## 10. Assumptions & Dependencies

| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| [System/component] | [Team] | [Status] | HIGH/MED/LOW |

---

## 11. Known Limitations

- [Limitation 1] — Reason: [why this constraint exists]

---

## 12. Related Documents

| Document | Location |
|----------|----------|
| Feature Requirements | [path to finalized Feature Requirements document] |
| API Contract | [path to API Contract, if generated] |
| Architecture Diagram | [link] |

---

## 13. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial system flow |
