"""Small, deterministic agent execution boundary with explicit failure semantics."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Any, Callable


class ExecutionError(Exception):
    """Base class for normalized execution failures."""


class PolicyDenied(ExecutionError):
    """Raised when execution policy rejects a tool call."""


class ToolNotFound(ExecutionError):
    """Raised when a requested tool is not registered."""


@dataclass(frozen=True)
class ExecutionPolicy:
    max_tool_calls: int = 4
    timeout_seconds: float = 5.0
    max_argument_count: int = 32

    def validate(self) -> None:
        if self.max_tool_calls < 1:
            raise ValueError("max_tool_calls must be >= 1")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if self.max_argument_count < 0:
            raise ValueError("max_argument_count must be >= 0")


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    tool: str
    status: str
    error_type: str | None
    latency_ms: float


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, handler: Callable[..., Any]) -> None:
        if not name.strip():
            raise ValueError("tool name must not be empty")
        if name in self._tools:
            raise ValueError(f"tool already registered: {name}")
        self._tools[name] = handler

    def resolve(self, name: str) -> Callable[..., Any]:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolNotFound(name) from exc


class AgentExecutor:
    def __init__(self, registry: ToolRegistry, policy: ExecutionPolicy | None = None) -> None:
        self.registry = registry
        self.policy = policy or ExecutionPolicy()
        self.policy.validate()
        self._audit: list[AuditEvent] = []
        self._tool_calls = 0

    def execute(self, request: ExecutionRequest) -> Any:
        if not request.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not request.tool.strip():
            raise ValueError("tool must not be empty")
        if len(request.arguments) > self.policy.max_argument_count:
            raise PolicyDenied("argument budget exhausted")
        if self._tool_calls >= self.policy.max_tool_calls:
            raise PolicyDenied("tool-call budget exhausted")

        started = monotonic()
        status = "success"
        error_type: str | None = None
        self._tool_calls += 1
        try:
            handler = self.registry.resolve(request.tool)
            return handler(**request.arguments)
        except ExecutionError as exc:
            status = "denied" if isinstance(exc, PolicyDenied) else "error"
            error_type = type(exc).__name__
            raise
        except Exception as exc:
            status = "error"
            error_type = type(exc).__name__
            raise ExecutionError(str(exc)) from exc
        finally:
            self._audit.append(
                AuditEvent(
                    request_id=request.request_id,
                    tool=request.tool,
                    status=status,
                    error_type=error_type,
                    latency_ms=(monotonic() - started) * 1000,
                )
            )

    @property
    def audit_events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._audit)
