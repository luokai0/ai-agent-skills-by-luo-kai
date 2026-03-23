---
author: luo-kai
name: nginx-expert
description: Expert-level Nginx configuration. Use when writing Nginx configs, setting up reverse proxies, load balancing, SSL/TLS termination, rate limiting, caching, virtual hosts, or debugging Nginx issues. Also use when the user mentions 'Nginx', 'server block', 'proxy_pass', 'upstream', 'rate limit', 'SSL certificate', 'Let's Encrypt', '502 bad gateway', or 'nginx.conf'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Nginx Expert

You are an expert in Nginx with deep knowledge of configuration, reverse proxying, load balancing, SSL/TLS, performance tuning, and security hardening.

## Before Starting

1. **Use case** — reverse proxy, load balancer, static file server, API gateway?
2. **SSL** — Let's Encrypt, custom cert, or no SSL?
3. **Backend** — Node.js, Python, Go, PHP, static files?
4. **Problem type** — writing config, debugging 502/504, performance, security?
5. **Environment** — bare metal, Docker, Kubernetes Ingress?

---

## Core Expertise Areas

- **Server blocks**: virtual hosts, default server, listen directives
- **Reverse proxy**: proxy_pass, proxy headers, WebSocket proxying
- **Load balancing**: round-robin, least_conn, ip_hash, weighted, health checks
- **SSL/TLS**: certificate config, HSTS, OCSP stapling, modern ciphers
- **Rate limiting**: limit_req_zone, limit_conn_zone, burst, nodelay
- **Caching**: proxy_cache, cache zones, cache bypass, stale cache
- **Security headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- **Performance**: gzip, brotli, keepalive, worker tuning, open file cache

---

## Key Patterns & Code

### nginx.conf — Global Settings
```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;          # one worker per CPU core
worker_rlimit_nofile 65535;     # max open files per worker
pid /run/nginx.pid;

events {
    worker_connections 4096;    # max connections per worker
    multi_accept on;            # accept multiple connections at once
    use epoll;                  # Linux epoll event model (most efficient)
}

http {
    # ── Basic Settings ────────────────────────────────────────────────────
    sendfile           on;      # efficient file sending
    tcp_nopush         on;      # send headers in one packet
    tcp_nodelay        on;      # disable Nagle for real-time
    keepalive_timeout  65;
    keepalive_requests 1000;
    types_hash_max_size 2048;
    server_tokens      off;     # hide Nginx version

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # ── Logging ───────────────────────────────────────────────────────────
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct=$upstream_connect_time '
                    'uht=$upstream_header_time urt=$upstream_response_time';

    access_log /var/log/nginx/access.log main buffer=16k flush=5s;
    error_log  /var/log/nginx/error.log warn;

    # ── Gzip Compression ──────────────────────────────────────────────────
    gzip               on;
    gzip_vary          on;
    gzip_proxied       any;
    gzip_comp_level    6;
    gzip_min_length    256;
    gzip_types
        text/plain text/css text/xml text/javascript
        application/json application/javascript application/xml
        application/rss+xml application/atom+xml
        image/svg+xml font/truetype font/opentype;

    # ── Rate Limiting Zones ───────────────────────────────────────────────
    limit_req_zone  $binary_remote_addr zone=api:10m    rate=10r/s;
    limit_req_zone  $binary_remote_addr zone=login:10m  rate=1r/s;
    limit_conn_zone $binary_remote_addr zone=conn:10m;

    # ── Proxy Cache Zone ──────────────────────────────────────────────────
    proxy_cache_path /var/cache/nginx
        levels=1:2
        keys_zone=api_cache:10m
        max_size=1g
        inactive=60m
        use_temp_path=off;

    # ── Include Virtual Hosts ─────────────────────────────────────────────
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### Reverse Proxy — Node.js / API
```nginx
# /etc/nginx/conf.d/api.conf

upstream api_backend {
    least_conn;                         # send to least busy server
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=1;
    server 127.0.0.1:3002 backup;      # only used if others are down
    keepalive 32;                       # keep connections to upstream alive
}

server {
    listen 80;
    server_name api.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # ── SSL ───────────────────────────────────────────────────────────────
    ssl_certificate     /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/api.example.com/chain.pem;

    ssl_protocols              TLSv1.2 TLSv1.3;
    ssl_ciphers                ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers  off;
    ssl_session_cache          shared:SSL:10m;
    ssl_session_timeout        1d;
    ssl_session_tickets        off;
    ssl_stapling               on;
    ssl_stapling_verify        on;
    resolver                   8.8.8.8 8.8.4.4 valid=300s;

    # ── Security Headers ──────────────────────────────────────────────────
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options           "SAMEORIGIN"    always;
    add_header X-Content-Type-Options    "nosniff"       always;
    add_header X-XSS-Protection          "1; mode=block" always;
    add_header Referrer-Policy           "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy        "camera=(), microphone=(), geolocation=()" always;
    add_header Content-Security-Policy   "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # ── Request Limits ────────────────────────────────────────────────────
    client_max_body_size  10m;
    client_body_timeout   30s;
    client_header_timeout 30s;

    # ── Rate Limiting ─────────────────────────────────────────────────────
    limit_req zone=api burst=20 nodelay;
    limit_conn conn 20;

    # ── Proxy Settings ────────────────────────────────────────────────────
    location / {
        proxy_pass         http://api_backend;
        proxy_http_version 1.1;

        # Required headers
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID      $request_id;

        # WebSocket support
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        # Timeouts
        proxy_connect_timeout  10s;
        proxy_send_timeout     30s;
        proxy_read_timeout     30s;

        # Buffering
        proxy_buffering    on;
        proxy_buffer_size  4k;
        proxy_buffers      8 4k;

        # Pass errors to client
        proxy_intercept_errors off;
    }

    # ── Health check endpoint — no rate limit, no logging ─────────────────
    location /health {
        proxy_pass http://api_backend;
        access_log off;
        limit_req  off;
    }

    # ── Block common attack paths ──────────────────────────────────────────
    location ~* \.(?:git|env|htaccess|htpasswd)$ {
        deny all;
        return 404;
    }
}

# WebSocket upgrade map
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
```

### Static Site with SPA Support
```nginx
server {
    listen 443 ssl http2;
    server_name app.example.com;

    ssl_certificate     /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;

    root  /var/www/app/dist;
    index index.html;

    # ── Aggressive caching for hashed assets ──────────────────────────────
    location ~* \.(?:js|css|woff2?|ttf|eot|svg|png|jpg|jpeg|gif|ico|webp|avif)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # ── No cache for HTML — always fresh ──────────────────────────────────
    location ~* \.html$ {
        expires -1;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # ── SPA routing — serve index.html for all routes ─────────────────────
    location / {
        try_files $uri $uri/ /index.html;
    }

    # ── API proxy ─────────────────────────────────────────────────────────
    location /api/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header Host            $host;
        proxy_set_header X-Real-IP       $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }
}
```

### Rate Limiting — Login Endpoint
```nginx
# Strict rate limiting for auth endpoints
location /api/auth/login {
    limit_req zone=login burst=5 nodelay;
    limit_req_status 429;

    proxy_pass http://api_backend;
    proxy_set_header Host            $host;
    proxy_set_header X-Real-IP       $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # Custom 429 response
    error_page 429 @rate_limited;
}

location @rate_limited {
    default_type application/json;
    add_header Retry-After 60 always;
    return 429 '{"error":"Too many requests","retryAfter":60}';
}
```

### Proxy Caching
```nginx
location /api/products {
    proxy_pass         http://api_backend;
    proxy_cache        api_cache;
    proxy_cache_key    "$scheme$host$request_uri$http_authorization";
    proxy_cache_valid  200 5m;      # cache 200 responses for 5 minutes
    proxy_cache_valid  404 1m;      # cache 404 for 1 minute
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503;
    proxy_cache_lock   on;          # prevent cache stampede

    add_header X-Cache-Status $upstream_cache_status;

    # Bypass cache for authenticated requests
    proxy_cache_bypass $http_authorization;
    proxy_no_cache     $http_authorization;
}
```

### Load Balancing Strategies
```nginx
# Round-robin (default)
upstream backend_round_robin {
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    server 10.0.0.3:3000;
}

# Least connections — best for long-lived connections
upstream backend_least_conn {
    least_conn;
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    server 10.0.0.3:3000;
}

# IP hash — sticky sessions (same client → same server)
upstream backend_sticky {
    ip_hash;
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
}

# Weighted — send more traffic to powerful servers
upstream backend_weighted {
    server 10.0.0.1:3000 weight=5;  # gets 5/7 of traffic
    server 10.0.0.2:3000 weight=2;  # gets 2/7 of traffic
}

# With health checks (Nginx Plus feature, or use upstream_check module)
upstream backend_health {
    server 10.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:3000 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:3000 backup;
}
```

### Let's Encrypt with Certbot
```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Get certificate (Nginx plugin — auto-configures nginx)
certbot --nginx -d example.com -d www.example.com

# Standalone (when nginx is not running)
certbot certonly --standalone -d example.com

# Wildcard certificate (requires DNS challenge)
certbot certonly --manual --preferred-challenges dns   -d "*.example.com" -d "example.com"

# Test auto-renewal
certbot renew --dry-run

# Auto-renewal is handled by systemd timer or cron
# Check it exists:
systemctl status certbot.timer
cat /etc/cron.d/certbot
```

### Debugging Common Issues
```bash
# Test config syntax
nginx -t
nginx -T  # test and print full config

# Reload without downtime
nginx -s reload
systemctl reload nginx

# Check error logs
tail -f /var/log/nginx/error.log
journalctl -u nginx -f

# Debug specific request
# Add to location block temporarily:
# add_header X-Debug-URI $uri;
# add_header X-Debug-Upstream $upstream_addr;

# Check what nginx is listening on
ss -tlnp | grep nginx

# Check open file count
cat /proc/$(pgrep nginx | head -1)/limits | grep "open files"

# Common error meanings:
# 502 Bad Gateway     → upstream is down or not accepting connections
# 504 Gateway Timeout → upstream is too slow (increase proxy_read_timeout)
# 499 Client Closed   → client disconnected before response
# 413 Too Large       → increase client_max_body_size

# Check upstream connectivity
curl -v http://127.0.0.1:3000/health

# Check if port is listening
ss -tlnp | grep :3000
```

### Docker Nginx Config
```nginx
# nginx.conf for Docker — no daemon mode
daemon off;
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    server_tokens off;

    upstream app {
        server app:3000;  # Docker service name as hostname
    }

    server {
        listen 80;

        location / {
            proxy_pass         http://app;
            proxy_http_version 1.1;
            proxy_set_header   Host              $host;
            proxy_set_header   X-Real-IP         $remote_addr;
            proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://app;
            access_log off;
        }
    }
}
```

---

## Best Practices

- Always run `nginx -t` before reloading to catch config errors
- Use `server_tokens off` to hide Nginx version from attackers
- Set `client_max_body_size` explicitly — default is 1MB which is too small for file uploads
- Use `proxy_set_header X-Forwarded-For` so app sees real client IP
- Always set timeouts — proxy_connect_timeout, proxy_send_timeout, proxy_read_timeout
- Use `keepalive` on upstream blocks for connection reuse
- Set `worker_processes auto` to use all CPU cores
- Use `access_log off` on health check and static asset endpoints
- Always redirect HTTP to HTTPS — never serve on port 80 in production

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No `nginx -t` before reload | Bad config takes down Nginx | Always test before reload |
| Wrong upstream address in Docker | Cannot connect to backend | Use service name not localhost |
| Missing X-Forwarded-For header | App sees Nginx IP not client IP | Add proxy_set_header X-Forwarded-For |
| No timeout settings | Requests hang forever | Always set proxy timeouts |
| client_max_body_size too small | 413 errors on file uploads | Increase to match your max upload |
| HTTP not redirecting to HTTPS | Mixed content or insecure traffic | Add 301 redirect from port 80 |
| No rate limiting | DDoS / brute force possible | Add limit_req_zone on public endpoints |
| Caching authenticated responses | User A sees User B data | Add proxy_cache_bypass on auth headers |

---

## Related Skills

- **linux-expert**: For Linux server setup and management
- **docker-expert**: For Nginx in containers
- **kubernetes-expert**: For Nginx Ingress Controller
- **appsec-expert**: For security headers and hardening
- **webperf-expert**: For caching and compression optimization
- **cicd-expert**: For automated Nginx config deployment
