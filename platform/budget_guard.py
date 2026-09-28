"""Hard agent budget enforcement."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Budget:
    tool_calls: int
    retries: int
    runtime_seconds: float
    tokens: int
    cost_usd: float


def allow(actual: Budget, limit: Budget) -> bool:
    return (
        actual.tool_calls <= limit.tool_calls
        and actual.retries <= limit.retries
        and actual.runtime_seconds <= limit.runtime_seconds
        and actual.tokens <= limit.tokens
        and actual.cost_usd <= limit.cost_usd
    )
