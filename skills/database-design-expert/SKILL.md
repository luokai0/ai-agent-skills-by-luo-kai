---
name: database-design
description: Expert database schema design and architecture. Use when designing relational or document schemas, normalization, ER diagrams, choosing between SQL and NoSQL, handling many-to-many relations, or optimizing data models. Also use when the user mentions 'schema design', 'normalization', 'ER diagram', 'foreign key', 'many-to-many', 'data model', 'database architecture', 'table design', or 'NoSQL vs SQL'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Database Design Expert

You are an expert in database schema design with deep knowledge of relational modeling, normalization, NoSQL patterns, and designing schemas that scale.

## Before Starting

1. **Database type** — PostgreSQL, MySQL, MongoDB, DynamoDB, or multiple?
2. **Scale** — thousands or millions of rows? Read-heavy or write-heavy?
3. **Problem type** — new schema design, reviewing existing, migration, normalization?
4. **Access patterns** — what queries will run most often?
5. **Constraints** — team expertise, existing systems, compliance requirements?

---

## Core Expertise Areas

- **Normalization**: 1NF, 2NF, 3NF, BCNF — when to normalize and when to denormalize
- **Relationships**: one-to-one, one-to-many, many-to-many with junction tables
- **Primary keys**: auto-increment, UUID, ULID, natural keys — trade-offs
- **Soft deletes**: deleted_at pattern, archive tables, status enums
- **Audit trails**: created_at, updated_at, history tables, temporal tables
- **Polymorphic associations**: single table inheritance, concrete table inheritance
- **NoSQL patterns**: document modeling, embedding vs referencing
- **Time-series data**: append-only patterns, partitioning by time

---

## Key Patterns & Code

### Design Process
```
Step 1: Identify entities
  What are the main nouns in the domain?
  User, Order, Product, Payment, Review, Category

Step 2: Identify relationships
  User places many Orders
  Order contains many Products (many-to-many via OrderItem)
  Product belongs to one Category
  Order has one Payment

Step 3: Identify attributes
  What data does each entity have?
  User: id, email, name, created_at
  Order: id, user_id, status, total_cents, created_at

Step 4: Normalize
  Remove repeating groups (1NF)
  Remove partial dependencies (2NF)
  Remove transitive dependencies (3NF)

Step 5: Identify access patterns
  What queries will run most often?
  Add indexes for those patterns
  Denormalize only when measured performance requires it

Step 6: Add operational columns
  created_at, updated_at, deleted_at
  version (for optimistic locking)
  status with CHECK constraint
```

### Normalization in Practice
```sql
-- 1NF: Atomic values, no repeating groups
-- WRONG: storing multiple values in one column
CREATE TABLE orders_wrong (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT,
  product_ids TEXT  -- '1,2,3' violates 1NF
);

-- RIGHT: separate table for the relationship
CREATE TABLE orders (
  id         BIGSERIAL PRIMARY KEY,
  user_id    BIGINT NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
  order_id   BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(id),
  quantity   INT NOT NULL CHECK (quantity > 0),
  unit_price_cents INT NOT NULL CHECK (unit_price_cents >= 0),
  PRIMARY KEY (order_id, product_id)
);

-- 2NF: No partial dependencies (only relevant for composite PKs)
-- WRONG: order_date depends only on order_id, not on (order_id, product_id)
CREATE TABLE order_items_wrong (
  order_id    BIGINT,
  product_id  BIGINT,
  order_date  DATE,  -- depends only on order_id, not composite PK
  quantity    INT,
  PRIMARY KEY (order_id, product_id)
);

-- RIGHT: move order_date to orders table where it belongs

-- 3NF: No transitive dependencies
-- WRONG: zip_code -> city, state (transitive dependency)
CREATE TABLE users_wrong (
  id       BIGSERIAL PRIMARY KEY,
  email    TEXT,
  zip_code TEXT,
  city     TEXT,  -- depends on zip_code, not user id
  state    TEXT   -- depends on zip_code, not user id
);

-- RIGHT: separate zip codes
CREATE TABLE zip_codes (
  zip_code TEXT PRIMARY KEY,
  city     TEXT NOT NULL,
  state    TEXT NOT NULL
);

CREATE TABLE users (
  id       BIGSERIAL PRIMARY KEY,
  email    TEXT NOT NULL UNIQUE,
  zip_code TEXT REFERENCES zip_codes(zip_code)
);
```

### Primary Key Strategies
```sql
-- Auto-increment: simple, small, fast joins
-- Problem: predictable (security), no distributed generation
CREATE TABLE users_autoincrement (
  id BIGSERIAL PRIMARY KEY  -- 8 bytes, sequential
);

-- UUID v4: globally unique, not sequential
-- Problem: random = bad index performance (page fragmentation)
CREATE TABLE users_uuid (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()  -- 16 bytes, random
);

-- ULID / UUID v7: globally unique AND time-ordered
-- Best of both worlds for most use cases
CREATE TABLE users_ulid (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()  -- use uuid_generate_v7() with extension
);
-- Or use ULID via application layer

-- Prefixed IDs (Stripe style): readable and self-describing
-- usr_01H2XKBD5T8X6Y3N0ZV9W, ord_01H2XKBD5T8X6Y3N0ZV9X
-- Generate in application code, store as TEXT
CREATE TABLE users_prefixed (
  id TEXT PRIMARY KEY  -- 'usr_' + ulid
);

-- When to use each:
-- Auto-increment: internal tables, high-write tables, simple apps
-- UUID v4: distributed systems, external-facing IDs (hide count)
-- UUID v7 / ULID: best default for most new projects
-- Prefixed: public APIs, developer-facing resources
```

### Many-to-Many Relationships
```sql
-- Simple many-to-many junction table
CREATE TABLE user_roles (
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id    UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  granted_by UUID REFERENCES users(id),
  PRIMARY KEY (user_id, role_id)
);

CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);

-- Many-to-many with extra attributes
CREATE TABLE order_items (
  id             BIGSERIAL PRIMARY KEY,  -- own PK when extra attributes exist
  order_id       UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id     UUID NOT NULL REFERENCES products(id),
  quantity       INT NOT NULL CHECK (quantity > 0),
  unit_price_cents INT NOT NULL,
  discount_pct   NUMERIC(5,2) NOT NULL DEFAULT 0
    CHECK (discount_pct BETWEEN 0 AND 100),
  UNIQUE (order_id, product_id)  -- prevent duplicates
);

-- Self-referential many-to-many (followers/following)
CREATE TABLE user_follows (
  follower_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id),
  CHECK (follower_id != following_id)  -- cannot follow yourself
);

CREATE INDEX idx_user_follows_following ON user_follows(following_id);
```

### Soft Deletes
```sql
-- Pattern 1: deleted_at timestamp (most common)
CREATE TABLE products (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name       TEXT NOT NULL,
  deleted_at TIMESTAMPTZ  -- NULL means not deleted
);

-- Always filter out deleted records
SELECT * FROM products WHERE deleted_at IS NULL;

-- Partial index — only index active records
CREATE INDEX idx_products_active ON products(name)
WHERE deleted_at IS NULL;

-- Pattern 2: status enum (when you need more states)
CREATE TYPE product_status AS ENUM ('active', 'archived', 'deleted');

CREATE TABLE products_v2 (
  id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name   TEXT NOT NULL,
  status product_status NOT NULL DEFAULT 'active'
);

CREATE INDEX idx_products_active_v2 ON products_v2(name)
WHERE status = 'active';

-- Pattern 3: archive table (separate active and deleted)
-- Best for tables with very high delete rates
CREATE TABLE products_archive (LIKE products INCLUDING ALL);

-- Move to archive instead of deleting
WITH deleted AS (
  DELETE FROM products WHERE id = $1 RETURNING *
)
INSERT INTO products_archive SELECT * FROM deleted;
```

### Audit Trail Patterns
```sql
-- Pattern 1: timestamps on every table (minimum)
CREATE TABLE orders (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id),
  status     TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-update updated_at with trigger
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $func$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$func$ LANGUAGE plpgsql;

CREATE TRIGGER orders_updated_at
  BEFORE UPDATE ON orders
  FOR EACH ROW
  EXECUTE FUNCTION set_updated_at();

-- Pattern 2: full history table
CREATE TABLE order_history (
  id          BIGSERIAL PRIMARY KEY,
  order_id    UUID NOT NULL REFERENCES orders(id),
  changed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  changed_by  UUID REFERENCES users(id),
  operation   TEXT NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
  old_data    JSONB,
  new_data    JSONB,
  changed_fields TEXT[]  -- which fields actually changed
);

CREATE INDEX idx_order_history_order_id ON order_history(order_id, changed_at DESC);

-- Trigger to capture history
CREATE OR REPLACE FUNCTION record_order_history()
RETURNS TRIGGER AS $func$
BEGIN
  INSERT INTO order_history (order_id, operation, old_data, new_data)
  VALUES (
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE row_to_json(OLD) END,
    CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE row_to_json(NEW) END
  );
  RETURN COALESCE(NEW, OLD);
END;
$func$ LANGUAGE plpgsql;
```

### Polymorphic Associations
```sql
-- Problem: Comments can belong to Posts OR Videos OR Products

-- Pattern 1: Nullable foreign keys (simple, but messy)
CREATE TABLE comments_nullable (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  body       TEXT NOT NULL,
  user_id    UUID NOT NULL REFERENCES users(id),
  post_id    UUID REFERENCES posts(id),     -- nullable
  video_id   UUID REFERENCES videos(id),    -- nullable
  product_id UUID REFERENCES products(id),  -- nullable
  CHECK (
    (post_id IS NOT NULL)::INT +
    (video_id IS NOT NULL)::INT +
    (product_id IS NOT NULL)::INT = 1  -- exactly one must be set
  )
);

-- Pattern 2: Generic association with type column
CREATE TABLE comments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  body            TEXT NOT NULL,
  user_id         UUID NOT NULL REFERENCES users(id),
  commentable_type TEXT NOT NULL CHECK (commentable_type IN ('post', 'video', 'product')),
  commentable_id  UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_comments_commentable
  ON comments(commentable_type, commentable_id);

-- Pattern 3: Separate tables per type (cleanest, best performance)
CREATE TABLE post_comments (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  body       TEXT NOT NULL,
  user_id    UUID NOT NULL REFERENCES users(id),
  post_id    UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE video_comments (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  body       TEXT NOT NULL,
  user_id    UUID NOT NULL REFERENCES users(id),
  video_id   UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Pattern 3 is verbose but has proper foreign keys and best query performance
```

### Complete E-commerce Schema Example
```sql
-- Users
CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  role          TEXT NOT NULL DEFAULT 'customer'
                  CHECK (role IN ('customer', 'admin', 'vendor')),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at    TIMESTAMPTZ
);

-- Product categories (self-referential for hierarchy)
CREATE TABLE categories (
  id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name      TEXT NOT NULL,
  slug      TEXT NOT NULL UNIQUE,
  parent_id UUID REFERENCES categories(id),
  sort_order INT NOT NULL DEFAULT 0
);

-- Products
CREATE TABLE products (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  slug        TEXT NOT NULL UNIQUE,
  description TEXT,
  category_id UUID NOT NULL REFERENCES categories(id),
  price_cents INT NOT NULL CHECK (price_cents >= 0),
  stock_qty   INT NOT NULL DEFAULT 0 CHECK (stock_qty >= 0),
  is_active   BOOLEAN NOT NULL DEFAULT true,
  metadata    JSONB NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Orders
CREATE TABLE orders (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id),
  status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
  subtotal_cents  INT NOT NULL CHECK (subtotal_cents >= 0),
  tax_cents       INT NOT NULL DEFAULT 0 CHECK (tax_cents >= 0),
  total_cents     INT NOT NULL CHECK (total_cents >= 0),
  currency        CHAR(3) NOT NULL DEFAULT 'USD',
  shipping_address JSONB NOT NULL,
  notes           TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Order items
CREATE TABLE order_items (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id         UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id       UUID NOT NULL REFERENCES products(id),
  quantity         INT NOT NULL CHECK (quantity > 0),
  unit_price_cents INT NOT NULL CHECK (unit_price_cents >= 0),
  UNIQUE (order_id, product_id)
);

-- Payments
CREATE TABLE payments (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id            UUID NOT NULL REFERENCES orders(id),
  amount_cents        INT NOT NULL CHECK (amount_cents > 0),
  currency            CHAR(3) NOT NULL,
  status              TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
  provider            TEXT NOT NULL,
  provider_payment_id TEXT UNIQUE,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_orders_user_id         ON orders(user_id);
CREATE INDEX idx_orders_status          ON orders(status) WHERE status NOT IN ('delivered', 'cancelled');
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_category      ON products(category_id) WHERE is_active = true;
CREATE INDEX idx_products_slug          ON products(slug);
CREATE INDEX idx_users_email            ON users(email) WHERE deleted_at IS NULL;
```

### SQL vs NoSQL Decision Guide
```
Use PostgreSQL/MySQL when:
  - Data has clear relationships and consistent structure
  - ACID transactions across multiple entities required
  - Complex queries with JOINs, aggregations, window functions
  - Schema is known upfront and relatively stable
  - Team knows SQL well
  Examples: financial data, user accounts, orders, inventory

Use MongoDB when:
  - Documents are self-contained (few JOINs needed)
  - Schema varies significantly between records
  - Hierarchical/nested data that maps naturally to documents
  - Rapid schema evolution during early development
  Examples: CMS content, product catalogs with varying attributes

Use DynamoDB/Cassandra when:
  - Massive write scale (millions/sec)
  - Access patterns are known and simple (key-value, range scans)
  - Eventual consistency is acceptable
  - Auto-scaling without operational overhead
  Examples: user sessions, IoT sensor data, event logs, shopping carts

Use Redis when:
  - Sub-millisecond latency required
  - Data fits in memory
  - Simple data structures (sorted sets, hashes, strings)
  Examples: caching, rate limiting, leaderboards, sessions

Use both (polyglot persistence):
  PostgreSQL as source of truth for transactions
  Redis for caching and sessions
  Elasticsearch for full-text search
  S3 for file storage
```

---

## Best Practices

- Design for your access patterns — add indexes based on actual queries
- Always use TIMESTAMPTZ not TIMESTAMP — always store UTC
- Use UUID or ULID for primary keys in distributed or public-facing systems
- Add CHECK constraints liberally — they document business rules in the schema
- Store money as integers (cents) — never float
- Use ENUM types or CHECK constraints for status fields
- Add NOT NULL to every column that should never be null
- Index foreign keys — PostgreSQL does not do this automatically
- Use ON DELETE CASCADE only when child rows are meaningless without parent

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Float for money | 0.1 + 0.2 = 0.30000000000000004 | Store as integer cents |
| TIMESTAMP without timezone | Wrong times across timezones | Always use TIMESTAMPTZ |
| No indexes on FKs | Slow JOINs and cascading deletes | Always index foreign key columns |
| Storing arrays in VARCHAR | Violates 1NF, hard to query | Use separate junction table |
| Sequential auto-increment public IDs | Exposes record count, scraping risk | Use UUID or ULID for external IDs |
| Missing NOT NULL | Unexpected nulls break queries | Add NOT NULL to every required column |
| No updated_at | Cannot sync or detect stale data | Add updated_at with trigger |
| Denormalizing too early | Inconsistent data, update anomalies | Normalize first, denormalize only when measured |

---

## Related Skills

- **postgresql-expert**: For PostgreSQL-specific queries and features
- **mongodb-expert**: For document database design
- **prisma-expert**: For schema design with Prisma ORM
- **system-design**: For database selection in system design
- **data-engineering**: For analytical schema design (star schema, data vault)
- **domain-driven-design**: For aligning database schema with domain model