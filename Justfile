set dotenv-load := true
VAULT_TOKEN := env_var("VAULT_TOKEN")

# ==========================================
# CI and Code Quality checks
# ==========================================

# Sync dependencies throughout all workspaces
sync:
    uv sync

# Start Ruff for certain service
lint service:
    uv run ruff check services/{{service}}

# Start Mypy for certain service
typecheck service:
    uv run mypy services/{{service}}

# Start tests
test service:
    uv run --package {{service}} pytest services/{{service}}/tests

# United command for CI, launches all checkups
ci-check service:
    just lint {{service}}
    just typecheck {{service}}
    just test {{service}}

# ==========================================
# Cluster administration k3d
# ==========================================

# Create local k3d cluster
cluster-up:
    @echo "Creating local k3d cluster..."
    k3d cluster create mlops-cluster --port "8080:80@loadbalancer"
    @echo "Cluster is ready! Kubeconfig updated automatically."

# Stop and delete (system clean up)
cluster-down:
    k3d cluster delete mlops-cluster

# ==========================================
# Infrastructure(Kubernetes / Helm)
# ==========================================

# Add Helm-repositories (executes only once)
helm-setup:
    helm repo add hashicorp https://helm.releases.hashicorp.com
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update

# Rise vault in Dev-mode
vault-up: helm-setup
    helm upgrade --install vault hashicorp/vault \
        --set "server.dev.enabled=true" \
        --set "server.dev.devRootToken={{VAULT_TOKEN}}" \
        --set "injector.enabled=false" \
        --wait

# Vault port forwarding to localhost
vault-ui:
    kubectl port-forward svc/vault 8200:8200

# Rise Redis in standalone mode (no auth for local dev)
redis-up: helm-setup
    helm upgrade --install redis bitnami/redis \
        --set architecture=standalone \
        --set auth.enabled=false \
        --wait

# Rise Kafka in KRaft mode (single broker, no auth, no persistence, pinned to a free chart version)
# Rise Kafka using official Apache image (Bypassing Bitnami)
kafka-up:
    kubectl apply -f infra/k8s/kafka-dev.yaml
    kubectl rollout status deployment/kafka --timeout=90s

# Start all infrastructure
infra-up: vault-up redis-up kafka-up
    @echo "All infrastructure components (Vault, Redis, Kafka) are running!"

# ==========================================
# API
# ==========================================
run-api:
    uv run --package api uvicorn src.main:app --app-dir services/api --reload
