import pytest

from agentic_platform.runtime import ExecutionPolicy


@pytest.mark.parametrize("timeout", [float("nan"), float("inf"), -1.0, 0.0])
def test_invalid_timeout_budgets_rejected(timeout):
    with pytest.raises(ValueError):
        ExecutionPolicy(timeout_seconds=timeout).validate()


def test_valid_timeout_budget():
    ExecutionPolicy(timeout_seconds=0.1).validate()

def test_worker_thread_execution_rejects_unsupported_signal_timeouts():
    from concurrent.futures import ThreadPoolExecutor

    from agentic_platform.runtime import (
        AgentExecutor,
        ExecutionError,
        ExecutionRequest,
        ToolRegistry,
    )

    registry = ToolRegistry()
    registry.register("echo", lambda: "ok")
    executor = AgentExecutor(registry)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(executor.execute, ExecutionRequest("req-worker", "echo"))
        with pytest.raises(ExecutionError, match="main thread"):
            future.result()
    assert executor.audit_events[-1].error_type == "ExecutionError"
