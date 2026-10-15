"""Test per l'operazione ``divisors``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.divisors import divisors


def test_divisors_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("divisors").name == "divisors"


def test_divisors_12():
    """divisors(12) = [1, 2, 3, 4, 6, 12]."""
    result = divisors("12")
    assert result.status == ResultStatus.EXACT
    assert "1" in result.exact
    assert "12" in result.exact


def test_divisors_7():
    """divisors(7) = [1, 7]."""
    result = divisors("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[1, 7]"


def test_divisors_1():
    """divisors(1) = [1]."""
    result = divisors("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[1]"


def test_divisors_zero():
    """divisors(0) -> errore."""
    result = divisors("0")
    assert result.status == ResultStatus.ERROR


def test_divisors_negativo():
    """divisors(-5) -> errore."""
    result = divisors("-5")
    assert result.status == ResultStatus.ERROR


def test_divisors_non_intero():
    """divisors(1/2) -> errore."""
    result = divisors("1/2")
    assert result.status == ResultStatus.ERROR


def test_divisors_input_vuoto():
    result = divisors("")
    assert result.status == ResultStatus.ERROR