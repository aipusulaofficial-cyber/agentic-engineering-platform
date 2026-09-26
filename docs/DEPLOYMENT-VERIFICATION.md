# Deployment verification

The repository contains a bounded reference implementation; no production deployment is claimed. Before deployment, verify container build, non-root execution, resource bounds, readiness, representative domain smoke tests, telemetry propagation, security/SBOM checks and rollback revision.

The core execution timeout is enforced on POSIX runtimes. Production adapters must additionally verify cancellation semantics, distributed concurrency limits, durable audit storage, dependency timeouts/retries and deployment-specific SLOs.
