"""Test per l'operazione ``combinations``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.combinations import combinations


def test_combinations_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("combinations").name == "combinations"


def test_combinations_5_2():
    result = combinations("5", "2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "10"


def test_combinations_10_3():
    result = combinations("10", "3")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "120"


def test_combinations_5_0():
    result = combinations("5", "0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_combinations_5_5():
    result = combinations("5", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_combinations_k_maggiore_di_n():
    result = combinations("3", "5")
    assert result.status == ResultStatus.ERROR


def test_combinations_n_negativo():
    result = combinations("-1", "2")
    assert result.status == ResultStatus.ERROR


def test_combinations_non_intero():
    result = combinations("1/2", "2")
    assert result.status == ResultStatus.ERROR


def test_combinations_input_vuoto():
    result = combinations("", "2")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_combinations_5_2_step():
    """combinations(5, 2) produce 3 step."""
    result = combinations("5", "2")
    assert len(result.steps) == 3


def test_combinations_5_2_step_finale():
    """L'ultimo step è il calcolo."""
    result = combinations("5", "2")
    last = result.steps[-1]
    assert last.rule_name == "calcolo"
    assert last.after == "10"


def test_combinations_5_0_step():
    """combinations(5, 0): 1 step."""
    result = combinations("5", "0")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "definizione"


def test_combinations_5_5_step():
    """combinations(5, 5): 1 step."""
    result = combinations("5", "5")
    assert len(result.steps) == 1