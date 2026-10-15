"""Test per l'operazione ``gcd``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.gcd import gcd


def test_gcd_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("gcd").name == "gcd"


def test_gcd_12_18():
    result = gcd("12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6"


def test_gcd_100_75():
    result = gcd("100", "75")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "25"


def test_gcd_coprimi():
    result = gcd("7", "13")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_gcd_con_negativo():
    result = gcd("-12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6"


def test_gcd_zero():
    result = gcd("0", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_gcd_entrambi_zero():
    """gcd(0, 0) -> errore (MCD non definito)."""
    result = gcd("0", "0")
    assert result.status == ResultStatus.ERROR
    assert "definito" in result.error.lower()


def test_gcd_non_intero():
    result = gcd("1/2", "3")
    assert result.status == ResultStatus.ERROR


def test_gcd_input_vuoto():
    result = gcd("", "3")
    assert result.status == ResultStatus.ERROR


def test_gcd_sintassi_invalida():
    result = gcd("2 +", "3")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_gcd_12_18_ha_step():
    """gcd(12, 18) produce passi."""
    result = gcd("12", "18")
    assert len(result.steps) >= 1


def test_gcd_12_18_step_finale():
    """L'ultimo step è il caso base."""
    result = gcd("12", "18")
    last = result.steps[-1]
    assert last.rule_name == "caso base"
    assert last.after == "6"


def test_gcd_100_75_step():
    """gcd(100, 75) produce 3 step."""
    result = gcd("100", "75")
    assert len(result.steps) == 3


def test_gcd_coprimi_step():
    """gcd(7, 13) = 1: 4 step."""
    result = gcd("7", "13")
    assert len(result.steps) == 4
    assert result.steps[-1].after == "1"


def test_gcd_zero_step():
    """gcd(0, 5) = 5: 1 step 'caso banale'."""
    result = gcd("0", "5")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "caso banale"


def test_gcd_zero_zero_step():
    """gcd(0, 0) -> errore, nessuno step."""
    result = gcd("0", "0")
    assert result.status == ResultStatus.ERROR
    assert result.steps == []