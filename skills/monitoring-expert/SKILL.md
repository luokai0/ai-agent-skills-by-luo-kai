---
name: monitoring-expert
description: Expert-level observability and monitoring. Use when setting up Prometheus, Grafana, Datadog, OpenTelemetry, distributed tracing, structured logging, alerting, SLOs/SLAs, or diagnosing production incidents. Also use when the user mentions 'Prometheus', 'Grafana', 'OpenTelemetry', 'distributed tracing', 'SLO', 'alerting', 'metrics', 'logs', 'traces', or 'production incident'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Observability & Monitoring Expert

You are an expert in observability and monitoring with deep knowledge of the three pillars (metrics, logs, traces), Prometheus, Grafana, OpenTelemetry, and SLO-based alerting.

## Before Starting

1. **Stack** — Prometheus/Grafana, Datadog, New Relic, CloudWatch?
2. **Environment** — Kubernetes, Docker, bare metal, serverless?
3. **Language** — Node.js, Python, Go, Java?
4. **Problem type** — setting up monitoring, writing alerts, debugging incident, SLO design?
5. **Scale** — single service or distributed microservices?

---

## Core Expertise Areas

- **Metrics**: Prometheus (counters, gauges, histograms, summaries), PromQL, recording rules
- **Logging**: structured logging (JSON), log levels, correlation IDs, ELK/Loki stack
- **Tracing**: OpenTelemetry SDK, distributed tracing, Jaeger, Tempo, trace context propagation
- **Alerting**: alerting rules, alert routing (Alertmanager), PagerDuty/Slack integration
- **Dashboards**: Grafana panels, variables, annotations, dashboard-as-code
- **SLOs**: SLI definition, error budget calculation, burn rate alerts
- **Incident response**: runbooks, postmortems, on-call practices
- **Kubernetes monitoring**: kube-state-metrics, node-exporter, cAdvisor

---

## Key Patterns & Code

### The Three Pillars of Observability
```
Metrics  → What is happening? (aggregated numbers over time)
Logs     → Why is it happening? (detailed event records)
Traces   → Where is it happening? (request flow across services)

Golden Signals (Google SRE):
  Latency   → How long do requests take?
  Traffic   → How much demand is there?
  Errors    → What is the error rate?
  Saturation → How full is the service?

RED Method (for services):
  Rate      → Requests per second
  Errors    → Error rate
  Duration  → Latency distribution

USE Method (for resources):
  Utilization  → How busy is the resource?
  Saturation   → How much extra work is queued?
  Errors       → Error rate of the resource
```

### Prometheus Metrics — Node.js
```javascript
import { Registry, Counter, Histogram, Gauge, collectDefaultMetrics } from 'prom-client';

const register = new Registry();

// Collect default Node.js metrics (CPU, memory, event loop lag)
collectDefaultMetrics({ register });

// Counter — only goes up (requests, errors, events)
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register],
});

// Histogram — distribution of values (latency, request size)
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [register],
});

// Gauge — can go up and down (active connections, queue size)
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
  registers: [register],
});

// Middleware to record metrics
export function metricsMiddleware(req, res, next) {
  const start = Date.now();
  const route = req.route?.path ?? req.path;

  activeConnections.inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const labels = {
      method: req.method,
      route,
      status_code: res.statusCode.toString(),
    };

    httpRequestsTotal.inc(labels);
    httpRequestDuration.observe(labels, duration);
    activeConnections.dec();
  });

  next();
}

// Expose /metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

### Prometheus Metrics — Python (FastAPI)
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Number of active requests'
)

@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    ACTIVE_REQUESTS.dec()
    return response

@app.get('/metrics')
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### PromQL — Essential Queries
```promql
# ── Request Rate ──────────────────────────────────────────────────────────────
# Requests per second over last 5 minutes
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m])) * 100

# ── Latency ───────────────────────────────────────────────────────────────────
# p50, p95, p99 latency
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# p99 latency per route
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route)
)

# ── Availability ──────────────────────────────────────────────────────────────
# Service availability (success rate)
sum(rate(http_requests_total{status_code!~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# ── Resource Usage ────────────────────────────────────────────────────────────
# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod)

# Memory usage by pod
sum(container_memory_working_set_bytes{container!=""}) by (pod)

# ── Kubernetes ────────────────────────────────────────────────────────────────
# Pods not running
kube_pod_status_phase{phase!="Running",phase!="Succeeded"} == 1

# Node CPU utilization
1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (node)

# Persistent volume usage
kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes * 100
```

### Prometheus Alerting Rules
```yaml
# /etc/prometheus/rules/api-alerts.yml
groups:
  - name: api
    interval: 30s
    rules:
      # ── Availability ────────────────────────────────────────────────────
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook: "https://wiki.example.com/runbooks/high-error-rate"

      # ── Latency ─────────────────────────────────────────────────────────
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1.0
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "High p99 latency on {{ $labels.service }}"
          description: "p99 latency is {{ $value | humanizeDuration }} (threshold: 1s)"

      # ── Availability ────────────────────────────────────────────────────
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
          page: "true"
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      # ── Kubernetes ──────────────────────────────────────────────────────
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"

      - alert: PodNotReady
        expr: kube_pod_status_ready{condition="true"} == 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} not ready"

      # ── Recording Rules (pre-compute expensive queries) ─────────────────
  - name: recording_rules
    rules:
      - record: job:http_requests_total:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      - record: job:http_errors_total:rate5m
        expr: sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (job)

      - record: job:http_request_duration_seconds:p99_5m
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
          )
```

### Alertmanager Configuration
```yaml
# /etc/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/xxx/yyy/zzz'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait:      30s   # wait before sending first notification
  group_interval:  5m    # wait before sending updated notification
  repeat_interval: 4h    # resend if still firing

  receiver: slack-warnings

  routes:
    # Critical alerts go to PagerDuty + Slack
    - match:
        severity: critical
      receiver: pagerduty-critical
      continue: true

    # Page-worthy alerts wake someone up
    - match:
        page: "true"
      receiver: pagerduty-critical

    # Team-specific routing
    - match:
        team: backend
      receiver: slack-backend

receivers:
  - name: slack-warnings
    slack_configs:
      - channel: '#alerts'
        title: '{{ template "slack.title" . }}'
        text: '{{ template "slack.text" . }}'
        send_resolved: true

  - name: slack-backend
    slack_configs:
      - channel: '#backend-alerts'
        send_resolved: true

  - name: pagerduty-critical
    pagerduty_configs:
      - service_key: 'your-pagerduty-integration-key'
        description: '{{ template "pagerduty.description" . }}'

inhibit_rules:
  # If service is down, suppress other alerts for that service
  - source_match:
      alertname: ServiceDown
    target_match_re:
      alertname: HighErrorRate|HighLatency
    equal: ['job']
```

### OpenTelemetry — Node.js Instrumentation
```javascript
// tracing.js — load BEFORE everything else
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'api',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.VERSION ?? '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV ?? 'production',
  }),

  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4318/v1/traces',
  }),

  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: 'http://otel-collector:4318/v1/metrics',
    }),
    exportIntervalMillis: 15000,
  }),

  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': { enabled: true },
      '@opentelemetry/instrumentation-express': { enabled: true },
      '@opentelemetry/instrumentation-pg': { enabled: true },
      '@opentelemetry/instrumentation-redis': { enabled: true },
    }),
  ],
});

sdk.start();

process.on('SIGTERM', () => sdk.shutdown());
```

### Structured Logging
```javascript
// logger.js — structured JSON logging with Pino
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: 'api',
    version: process.env.VERSION ?? '1.0.0',
    env: process.env.NODE_ENV ?? 'production',
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Request logger middleware
export function requestLogger(req, res, next) {
  const start = Date.now();
  const requestId = req.headers['x-request-id'] ?? crypto.randomUUID();

  req.log = logger.child({ requestId });
  res.setHeader('x-request-id', requestId);

  res.on('finish', () => {
    req.log.info({
      type: 'request',
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - start,
      userAgent: req.headers['user-agent'],
    }, 'Request completed');
  });

  next();
}

// Usage — always use structured fields not string interpolation
logger.info({ userId: user.id, action: 'login' }, 'User logged in');
logger.error({ err: error, userId: user.id }, 'Failed to process payment');

// Child logger for request context
const reqLogger = logger.child({ requestId, userId });
reqLogger.info({ orderId }, 'Order created');
```

### SLO Design & Error Budget
```
SLI (Service Level Indicator) — what to measure
  - Availability: % of successful requests
  - Latency: % of requests faster than threshold
  - Throughput: requests per second

SLO (Service Level Objective) — target
  - 99.9% of requests succeed (availability)
  - 99% of requests complete in < 200ms (latency)

Error Budget = 1 - SLO
  - 99.9% SLO = 0.1% error budget = 43.8 min/month downtime allowed

Burn Rate Alert — alert before budget is exhausted
  - 1x burn rate = consuming budget at exactly SLO rate
  - 2x burn rate = will exhaust budget in half the window
  - 14.4x burn rate = will exhaust monthly budget in 2 hours

Multi-window burn rate alerts (Google SRE recommendation):
  Fast burn (page now):  14.4x over 1h AND 14.4x over 5m
  Slow burn (ticket):    1x over 6h AND 1x over 30m
```
```yaml
# SLO-based alerting with Prometheus
groups:
  - name: slo_alerts
    rules:
      # Fast burn — page immediately (exhausts budget in 1 hour)
      - alert: SLOBurnRateFast
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > 14.4 * 0.001
          and
          (
            sum(rate(http_requests_total{status_code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 14.4 * 0.001
        labels:
          severity: critical
          page: "true"
        annotations:
          summary: "SLO fast burn — error budget will be exhausted in ~1 hour"

      # Slow burn — create ticket
      - alert: SLOBurnRateSlow
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[6h]))
            /
            sum(rate(http_requests_total[6h]))
          ) > 6 * 0.001
        labels:
          severity: warning
        annotations:
          summary: "SLO slow burn — investigate before budget is exhausted"
```

### Grafana Dashboard as Code
```json
{
  "dashboard": {
    "title": "API Overview",
    "tags": ["api", "production"],
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (status_code)",
            "legendFormat": "{{status_code}}"
          }
        ]
      },
      {
        "title": "p99 Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "title": "Error Rate %",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
          }
        ],
        "thresholds": {
          "steps": [
            {"value": 0, "color": "green"},
            {"value": 1, "color": "yellow"},
            {"value": 5, "color": "red"}
          ]
        }
      }
    ]
  }
}
```

---

## Best Practices

- Instrument everything from day one — retrofitting observability is painful
- Use structured logging (JSON) always — never unstructured strings
- Add correlation IDs (request ID, trace ID) to every log line
- Alert on symptoms (high error rate, slow latency) not causes (CPU high)
- Use multi-window burn rate alerts for SLOs — not simple threshold alerts
- Keep dashboards focused — one dashboard per service, not one giant dashboard
- Write runbooks for every alert — link from the alert annotation
- Use recording rules for expensive PromQL queries used in dashboards
- Test alerts regularly — a silent alert is worse than no alert

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Alerting on causes not symptoms | Too many noisy irrelevant alerts | Alert on error rate and latency, not CPU |
| No correlation IDs in logs | Cannot trace a request across services | Add request ID to every log line |
| High cardinality labels | Prometheus OOM from too many time series | Never use user ID or request ID as label |
| Alert fatigue | Too many alerts, team ignores them | Start with fewer high-quality alerts |
| No runbooks | On-call does not know what to do | Write runbook for every alert |
| Logging too much | Storage costs, hard to find signal | Log at INFO in prod, DEBUG only when needed |
| Unstructured log strings | Hard to query and filter | Always use structured JSON logging |
| Missing SLOs | No clear definition of good service | Define SLIs and SLOs for every service |

---

## Related Skills

- **kubernetes-expert**: For Kubernetes monitoring with Prometheus
- **docker-expert**: For containerized monitoring stack
- **cicd-expert**: For deployment tracking and alerting
- **linux-expert**: For host-level performance monitoring
- **aws-expert**: For CloudWatch and X-Ray
- **system-design**: For designing observable distributed systems
