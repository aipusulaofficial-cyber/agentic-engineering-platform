import time
import unittest

from agentic_platform.runtime import (
    AgentExecutor,
    ExecutionError,
    ExecutionPolicy,
    ExecutionRequest,
    ExecutionTimeout,
    PolicyDenied,
    ToolRegistry,
)


class AgentExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        registry = ToolRegistry()
        registry.register("echo", lambda value: value)
        self.executor = AgentExecutor(registry, ExecutionPolicy(max_tool_calls=2))

    def test_executes_and_records_audit_event(self) -> None:
        result = self.executor.execute(ExecutionRequest("req-1", "echo", {"value": "ok"}))
        self.assertEqual(result, "ok")
        event = self.executor.audit_events[0]
        self.assertEqual((event.request_id, event.status, event.error_type), ("req-1", "success", None))
        self.assertGreaterEqual(event.latency_ms, 0)

    def test_unknown_tool_is_normalized_and_audited(self) -> None:
        with self.assertRaises(ExecutionError):
            self.executor.execute(ExecutionRequest("req-2", "missing"))
        self.assertEqual(self.executor.audit_events[0].error_type, "ToolNotFound")

    def test_tool_call_budget_is_explicit(self) -> None:
        self.executor.execute(ExecutionRequest("req-3", "echo", {"value": 1}))
        self.executor.execute(ExecutionRequest("req-4", "echo", {"value": 2}))
        with self.assertRaises(PolicyDenied):
            self.executor.execute(ExecutionRequest("req-5", "echo", {"value": 3}))

    def test_timeout_is_enforced_and_audited(self) -> None:
        registry = ToolRegistry()

        def slow_tool() -> None:
            time.sleep(0.2)

        registry.register("slow", slow_tool)
        executor = AgentExecutor(registry, ExecutionPolicy(timeout_seconds=0.02))
        with self.assertRaises(ExecutionTimeout):
            executor.execute(ExecutionRequest("req-timeout", "slow"))
        event = executor.audit_events[0]
        self.assertEqual((event.status, event.error_type), ("error", "ExecutionTimeout"))
        self.assertLess(event.latency_ms, 150)

    def test_policy_values_are_validated(self) -> None:
        with self.assertRaises(ValueError):
            AgentExecutor(ToolRegistry(), ExecutionPolicy(max_tool_calls=0))
        with self.assertRaises(ValueError):
            AgentExecutor(ToolRegistry(), ExecutionPolicy(timeout_seconds=0))
        with self.assertRaises(ValueError):
            AgentExecutor(ToolRegistry(), ExecutionPolicy(max_argument_count=-1))

    def test_argument_budget_is_enforced(self) -> None:
        executor = AgentExecutor(
            self.executor.registry,
            ExecutionPolicy(max_argument_count=0),
        )
        with self.assertRaises(PolicyDenied):
            executor.execute(ExecutionRequest("req-args", "echo", {"value": 1}))
        event = executor.audit_events[0]
        self.assertEqual((event.status, event.error_type), ("denied", "PolicyDenied"))

    def test_handler_exception_is_normalized_and_audited(self) -> None:
        registry = ToolRegistry()

        def broken() -> None:
            raise RuntimeError("boom")

        registry.register("broken", broken)
        executor = AgentExecutor(registry)
        with self.assertRaises(ExecutionError) as ctx:
            executor.execute(ExecutionRequest("req-error", "broken"))
        self.assertIsInstance(ctx.exception.__cause__, RuntimeError)
        event = executor.audit_events[0]
        self.assertEqual((event.status, event.error_type), ("error", "RuntimeError"))

    def test_duplicate_and_blank_tool_registration_is_rejected(self) -> None:
        registry = ToolRegistry()
        registry.register("echo", lambda: None)
        with self.assertRaises(ValueError):
            registry.register("echo", lambda: None)
        with self.assertRaises(ValueError):
            registry.register(" ", lambda: None)


if __name__ == "__main__":
    unittest.main()
