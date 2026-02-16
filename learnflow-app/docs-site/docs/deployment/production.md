---
sidebar_position: 3
---

# Production Deployment

Production uses ArgoCD for GitOps-based continuous delivery.

## Initial Setup

```bash
bash scripts/setup-argocd.sh
bash scripts/setup-monitoring.sh
bash scripts/setup-external-secrets.sh
```

## Deploy

```bash
# Apply ArgoCD manifests
kubectl apply -f argocd/applications/production.yaml

# Sync
argocd app sync learnflow-production
```

## Promote Staging to Production

```bash
bash scripts/promote-to-production.sh
```

## Rollback

```bash
# Helm rollback
helm history learnflow-backend -n learnflow
helm rollback learnflow-backend <revision> -n learnflow

# ArgoCD rollback
argocd app history learnflow-production
argocd app rollback learnflow-production <id>

# Full rollback script
bash scripts/rollback.sh
```

## CI/CD Pipelines

| Pipeline | Trigger | Action |
|----------|---------|--------|
| `ci.yaml` | Push to any branch | Build, lint, test |
| `promote-production.yaml` | Manual | Promote staging image to production |
| `rollback.yaml` | Manual | Roll back to previous version |

## Monitoring

- Prometheus + Grafana installed via `setup-monitoring.sh`
- Each service exposes `/health` for Kubernetes probes
- Dapr provides built-in observability with tracing
