#!/bin/bash
set -e

ENV_FILE=".env"
VAULT_MOUNT="secret"
SECRET_DOC="env"
VAULT_POD="vault-0"

echo "--- Importing all variables into (Pod: $VAULT_POD) at $VAULT_MOUNT/$SECRET_DOC ---"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: File $ENV_FILE not found!"
    exit 1
fi

if [ -z "$VAULT_TOKEN" ]; then
    echo "Error: VAULT_TOKEN environment variable is not set!"
    exit 1
fi

declare -a vault_args=()

while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    value=$(echo "$value" | tr -d '\r')
    vault_args+=("$key=$value")
done < "$ENV_FILE"

if [ ${#vault_args[@]} -gt 0 ]; then
    echo "Writing ${#vault_args[@]} variables to: $VAULT_MOUNT/$SECRET_DOC"
    kubectl exec "$VAULT_POD" -- env VAULT_TOKEN="$VAULT_TOKEN" \
        vault kv put "$VAULT_MOUNT/$SECRET_DOC" "${vault_args[@]}" > /dev/null
    echo "--- Import has been completed successfully ---"
else
    echo "Warning: No valid variables found in $ENV_FILE."
fi

echo "--- Configuring Kubernetes Auth Method for Sidecar Injector ---"

kubectl exec "$VAULT_POD" -- env VAULT_TOKEN="$VAULT_TOKEN" \
    sh -c "vault auth enable kubernetes 2>/dev/null || true"

echo "Configuring Kubernetes Auth..."
kubectl exec "$VAULT_POD" -- env VAULT_TOKEN="$VAULT_TOKEN" \
    sh -c 'vault write auth/kubernetes/config \
        kubernetes_host="https://kubernetes.default.svc:443" \
        disable_iss_validation=true' > /dev/null

echo "Creating policy..."
kubectl exec -i "$VAULT_POD" -- env VAULT_TOKEN="$VAULT_TOKEN" \
    sh -c "echo '
path \"secret/data/env\" {
  capabilities = [\"read\"]
}
' | vault policy write mlops-policy -"

echo "Binding role..."
kubectl exec "$VAULT_POD" -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault write auth/kubernetes/role/mlops-app \
    bound_service_account_names=mlops-sa \
    bound_service_account_namespaces=default \
    policies=mlops-policy \
    ttl=24h > /dev/null

echo "--- Vault Sidecar config completed successfully ---"
