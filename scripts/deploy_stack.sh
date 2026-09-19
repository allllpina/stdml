#!/bin/bash
set -euo pipefail

echo "Starting full stack deployment..."

# 1. Apply base infrastructure RBAC permissions for Vault
echo "Applying Vault auth delegator permissions..."
kubectl apply -f infra/k8s/vault-auth-delegator.yaml

# 2. Seed environment variables into Vault
echo "Deploying infrastructure"
just infra-up

echo "Seeding secrets into Vault..."
just vault-seed

# 3. Establish temporary port-forward for Feast initialization
echo "Opening temporary port-forward to Redis..."
kubectl port-forward svc/redis-master 6379:6379 > /dev/null 2>&1 &
REDIS_PF_PID=$!

trap 'kill "$REDIS_PF_PID" 2>/dev/null || true' EXIT

if command -v nc &>/dev/null; then
    for i in {1..10}; do nc -z 127.0.0.1 6379 && break || sleep 0.5; done
else
    sleep 2
fi

# 4. Run Feast seed from host pointing to localhost Redis
echo "Running Feast seed..."
FEAST_REDIS_CONN="127.0.0.1:6379" just feast-seed

# 3. Apply Kubernetes manifests via Kustomize (Kafka, Redis, Vault, API, Worker)
echo "Deploying Kubernetes manifests..."
kubectl apply -k infra/k8s

# 4. Wait for deployments to stabilize
echo "Waiting for services to stabilize..."
kubectl rollout status deployment/api --timeout=60s
kubectl rollout status deployment/worker --timeout=60s

echo "Stack successfully deployed and initialized!"
