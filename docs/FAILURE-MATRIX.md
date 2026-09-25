# Failure matrix

| Failure | Detection | Action | Retry? | Runtime status |
|---|---|---|---|---|
| Invalid request ID | request validation | reject | No | implemented |
| Unknown tool | registry resolution | normalize and audit | No | implemented |
| Tool exception | execution boundary | normalize and audit | Adapter-specific | implemented |
| Tool-call budget exhausted | execution policy | fail closed | No | implemented |
| Dependency timeout | provider adapter | normalize | Safe/idempotent only | extension point |
| Repeated dependency failure | provider policy | open circuit | No while open | extension point |
| Local overload | bounded executor | fail fast | No | extension point |
| Policy/tool denial | authorization boundary | fail closed | No | extension point |

The runtime status column distinguishes implemented behavior from future adapter capabilities.
