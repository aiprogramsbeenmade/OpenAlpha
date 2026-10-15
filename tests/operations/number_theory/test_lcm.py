"""Test per l'operazione ``lcm``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.lcm import lcm


def test_lcm_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("lcm").name == "lcm"


def test_lcm_12_18():
    result = lcm("12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "36"


def test_lcm_4_6():
    result = lcm("4", "6")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_lcm_coprimi():
    result = lcm("7", "13")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "91"


def test_lcm_con_negativo():
    result = lcm("-12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "36"


def test_lcm_zero_e_cinque():
    result = lcm("0", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_lcm_zero_zero():
    result = lcm("0", "0")
    assert result.status == ResultStatus.ERROR
    assert "definito" in result.error.lower()


def test_lcm_non_intero():
    result = lcm("1/2", "3")
    assert result.status == ResultStatus.ERROR


def test_lcm_input_vuoto():
    result = lcm("", "3")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_lcm_12_18_step():
    """lcm(12, 18) produce 3 step."""
    result = lcm("12", "18")
    assert len(result.steps) == 3


def test_lcm_12_18_step_finale():
    """L'ultimo step è la divisione."""
    result = lcm("12", "18")
    last = result.steps[-1]
    assert last.rule_name == "divisione"
    assert last.after == "36"


def test_lcm_zero_step():
    """lcm(0, 5) = 0: 1 step 'caso banale'."""
    result = lcm("0", "5")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "caso banale"


def test_lcm_zero_zero_step():
    """lcm(0, 0) -> errore, nessuno step."""
    result = lcm("0", "0")
    assert result.status == ResultStatus.ERROR
    assert result.steps == []