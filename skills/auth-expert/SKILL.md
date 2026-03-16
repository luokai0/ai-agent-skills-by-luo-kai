---
name: auth-expert
description: Expert-level authentication and authorization. Use when implementing OAuth2, OIDC, JWT, session management, RBAC, ABAC, MFA, SSO, password hashing, or integrating auth providers (Auth0, Clerk, NextAuth, Supabase Auth). Also use when the user mentions 'OAuth', 'JWT', 'OIDC', 'RBAC', 'MFA', 'SSO', 'session management', 'refresh token', 'access token', or 'login flow'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Authentication & Authorization Expert

You are an expert in authentication and authorization with deep knowledge of OAuth2, OIDC, JWT, session management, RBAC, MFA, and modern auth providers.

## Before Starting

1. **Auth type** — JWT, sessions, OAuth2, OIDC, API keys?
2. **Stack** — Node.js, Python, Go, Next.js, mobile?
3. **Provider** — self-hosted, Auth0, Clerk, Supabase, Cognito?
4. **Problem type** — implementing from scratch, debugging, security review?
5. **Requirements** — MFA, SSO, social login, enterprise (SAML)?

---

## Core Expertise Areas

- **OAuth2 flows**: authorization code + PKCE, client credentials, device flow
- **OIDC**: ID tokens, UserInfo endpoint, discovery, provider integration
- **JWT**: structure, signing (RS256, ES256, HS256), validation, rotation
- **Session management**: secure cookies, session fixation, sliding expiry
- **RBAC/ABAC**: role design, permission modeling, policy enforcement
- **MFA**: TOTP, WebAuthn/Passkeys, SMS/email OTP, recovery codes
- **Refresh token rotation**: silent refresh, token families, revocation
- **SSO**: SAML 2.0, OIDC federation, enterprise IdP integration

---

## Key Patterns & Code

### OAuth2 Authorization Code + PKCE Flow
```
Most secure flow for SPAs and mobile apps.
Never use implicit flow — it is deprecated.

Flow:
1. App generates code_verifier (random 43-128 char string)
2. App hashes it: code_challenge = BASE64URL(SHA256(code_verifier))
3. App redirects to auth server with code_challenge
4. User authenticates and consents
5. Auth server redirects back with authorization code
6. App exchanges code + code_verifier for tokens
7. Auth server verifies hash(code_verifier) == code_challenge

Why PKCE: prevents authorization code interception attacks
Even if code is stolen, attacker does not have code_verifier
```
```typescript
// PKCE implementation
import crypto from 'crypto';

function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

function generateState(): string {
  return crypto.randomBytes(16).toString('hex');
}

// Step 1: Build authorization URL
function buildAuthUrl(config: OAuthConfig): { url: string; state: string; verifier: string } {
  const state = generateState();
  const verifier = generateCodeVerifier();
  const challenge = generateCodeChallenge(verifier);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    scope: 'openid profile email',
    state,
    code_challenge: challenge,
    code_challenge_method: 'S256',
  });

  return {
    url: `${config.authorizationEndpoint}?${params}`,
    state,
    verifier,
  };
}

// Step 2: Exchange code for tokens
async function exchangeCode(
  code: string,
  verifier: string,
  config: OAuthConfig
): Promise<TokenResponse> {
  const response = await fetch(config.tokenEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: config.redirectUri,
      client_id: config.clientId,
      code_verifier: verifier,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Token exchange failed: ${error.error_description}`);
  }

  return response.json();
}
```

### JWT — Implementation & Validation
```typescript
import jwt from 'jsonwebtoken';
import { readFileSync } from 'fs';

// Use RS256 (asymmetric) for production — private key signs, public key verifies
// Use HS256 (symmetric) only for internal services with shared secret

// Load RSA keys
const privateKey = readFileSync('private.pem');
const publicKey  = readFileSync('public.pem');

interface TokenPayload {
  sub: string;          // user ID
  email: string;
  role: string;
  sessionId: string;
  iat?: number;         // issued at (auto-set by jwt.sign)
  exp?: number;         // expiry (auto-set)
}

// Sign access token — short lived
function signAccessToken(payload: Omit<TokenPayload, 'iat' | 'exp'>): string {
  return jwt.sign(payload, privateKey, {
    algorithm: 'RS256',
    expiresIn: '15m',   // short lived — 15 minutes
    issuer: 'https://auth.example.com',
    audience: 'https://api.example.com',
  });
}

// Sign refresh token — long lived, stored in DB
function signRefreshToken(userId: string, sessionId: string): string {
  return jwt.sign({ sub: userId, sessionId }, privateKey, {
    algorithm: 'RS256',
    expiresIn: '7d',
    issuer: 'https://auth.example.com',
  });
}

// Validate and decode token
function verifyAccessToken(token: string): TokenPayload {
  try {
    return jwt.verify(token, publicKey, {
      algorithms: ['RS256'],      // never allow 'none' algorithm
      issuer: 'https://auth.example.com',
      audience: 'https://api.example.com',
    }) as TokenPayload;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new UnauthorizedError('Token expired');
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new UnauthorizedError('Invalid token');
    }
    throw error;
  }
}

// Auth middleware
export function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing authorization header' });
  }

  const token = authHeader.slice(7);
  try {
    req.user = verifyAccessToken(token);
    next();
  } catch (error) {
    return res.status(401).json({ error: error.message });
  }
}
```

### Refresh Token Rotation
```typescript
// Refresh token rotation prevents token theft
// Each refresh invalidates the old token and issues a new one
// If old token is used again → token family is revoked (theft detected)

interface Session {
  id: string;
  userId: string;
  refreshToken: string;   // hashed
  familyId: string;       // for theft detection
  expiresAt: Date;
  createdAt: Date;
}

async function refreshTokens(refreshToken: string): Promise<TokenPair> {
  // Find session by refresh token hash
  const tokenHash = hashToken(refreshToken);
  const session = await db.session.findOne({ where: { refreshToken: tokenHash } });

  if (!session) {
    // Token not found — may be theft attempt
    // Check if it belongs to a family and revoke all sessions in family
    const revokedToken = await db.revokedToken.findOne({ where: { tokenHash } });
    if (revokedToken) {
      // Token was already used — THEFT DETECTED
      await db.session.deleteMany({ where: { familyId: revokedToken.familyId } });
      throw new UnauthorizedError('Token reuse detected — all sessions revoked');
    }
    throw new UnauthorizedError('Invalid refresh token');
  }

  if (session.expiresAt < new Date()) {
    await db.session.delete({ where: { id: session.id } });
    throw new UnauthorizedError('Refresh token expired');
  }

  // Rotate: invalidate old token, issue new one
  const newRefreshToken = crypto.randomBytes(32).toString('hex');
  const newAccessToken  = signAccessToken({ sub: session.userId, sessionId: session.id });

  // Store old token hash as revoked (for theft detection)
  await db.revokedToken.create({
    data: { tokenHash, familyId: session.familyId, expiresAt: session.expiresAt }
  });

  // Update session with new refresh token
  await db.session.update({
    where: { id: session.id },
    data: {
      refreshToken: hashToken(newRefreshToken),
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    }
  });

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}

function hashToken(token: string): string {
  return crypto.createHash('sha256').update(token).digest('hex');
}
```

### Secure Session Management
```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,  // 32+ random bytes
  name: '__Host-session',               // __Host- prefix = more secure
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,       // not accessible via JS
    secure: true,         // HTTPS only
    sameSite: 'strict',   // CSRF protection
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
  },
}));

// Session fixation prevention — regenerate session ID after login
async function login(req: Request, userId: string) {
  return new Promise<void>((resolve, reject) => {
    // Regenerate session ID to prevent fixation attack
    req.session.regenerate((err) => {
      if (err) return reject(err);
      req.session.userId = userId;
      req.session.loginAt = Date.now();
      req.session.save((err) => {
        if (err) return reject(err);
        resolve();
      });
    });
  });
}

// Logout — destroy session completely
async function logout(req: Request) {
  return new Promise<void>((resolve, reject) => {
    req.session.destroy((err) => {
      if (err) return reject(err);
      resolve();
    });
  });
}
```

### RBAC Implementation
```typescript
// Role-Based Access Control

// Define permissions
const permissions = {
  // posts
  'posts:read':   ['user', 'moderator', 'admin'],
  'posts:create': ['user', 'moderator', 'admin'],
  'posts:update': ['moderator', 'admin'],
  'posts:delete': ['admin'],

  // users
  'users:read':   ['moderator', 'admin'],
  'users:update': ['admin'],
  'users:delete': ['admin'],

  // admin
  'admin:access': ['admin'],
} as const;

type Permission = keyof typeof permissions;
type Role = 'user' | 'moderator' | 'admin';

function hasPermission(role: Role, permission: Permission): boolean {
  return (permissions[permission] as readonly string[]).includes(role);
}

// Middleware factory
function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!hasPermission(req.user.role as Role, permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}

// Usage
app.delete('/api/posts/:id',
  authenticate,
  requirePermission('posts:delete'),
  deletePostHandler
);

app.get('/api/users',
  authenticate,
  requirePermission('users:read'),
  getUsersHandler
);
```

### TOTP MFA Implementation
```typescript
import { authenticator } from 'otplib';
import QRCode from 'qrcode';

// Generate TOTP secret for user
async function setupMFA(userId: string, userEmail: string) {
  const secret = authenticator.generateSecret();

  // Store secret (encrypted) in database
  await db.user.update({
    where: { id: userId },
    data: {
      mfaSecret: encrypt(secret),  // encrypt at rest
      mfaEnabled: false,           // not enabled until verified
    }
  });

  // Generate QR code for authenticator app
  const otpAuthUrl = authenticator.keyuri(userEmail, 'MyApp', secret);
  const qrCodeDataUrl = await QRCode.toDataURL(otpAuthUrl);

  return { secret, qrCodeDataUrl };
}

// Verify TOTP token during setup
async function verifyMFASetup(userId: string, token: string): Promise<boolean> {
  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user?.mfaSecret) throw new Error('MFA not initialized');

  const secret = decrypt(user.mfaSecret);
  const isValid = authenticator.verify({ token, secret });

  if (isValid) {
    // Generate backup codes
    const backupCodes = generateBackupCodes();

    await db.user.update({
      where: { id: userId },
      data: {
        mfaEnabled: true,
        backupCodes: backupCodes.map(code => hashToken(code)),
      }
    });

    return true;
  }
  return false;
}

// Verify TOTP during login
async function verifyMFALogin(userId: string, token: string): Promise<boolean> {
  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user?.mfaSecret || !user.mfaEnabled) return true; // MFA not enabled

  const secret = decrypt(user.mfaSecret);

  // Check TOTP token
  if (authenticator.verify({ token, secret })) return true;

  // Check backup codes
  const hashedToken = hashToken(token);
  const backupCodeIndex = user.backupCodes.indexOf(hashedToken);
  if (backupCodeIndex !== -1) {
    // Remove used backup code
    const newCodes = [...user.backupCodes];
    newCodes.splice(backupCodeIndex, 1);
    await db.user.update({
      where: { id: userId },
      data: { backupCodes: newCodes }
    });
    return true;
  }

  return false;
}

function generateBackupCodes(count = 10): string[] {
  return Array.from({ length: count }, () =>
    crypto.randomBytes(5).toString('hex').toUpperCase()
      .replace(/(.{5})/g, '$1-').slice(0, -1)  // format: XXXXX-XXXXX
  );
}
```

### NextAuth.js (Next.js)
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import { PrismaAdapter } from '@auth/prisma-adapter';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { db } from '@/lib/db';
import { verifyPassword } from '@/lib/auth';
import { z } from 'zod';

const handler = NextAuth({
  adapter: PrismaAdapter(db),

  providers: [
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    Credentials({
      credentials: {
        email: { type: 'email' },
        password: { type: 'password' },
      },
      async authorize(credentials) {
        const parsed = z.object({
          email: z.string().email(),
          password: z.string().min(8),
        }).safeParse(credentials);

        if (!parsed.success) return null;

        const user = await db.user.findUnique({
          where: { email: parsed.data.email }
        });

        if (!user?.passwordHash) return null;

        const valid = await verifyPassword(
          parsed.data.password,
          user.passwordHash
        );

        return valid ? user : null;
      },
    }),
  ],

  session: { strategy: 'jwt' },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.id   = token.id as string;
      session.user.role = token.role as string;
      return session;
    },
  },

  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
});

export { handler as GET, handler as POST };
```

---

## Best Practices

- Use authorization code + PKCE for all browser and mobile OAuth flows
- Access tokens should expire in 15 minutes — use refresh tokens for longevity
- Always rotate refresh tokens on use — detect theft via token reuse
- Store refresh tokens hashed in the database — never plaintext
- Use HttpOnly + Secure + SameSite=Strict cookies for session tokens
- Regenerate session ID after login to prevent session fixation
- Never put sensitive data in JWT payload — it is only base64 encoded not encrypted
- Verify JWT algorithm explicitly — never allow 'none' algorithm
- Use RS256 or ES256 for JWTs — not HS256 in distributed systems

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Long-lived access tokens | Stolen token gives long access window | Expire access tokens in 15 minutes |
| No refresh token rotation | Stolen refresh token usable indefinitely | Rotate on every use, detect reuse |
| JWT with sensitive data | Data readable by anyone (base64) | Never put PII or secrets in JWT |
| Allowing 'none' algorithm | Attacker can forge tokens | Explicitly specify allowed algorithms |
| No session regeneration after login | Session fixation attack | Always call session.regenerate() after login |
| TOTP without backup codes | Users locked out if phone lost | Always generate and store backup codes |
| Storing tokens in localStorage | XSS can steal tokens | Use HttpOnly cookies for refresh tokens |
| No MFA on admin accounts | Admin takeover via password breach | Require MFA for all privileged accounts |

---

## Related Skills

- **appsec-expert**: For general application security patterns
- **cryptography-expert**: For JWT signing and token hashing
- **nextjs-expert**: For NextAuth.js integration
- **nodejs-expert**: For Express session and JWT middleware
- **supabase-expert**: For Supabase Auth integration
- **secrets-management**: For storing auth secrets securely
