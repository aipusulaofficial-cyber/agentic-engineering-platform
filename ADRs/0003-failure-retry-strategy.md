# ADR-0003: Failure and retry strategy

## Decision
The core runtime enforces bounded execution time and tool-call budgets. Provider/dependency adapters must use explicit timeouts, bounded exponential backoff, idempotency-aware retries, bounded concurrency, rate limiting where applicable, graceful degradation and circuit breaking for repeated dependency failures.

## Why
These controls make failure behavior deterministic and observable while preventing hidden latency amplification.

## Alternatives considered
Unlimited retries, blind retries and unbounded queues were rejected.

## Trade-offs
The core prefers bounded failure over hidden latency amplification. In-process hard timeouts use POSIX signal support; adapters that require portable or distributed cancellation must enforce their own cancellation semantics.

## Consequences
Executable tests must cover every runtime control before it is represented as implemented. Provider-specific resilience remains outside the dependency-free core.
