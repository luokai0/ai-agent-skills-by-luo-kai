# AgentSkills Registry API Reference

The CLI communicates with the server via these REST API endpoints. This reference is for agents or developers who need to understand the underlying protocol.

## Endpoints

### Search Skills

```
GET /v1/skills?q={keyword}
```

Returns a list of skills matching the keyword.

**Response (200):**

```json
{
  "total": 1,
  "page": 1,
  "per_page": 20,
  "results": [
    {
      "name": "code-review-agent",
      "description": "Automated PR code review",
      "owner": "liuyukai",
      "downloads": 42,
      "latest_version": "1.2.0",
      "tags": ["code-review", "github"]
    }
  ]
}
```

### Get Skill Info

```
GET /v1/skills/{name}
```

Returns metadata for a specific skill.

**Response (200):**

```json
{
  "name": "code-review-agent",
  "owner": "liuyukai",
  "downloads": 42,
  "latest_version": {
    "version": "1.2.0",
    "description": "Automated PR code review",
    "checksum": "sha256:abc123...",
    "size_bytes": 2048,
    "published_at": "2026-01-15T10:30:00Z"
  }
}
```

### Download Bundle

```
GET /v1/skills/{name}/versions/{version}/download
```

Downloads the `.tar.gz` bundle for a specific version.

**Response Headers:**
- `X-Checksum-SHA256`: hex-encoded SHA256 of the bundle file
- `Content-Type`: `application/gzip`

### Publish Skill

```
POST /v1/skills/publish
Content-Type: multipart/form-data
Authorization: Bearer {token}
```

Upload a `.tar.gz` bundle. The form field name is `file`.

**Response (201):**

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "checksum": "sha256:def456...",
  "published_at": "2026-03-01T12:00:00Z"
}
```
