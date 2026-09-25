# Failure matrix

| Failure | Detection | Action | Retry? | Runtime status |
|---|---|---|---|---|
| Invalid/untrusted input | future contract validation | reject | No | planned |
| Dependency timeout | future timeout budget | normalize | Safe/idempotent only | planned |
| Dependency error | future provider adapter | exponential backoff | Safe/idempotent only | planned |
| Repeated failure | future circuit breaker | open circuit | No while open | planned |
| Local overload | future bounded executor/rate limiter | fail fast | No | planned |
| Policy/tool denial | future authorization | fail closed | No | planned |

The table is a design contract, not a claim of current runtime behavior.