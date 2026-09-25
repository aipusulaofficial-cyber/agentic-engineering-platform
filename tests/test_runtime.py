import unittest

from agentic_platform.runtime import (
    AgentExecutor,
    ExecutionError,
    ExecutionPolicy,
    ExecutionRequest,
    PolicyDenied,
    ToolRegistry,
)


class AgentExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        registry = ToolRegistry()
        registry.register("echo", lambda value: value)
        self.executor = AgentExecutor(registry, ExecutionPolicy(max_tool_calls=1))

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
        with self.assertRaises(PolicyDenied):
            self.executor.execute(ExecutionRequest("req-4", "echo", {"value": 2}))


if __name__ == "__main__":
    unittest.main()
