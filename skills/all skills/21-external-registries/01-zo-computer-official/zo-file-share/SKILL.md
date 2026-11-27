---
name: file-share
description: Share files with email-gated access. Users must confirm their email before downloading. Includes a web UI for requesting access and a CLI for managing files and users.
compatibility: Created for Zo Computer
metadata:
  author: 0.zo.computer
  category: Official
---

## Prerequisites

- **Gmail must be connected** for email delivery to work.

## Setup

1. **Ensure Gmail is connected** at [Settings &gt; Integrations](/?t=settings&s=integrations)

2. **Register the service** (if not already running). Note the base URL will need to be adjusted with the user's handle.

   ```markdown
   register_user_service with:
   - label: file-share
   - protocol: http
   - local_port: 8765
   - entrypoint: bun run /home/workspace/Skills/file-share/scripts/server.ts
   - workdir: /home/workspace/Skills/file-share/scripts
   - env_vars: {"FILE_SHARE_BASE_URL": "https://file-share-<HANDLE>.zocomputer.io"}
   ```

# File Share

Share files from your workspace with email verification. Users request access, confirm their email, then receive a download link.

## Quick Start

1. **Add a file to share:**

   ```bash
   cd Skills/file-share/scripts
   bun cli.ts add-file /path/to/your/file.pdf "My Document"
   ```

2. **Share the public URL:** https://file-share-<HANDLE>.zocomputer.io

3. **Users visit the URL**, select a file, enter their email, and receive a confirmation link. After confirming, they get a download link.

## CLI Commands

Run from `Skills/file-share/scripts/`:

| Command | Description |
| --- | --- |
| `bun cli.ts list-files` | Show all registered files |
| `bun cli.ts list-users` | Show all users and confirmation status |
| `bun cli.ts add-file <path> [name]` | Register a file for sharing |
| `bun cli.ts remove-file <file_id>` | Remove a file from sharing |
| `bun cli.ts add-user <email> <file_id>` | Pre-register a user with file access |
| `bun cli.ts remove-user <user_id>` | Remove a user completely |
| `bun cli.ts revoke-access <user_id> <file_id>` | Revoke specific file access |
| `bun cli.ts confirm-user <user_id>` | Manually confirm a user |
| `bun cli.ts file-users <file_id>` | List users with access to a file |

## How It Works

1. **File Registration** - Use the CLI to register files from anywhere in your workspace
2. **Access Request** - Users visit the web UI, select a file, enter their email
3. **Email Confirmation** - A confirmation email is sent via Zo's email API
4. **Access Granted** - After clicking the confirmation link, a download link is emailed

## Service Configuration

The service runs at: **https://file-share-<HANDLE>.zocomputer.io**

To reconfigure or restart, update the service via Zo:

- Service ID: `svc_aa9ae5wB4ts`
- Port: 8765
- Entrypoint: `bun run /home/workspace/Skills/file-share/scripts/server.ts`

## Database

The database file `assets/file-share.db` is **not included** — it's created automatically on first run, or you can create it manually.

**Schema:**

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  confirmed INTEGER DEFAULT 0,
  confirmation_token TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  path TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  file_id INTEGER NOT NULL,
  access_token TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (file_id) REFERENCES files(id),
  UNIQUE(user_id, file_id)
);
```

**Tables:**

- `users` — email, confirmed status, confirmation token
- `files` — name, path to file in workspace
- `user_files` — links users to files with unique access tokens

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Web UI for requesting access |
| `/health` | GET | Health check |
| `/files` | GET | List available files (JSON) |
| `/request-access` | POST | Request file access `{email, file_id}` |
| `/confirm/:token` | GET | Confirm email |
| `/file/:file_id/:token` | GET | Download file (requires valid token) |
