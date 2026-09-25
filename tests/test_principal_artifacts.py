from pathlib import Path

def test_principal_artifacts_are_explicit():
    required=["ARCHITECTURE.md","ENGINEERING-CHAIN.md","docs/PRINCIPAL-ENGINEERING.md","docs/CONTRACTS.md","docs/FAILURE-MATRIX.md","docs/OPERATIONS.md","docs/SLO.md","ADRs/0001-architecture-boundary.md","ADRs/0003-failure-retry-strategy.md","ADRs/0004-security-decision.md"]
    for path in required: assert Path(path).exists(), path

def test_runtime_boundary_is_truthful():
    text=Path("docs/PRINCIPAL-ENGINEERING.md").read_text().lower()
    assert "not implemented" in text or "reference" in text
