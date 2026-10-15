"""Test per l'operazione ``factorial``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.factorial import factorial


def test_factorial_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("factorial").name == "factorial"


def test_factorial_5():
    result = factorial("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "120"


def test_factorial_0():
    result = factorial("0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_factorial_1():
    result = factorial("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_factorial_10():
    result = factorial("10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3628800"


def test_factorial_20():
    result = factorial("20")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2432902008176640000"


def test_factorial_negativo():
    result = factorial("-1")
    assert result.status == ResultStatus.ERROR


def test_factorial_non_intero():
    result = factorial("1/2")
    assert result.status == ResultStatus.ERROR


def test_factorial_input_vuoto():
    result = factorial("")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_factorial_5_step():
    """factorial(5) produce 2 step."""
    result = factorial("5")
    assert len(result.steps) == 2


def test_factorial_5_step_calcolo():
    """L'ultimo step è il calcolo."""
    result = factorial("5")
    last = result.steps[-1]
    assert last.rule_name == "calcolo"
    assert last.after == "120"


def test_factorial_0_step():
    """factorial(0): 1 step."""
    result = factorial("0")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "definizione"


def test_factorial_1_step():
    """factorial(1): 1 step."""
    result = factorial("1")
    assert len(result.steps) == 1


def test_factorial_20_step_riassunto():
    """factorial(20): n > 10, 1 step riassuntivo."""
    result = factorial("20")
    assert len(result.steps) == 1
    assert "20" in result.steps[0].description