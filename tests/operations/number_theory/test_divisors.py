"""Test per l'operazione ``divisors``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.divisors import divisors


def test_divisors_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("divisors").name == "divisors"


def test_divisors_12():
    result = divisors("12")
    assert result.status == ResultStatus.EXACT
    assert "1" in result.exact
    assert "12" in result.exact


def test_divisors_7():
    result = divisors("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[1, 7]"


def test_divisors_1():
    result = divisors("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[1]"


def test_divisors_16():
    result = divisors("16")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[1, 2, 4, 8, 16]"


def test_divisors_zero():
    result = divisors("0")
    assert result.status == ResultStatus.ERROR


def test_divisors_negativo():
    result = divisors("-5")
    assert result.status == ResultStatus.ERROR


def test_divisors_non_intero():
    result = divisors("1/2")
    assert result.status == ResultStatus.ERROR


def test_divisors_input_vuoto():
    result = divisors("")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_divisors_12_step():
    """divisors(12) produce 4 step (3 coppie + elenco)."""
    result = divisors("12")
    assert len(result.steps) == 4


def test_divisors_12_step_finale():
    """L'ultimo step è l'elenco completo."""
    result = divisors("12")
    last = result.steps[-1]
    assert last.rule_name == "elenco completo"
    assert "{1, 2, 3, 4, 6, 12}" in last.after


def test_divisors_7_step():
    """divisors(7) produce 2 step."""
    result = divisors("7")
    assert len(result.steps) == 2


def test_divisors_16_quadrato_perfetto():
    """divisors(16) ha uno step 'quadrato perfetto'."""
    result = divisors("16")
    step_names = [s.rule_name for s in result.steps]
    assert "quadrato perfetto" in step_names


def test_divisors_1_step():
    """divisors(1) produce 2 step."""
    result = divisors("1")
    assert len(result.steps) == 2