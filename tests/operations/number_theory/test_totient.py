"""Test per l'operazione ``totient``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.totient import totient


def test_totient_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("totient").name == "totient"


def test_totient_10():
    result = totient("10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "4"


def test_totient_7():
    result = totient("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6"


def test_totient_1():
    result = totient("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_totient_primo():
    result = totient("13")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_totient_zero():
    result = totient("0")
    assert result.status == ResultStatus.ERROR


def test_totient_negativo():
    result = totient("-5")
    assert result.status == ResultStatus.ERROR


def test_totient_non_intero():
    result = totient("1/2")
    assert result.status == ResultStatus.ERROR


def test_totient_input_vuoto():
    result = totient("")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_totient_10_step():
    """totient(10) produce 3 step."""
    result = totient("10")
    assert len(result.steps) == 3


def test_totient_10_step_finale():
    """L'ultimo step è il calcolo."""
    result = totient("10")
    last = result.steps[-1]
    assert last.rule_name == "calcolo"
    assert last.after == "4"


def test_totient_7_step():
    """totient(7): n è primo, 1 step."""
    result = totient("7")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "formula per primi"


def test_totient_1_step():
    """totient(1): 1 step."""
    result = totient("1")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "definizione"


def test_totient_12_step():
    """totient(12): 3 step (fattorizzazione, formula, calcolo)."""
    result = totient("12")
    assert len(result.steps) == 3