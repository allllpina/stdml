# STDML Workspace

![Python](https://img.shields.io/badge/python-3.12.3-blue.svg)
![Environment](https://img.shields.io/badge/environment-Nix%20%7C%20uv-success.svg)
![License](https://shields.io/badge/license-Apache%202-blue)

An End-to-End MLOps Platform built on a robust microservices architecture. This monorepo provides a production-ready infrastructure for orchestrating API gateways, asynchronous machine learning workers, and local Kubernetes deployments.

Designed for scalability and seamless developer experience, the workspace centralizes configuration, dependency management, and strict code quality standards across all underlying services.

## Core Architecture & Features

* **Microservices Design:** Decoupled architecture utilizing FastAPI for the gateway and scalable, event-driven ML workers.
* **Cloud-Native Infrastructure:** Fully reproducible local Kubernetes cluster provisioning via `k3d` and `Helm`.
* **Centralized Secrets:** Dynamic configuration and secure credentials management powered by HashiCorp `Vault`.
* **Deterministic Environments:** `Nix` Flakes combined with `uv` workspaces guarantee identical, blazing-fast package resolution across the monorepo.
* **Developer Ergonomics:** Streamlined workflow automation using `Just` as a modern command runner.
* **Strict Code Quality:** Mandatory type safety and linting enforced across all services via `Mypy` and `Ruff`.

## Documentation

Comprehensive documentation—including system prerequisites, local cluster setup, Vault initialization, and microservice development workflows—is maintained in the project Wiki.

📚[Go to the STDML Workspace Wiki](https://github.com/allllpina/stdml/wiki)
