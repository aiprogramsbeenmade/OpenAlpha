"""Test per l'operazione ``permutations``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.permutations import permutations


def test_permutations_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("permutations").name == "permutations"


def test_permutations_5_2():
    result = permutations("5", "2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "20"


def test_permutations_10_3():
    result = permutations("10", "3")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "720"


def test_permutations_5_0():
    result = permutations("5", "0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_permutations_5_5():
    result = permutations("5", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "120"


def test_permutations_k_maggiore_di_n():
    result = permutations("3", "5")
    assert result.status == ResultStatus.ERROR


def test_permutations_non_intero():
    result = permutations("1/2", "2")
    assert result.status == ResultStatus.ERROR


def test_permutations_input_vuoto():
    result = permutations("", "2")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_permutations_5_2_step():
    """permutations(5, 2) produce 3 step."""
    result = permutations("5", "2")
    assert len(result.steps) == 3


def test_permutations_5_2_step_finale():
    """L'ultimo step è il calcolo."""
    result = permutations("5", "2")
    last = result.steps[-1]
    assert last.rule_name == "calcolo"
    assert last.after == "20"


def test_permutations_5_0_step():
    """permutations(5, 0): 1 step."""
    result = permutations("5", "0")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "definizione"


def test_permutations_5_5_step():
    """permutations(5, 5): 3 step (formula, fattoriali, calcolo)."""
    result = permutations("5", "5")
    assert len(result.steps) == 3