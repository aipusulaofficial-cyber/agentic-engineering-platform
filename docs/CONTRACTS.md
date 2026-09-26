# Contracts

The runtime exposes an executable contract for untrusted request metadata and controlled tool invocation.

- **Execution request:** non-empty request_id, tool name and structured arguments.
- **Policy contract:** positive timeout budget, bounded maximum tool calls and bounded argument count.
- **Tool contract:** uniquely registered callable resolved by name.
- **Timeout contract:** on POSIX runtimes, a tool call is interrupted when it exceeds timeout_seconds and normalized as ExecutionTimeout.
- **Failure contract:** unknown tools, policy denials, timeouts and unexpected handler failures are explicit execution errors.
- **Audit contract:** every attempted execution that enters the execution boundary emits request ID, tool, status, error type and latency.

The core uses a POSIX signal for hard in-process timeout enforcement. Provider/tool adapters can be layered above this boundary without coupling the core to external services.
