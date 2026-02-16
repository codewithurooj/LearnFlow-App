---
sidebar_position: 2
---

# Kubernetes Deployment

## Prerequisites

- Minikube v1.30+ (or remote K8s cluster)
- kubectl, Helm v3, Dapr CLI v1.13+

## Deploy

```bash
# Start cluster
minikube start --cpus=4 --memory=8192 --driver=docker

# Install Dapr
dapr init -k

# Deploy PostgreSQL
helm install postgres bitnami/postgresql \
  -f infrastructure/postgres/values.yaml \
  -n learnflow --create-namespace

# Deploy Kafka
helm install kafka bitnami/kafka \
  -f infrastructure/kafka/values.yaml \
  -n kafka --create-namespace

# Apply Dapr components
kubectl apply -f infrastructure/dapr/components/ -n learnflow

# Deploy Kong
helm install kong kong/kong \
  -f infrastructure/kong/values.yaml -n learnflow

# Deploy backend services
helm install learnflow-backend backend/deploy/helm/learnflow-backend \
  -n learnflow --set openai.apiKey=$OPENAI_API_KEY

# Verify
bash infrastructure/verify/full-stack-check.sh
```

## Run Migrations

```bash
POSTGRES_POD=$(kubectl get pods -n learnflow -l app=postgresql \
  -o jsonpath='{.items[0].metadata.name}')

for f in infrastructure/postgres/migrations/*.sql; do
  kubectl exec -i $POSTGRES_POD -n learnflow -- \
    psql -U learnflow -d learnflow < "$f"
done
```
