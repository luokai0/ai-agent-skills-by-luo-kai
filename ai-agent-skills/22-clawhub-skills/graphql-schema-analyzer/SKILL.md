---
name: graphql-schema-analyzer
description: Analyze GraphQL schemas for performance, security, complexity, and best practices — detect N+1 queries, circular references, excessive depth, and missing authorization.
metadata:
  tags: ["graphql", "api", "performance", "security", "schema"]
---

# GraphQL Schema Analyzer

Analyze GraphQL schemas for performance bottlenecks, security vulnerabilities, query complexity issues, and best practices. Detects N+1 resolver patterns, circular references, excessive query depth, missing authorization, and schema design anti-patterns.

## Usage

```
"Analyze my GraphQL schema for issues"
"Check for N+1 queries in my resolvers"
"Audit GraphQL authorization and security"
"Optimize my GraphQL schema performance"
```

## How It Works

### 1. Schema Discovery

```bash
# Find schema files
find . -name "*.graphql" -o -name "*.gql" -o -name "schema.ts" -o -name "typeDefs*" | head -20
# Find resolver files
find . -name "*resolver*" -o -name "*resolvers*" | head -20
# Check for schema-first vs code-first
grep -rn "buildSchema\|makeExecutableSchema\|@ObjectType\|@Field" src/ 2>/dev/null | head -10
```

### 2. Schema Analysis

**Type design:**
- Nullable vs non-nullable fields (default to non-nullable, opt into nullable)
- Proper use of interfaces and unions
- Enum types vs string fields
- Input types vs reusing output types
- Relay-style pagination (connections) vs offset pagination
- Proper ID types

**Naming conventions:**
- PascalCase for types, camelCase for fields
- Consistent verb prefixes for mutations (create/update/delete)
- Query names reflect what they return
- Input type naming (CreateUserInput, not UserInput)

### 3. Performance Analysis

**N+1 query detection:**
- List resolvers that fetch related data individually
- Missing DataLoader usage for batched lookups
- Nested resolvers triggering individual database queries

**Query complexity:**
- Fields that return large lists without pagination
- Deeply nested types (>4 levels)
- Expensive computed fields without caching
- Missing query depth/complexity limits

**Resolver efficiency:**
- Overfetching from database (SELECT * when only 2 fields needed)
- Missing field-level resolvers (resolving entire object when partial suffices)
- Redundant resolver calls for the same data

### 4. Security Audit

**Authorization:**
- Fields/mutations without auth checks
- Authorization at resolver level vs directive level
- Introspection enabled in production
- Sensitive fields exposed (email, phone, internal IDs)

**Denial of service:**
- No query depth limit
- No query complexity limit
- No rate limiting
- Circular references enabling infinite depth queries
- Aliases allowing query multiplication
- Batch queries without limits

**Data leakage:**
- Error messages exposing internal details
- Stack traces in production responses
- Field suggestions in production (did you mean X?)

### 5. Best Practices

- Deprecation annotations on legacy fields
- Description/documentation on types and fields
- Proper error handling (user errors vs system errors)
- Subscription efficiency (pub/sub vs polling)
- Schema stitching/federation best practices
- Versioning strategy (no versioning in GraphQL — evolve the schema)

## Output

```
## GraphQL Schema Analysis

**Types:** 34 | **Queries:** 12 | **Mutations:** 18 | **Subscriptions:** 3

### 🔴 Critical (3)
1. **N+1 on User.posts resolver** — resolvers/user.ts:23
   Each user in a list query triggers individual posts query
   → Implement DataLoader: batch user IDs → single query

2. **No query depth limit** — server.ts
   Allows queries nested to unlimited depth
   → Add depth limiting plugin (max 8-10 levels)

3. **Introspection enabled in production** — server.ts:15
   Full schema discoverable by anyone
   → Disable in production: `introspection: process.env.NODE_ENV !== 'production'`

### 🟡 Warnings (5)
4. 3 mutations without authorization middleware
5. User.email exposed without field-level auth
6. `posts` query returns unbounded list (no pagination)
7. Circular reference: User → Posts → Author → Posts
8. 5 deprecated fields without migration timeline

### 📊 Schema Metrics
- Average type size: 6.2 fields
- Deepest nesting: 7 levels (User → Posts → Comments → Author → ...)
- Largest type: Order (18 fields — consider splitting)
- Undocumented types: 12/34 (35%)

### ✅ Good Practices
- Relay-style pagination on main collections
- Input validation via custom scalars (Email, DateTime)
- Proper union types for polymorphic returns
- Error union pattern for typed error handling
```
