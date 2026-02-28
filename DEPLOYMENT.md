# Deployment Guide

## Overview

The project uses GitLab CI/CD to build a Docker image and deploy it to Kubernetes via Helm.

```
Pipeline: lint → test → build → deploy
Environments: dev (auto) · staging (auto on main) · production (manual)
```

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| GitLab with Container Registry | 16.x |
| GitLab Runner (Docker executor) | 16.x |
| Kubernetes cluster | 1.28+ |
| Helm | 3.14+ |
| cert-manager (optional, for TLS) | 1.14+ |
| NGINX Ingress Controller | 1.10+ |

---

## 1. GitLab CI/CD Variables

Set the following variables under **Settings → CI/CD → Variables** in GitLab.

### Required for all environments

| Variable | Description | Masked |
|----------|-------------|--------|
| `KUBE_CONFIG` | Base64-encoded kubeconfig file (`base64 -w0 ~/.kube/config`) | Yes |
| `DATABASE_URL` | Full async DSN, e.g. `postgresql+asyncpg://user:pass@host/db` | Yes |
| `SECRET_KEY` | JWT/session signing secret (generate with `openssl rand -hex 32`) | Yes |
| `AWS_ACCESS_KEY_ID` | AWS IAM key for S3 access | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret | Yes |
| `AWS_BUCKET_NAME` | S3 bucket name for file storage | No |
| `AWS_REGION` | AWS region, e.g. `us-east-1` | No |
| `SMS_API_KEY` | Mobizon API key for SMS | Yes |

### Per-environment overrides

GitLab supports environment-scoped variables. Create separate values for each
environment (`dev`, `staging`, `production`) by setting the **Environment** scope
on the variable.

For example, set `DATABASE_URL` three times, each scoped to a different
environment, pointing to the respective database.

---

## 2. Kubernetes Setup

### Create namespaces

```bash
kubectl create namespace dev
kubectl create namespace staging
kubectl create namespace production
```

### Create an ImagePullSecret (if the registry is private)

```bash
kubectl create secret docker-registry gitlab-registry \
  --docker-server=registry.gitlab.com \
  --docker-username=<gitlab-deploy-token-user> \
  --docker-password=<gitlab-deploy-token> \
  --namespace dev

# Repeat for staging and production namespaces.
```

Add `imagePullSecrets` to the Helm values if needed:

```yaml
imagePullSecrets:
  - name: gitlab-registry
```

### Encode and store the kubeconfig

```bash
base64 -w0 ~/.kube/config
# Paste the output as the KUBE_CONFIG CI variable.
```

---

## 3. Helm Chart

Chart location: `helm/sofa-server/`

### Values files

| File | Used by |
|------|---------|
| `values.yaml` | Defaults / dev baseline |
| `values-staging.yaml` | Staging overrides |
| `values-production.yaml` | Production overrides |

### Manual deploy (outside CI)

```bash
# Dev
helm upgrade --install sofa-server helm/sofa-server \
  --namespace dev \
  --set image.repository=registry.gitlab.com/<group>/sofa_server \
  --set image.tag=<sha> \
  --set migration.run=true \
  --set secret.DATABASE_URL="postgresql+asyncpg://..." \
  --set secret.SECRET_KEY="..." \
  --wait

# Staging
helm upgrade --install sofa-server helm/sofa-server \
  --namespace staging \
  --values helm/sofa-server/values-staging.yaml \
  --set image.tag=<sha> \
  --set migration.run=true \
  ...

# Production
helm upgrade --install sofa-server helm/sofa-server \
  --namespace production \
  --values helm/sofa-server/values-production.yaml \
  --set image.tag=<sha> \
  --set migration.run=true \
  ...
```

### Rollback

```bash
helm rollback sofa-server --namespace production
```

---

## 4. Pipeline Stages

### lint

- `lint:ruff` — runs `ruff check` and `ruff format --check` on `src/`.
- `lint:mypy` — type-checks the codebase.

Runs on every branch and every merge request.

### test

- `test:pytest` — runs the full test suite.
- GitLab **services** spin up PostgreSQL 16, Redis 7, and Elasticsearch 8 as
  sidecar containers. No Docker-in-Docker is required for tests.

### build

- Builds the Docker image using Docker-in-Docker (`docker:27-dind`).
- Pushes two tags to the GitLab Container Registry:
  - `registry.gitlab.com/<group>/sofa_server:<commit-sha>` (immutable)
  - `registry.gitlab.com/<group>/sofa_server:latest`
- Runs only on `dev` and `main` branches.

### deploy

| Job | Branch | Trigger | Namespace |
|-----|--------|---------|-----------|
| `deploy:dev` | `dev` | Automatic | `dev` |
| `deploy:staging` | `main` | Automatic | `staging` |
| `deploy:production` | `main` | **Manual** | `production` |

Each deploy job:
1. Decodes `KUBE_CONFIG` and configures `kubectl`.
2. Runs `helm upgrade --install` with `--set migration.run=true`, which
   triggers the pre-install/pre-upgrade Helm hook that runs
   `alembic upgrade head` as a Kubernetes Job before the new pods start.
3. Uses `--wait --timeout` so the job fails if pods do not become ready.

---

## 5. Database Migrations

Migrations are run automatically as a Kubernetes `Job` (Helm hook) before every
deploy. The job uses the same Docker image as the application and runs:

```bash
alembic upgrade head
```

The Job is annotated with `helm.sh/hook-delete-policy: hook-succeeded` so it is
cleaned up automatically after a successful run.

To skip migrations in a deploy:

```bash
helm upgrade --install sofa-server helm/sofa-server \
  --set migration.run=false \
  ...
```

---

## 6. Updating Hostnames

Replace placeholder hostnames in the values files with real ones:

| File | Variable | Placeholder |
|------|----------|-------------|
| `values.yaml` | `ingress.host` | `api.example.com` |
| `values-staging.yaml` | `ingress.host` | `staging-api.example.com` |
| `values-production.yaml` | `ingress.host` | `api.example.com` |

Also replace `registry.gitlab.com/your-group/sofa_server` in `values.yaml`
with the actual GitLab Container Registry path for the project.
