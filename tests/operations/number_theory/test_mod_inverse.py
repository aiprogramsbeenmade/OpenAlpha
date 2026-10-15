"""Test per l'operazione ``mod_inverse``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.mod_inverse import mod_inverse


def test_mod_inverse_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("mod_inverse").name == "mod_inverse"


def test_mod_inverse_3_7():
    result = mod_inverse("3", "7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_mod_inverse_10_17():
    result = mod_inverse("10", "17")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_mod_inverse_non_esiste():
    result = mod_inverse("2", "4")
    assert result.status == ResultStatus.UNSUPPORTED


def test_mod_inverse_modulo_zero():
    result = mod_inverse("3", "0")
    assert result.status == ResultStatus.ERROR
    assert "modulo" in result.error.lower()


def test_mod_inverse_non_intero():
    result = mod_inverse("1/2", "7")
    assert result.status == ResultStatus.ERROR


def test_mod_inverse_input_vuoto():
    result = mod_inverse("", "7")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_mod_inverse_3_7_step():
    """mod_inverse(3, 7) produce 2 step."""
    result = mod_inverse("3", "7")
    assert len(result.steps) == 2


def test_mod_inverse_3_7_step_finale():
    """L'ultimo step è il risultato."""
    result = mod_inverse("3", "7")
    last = result.steps[-1]
    assert last.rule_name == "risultato"
    assert last.after == "5"


def test_mod_inverse_10_17_step():
    """mod_inverse(10, 17) produce 2 step."""
    result = mod_inverse("10", "17")
    assert len(result.steps) == 2


def test_mod_inverse_non_esiste_step():
    """mod_inverse(2, 4): 1 step 'condizione di esistenza'."""
    result = mod_inverse("2", "4")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "condizione di esistenza"