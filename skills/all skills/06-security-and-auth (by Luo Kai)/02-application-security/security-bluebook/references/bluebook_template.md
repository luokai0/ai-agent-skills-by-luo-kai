# Security Blue Book v1 (Template)

## Normative Language
- MUST: required for compliance and release
- SHOULD: recommended best practice
- CAN: optional or context-dependent

## Scope
- Product: [TODO]
- Environment: [TODO] (dev/beta/prod)
- Data classes handled: [PII | PHI | financial | tokens | content | other]
- Out of scope: [TODO]

## Threat Model (MVP)
- Assumptions: [TODO]
- Primary risks: [TODO]
- Out-of-scope threats: [TODO]

## Data Classification and Handling
- PII: [rules]
- PHI: [rules]
- Financial: [rules]
- Tokens/credentials: [rules]
- Content: [rules]

## Trust Boundaries
- Client: [controls]
- Server: [controls]
- Third parties: [controls]

## Authentication and Session Rules
- Auth methods: [TODO]
- Session lifetime: [TODO]
- MFA policy: [TODO]
- Device/session revocation: [TODO]

## Token Handling Policy
- Storage: [TODO]
- Scope/least privilege: [TODO]
- Rotation: [TODO]
- Revoke/disconnect semantics: [TODO]

## Logging and Audit Policy
- Must log: [TODO]
- Must never log: [TODO]
- Redaction rules: [TODO]

## Ingestion or Capture Policy (if applicable)
- Email ingestion: [rules]
- Browser/session capture: [rules]
- Other connectors: [rules]

## Storage and Encryption
- At rest: [TODO]
- In transit: [TODO]
- Secret management: [TODO]

## Retention and Deletion
- Default retention: [TODO]
- User-initiated deletion: [TODO]
- Audit for deletions: [TODO]

## Incident Response (MVP)
1. Detect: [TODO]
2. Contain: [TODO]
3. Notify: [TODO]
4. Rotate: [TODO]
5. Postmortem: [TODO]

## Security Gates (Pass/Fail)
1. [Gate 1]
2. [Gate 2]
3. [Gate 3]

## Pre-Launch Go/No-Go Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Security Exceptions
- If a MUST cannot be met, record an exception with scope, duration, and mitigation.
