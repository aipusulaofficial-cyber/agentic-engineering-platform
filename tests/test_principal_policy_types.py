import math

import pytest

from agentic_platform.runtime import AgentExecutor, ExecutionPolicy, ToolRegistry


@pytest.mark.parametrize("value", [0, -1, True, 1.5, "4"])
def test_invalid_tool_call_limits_rejected(value):
    with pytest.raises(ValueError, match="max_tool_calls"):
        AgentExecutor(ToolRegistry(), ExecutionPolicy(max_tool_calls=value))


@pytest.mark.parametrize("value", [0, -1, True, math.nan, math.inf, "5"])
def test_invalid_timeouts_rejected(value):
    with pytest.raises(ValueError, match="timeout_seconds"):
        AgentExecutor(ToolRegistry(), ExecutionPolicy(timeout_seconds=value))


@pytest.mark.parametrize("value", [-1, True, 1.5, math.nan])
def test_invalid_argument_budgets_rejected(value):
    with pytest.raises(ValueError, match="max_argument_count"):
        AgentExecutor(ToolRegistry(), ExecutionPolicy(max_argument_count=value))


def test_noncallable_registry_entry_rejected():
    registry = ToolRegistry()
    with pytest.raises(ValueError, match="callable"):
        registry.register("not-a-tool", None)
