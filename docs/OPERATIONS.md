# Operational runbook

The reference runtime is dependency-free and deterministic. Each execution records request_id, tool name, status, normalized error type and latency in an in-memory audit trail.

Required production extensions: durable audit storage, correlation propagation, p50/p95/p99 latency, dependency latency, retry_count, concurrency/resource saturation, deployment revision, health/readiness, rollback procedure and security audit trail.

## Failure handling
1. Reject malformed request metadata before tool execution.
2. Enforce the tool-call budget before resolving a tool.
3. Normalize unknown tools and unexpected handler exceptions at the execution boundary.
4. Preserve an audit event for every attempted execution.
5. Keep retries outside the core executor so idempotency and provider semantics remain explicit.
