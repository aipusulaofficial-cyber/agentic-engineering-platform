# AIPusula Platform Integration — Governed Agent Runtime

## Runtime control loop
`request -> identity -> policy -> budget -> plan -> tool execution -> state -> evaluation -> audit`

Every agent run MUST have:
- correlation/trace ID
- policy decision
- allowed tool set
- max tool calls
- max tokens
- max cost
- max runtime
- max retries
- state/memory reference
- final outcome + failure reason

## Enforcement
Budgets are hard limits, not advisory telemetry. On violation, stop execution, emit a deterministic reason code and write an audit event.

## Tool policy
Tools are allow-listed by policy. Authorization is checked at execution time, not only at planning time.

## Reliability
Use bounded concurrency, timeouts, retry budgets, idempotency and circuit-breaking around external tools.

## Evaluation
Agent runs feed the AI Quality Gate. Record task success, tool-call correctness, policy violations, latency and cost.

## Integration points
- secure-ai-gateway: identity/authz/policy
- enterprise-rag-platform: governed retrieval
- distributed-ai-inference-platform: model execution
- ai-cost-optimization-platform: per-run economics
- ai-observability-platform: trace/tool telemetry
- ai-evaluation-platform: release/evaluation gate

## Engineering standard
Code -> Contract -> Test -> Security -> Runtime -> Observability -> Deployment -> Evidence
