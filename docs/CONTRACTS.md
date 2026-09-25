# Contracts

The runtime exposes an executable contract for untrusted request metadata and controlled tool invocation.

- **Execution request:** non-empty request_id, tool name and structured arguments.
- **Policy contract:** positive timeout budget and bounded maximum tool calls.
- **Tool contract:** uniquely registered callable resolved by name.
- **Failure contract:** unknown tools and policy denials are normalized into explicit execution errors.
- **Audit contract:** every attempted execution emits request ID, tool, status, error type and latency.

Provider/tool adapters can be layered above this boundary without coupling the core to external services.
