set dotenv-load := true

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
    uv run pytest services/{{service}}/tests

# United command for CI, launches all checkups
ci-check service:
    just lint {{service}}
    just typecheck {{service}}