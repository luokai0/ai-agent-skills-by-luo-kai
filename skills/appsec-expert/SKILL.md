---
name: appsec-expert
description: Expert-level application security. Use when identifying security vulnerabilities, implementing input validation, preventing XSS/CSRF/SQLi/SSRF, securing APIs, implementing secure coding practices, or performing threat modeling. Also use when the user mentions 'OWASP', 'XSS', 'CSRF', 'SQL injection', 'security vulnerability', 'threat model', 'penetration testing', 'CVE', or 'security audit'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Application Security Expert

You are an expert in application security with deep knowledge of the OWASP Top 10, secure coding practices, threat modeling, and defensive programming patterns.

## Before Starting

1. **Tech stack** — language, framework, database?
2. **Problem type** — vulnerability fix, security review, threat model, secure feature design?
3. **Environment** — web app, API, mobile backend, microservices?
4. **Compliance** — PCI-DSS, HIPAA, SOC2, GDPR requirements?
5. **Severity** — is this a live vulnerability or proactive hardening?

---

## Core Expertise Areas

- **OWASP Top 10**: injection, broken auth, XSS, IDOR, security misconfig, vulnerable components
- **Input validation**: allowlists, parameterized queries, output encoding, sanitization
- **Authentication security**: password hashing, MFA, session management, JWT security
- **Authorization**: RBAC, ABAC, IDOR prevention, least privilege
- **API security**: rate limiting, input validation, authentication, CORS, mass assignment
- **Cryptography**: encryption at rest/transit, hashing, key management
- **Dependency security**: CVE scanning, SCA, supply chain attacks
- **Threat modeling**: STRIDE, attack surface analysis, data flow diagrams

---

## Key Patterns & Code

### OWASP Top 10 — Quick Reference
```
A01 Broken Access Control    → IDOR, privilege escalation, missing auth checks
A02 Cryptographic Failures   → Weak crypto, unencrypted sensitive data, MD5/SHA1
A03 Injection                → SQL, NoSQL, LDAP, OS command injection
A04 Insecure Design          → Missing threat model, insecure design patterns
A05 Security Misconfiguration → Default creds, verbose errors, open cloud storage
A06 Vulnerable Components    → Outdated deps with known CVEs
A07 Auth Failures            → Weak passwords, no MFA, broken session management
A08 Software Integrity       → Unsigned code, malicious dependencies
A09 Logging Failures         → No audit logs, logging sensitive data
A10 SSRF                     → Fetching attacker-controlled URLs
```

### SQL Injection Prevention
```javascript
// NEVER do this — vulnerable to SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ALWAYS use parameterized queries
// Node.js with pg
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1 AND active = $2',
  [email, true]
);

// Node.js with mysql2
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE email = ? AND active = ?',
  [email, true]
);

// Python with psycopg2
cursor.execute(
  'SELECT * FROM users WHERE email = %s AND active = %s',
  (email, True)
)

// Python with SQLAlchemy ORM (safe by default)
user = db.query(User).filter(
  User.email == email,
  User.active == True
).first()

// If you MUST use dynamic table/column names (rare)
// Use an allowlist — never interpolate user input directly
const ALLOWED_COLUMNS = new Set(['name', 'email', 'created_at']);
const ALLOWED_ORDERS  = new Set(['ASC', 'DESC']);

function buildQuery(sortColumn, sortOrder) {
  if (!ALLOWED_COLUMNS.has(sortColumn)) throw new Error('Invalid column');
  if (!ALLOWED_ORDERS.has(sortOrder.toUpperCase())) throw new Error('Invalid order');
  return `SELECT * FROM users ORDER BY ${sortColumn} ${sortOrder}`;
}
```

### XSS Prevention
```javascript
// ── Stored/Reflected XSS ──────────────────────────────────────────────────

// NEVER insert user data directly into HTML
element.innerHTML = userInput;                   // vulnerable
document.write(userInput);                       // vulnerable

// ALWAYS use safe DOM methods
element.textContent = userInput;                 // safe — escapes HTML
element.setAttribute('data-value', userInput);  // safe for attributes

// In React — safe by default, but watch out for dangerouslySetInnerHTML
// Safe:
<div>{userInput}</div>

// Dangerous — only use with sanitized content:
<div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />

// If you must render HTML, use DOMPurify to sanitize first
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
});
element.innerHTML = clean;

// ── DOM XSS ───────────────────────────────────────────────────────────────
// Never use location.hash or URL params directly in innerHTML
const params = new URLSearchParams(window.location.search);
const name = params.get('name');
// Safe:
document.getElementById('greeting').textContent = `Hello, ${name}`;
// Dangerous:
document.getElementById('greeting').innerHTML = `Hello, ${name}`;

// ── Content Security Policy (defense in depth) ────────────────────────────
// Add to every response:
// Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}';
```

### CSRF Prevention
```javascript
// ── CSRF Token (traditional forms) ───────────────────────────────────────
import crypto from 'crypto';

// Generate and store token in session
function generateCSRFToken(session) {
  const token = crypto.randomBytes(32).toString('hex');
  session.csrfToken = token;
  return token;
}

// Validate on every state-changing request
function validateCSRFToken(req, res, next) {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next(); // safe methods don't need CSRF protection
  }

  const token = req.headers['x-csrf-token'] ?? req.body._csrf;
  const sessionToken = req.session?.csrfToken;

  if (!token || !sessionToken || !crypto.timingSafeEqual(
    Buffer.from(token),
    Buffer.from(sessionToken)
  )) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  next();
}

// ── SameSite Cookie (modern defense) ─────────────────────────────────────
// Set cookies with SameSite=Strict or SameSite=Lax
res.cookie('session', sessionId, {
  httpOnly: true,     // not accessible via JavaScript
  secure: true,       // HTTPS only
  sameSite: 'strict', // never sent in cross-site requests
  maxAge: 24 * 60 * 60 * 1000,
});

// ── CORS Configuration ────────────────────────────────────────────────────
// Be explicit — never use wildcard with credentials
app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,  // allow cookies
  maxAge: 86400,      // preflight cache for 24h
}));
```

### IDOR Prevention (Broken Access Control)
```javascript
// ── Insecure Direct Object Reference ──────────────────────────────────────

// VULNERABLE — no ownership check
app.get('/api/documents/:id', async (req, res) => {
  const doc = await db.document.findById(req.params.id);
  return res.json(doc); // any user can read any document!
});

// SECURE — always verify ownership
app.get('/api/documents/:id', authenticate, async (req, res) => {
  const doc = await db.document.findOne({
    where: {
      id: req.params.id,
      ownerId: req.user.id,  // ensure user owns this document
    }
  });

  if (!doc) {
    // Return 404 not 403 — don't leak existence of resources
    return res.status(404).json({ error: 'Document not found' });
  }

  return res.json(doc);
});

// ── Authorization middleware ──────────────────────────────────────────────
function requireOwnership(Model) {
  return async (req, res, next) => {
    const resource = await Model.findOne({
      where: { id: req.params.id, userId: req.user.id }
    });

    if (!resource) return res.status(404).json({ error: 'Not found' });

    req.resource = resource;
    next();
  };
}

app.put('/api/posts/:id',
  authenticate,
  requireOwnership(Post),
  async (req, res) => {
    await req.resource.update(req.body);
    res.json(req.resource);
  }
);

// ── RBAC ─────────────────────────────────────────────────────────────────
function requireRole(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

app.delete('/api/users/:id',
  authenticate,
  requireRole('admin', 'superadmin'),
  deleteUserHandler
);
```

### Input Validation with Zod
```typescript
import { z } from 'zod';

// Define strict schemas for all inputs
const CreateUserSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name too long')
    .regex(/^[a-zA-Z\s'-]+$/, 'Name contains invalid characters'),

  email: z.string()
    .email('Invalid email format')
    .max(255)
    .toLowerCase(),

  age: z.number()
    .int()
    .min(13, 'Must be at least 13')
    .max(120),

  website: z.string()
    .url()
    .startsWith('https://', 'Must use HTTPS')
    .optional(),

  role: z.enum(['user', 'moderator']),  // allowlist for role

  // Never accept HTML in plain text fields
  bio: z.string()
    .max(500)
    .transform(val => val.trim()),
});

// Validate middleware
function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(422).json({
        error: 'Validation failed',
        details: result.error.flatten().fieldErrors,
      });
    }
    req.validatedBody = result.data;
    next();
  };
}

app.post('/api/users',
  validate(CreateUserSchema),
  createUserHandler
);
```

### SSRF Prevention
```javascript
import dns from 'dns/promises';
import net from 'net';

// Block list of private/internal IP ranges
function isPrivateIP(ip) {
  const privateRanges = [
    /^127\./,           // loopback
    /^10\./,            // RFC1918
    /^172\.(1[6-9]|2[0-9]|3[01])\./,  // RFC1918
    /^192\.168\./,      // RFC1918
    /^169\.254\./,      // link-local
    /^::1$/,            // IPv6 loopback
    /^fc00:/,           // IPv6 private
    /^fe80:/,           // IPv6 link-local
  ];
  return privateRanges.some(range => range.test(ip));
}

async function safeURL(urlString) {
  let url;
  try {
    url = new URL(urlString);
  } catch {
    throw new Error('Invalid URL format');
  }

  // Allowlist protocols
  if (!['http:', 'https:'].includes(url.protocol)) {
    throw new Error('Only HTTP/HTTPS allowed');
  }

  // Allowlist domains (preferred approach)
  const ALLOWED_DOMAINS = new Set(['api.github.com', 'api.example.com']);
  if (!ALLOWED_DOMAINS.has(url.hostname)) {
    throw new Error('Domain not allowed');
  }

  // Resolve DNS and check if it resolves to private IP
  const addresses = await dns.resolve(url.hostname);
  for (const addr of addresses) {
    if (isPrivateIP(addr)) {
      throw new Error('Request to private network not allowed');
    }
  }

  return url;
}

// Usage
app.post('/api/webhook-test', async (req, res) => {
  const url = await safeURL(req.body.webhookUrl);
  const response = await fetch(url.toString());
  res.json({ status: response.status });
});
```

### Password Security
```javascript
import argon2 from 'argon2';
import crypto from 'crypto';

// Hash password with argon2id (best current choice)
async function hashPassword(password) {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,  // 64MB
    timeCost: 3,        // 3 iterations
    parallelism: 4,     // 4 threads
  });
}

// Verify password
async function verifyPassword(hash, password) {
  return argon2.verify(hash, password);
}

// Password policy validation
function validatePassword(password) {
  const errors = [];
  if (password.length < 12) errors.push('At least 12 characters required');
  if (!/[A-Z]/.test(password)) errors.push('At least one uppercase letter required');
  if (!/[a-z]/.test(password)) errors.push('At least one lowercase letter required');
  if (!/[0-9]/.test(password)) errors.push('At least one number required');
  if (!/[^A-Za-z0-9]/.test(password)) errors.push('At least one special character required');

  // Check against common password list
  if (COMMON_PASSWORDS.has(password.toLowerCase())) {
    errors.push('Password is too common');
  }

  return errors;
}

// Secure token generation (for password reset, email verification)
function generateSecureToken(bytes = 32) {
  return crypto.randomBytes(bytes).toString('hex');
}

// Rate limit password attempts
const loginAttempts = new Map();

function checkRateLimit(identifier) {
  const now = Date.now();
  const attempts = loginAttempts.get(identifier) ?? [];
  const recentAttempts = attempts.filter(t => now - t < 15 * 60 * 1000);

  if (recentAttempts.length >= 5) {
    throw new Error('Too many login attempts. Try again in 15 minutes.');
  }

  loginAttempts.set(identifier, [...recentAttempts, now]);
}
```

### Security Headers Middleware
```javascript
// Apply to every response
app.use((req, res, next) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Enable XSS filter in older browsers
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // HSTS — force HTTPS for 1 year
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains; preload'
  );

  // Control referrer information
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Restrict browser features
  res.setHeader(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=(), payment=()'
  );

  // Content Security Policy
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.nonce = nonce;
  res.setHeader(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      `script-src 'self' 'nonce-${nonce}'`,
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; ')
  );

  next();
});
```

### Threat Modeling — STRIDE
```
S — Spoofing         → Can attacker impersonate another user?
T — Tampering        → Can attacker modify data in transit or at rest?
R — Repudiation      → Can user deny performing an action?
I — Information Disclosure → Can attacker access data they should not?
D — Denial of Service → Can attacker make service unavailable?
E — Elevation of Privilege → Can attacker gain more permissions than allowed?

Threat Modeling Steps:
1. Define scope — what are we protecting?
2. Draw data flow diagram — where does data go?
3. Identify trust boundaries — where does data cross security boundaries?
4. Apply STRIDE to each component and data flow
5. Rate risk — likelihood × impact
6. Define mitigations
7. Verify mitigations are implemented

Questions to ask:
  - What happens if user X can access resource Y?
  - What happens if this request is replayed?
  - What happens if this field is empty/null/max length?
  - What happens if this network call fails?
  - What sensitive data is logged?
  - What happens if the database is read by an attacker?
```

---

## Best Practices

- Validate ALL input on the server side — client-side validation is UX only
- Use parameterized queries for ALL database queries — no exceptions
- Hash passwords with argon2id, bcrypt, or scrypt — never MD5 or SHA1
- Apply principle of least privilege — minimize access at every layer
- Return 404 not 403 for IDOR — do not leak existence of resources
- Never log sensitive data — passwords, tokens, PII, credit cards
- Keep dependencies updated — run Snyk or Dependabot on every PR
- Use HTTPS everywhere — no exceptions in production
- Apply security headers on every response

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| String interpolation in SQL | SQL injection | Always use parameterized queries |
| innerHTML with user data | XSS vulnerability | Use textContent or DOMPurify |
| No ownership check on resources | IDOR — users access each others data | Always filter by authenticated user ID |
| Returning 403 for IDOR | Leaks existence of resource | Return 404 for unauthorized resource access |
| Logging sensitive data | PII/secrets in log files | Audit what is logged, mask sensitive fields |
| Weak password hashing (MD5/SHA1) | Passwords cracked in seconds | Use argon2id with proper parameters |
| Wildcard CORS with credentials | Cross-origin attacks | Use explicit origin allowlist |
| No rate limiting on auth | Brute force attacks | Rate limit login, password reset, OTP endpoints |

---

## Related Skills

- **auth-expert**: For OAuth2, JWT, and session security
- **cryptography-expert**: For encryption and hashing implementation
- **devsecops-expert**: For integrating security into CI/CD
- **api-design-expert**: For secure API design patterns
- **nginx-expert**: For security headers and rate limiting
- **secrets-management**: For secure handling of credentials
