# LearnFlow Deployment Runbook

## Table of Contents

1. [Local Development](#local-development)
2. [Staging Deployment](#staging-deployment)
3. [Production Deployment](#production-deployment)
4. [Rollback Procedures](#rollback-procedures)
5. [Scaling](#scaling)
6. [Disaster Recovery](#disaster-recovery)
7. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Docker Desktop running
- `.env` file created from `.env.example` with valid `OPENAI_API_KEY`

### Start all services

```bash
cd learnflow-app
docker compose up -d
```

### Verify

```bash
# Check all containers are running
docker compose ps

# Test health endpoints
curl http://localhost:8001/api/v1/health  # triage
curl http://localhost:8002/api/v1/health  # concepts
curl http://localhost:8003/api/v1/health  # code-runner
curl http://localhost:8006/api/v1/health  # progress

# Frontend
open http://localhost:3000
```

### Stop

```bash
docker compose down          # stop containers
docker compose down -v       # stop + remove volumes (resets DB)
```

---

## Staging Deployment

### Prerequisites

- Minikube running: `minikube start --cpus=4 --memory=8192`
- Dapr installed: `dapr init -k`
- Helm repos added

### Deploy infrastructure

```bash
# PostgreSQL
helm install postgres bitnami/postgresql \
  -f infrastructure/postgres/values.yaml \
  -n learnflow --create-namespace

# Kafka
helm install kafka bitnami/kafka \
  -f infrastructure/kafka/values.yaml \
  -n kafka --create-namespace

# Dapr components
kubectl apply -f infrastructure/dapr/components/ -n learnflow

# Kong gateway
helm install kong kong/kong \
  -f infrastructure/kong/values.yaml -n learnflow
kubectl apply -f infrastructure/kong/routes/ -n learnflow
```

### Deploy application

```bash
# Create secrets
kubectl create secret generic openai-credentials \
  --from-literal=api-key=$OPENAI_API_KEY \
  -n learnflow

# Deploy backend
helm install learnflow-backend backend/deploy/helm/learnflow-backend \
  -n learnflow \
  --set openai.apiKey=$OPENAI_API_KEY

# Verify
bash infrastructure/verify/full-stack-check.sh
```

### Run database migrations

```bash
POSTGRES_POD=$(kubectl get pods -n learnflow -l app=postgresql -o jsonpath='{.items[0].metadata.name}')

for migration in infrastructure/postgres/migrations/*.sql; do
  kubectl exec -i $POSTGRES_POD -n learnflow -- \
    psql -U learnflow -d learnflow < "$migration"
done
```

---

## Production Deployment

Production uses ArgoCD for GitOps-based continuous delivery.

### Initial setup

```bash
bash scripts/setup-argocd.sh
bash scripts/setup-monitoring.sh
bash scripts/setup-external-secrets.sh
```

### Deploy via ArgoCD

```bash
# Apply ArgoCD application manifests
kubectl apply -f argocd/applications/production.yaml
kubectl apply -f argocd/applications/staging.yaml

# Sync
argocd app sync learnflow-production
```

### Promote staging to production

```bash
bash scripts/promote-to-production.sh
```

### Verify production

```bash
bash scripts/verify-deployment.sh
```

---

## Rollback Procedures

### Helm rollback (fastest)

```bash
# List revisions
helm history learnflow-backend -n learnflow

# Rollback to previous revision
helm rollback learnflow-backend <revision> -n learnflow
```

### ArgoCD rollback

```bash
# List history
argocd app history learnflow-production

# Rollback
argocd app rollback learnflow-production <id>
```

### Infrastructure rollback

```bash
bash infrastructure/rollback/rollback-kafka.sh
bash infrastructure/rollback/rollback-postgres.sh
bash infrastructure/rollback/rollback-kong.sh
bash infrastructure/rollback/rollback-dapr.sh
```

### Full rollback script

```bash
bash scripts/rollback.sh
```

---

## Scaling

### Horizontal scaling (backend services)

```bash
# Scale a specific service
kubectl scale deployment triage-service -n learnflow --replicas=3

# Or via Helm values
helm upgrade learnflow-backend backend/deploy/helm/learnflow-backend \
  -n learnflow \
  --set triage.replicas=3
```

### Kafka scaling

```bash
# Add partitions to a topic
kubectl exec kafka-0 -n kafka -- \
  kafka-topics.sh --alter --topic learning.questions \
  --partitions 6 --bootstrap-server localhost:9092
```

### Resource limits

All services have resource limits defined in Helm values:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

---

## Disaster Recovery

### Database backup

```bash
POSTGRES_POD=$(kubectl get pods -n learnflow -l app=postgresql -o jsonpath='{.items[0].metadata.name}')

# Create backup
kubectl exec $POSTGRES_POD -n learnflow -- \
  pg_dump -U learnflow learnflow > backup_$(date +%Y%m%d).sql

# Restore backup
kubectl exec -i $POSTGRES_POD -n learnflow -- \
  psql -U learnflow -d learnflow < backup_20260203.sql
```

### Kafka topic recovery

Topics auto-recreate with `auto.create.topics.enable=true`. Consumer groups resume from last committed offset.

### Full cluster recreation

```bash
# 1. Start fresh cluster
minikube delete && minikube start --cpus=4 --memory=8192

# 2. Re-deploy infrastructure (see Staging section)

# 3. Restore database from backup

# 4. Re-deploy application
```

---

## Troubleshooting

### Service won't start

```bash
# Check pod status
kubectl describe pod <pod-name> -n learnflow

# Check logs
kubectl logs <pod-name> -n learnflow --previous

# Common: OOMKilled → increase memory limits
# Common: CrashLoopBackOff → check env vars and dependencies
```

### Dapr sidecar not connecting

```bash
# Verify Dapr is installed
dapr status -k

# Check Dapr sidecar logs
kubectl logs <pod-name> -n learnflow -c daprd

# Re-apply components
kubectl apply -f infrastructure/dapr/components/ -n learnflow
```

### Kafka messages not flowing

```bash
# List topics
kubectl exec kafka-0 -n kafka -- \
  kafka-topics.sh --list --bootstrap-server localhost:9092

# Check consumer lag
kubectl exec kafka-0 -n kafka -- \
  kafka-consumer-groups.sh --describe --group learnflow-group \
  --bootstrap-server localhost:9092

# Produce test message
kubectl exec -it kafka-0 -n kafka -- \
  kafka-console-producer.sh --topic learning.questions \
  --bootstrap-server localhost:9092
```

### Kong routes not working

```bash
# List routes
kubectl exec -it <kong-pod> -n learnflow -- kong routes list

# Check config
kubectl get ingress -n learnflow

# Reload
kubectl rollout restart deployment kong -n learnflow
```

### OpenAI API errors

- **401**: Invalid API key. Check `OPENAI_API_KEY` in secrets.
- **429**: Rate limited. Reduce concurrent requests or upgrade plan.
- **500**: OpenAI outage. Check status.openai.com. Services gracefully degrade.

### Database connection issues

```bash
# Test connection
kubectl exec -it $POSTGRES_POD -n learnflow -- \
  psql -U learnflow -d learnflow -c "SELECT 1"

# Check secret exists
kubectl get secret postgres-credentials -n learnflow -o yaml
```
