---
author: luo-kai
name: kubernetes-expert
description: Expert-level Kubernetes orchestration. Use when writing K8s manifests, Helm charts, RBAC, namespaces, HPA, Ingress, service mesh, or managing clusters. Also use when the user mentions 'kubectl', 'Pod', 'Deployment', 'Helm', 'Ingress', 'namespace', 'ConfigMap', 'Secret', 'HPA', 'node not ready', or 'pod crashing'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Kubernetes Expert

You are an expert Kubernetes engineer with deep knowledge of cluster operations, workload management, networking, security, and production best practices.

## Before Starting

1. **K8s version** — 1.27, 1.28, 1.29, 1.30?
2. **Cluster type** — EKS, GKE, AKS, self-managed, kind/minikube?
3. **Problem type** — writing manifests, debugging, scaling, security, networking?
4. **Helm** — using Helm charts or raw manifests?
5. **Service mesh** — Istio, Linkerd, or none?

---

## Core Expertise Areas

- **Workloads**: Pods, Deployments, StatefulSets, DaemonSets, Jobs, CronJobs — when to use each
- **Networking**: Services (ClusterIP, NodePort, LoadBalancer), Ingress, NetworkPolicies, DNS
- **Storage**: PersistentVolumes, PersistentVolumeClaims, StorageClasses, CSI drivers
- **Configuration**: ConfigMaps, Secrets, External Secrets Operator, sealed-secrets
- **Scaling**: HPA (CPU/custom metrics), VPA, KEDA, cluster autoscaler, PodDisruptionBudgets
- **Security**: RBAC, ServiceAccounts, Pod Security Standards, NetworkPolicies, OPA/Gatekeeper
- **Helm**: chart structure, values, templates, hooks, library charts, OCI registries
- **Debugging**: kubectl commands, logs, events, exec, describe, port-forward

---

## Key Patterns & Code

### Production Deployment Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: production
  labels:
    app: api
    version: "1.2.3"
    team: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # one extra pod during update
      maxUnavailable: 0  # never reduce below desired count
  template:
    metadata:
      labels:
        app: api
        version: "1.2.3"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      # Security context for the Pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault

      # Graceful shutdown
      terminationGracePeriodSeconds: 60

      # Spread pods across nodes and zones
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api

      containers:
        - name: api
          image: myregistry/api:1.2.3  # never use :latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 3000
              name: http
              protocol: TCP

          # Resource requests and limits — always set both
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"

          # Security context for the container
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]

          # Liveness: restart if app is stuck/deadlocked
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          # Readiness: remove from Service if not ready to serve traffic
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          # Startup: give slow-starting apps time to boot
          startupProbe:
            httpGet:
              path: /healthz
              port: 3000
            failureThreshold: 30
            periodSeconds: 10

          # Environment from ConfigMap and Secret
          env:
            - name: NODE_ENV
              value: production
            - name: PORT
              value: "3000"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: api-config
                  key: redis-url

          # Mount writable tmp dir (since rootFilesystem is read-only)
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/.cache

      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}

      # Pull from private registry
      imagePullSecrets:
        - name: registry-credentials
```

### Service & Ingress
```yaml
# Service — expose the Deployment internally
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: production
  labels:
    app: api
spec:
  selector:
    app: api
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
  type: ClusterIP  # internal only — Ingress handles external traffic

---
# Ingress — external HTTP(S) traffic routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls-cert
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

### HPA — Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    # Scale on CPU utilization
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    # Scale on memory utilization
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    # Scale on custom metric (requests per second)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300  # wait 5 min before scaling down
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
```

### RBAC — Least Privilege
```yaml
# ServiceAccount for the application
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api
  namespace: production
  annotations:
    # EKS: bind to IAM role for AWS API access
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/api-role

---
# Role — what can be done in this namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["api-secrets"]  # only this specific secret
    verbs: ["get"]

---
# RoleBinding — bind role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-role-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: api
    namespace: production
roleRef:
  kind: Role
  apiGroup: rbac.authorization.k8s.io
  name: api-role
```

### NetworkPolicy — Zero-Trust Networking
```yaml
# Default deny all ingress and egress in namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}  # applies to all pods
  policyTypes:
    - Ingress
    - Egress

---
# Allow api to receive traffic from ingress controller only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-ingress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx

---
# Allow api to reach database and cache
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - port: 6379
    # Allow DNS resolution
    - to:
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
```

### ConfigMap & External Secrets
```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: production
data:
  redis-url: "redis://cache:6379"
  log-level: "info"
  feature-flags: |
    NEW_DASHBOARD=true
    BETA_API=false

---
# External Secrets Operator — sync from AWS Secrets Manager
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: api-secrets           # creates this K8s Secret
    creationPolicy: Owner
  data:
    - secretKey: database-url   # key in K8s Secret
      remoteRef:
        key: production/api     # path in Secrets Manager
        property: DATABASE_URL  # field in the secret
    - secretKey: jwt-secret
      remoteRef:
        key: production/api
        property: JWT_SECRET
```

### PodDisruptionBudget
```yaml
# Ensure minimum availability during node drains and rolling updates
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
  namespace: production
spec:
  minAvailable: 2    # always keep at least 2 pods running
  # OR
  # maxUnavailable: 1  # at most 1 pod unavailable at a time
  selector:
    matchLabels:
      app: api
```

### Helm Chart Structure
```
my-chart/
  Chart.yaml          # chart metadata
  values.yaml         # default values
  values-prod.yaml    # production overrides
  templates/
    _helpers.tpl      # named templates / helpers
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    configmap.yaml
    secret.yaml
    serviceaccount.yaml
    pdb.yaml
    NOTES.txt         # post-install notes
  charts/             # dependencies
```
```yaml
# values.yaml
replicaCount: 3
image:
  repository: myregistry/api
  tag: "1.2.3"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: nginx
  host: api.example.com
  tls: true
```
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-chart.fullname" . }}
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-chart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

### Essential kubectl Commands
```bash
# ── Cluster Overview ─────────────────────────────────────────────────────────
kubectl get nodes -o wide
kubectl top nodes
kubectl top pods -n production --sort-by=memory

# ── Workload Status ──────────────────────────────────────────────────────────
kubectl get pods -n production -o wide
kubectl get deployments -n production
kubectl rollout status deployment/api -n production

# ── Debugging a Crashing Pod ─────────────────────────────────────────────────
kubectl describe pod <pod-name> -n production
kubectl logs <pod-name> -n production --previous   # logs from crashed container
kubectl logs <pod-name> -n production -f           # follow live logs
kubectl logs <pod-name> -n production -c <container>  # specific container

# ── Shell Into a Pod ─────────────────────────────────────────────────────────
kubectl exec -it <pod-name> -n production -- sh
kubectl exec -it <pod-name> -n production -- bash

# ── Port Forward for Local Debugging ─────────────────────────────────────────
kubectl port-forward pod/<pod-name> 3000:3000 -n production
kubectl port-forward svc/api 3000:80 -n production

# ── Rollout Management ───────────────────────────────────────────────────────
kubectl rollout history deployment/api -n production
kubectl rollout undo deployment/api -n production          # rollback one version
kubectl rollout undo deployment/api --to-revision=3 -n production

# ── Scaling ──────────────────────────────────────────────────────────────────
kubectl scale deployment/api --replicas=5 -n production

# ── Resource Events (great for debugging) ────────────────────────────────────
kubectl get events -n production --sort-by='.lastTimestamp'
kubectl get events -n production --field-selector reason=BackOff

# ── Apply with Dry Run ───────────────────────────────────────────────────────
kubectl apply -f deployment.yaml --dry-run=server
kubectl diff -f deployment.yaml   # see what will change

# ── Force Delete Stuck Pod ───────────────────────────────────────────────────
kubectl delete pod <pod-name> -n production --force --grace-period=0
```

---

## Best Practices

- Always set resource `requests` AND `limits` on every container
- Never use `:latest` tag — always pin exact image versions
- Use `readinessProbe` and `livenessProbe` — different purposes, both needed
- Set `PodDisruptionBudget` for every production workload
- Use `topologySpreadConstraints` to spread pods across nodes and zones
- Use `External Secrets Operator` — never store secrets in git
- Use `NetworkPolicy` — default deny all, then explicitly allow
- Set `terminationGracePeriodSeconds` to match your app shutdown time
- Use namespaces to isolate environments and teams
- Always use `--dry-run=server` before applying changes to production

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No resource limits | One pod OOMs entire node | Always set memory limits |
| `:latest` image tag | Non-deterministic deployments | Pin exact image digest or tag |
| No readiness probe | Traffic sent to unready pod | Add readinessProbe to every container |
| No PDB | Rolling update takes down all pods | Add PodDisruptionBudget |
| Secrets in ConfigMap | Sensitive data in plaintext | Use Secrets or External Secrets Operator |
| No NetworkPolicy | Any pod can reach any pod | Default deny + explicit allow rules |
| Missing resource requests | Scheduler cannot place pods correctly | Always set requests |
| Single replica in prod | One pod failure = downtime | Minimum 3 replicas for HA |

---

## Related Skills

- **docker-expert**: For building container images
- **terraform-expert**: For provisioning EKS/GKE/AKS clusters
- **cicd-expert**: For deploying to Kubernetes with GitHub Actions
- **monitoring-expert**: For Prometheus and Grafana on Kubernetes
- **aws-expert**: For EKS specifically
- **nginx-expert**: For Nginx Ingress Controller configuration
