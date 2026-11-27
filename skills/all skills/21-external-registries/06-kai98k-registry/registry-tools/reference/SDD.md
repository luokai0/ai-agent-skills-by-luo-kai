# AgentSkills — Software Design Document (SDD)

**Version:** 1.0 (MVP)
**Date:** 2026-02-20
**Author:** LIU YU KAI
**Purpose:** 本文件為 Claude Code 的開發藍圖。請嚴格依照本文件的規格、目錄結構、API Contract 與 DB Schema 進行開發與驗證。

---

## 1. 專案概述

AgentSkills 是一個 AI Agent Skill 的集中式 Registry 平台，類似 npm 或 Docker Hub。開發者可透過 CLI 工具上傳（push）與下載（pull）標準化的 Skill Bundle，平台負責版本控制、Metadata 解析與檔案儲存。

**MVP 範圍僅包含：**

- FastAPI 後端 API（Python）
- Go CLI 工具
- PostgreSQL 資料庫
- MinIO 物件儲存（S3 相容）
- Docker Compose 本地開發環境

**MVP 明確不包含：**

- Web UI 前端
- OAuth / 第三方登入
- Semver range resolution（`^1.0.0`）
- Skill 之間的依賴關係
- unpublish / deprecate 功能
- 自動版本號 bump

---

## 2. Skill Bundle 標準

每個 Skill 是一個目錄，打包為 `.tar.gz` 上傳。

### 2.1 目錄結構

```
my-skill/
├── SKILL.md         (必填) 核心定義：YAML Frontmatter + Markdown 指令
├── scripts/         (選填) Agent 可呼叫的腳本
├── references/      (選填) RAG / Few-shot 參考文件
└── assets/          (選填) 靜態模板與資源
```

### 2.2 SKILL.md Frontmatter 規格

```yaml
---
name: "code-review-agent"           # 必填, 全域唯一, 格式: [a-z0-9\-], 3-64 字元
version: "1.0.0"                    # 必填, 嚴格 semver (MAJOR.MINOR.PATCH)
description: "PR code review skill" # 必填, 最長 256 字元
author: "liuyukai"                  # 必填, 與上傳者帳號一致
tags:                               # 選填, 最多 10 個, 每個最長 32 字元
  - code-review
  - github
license: "MIT"                      # 選填, SPDX identifier
min_agent_version: ">=0.1.0"        # 選填, 保留欄位 (MVP 不驗證)
---

# Code Review Agent

以下為 Markdown 格式的 Skill 指令內容...
```

### 2.3 Frontmatter 驗證規則

| 欄位 | 類型 | 必填 | 驗證規則 |
|------|------|------|----------|
| name | string | ✅ | `/^[a-z0-9\-]{3,64}$/`，不允許連續 `--` |
| version | string | ✅ | 嚴格 semver，使用 Python `semver` 套件驗證 |
| description | string | ✅ | 1-256 字元 |
| author | string | ✅ | 必須與 API Token 對應的 username 一致 |
| tags | list[string] | ❌ | 最多 10 個，每個 `/^[a-z0-9\-]{1,32}$/` |
| license | string | ❌ | 若提供需為合法 SPDX identifier |
| min_agent_version | string | ❌ | MVP 階段僅儲存，不做邏輯判斷 |

---

## 3. 系統架構

```
┌──────────────────────────────────────────┐
│            docker-compose                │
│                                          │
│  ┌─────────────┐    ┌─────────────────┐  │
│  │ PostgreSQL   │    │ MinIO (S3)      │  │
│  │ port: 5432   │    │ API:  9000      │  │
│  │              │    │ Console: 9001   │  │
│  └──────┬───────┘    └──────┬──────────┘  │
│         │                   │             │
│         └─────────┬─────────┘             │
│              ┌────┴────┐                  │
│              │ FastAPI  │                  │
│              │ port:8000│                  │
│              └────┬─────┘                  │
│                   │                        │
└───────────────────┼────────────────────────┘
                    │
             ┌──────┴──────┐
             │   Go CLI    │
             │ (本機執行)   │
             └─────────────┘
```

---

## 4. 資料庫設計 (PostgreSQL)

### 4.1 Schema

```sql
-- init.sql
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
-- SKILLS (一個 name 一筆)
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
-- SKILL VERSIONS (每次 publish 一筆, immutable)
-- ==========================================
CREATE TABLE skill_versions (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id      UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    version       VARCHAR(32) NOT NULL,
    bundle_key    TEXT NOT NULL,           -- MinIO object key, e.g. "code-review-agent/1.0.0.tar.gz"
    metadata      JSONB NOT NULL,          -- 完整 frontmatter
    checksum      VARCHAR(64) NOT NULL,    -- SHA-256 hex digest
    size_bytes    BIGINT NOT NULL,         -- bundle 檔案大小
    published_at  TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT uq_skill_version UNIQUE (skill_id, version)
);

CREATE INDEX idx_skill_versions_latest
    ON skill_versions (skill_id, published_at DESC);

CREATE INDEX idx_skills_name
    ON skills (name);

-- ==========================================
-- SEED DATA (開發用測試帳號)
-- ==========================================
INSERT INTO users (username, api_token)
VALUES ('dev', 'dev-token-12345');
```

### 4.2 設計決策

- **兩表分離**：`skills` 存身份與聚合資料（downloads），`skill_versions` 存每次發布的 immutable 記錄。
- **Immutable publish**：同一 `(skill_id, version)` 不可覆寫，嘗試重複發布回傳 `409 Conflict`。
- **Soft latest**：最新版透過 `published_at DESC LIMIT 1` 查詢，不額外維護 `latest` 欄位。
- **JSONB metadata**：frontmatter 全文存入，支援未來擴充欄位時不需 migration。

---

## 5. API 設計 (FastAPI)

**Base URL:** `http://localhost:8000/v1`

### 5.1 認證

MVP 使用靜態 API Token，透過 `Authorization: Bearer <token>` Header 傳遞。

```
Authorization: Bearer dev-token-12345
```

認證失敗回傳 `401 Unauthorized`。僅 `POST` (publish) 需要認證，`GET` 端點皆為公開。

### 5.2 端點規格

#### `POST /v1/skills/publish`

上傳一個 Skill Bundle。

**Request:**

- Header: `Authorization: Bearer <token>`
- Body: `multipart/form-data`
  - `file`: `.tar.gz` 檔案 (最大 50MB)

**Server 端處理流程：**

1. 驗證 API Token → 取得 `user`
2. 解壓縮 `.tar.gz` 至暫存目錄
3. 找到並解析 `SKILL.md` 的 YAML Frontmatter
4. 執行 Frontmatter 驗證（見 §2.3）
5. 確認 `author` == `user.username`
6. 計算整個 `.tar.gz` 的 SHA-256 checksum
7. 查詢 DB：若 `name` 不存在 → 新建 `skills` 記錄（owner = user）
8. 查詢 DB：若 `name` 存在但 `owner_id != user.id` → 403 Forbidden
9. 查詢 DB：若 `(skill_id, version)` 已存在 → 409 Conflict
10. 上傳 `.tar.gz` 至 MinIO → key: `{name}/{version}.tar.gz`
11. 寫入 `skill_versions` 記錄
12. 更新 `skills.updated_at`

**Success Response:** `201 Created`

```json
{
  "name": "code-review-agent",
  "version": "1.0.0",
  "checksum": "sha256:a1b2c3d4...",
  "published_at": "2026-02-20T10:00:00Z"
}
```

**Error Responses:**

| Code | Condition | Body |
|------|-----------|------|
| 400 | 無 SKILL.md / Frontmatter 驗證失敗 / 非 .tar.gz | `{"error": "具體錯誤訊息"}` |
| 401 | Token 無效或缺少 | `{"error": "Unauthorized"}` |
| 403 | name 已被其他使用者佔用 | `{"error": "Skill 'x' is owned by another user"}` |
| 409 | 版本已存在 | `{"error": "Version 1.0.0 already exists"}` |
| 413 | 檔案超過 50MB | `{"error": "Bundle exceeds 50MB limit"}` |

---

#### `GET /v1/skills/{name}`

取得 Skill 資訊與最新版本。

**Success Response:** `200 OK`

```json
{
  "name": "code-review-agent",
  "owner": "liuyukai",
  "downloads": 42,
  "created_at": "2026-02-20T10:00:00Z",
  "latest_version": {
    "version": "1.2.0",
    "description": "PR code review skill",
    "checksum": "sha256:a1b2c3d4...",
    "size_bytes": 15360,
    "published_at": "2026-02-20T12:00:00Z",
    "metadata": { ... }
  }
}
```

**Error:** `404 Not Found` 若 name 不存在。

---

#### `GET /v1/skills/{name}/versions`

列出 Skill 所有版本。

**Success Response:** `200 OK`

```json
{
  "name": "code-review-agent",
  "versions": [
    {
      "version": "1.2.0",
      "checksum": "sha256:...",
      "size_bytes": 15360,
      "published_at": "2026-02-20T12:00:00Z"
    },
    {
      "version": "1.0.0",
      "checksum": "sha256:...",
      "size_bytes": 12288,
      "published_at": "2026-02-20T10:00:00Z"
    }
  ]
}
```

---

#### `GET /v1/skills/{name}/versions/{version}/download`

下載指定版本的 Bundle。

**行為：** 回傳 MinIO presigned URL 做 302 Redirect，或直接串流檔案內容（MVP 用串流較簡單）。

**Response:** `200 OK`

- `Content-Type: application/gzip`
- `Content-Disposition: attachment; filename="code-review-agent-1.0.0.tar.gz"`
- `X-Checksum-SHA256: a1b2c3d4...`
- Body: raw binary

**Side effect:** `skills.downloads += 1`

**Error:** `404` 若 name 或 version 不存在。

---

#### `GET /v1/skills?q={keyword}&tag={tag}&page={n}&per_page={n}`

搜尋 Skills。

**Query Parameters:**

| Param | Type | Default | 說明 |
|-------|------|---------|------|
| q | string | - | 搜尋 name 和 description（ILIKE） |
| tag | string | - | 精確匹配 metadata tags（可多次傳遞） |
| page | int | 1 | 頁碼 |
| per_page | int | 20 | 每頁數量，最大 100 |

**Success Response:** `200 OK`

```json
{
  "total": 45,
  "page": 1,
  "per_page": 20,
  "results": [
    {
      "name": "code-review-agent",
      "description": "PR code review skill",
      "owner": "liuyukai",
      "downloads": 42,
      "latest_version": "1.2.0",
      "updated_at": "2026-02-20T12:00:00Z",
      "tags": ["code-review", "github"]
    }
  ]
}
```

---

#### `GET /v1/health`

健康檢查端點。

**Response:** `200 OK`

```json
{
  "status": "ok",
  "database": "connected",
  "storage": "connected"
}
```

---

## 6. 後端專案結構 (Python / FastAPI)

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app 入口, lifespan, middleware
│   ├── config.py              # pydantic-settings, 環境變數讀取
│   ├── dependencies.py        # Depends: get_db, get_current_user, get_s3
│   ├── models.py              # SQLAlchemy ORM models (對應 §4.1 schema)
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── skills.py          # 所有 /v1/skills 端點
│   │   └── health.py          # /v1/health
│   └── services/
│       ├── __init__.py
│       ├── storage.py          # MinIO/S3 上傳、下載、presigned URL
│       ├── parser.py           # .tar.gz 解壓、SKILL.md 解析、YAML 驗證
│       └── auth.py             # API Token 驗證邏輯
├── tests/
│   ├── conftest.py            # pytest fixtures: test DB, test S3, test client
│   ├── test_publish.py        # publish 端點完整測試
│   ├── test_pull.py           # download 端點測試
│   ├── test_search.py         # search 端點測試
│   └── test_parser.py         # SKILL.md 解析與驗證測試
├── alembic/                   # DB migration (選配, MVP 可直接用 init.sql)
│   ├── alembic.ini
│   └── versions/
├── requirements.txt
└── Dockerfile
```

### 6.1 核心依賴 (requirements.txt)

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy[asyncio]>=2.0
asyncpg>=0.30.0
pydantic>=2.0
pydantic-settings>=2.0
boto3>=1.35.0
python-multipart>=0.0.9
pyyaml>=6.0
semver>=3.0
python-frontmatter>=1.1
httpx>=0.27.0
pytest>=8.0
pytest-asyncio>=0.24.0
```

### 6.2 config.py 規格

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://dev:devpass@localhost:5432/agentskills"

    # MinIO / S3
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "skills"
    s3_region: str = "us-east-1"

    # App
    max_bundle_size: int = 50 * 1024 * 1024  # 50MB
    api_prefix: str = "/v1"

    class Config:
        env_file = ".env"
```

### 6.3 parser.py 核心邏輯

```python
"""
SKILL.md 解析流程：
1. 接收上傳的 .tar.gz bytes
2. 解壓至暫存目錄 (tempfile.mkdtemp)
3. 遍歷解壓後的檔案，找到 SKILL.md（必須在根目錄或一層子目錄內）
4. 使用 python-frontmatter 解析 YAML + Markdown body
5. 對 YAML 執行 §2.3 驗證規則
6. 回傳 ParsedSkill dataclass

注意事項：
- 解壓時檢查 zip bomb（解壓後總大小不超過 200MB）
- 路徑穿越攻擊防護（所有解壓路徑必須在暫存目錄下）
- 暫存目錄用完即刪
"""
```

### 6.4 storage.py 核心邏輯

```python
"""
使用 boto3 連接 MinIO（S3 相容 API）。

關鍵設定（確保 MinIO 相容）：
- endpoint_url: 必須設定為 config.s3_endpoint
- 使用 path-style addressing（MinIO 不支援 virtual-hosted-style）

核心方法：
- upload_bundle(name, version, file_bytes) -> bundle_key
- download_bundle(bundle_key) -> StreamingResponse
- check_health() -> bool
"""
```

---

## 7. CLI 設計 (Go / Cobra)

### 7.1 專案結構

```
cli/
├── main.go
├── go.mod
├── go.sum
├── cmd/
│   ├── root.go         # Cobra root command, global flags
│   ├── init_cmd.go     # agentskills init
│   ├── push.go         # agentskills push
│   ├── pull.go         # agentskills pull
│   ├── search.go       # agentskills search
│   └── login.go        # agentskills login (存 token 到 config)
├── internal/
│   ├── config/
│   │   └── config.go   # 讀取 ~/.agentskills/config.yaml
│   ├── api/
│   │   └── client.go   # HTTP client, 封裝所有 API 呼叫
│   ├── bundle/
│   │   └── pack.go     # tar.gz 打包與解壓邏輯
│   └── parser/
│       └── frontmatter.go  # 本地 SKILL.md 驗證 (push 前預檢)
└── Makefile            # build targets for linux/darwin/windows
```

### 7.2 指令規格

#### `agentskills init [name]`

在當前目錄建立 Skill 骨架。

```bash
$ agentskills init my-new-skill

Created my-new-skill/
  ├── SKILL.md        (已填入模板 frontmatter)
  ├── scripts/
  ├── references/
  └── assets/
```

SKILL.md 模板：

```yaml
---
name: "my-new-skill"
version: "0.1.0"
description: ""
author: ""
tags: []
---

# my-new-skill

Describe your skill here.
```

#### `agentskills push [path]`

打包並上傳 Skill Bundle。

```bash
$ agentskills push ./my-skill

Validating SKILL.md...        ✓
Packing bundle...             ✓ (12.3 KB)
Uploading my-skill@1.0.0...   ✓
Checksum: sha256:a1b2c3d4...

Published my-skill@1.0.0 successfully.
```

**流程：**

1. 讀取 `path/SKILL.md`，本地解析並驗證 frontmatter
2. 將整個目錄打包為 `.tar.gz`（排除 `.git`, `node_modules`, `__pycache__`）
3. 計算 SHA-256
4. POST 至 `/v1/skills/publish`
5. 驗證 server 回傳的 checksum 與本地一致
6. 輸出結果

**排除清單 (hardcoded)：**

```
.git/
.DS_Store
node_modules/
__pycache__/
*.pyc
.env
```

#### `agentskills pull <name>[@version]`

下載 Skill Bundle 並解壓至當前目錄。

```bash
$ agentskills pull code-review-agent
Downloading code-review-agent@1.2.0 (latest)...  ✓
Verifying checksum...                              ✓
Extracted to ./code-review-agent/

$ agentskills pull code-review-agent@1.0.0
Downloading code-review-agent@1.0.0...            ✓
Verifying checksum...                              ✓
Extracted to ./code-review-agent/
```

**流程：**

1. 解析 `name` 和可選的 `@version`
2. 若無 version → `GET /v1/skills/{name}` 取 latest version
3. `GET /v1/skills/{name}/versions/{version}/download` 下載 `.tar.gz`
4. 驗證 `X-Checksum-SHA256` header 與下載內容的 SHA-256 一致
5. 解壓至 `./{name}/`（若目錄已存在，提示覆蓋確認）

#### `agentskills search <keyword>`

搜尋平台上的 Skills。

```bash
$ agentskills search code-review

NAME                  VERSION  DOWNLOADS  DESCRIPTION
code-review-agent     1.2.0    42         PR code review skill
code-review-lite      0.3.0    7          Lightweight review helper
```

#### `agentskills login`

儲存 API Token 至本地設定。

```bash
$ agentskills login
Enter API token: ********
Token saved to ~/.agentskills/config.yaml
```

### 7.3 本地設定檔

路徑: `~/.agentskills/config.yaml`

```yaml
api_url: "http://localhost:8000"
token: "dev-token-12345"
```

### 7.4 核心依賴 (go.mod)

```
module github.com/liuyukai/agentskills-cli

go 1.22

require (
    github.com/spf13/cobra v1.8+
    github.com/spf13/viper v1.19+  // config 讀取
    gopkg.in/yaml.v3 v3.0+         // frontmatter 解析
)
```

---

## 8. Docker Compose 開發環境

### 8.1 docker-compose.yml

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: agentskills
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev -d agentskills"]
      interval: 5s
      timeout: 5s
      retries: 5

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - miniodata:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 5s
      timeout: 5s
      retries: 5

  minio-init:
    image: minio/mc:latest
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
      mc alias set local http://minio:9000 minioadmin minioadmin;
      mc mb --ignore-existing local/skills;
      echo 'Bucket skills created';
      "

volumes:
  pgdata:
  miniodata:
```

### 8.2 啟動與驗證指令

```bash
# 1. 啟動基礎設施
docker compose up -d

# 2. 驗證 PostgreSQL
docker compose exec postgres psql -U dev -d agentskills -c "SELECT COUNT(*) FROM users;"
# 預期輸出: 1 (dev 帳號)

# 3. 驗證 MinIO
curl -s http://localhost:9000/minio/health/live
# 預期輸出: HTTP 200

# 4. 啟動 FastAPI (開發模式)
cd api && uvicorn app.main:app --reload --port 8000

# 5. 驗證 API
curl http://localhost:8000/v1/health
# 預期輸出: {"status":"ok","database":"connected","storage":"connected"}

# 6. 完整 publish 測試
mkdir -p /tmp/test-skill && cat > /tmp/test-skill/SKILL.md << 'EOF'
---
name: "test-skill"
version: "0.1.0"
description: "A test skill for validation"
author: "dev"
tags:
  - test
---

# Test Skill

This is a test.
EOF

cd /tmp && tar -czf test-skill.tar.gz -C test-skill .
curl -X POST http://localhost:8000/v1/skills/publish \
  -H "Authorization: Bearer dev-token-12345" \
  -F "file=@test-skill.tar.gz"
# 預期: 201 Created

# 7. 驗證 pull
curl http://localhost:8000/v1/skills/test-skill
# 預期: 200 OK with latest_version.version == "0.1.0"

curl -O http://localhost:8000/v1/skills/test-skill/versions/0.1.0/download
# 預期: 下載 .tar.gz 檔案

# 8. 驗證 immutable publish (重複版本)
curl -X POST http://localhost:8000/v1/skills/publish \
  -H "Authorization: Bearer dev-token-12345" \
  -F "file=@test-skill.tar.gz"
# 預期: 409 Conflict

# 9. Go CLI 測試 (API 啟動後)
cd cli && go run main.go push /tmp/test-skill
go run main.go pull test-skill
go run main.go search test
```

---

## 9. 測試策略

### 9.1 後端測試 (pytest)

**conftest.py 需提供：**

- `test_db`：使用 SQLite async (`aiosqlite`) 作為測試資料庫，每個 test function 自動 rollback
- `test_s3`：mock boto3 client 或使用 `moto` library 模擬 S3
- `test_client`：FastAPI `TestClient`，注入 test_db 和 test_s3

**必要測試案例：**

| 測試檔案 | 案例 | 預期 |
|----------|------|------|
| test_parser.py | 合法 SKILL.md | 正確解析所有欄位 |
| test_parser.py | 缺少 name 欄位 | ValidationError |
| test_parser.py | version 非 semver | ValidationError |
| test_parser.py | name 含大寫或特殊字元 | ValidationError |
| test_parser.py | 無 SKILL.md 的 tar.gz | FileNotFoundError |
| test_publish.py | 正常 publish | 201, DB 有記錄, MinIO 有檔案 |
| test_publish.py | 無 auth header | 401 |
| test_publish.py | 重複版本 | 409 |
| test_publish.py | name 被他人佔用 | 403 |
| test_publish.py | 超過 50MB | 413 |
| test_pull.py | 下載 latest | 200, 正確 binary |
| test_pull.py | 下載指定版本 | 200, checksum 正確 |
| test_pull.py | 不存在的 skill | 404 |
| test_search.py | keyword 搜尋 | 回傳匹配結果 |
| test_search.py | tag 篩選 | 僅回傳有該 tag 的結果 |
| test_search.py | 空結果 | 200, results: [] |

### 9.2 CLI 測試 (go test)

- 本地 frontmatter 解析與驗證
- tar.gz 打包排除清單
- SHA-256 checksum 計算
- API client 呼叫 (使用 httptest mock server)
- config 檔讀寫

---

## 10. 安全性注意事項

| 威脅 | 防護措施 |
|------|----------|
| Zip bomb | 解壓時限制總大小 200MB，超過即中止 |
| 路徑穿越 (../../etc/passwd) | 所有解壓路徑檢查必須在暫存目錄下 |
| 任意檔案執行 | Server 端僅解析 SKILL.md，不執行 scripts/ 內任何檔案 |
| Token 洩漏 | CLI config 檔設 0600 權限；API logs 不記錄完整 token |
| SQL Injection | 使用 SQLAlchemy ORM parameterized queries |
| 超大檔案 DoS | FastAPI 層限制 request body 50MB |

---

## 11. 開發順序建議

以下為建議的實作優先順序，每個步驟完成後應可獨立驗證：

```
Step 1: 基礎設施
  └─ docker-compose.yml + init.sql → `docker compose up` 驗證 DB 和 MinIO

Step 2: FastAPI 骨架
  └─ main.py + config.py + health.py → `/v1/health` 回傳 connected

Step 3: Parser 模組
  └─ parser.py + test_parser.py → 所有解析測試通過

Step 4: Storage 模組
  └─ storage.py → 可上傳/下載 MinIO 檔案

Step 5: Publish 端點
  └─ POST /v1/skills/publish + test_publish.py → 完整 publish 流程

Step 6: Query 端點
  └─ GET /skills/{name}, /versions, /download, /search → 所有 GET 測試通過

Step 7: Go CLI 骨架
  └─ root.go + config.go + login.go → `agentskills login` 可存 token

Step 8: CLI push/pull
  └─ push.go + pull.go → 完整 CLI ↔ API 流程跑通

Step 9: CLI search + init
  └─ search.go + init_cmd.go → 所有 CLI 指令完成

Step 10: 整合驗證
  └─ 執行 §8.2 所有驗證指令，確認端對端流程正常
```

---

## 12. CLAUDE.md (放在 Repo 根目錄)

以下內容應放在 Repo 根目錄的 `CLAUDE.md`，供 Claude Code 開發時參考：

```markdown
# AgentSkills

AI Agent Skill Registry — CLI + API for publishing and pulling skill bundles.

## Architecture

- Backend: FastAPI (Python 3.12+) in `api/`
- CLI: Go + Cobra in `cli/`
- DB: PostgreSQL 16 (docker)
- Storage: MinIO S3-compatible (docker)
- Spec: See `SDD.md` for complete design document

## Infrastructure

- `docker compose up -d`: Start PostgreSQL (5432) + MinIO (9000/9001)
- `docker compose down -v`: Tear down with volumes

## Development — API

- `cd api && uvicorn app.main:app --reload --port 8000`
- `cd api && pytest -xvs`
- Python 3.12+, dependencies in requirements.txt
- Use `pip install -r requirements.txt --break-system-packages` if needed

## Development — CLI

- `cd cli && go run main.go <command>`
- `cd cli && go test ./...`
- Go 1.22+

## Key Rules

- ALWAYS read SDD.md before making architectural decisions
- DB schema is defined in init.sql — do not deviate
- API responses must match SDD.md §5.2 exactly
- Frontmatter validation rules are in SDD.md §2.3 — implement all of them
- Tests are mandatory for every endpoint and parser function
- Use async SQLAlchemy (asyncpg) — no sync database calls
- Use boto3 with endpoint_url for MinIO — path-style addressing required
- Never execute uploaded scripts server-side
```

---

*End of Document*