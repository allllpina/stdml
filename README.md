# STDML Workspace

End-to-End MLOps Platform based on a microservices architecture. This monorepo contains the infrastructure configurations, API gateways, and machine learning workers.

## Prerequisites

To develop and run this project locally, ensure you have the following tools installed:
- **Nix** (with Flakes enabled) for declarative environment builds.
- **Just** as a command runner (replaces Make).
- **Docker** for running local containerized infrastructure.
- **uv** for fast Python package and workspace management.
- **k3d** and **Helm** (provided via Nix devShell or installed globally).

## Project Setup

The project uses `uv` workspaces to manage multiple Python microservices under a single global `uv.lock` file.

1. Clone the repository and navigate to the project root.
2. Synchronize all workspace dependencies:
   ```bash
   just sync
   ```
## Infrastructure Management
The local development environment runs on a k3d (Kubernetes) cluster with HashiCorp Vault for secrets management.

**Cluster Lifecycle:**

- Create and start the cluster:
```bash
just cluster-up
```

- Stop and destroy the cluster:
```bash
just cluster-down
```

**Vault Integration:**

- Deploy Vault in dev-mode via Helm:
```bash
just vault-up
```
- Forward ports to access the Vault UI (http://localhost:8200):
```bash
just vault-ui
```
_(Note: The default development root token is set to `root`)._

## Development Workflow
We enforce strict linting and type-checking across all microservices using Ruff and Mypy.

**Code Quality Commands:**

Run checks for a specific microservice by passing its directory name as an argument. For example, to check the `api_gateway` service:

- Run Ruff (Linter & Formatter):
```bash
just lint api_gateway
```

- Run Mypy (Type Checker):
```bash
just typecheck api_gateway
```

- Run full CI pipeline locally:
```bash
just ci-check api_gateway
```

**Managing Dependencies:**
To add a new package to a specific microservice, use the `--package` flag:
```bash
uv add fastapi pydantic --package api_gateway
```