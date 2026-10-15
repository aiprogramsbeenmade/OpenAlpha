"""Test per l'operazione ``totient``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.totient import totient


def test_totient_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("totient").name == "totient"


def test_totient_10():
    """φ(10) = 4."""
    result = totient("10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "4"


def test_totient_7():
    """φ(7) = 6."""
    result = totient("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6"


def test_totient_1():
    """φ(1) = 1."""
    result = totient("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_totient_primo():
    """φ(p) = p - 1 per p primo."""
    result = totient("13")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_totient_zero():
    """φ(0) -> errore."""
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