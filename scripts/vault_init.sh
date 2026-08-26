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

# Читаємо всі змінні підряд
while IFS='=' read -r key value; do
    # Skip comments and empty lines
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