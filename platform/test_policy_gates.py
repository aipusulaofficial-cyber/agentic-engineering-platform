from budget_guard import Budget, allow

def test_budget_is_hard_limit():
    limit = Budget(20, 3, 300, 50000, 5.0)
    assert allow(Budget(20, 3, 300, 50000, 5.0), limit)
    assert not allow(Budget(21, 3, 300, 50000, 5.0), limit)
