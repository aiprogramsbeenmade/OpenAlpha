"""Test per l'operazione ``prime``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.prime import prime


def test_prime_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("prime").name == "prime"


def test_prime_1():
    """prime(1) = 2."""
    result = prime("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_prime_10():
    """prime(10) = 29."""
    result = prime("10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "29"


def test_prime_100():
    """prime(100) = 541."""
    result = prime("100")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "541"


def test_prime_zero():
    """prime(0) -> errore."""
    result = prime("0")
    assert result.status == ResultStatus.ERROR


def test_prime_negativo():
    """prime(-1) -> errore."""
    result = prime("-1")
    assert result.status == ResultStatus.ERROR


def test_prime_non_intero():
    result = prime("1/2")
    assert result.status == ResultStatus.ERROR


def test_prime_input_vuoto():
    result = prime("")
    assert result.status == ResultStatus.ERROR