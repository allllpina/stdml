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

# 

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

# Add Helm-repository HashiCorp (executes only once)
helm-setup:
    helm repo add hashicorp https://helm.releases.hashicorp.com
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

# ==========================================
# API
# ==========================================
run-api:
    uv run --package api uvicorn src.main:app --app-dir services/api --reload
