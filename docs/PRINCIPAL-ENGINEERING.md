# Principal Engineering Contract

## Scope
This document defines the engineering decisions that make this repository reviewable as a production-oriented reference implementation.

## Core boundary
**Primary concern:** Agentic execution.

Keep planning, policy, tool invocation, and state management behind explicit interfaces; bound tool calls and execution time; make retries idempotency-aware; preserve an execution audit trail.

## Non-functional requirements
- **Determinism:** core behavior should be reproducible in tests without requiring live external services.
- **Failure semantics:** expected failure classes must be explicit and observable; hidden retries are avoided.
- **Security:** validate untrusted inputs, use safe defaults, and minimize privilege at boundaries.
- **Operability:** expose health/readiness signals where applicable and preserve enough context to diagnose a failed operation.
- **Change safety:** CI is a release gate; architecture changes should update the relevant ADR and tests.

## Review checklist
- [x] Public contracts are validated.
- [x] Domain policy is independent from infrastructure adapters.
- [x] Failure and retry behavior is explicit.
- [x] Resource limits are bounded where work can grow.
- [x] Tests cover happy path, invalid input, and representative failure paths.
- [x] Security-sensitive decisions are auditable.
- [x] CI validates the repository before merge.
- [x] Architecture trade-offs are documented rather than implied.

## Evidence boundary
This repository is a bounded reference implementation, not a deployed production service. Hard execution timeouts are implemented for POSIX runtimes; provider-specific retries, durable audit storage, distributed concurrency controls and deployment operations remain explicit extension points.

## What this is not
Production deployment still requires environment-specific SLOs, capacity planning, secrets management, dependency hardening, and operational ownership.
