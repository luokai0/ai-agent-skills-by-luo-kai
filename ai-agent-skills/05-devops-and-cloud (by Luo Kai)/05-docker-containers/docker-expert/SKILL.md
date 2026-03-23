---
author: luo-kai
name: docker-expert
description: Expert-level Docker and containerization. Use when writing Dockerfiles, docker-compose files, multi-stage builds, optimizing image size, container networking, volumes, secrets, health checks, or debugging container issues. Also use when the user mentions 'Dockerfile', 'docker-compose', 'container', 'image size', 'layer cache', 'registry', 'container wont start', or 'docker build'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Docker Expert

You are an expert in Docker and containerization with deep knowledge of container internals, image optimization, and production deployment patterns.

## Before Starting

1. **Language/runtime** — Node.js, Python, Go, Java, Rust?
2. **Use case** — development, production, CI/CD?
3. **Compose or single container?**
4. **Specific issue?** — image too large, build too slow, networking problem, container crashes?

---

## Core Expertise Areas

- **Dockerfile optimization**: layer caching order, multi-stage builds, .dockerignore, ARG vs ENV
- **Security**: non-root users, read-only filesystems, minimal base images, image scanning
- **docker-compose**: service dependencies, health checks, networks, profiles, override files
- **Networking**: bridge, host, overlay networks, DNS resolution between containers
- **Volumes**: named volumes, bind mounts, tmpfs, volume drivers
- **Production patterns**: resource limits, restart policies, init processes (tini/dumb-init)
- **Registry**: image tagging strategies, multi-arch builds with buildx, SBOM
- **Debugging**: exec, logs, inspect, events, stats, copying files out of containers

---

## Key Patterns & Code

### Optimized Multi-Stage Dockerfile — Node.js
```dockerfile
# ─── Stage 1: Install production dependencies ───────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app

# Copy ONLY package files first — layer cached until these change
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# ─── Stage 2: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ─── Stage 3: Production image (minimal) ─────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app

# Security: create non-root user
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 --ingroup nodejs appuser

# Copy only what is needed from previous stages
COPY --from=deps    --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/dist        ./dist
COPY --from=builder --chown=appuser:nodejs /app/package.json ./

USER appuser
EXPOSE 3000
ENV NODE_ENV=production PORT=3000

# Health check — orchestrators use this to know when app is ready
HEALTHCHECK \
  --interval=30s \
  --timeout=10s \
  --start-period=40s \
  --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

ENTRYPOINT ["node", "dist/server.js"]
```

### Optimized Multi-Stage Dockerfile — Python
```dockerfile
# ─── Stage 1: Build dependencies ─────────────────────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ─── Stage 2: Production image ───────────────────────────────────────────────
FROM python:3.12-slim AS runner
WORKDIR /app

# Non-root user
RUN useradd --system --uid 1001 --no-create-home appuser

# Copy installed packages from builder
COPY --from=builder /install /usr/local

COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Optimized Multi-Stage Dockerfile — Go
```dockerfile
# ─── Stage 1: Build ──────────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Download dependencies first (cached layer)
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build static binary — no external dependencies
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-w -s" \
    -o server ./cmd/server

# ─── Stage 2: Minimal production image ───────────────────────────────────────
# distroless: no shell, no package manager — smallest attack surface
FROM gcr.io/distroless/static-debian12 AS runner

COPY --from=builder /app/server /server

EXPOSE 8080
USER nonroot:nonroot

ENTRYPOINT ["/server"]
```

### .dockerignore — Always Create This
```
# Version control
.git
.gitignore

# Dependencies (always reinstalled in container)
node_modules
vendor
__pycache__
*.pyc
.venv
venv

# Build artifacts
dist
build
.next
out
target

# Test & coverage
coverage
*.test
.pytest_cache
__tests__

# Environment files — NEVER include these
.env
.env.*
*.env

# Logs
*.log
logs

# Editor
.vscode
.idea
*.swp
*.swo

# Docker files themselves
docker-compose*.yml
Dockerfile*

# Docs
README.md
CHANGELOG.md
docs
```

### docker-compose — Production Pattern
```yaml
version: "3.9"

services:
  api:
    build:
      context: .
      target: runner        # use specific build stage
      cache_from:
        - type=registry,ref=myregistry/myapp:cache
    image: myregistry/myapp:${TAG:-latest}
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
        reservations:
          memory: 256M
    read_only: true           # security: read-only filesystem
    tmpfs:
      - /tmp                  # writable temp dir
    networks:
      - app-net
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped
    networks:
      - app-net

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - app-net

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - app-net

volumes:
  pgdata:
    driver: local

networks:
  app-net:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### docker-compose Override for Development
```yaml
# docker-compose.override.yml — auto-loaded in development
version: "3.9"

services:
  api:
    build:
      target: builder       # use dev stage with devDependencies
    volumes:
      - .:/app              # bind mount source for hot reload
      - /app/node_modules   # anonymous volume to preserve container's node_modules
    environment:
      NODE_ENV: development
      DEBUG: "*"
    command: npm run dev    # override production command
    ports:
      - "9229:9229"         # Node.js debugger port

  db:
    ports:
      - "5432:5432"         # expose for local tools like pgAdmin

  cache:
    ports:
      - "6379:6379"         # expose for local Redis tools
```

### Networking Patterns
```bash
# Containers on same network communicate by service name
# api → db:5432 (service name = hostname)
# api → cache:6379

# Inspect container network
docker inspect mycontainer | jq '.[0].NetworkSettings.Networks'

# Connect running container to another network
docker network connect my-network my-container

# Create custom network with specific subnet
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  --ip-range 172.20.240.0/20 \
  my-custom-net

# List all networks
docker network ls

# Remove unused networks
docker network prune
```

### Debugging Commands
```bash
# Get interactive shell in running container
docker exec -it <container_name> sh

# Debug a stopped or crashing container
# Override entrypoint to get shell
docker run --rm -it --entrypoint sh myimage:latest

# Follow logs with timestamps
docker logs -f --timestamps --tail=100 <container_name>

# Copy files out of container for inspection
docker cp <container_name>:/app/logs/error.log ./error.log

# Real-time resource usage
docker stats --no-stream

# Inspect everything about a container
docker inspect <container_name>

# View image layers and sizes
docker history myimage:latest --human --no-trunc

# Check what changed in container filesystem vs image
docker diff <container_name>

# Scan image for vulnerabilities
docker scout cves myimage:latest

# Build with detailed output for debugging cache
docker build --progress=plain --no-cache .

# Check why container exited
docker inspect <container_name> | jq '.[0].State'
```

### Multi-Arch Build with Buildx
```bash
# Create and use a buildx builder
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap

# Build for multiple architectures and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myregistry/myapp:latest \
  --push \
  .

# Build with cache export to registry
docker buildx build \
  --cache-from type=registry,ref=myregistry/myapp:cache \
  --cache-to type=registry,ref=myregistry/myapp:cache,mode=max \
  --tag myregistry/myapp:latest \
  --push \
  .
```

### Health Check Patterns
```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# TCP health check (when no HTTP endpoint)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD nc -z localhost 5432 || exit 1

# Custom script health check
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh
HEALTHCHECK --interval=30s CMD /healthcheck.sh
```

---

## Best Practices

- Always use specific image tags — never `latest` in production (`node:20-alpine` not `node:latest`)
- Always create `.dockerignore` — dramatically speeds up builds and reduces context size
- Run as non-root user in every production container
- Use multi-stage builds — final image should contain only what is needed to run
- Set memory and CPU limits — prevent one container from starving others
- Add `HEALTHCHECK` to every production image
- Use `read_only: true` + `tmpfs` for `/tmp` — better security posture
- Never put secrets in `ENV` or `ARG` — use Docker secrets or secret mounts
- Pin base image digests for reproducibility in critical systems
- Use `dumb-init` or `tini` as PID 1 to handle signals properly

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No `.dockerignore` | Huge build context, slow builds, secrets leaked | Always create `.dockerignore` |
| Running as root | Security vulnerability | Add non-root user in Dockerfile |
| Copy source before package.json | Cache busted on every code change | Copy package.json first, then source |
| Secrets in `ENV` or `ARG` | Visible in `docker inspect` and image history | Use `--secret` mount or Docker secrets |
| No health check | Orchestrator cannot detect unhealthy app | Add `HEALTHCHECK` instruction |
| `latest` tag | Non-deterministic, impossible to rollback | Always pin exact version tags |
| One huge RUN command | Hard to debug layer failures | Split logical steps into separate RUN |
| No resource limits | One container can OOM the host | Always set memory limits in production |

---

## Related Skills

- **kubernetes-expert**: For orchestrating containers at scale
- **cicd-expert**: For Docker in CI/CD pipelines
- **nginx-expert**: For Nginx as a reverse proxy in containers
- **linux-expert**: For Linux container internals
- **aws-expert**: For ECR, ECS, and EKS on AWS
