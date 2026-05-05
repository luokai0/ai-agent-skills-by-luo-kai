CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==========================================
-- USERS
-- ==========================================
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(64)  UNIQUE NOT NULL,
    api_token   VARCHAR(128) UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ  DEFAULT now()
);

-- ==========================================
-- SKILLS (one row per skill name)
-- ==========================================
CREATE TABLE skills (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(128) UNIQUE NOT NULL,
    owner_id    UUID NOT NULL REFERENCES users(id),
    downloads   BIGINT DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

-- ==========================================
-- SKILL VERSIONS (one row per publish, immutable)
-- ==========================================
CREATE TABLE skill_versions (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id      UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    version       VARCHAR(32) NOT NULL,
    bundle_key    TEXT NOT NULL,           -- MinIO object key, e.g. "code-review-agent/1.0.0.tar.gz"
    metadata      JSONB NOT NULL,          -- full frontmatter
    checksum      VARCHAR(64) NOT NULL,    -- SHA-256 hex digest
    size_bytes    BIGINT NOT NULL,         -- bundle file size
    published_at  TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT uq_skill_version UNIQUE (skill_id, version)
);

CREATE INDEX idx_skill_versions_latest
    ON skill_versions (skill_id, published_at DESC);

CREATE INDEX idx_skills_name
    ON skills (name);

-- ==========================================
-- SEED DATA (dev test account)
-- ==========================================
INSERT INTO users (username, api_token)
VALUES ('dev', 'dev-token-12345');
