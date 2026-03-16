---
name: cicd-expert
description: Expert-level CI/CD pipeline development. Use when building GitHub Actions, GitLab CI, Jenkins, CircleCI, or ArgoCD pipelines, implementing automated testing, deployment strategies (blue/green, canary), or release automation. Also use when the user mentions 'GitHub Actions', 'pipeline', 'CI/CD', 'deployment strategy', 'blue-green', 'canary', 'rollback', 'automated testing', or 'release automation'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# CI/CD Expert

You are an expert in CI/CD pipelines and DevOps automation with deep knowledge of GitHub Actions, GitLab CI, deployment strategies, and release engineering.

## Before Starting

1. **Platform** — GitHub Actions, GitLab CI, Jenkins, CircleCI?
2. **Deployment target** — Kubernetes, ECS, EC2, serverless, static?
3. **Language/framework** — Node.js, Python, Go, Java?
4. **Deployment strategy** — rolling, blue/green, canary?
5. **Problem type** — writing pipeline, speeding up builds, deployment issues?

---

## Core Expertise Areas

- **GitHub Actions**: workflows, jobs, steps, matrices, reusable workflows, composite actions
- **GitLab CI**: stages, jobs, artifacts, cache, environments, rules
- **Docker in CI**: layer caching, multi-stage builds, registry push, image scanning
- **Testing**: unit, integration, e2e in CI, test parallelism, flaky test handling
- **Deployment strategies**: rolling, blue/green, canary, feature flags
- **Release automation**: semantic versioning, changelogs, GitHub releases, tagging
- **Secrets management**: GitHub secrets, OIDC auth, vault integration
- **Observability**: pipeline metrics, deployment tracking, rollback triggers

---

## Key Patterns & Code

### GitHub Actions — Full CI/CD Pipeline
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true  # cancel older runs on same branch

env:
  NODE_VERSION: "20"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ── Job 1: Lint & Type Check ──────────────────────────────────────────────
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: npm

      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  # ── Job 2: Unit Tests ─────────────────────────────────────────────────────
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: npm

      - run: npm ci
      - run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  # ── Job 3: Build & Push Docker Image ─────────────────────────────────────
  build:
    name: Build & Push Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix=sha-

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  # ── Job 4: Deploy to Staging ──────────────────────────────────────────────
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC — no static keys)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsStaging
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster staging \
            --service api \
            --force-new-deployment \
            --region us-east-1

  # ── Job 5: Deploy to Production ───────────────────────────────────────────
  deploy-prod:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'release'
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsProduction
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service api \
            --force-new-deployment
```

### Reusable Workflow
```yaml
# .github/workflows/deploy.yml — reusable workflow
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      aws-role-arn:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.aws-role-arn }}
          aws-region: us-east-1

      - name: Deploy
        run: |
          echo "Deploying ${{ inputs.image-tag }} to ${{ inputs.environment }}"
          aws ecs update-service --cluster ${{ inputs.environment }} --service api --force-new-deployment

# Calling the reusable workflow
# .github/workflows/main.yml
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
    secrets:
      aws-role-arn: ${{ secrets.STAGING_AWS_ROLE_ARN }}
```

### Matrix Testing
```yaml
jobs:
  test:
    name: Test (Node ${{ matrix.node }}, OS ${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # run all combinations even if one fails
      matrix:
        node: ["18", "20", "22"]
        os: [ubuntu-latest, windows-latest, macos-latest]
        exclude:
          - os: windows-latest
            node: "18"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

### Caching Strategies
```yaml
# Node.js — cache node_modules
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: npm  # built-in npm cache

# Python — cache pip packages
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip

# Go — cache Go modules
- uses: actions/setup-go@v5
  with:
    go-version: "1.22"
    cache: true

# Custom cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
      .next/cache
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Docker layer cache via GitHub Actions Cache
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Blue/Green Deployment on ECS
```bash
#!/bin/bash
# blue-green-deploy.sh

set -euo pipefail

CLUSTER="production"
SERVICE="api"
NEW_IMAGE="$1"
REGION="us-east-1"

echo "Starting blue/green deployment..."

# Get current task definition
TASK_DEF=$(aws ecs describe-services   --cluster $CLUSTER   --services $SERVICE   --query 'services[0].taskDefinition'   --output text)

# Register new task definition with updated image
NEW_TASK_DEF=$(aws ecs describe-task-definition   --task-definition $TASK_DEF   --query 'taskDefinition' |   jq --arg IMAGE "$NEW_IMAGE"   '.containerDefinitions[0].image = $IMAGE |
   del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)')

NEW_TASK_ARN=$(aws ecs register-task-definition   --cli-input-json "$NEW_TASK_DEF"   --query 'taskDefinition.taskDefinitionArn'   --output text)

echo "New task definition: $NEW_TASK_ARN"

# Update service with new task definition
aws ecs update-service   --cluster $CLUSTER   --service $SERVICE   --task-definition $NEW_TASK_ARN   --region $REGION

# Wait for deployment to complete
echo "Waiting for deployment to stabilize..."
aws ecs wait services-stable   --cluster $CLUSTER   --services $SERVICE   --region $REGION

echo "Deployment complete!"

# Verify health
RUNNING=$(aws ecs describe-services   --cluster $CLUSTER   --services $SERVICE   --query 'services[0].runningCount'   --output text)

echo "Running tasks: $RUNNING"
```

### Canary Deployment with Kubernetes
```yaml
# canary-deploy.yml GitHub Action step
- name: Canary Deploy
  run: |
    # Deploy canary with 10% traffic
    kubectl set image deployment/api-canary       api=${{ env.IMAGE }}:${{ github.sha }}

    kubectl scale deployment/api-canary --replicas=1

    # Wait and check error rate
    sleep 300  # 5 minutes

    ERROR_RATE=$(kubectl exec -it prometheus-0 --       promtool query instant       'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])'       | grep -oP '\d+\.\d+')

    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate $ERROR_RATE exceeds threshold, rolling back"
      kubectl rollout undo deployment/api-canary
      exit 1
    fi

    # Promote to full rollout
    kubectl set image deployment/api       api=${{ env.IMAGE }}:${{ github.sha }}
    kubectl rollout status deployment/api
```

### Semantic Release Automation
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # full history for semantic-release

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm

      - run: npm ci

      - name: Semantic Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```
```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): v${nextRelease.version} [skip ci]"
    }]
  ]
}
```

### GitLab CI Pipeline
```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

default:
  image: node:20-alpine
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths:
      - node_modules/

lint:
  stage: lint
  script:
    - npm ci
    - npm run lint
    - npm run typecheck

test:
  stage: test
  script:
    - npm ci
    - npm run test:coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/api api=$IMAGE_TAG
  only:
    - develop

deploy-prod:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - kubectl set image deployment/api api=$IMAGE_TAG
  when: manual  # requires manual approval
  only:
    - main
```

### Branch Protection & Required Checks
```yaml
# Enforce these in GitHub repository settings:
# Settings > Branches > Branch protection rules

Required status checks:
  - lint
  - test
  - build

Required reviews: 1
Dismiss stale reviews: true
Require up-to-date branches: true
Restrict pushes: only CI service account
```

---

## Best Practices

- Use OIDC for cloud authentication — never store static cloud credentials as secrets
- Cache dependencies aggressively — biggest CI speedup available
- Use concurrency groups to cancel redundant runs on the same branch
- Pin action versions to full SHA — not just tag (e.g. actions/checkout@v4 is fine, but SHA is safer)
- Run lint and typecheck before tests — fail fast on cheap checks first
- Use environments with protection rules for staging and production deployments
- Store test results and coverage as artifacts for visibility
- Use matrix builds to test across multiple versions and platforms
- Never auto-deploy to production on push — require a release event or manual approval

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Static cloud credentials in secrets | Credentials can leak or expire | Use OIDC role assumption instead |
| No dependency caching | Slow builds (npm install every time) | Cache node_modules/pip/go modules |
| Deploying on every push to main | Accidental production deploys | Deploy only on release events or manual trigger |
| No concurrency control | Parallel runs on same branch cause conflicts | Add concurrency group with cancel-in-progress |
| Pinning actions to tags only | Tag can be moved to malicious commit | Pin to full commit SHA for security |
| No rollback strategy | Bad deploy = manual intervention | Always have automated rollback on health check failure |
| Ignoring flaky tests | False failures erode CI trust | Track and fix flaky tests immediately |
| Long sequential pipelines | Slow feedback loop | Parallelize independent jobs |

---

## Related Skills

- **docker-expert**: For building and pushing container images
- **kubernetes-expert**: For deploying to Kubernetes clusters
- **aws-expert**: For AWS CodePipeline and ECS deployments
- **terraform-expert**: For infrastructure changes in CI/CD
- **monitoring-expert**: For deployment health tracking
- **git-expert**: For branching strategies and conventional commits
