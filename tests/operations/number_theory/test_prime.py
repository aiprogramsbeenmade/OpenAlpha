"""Test per l'operazione ``prime``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.prime import prime


def test_prime_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("prime").name == "prime"


def test_prime_1():
    result = prime("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_prime_10():
    result = prime("10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "29"


def test_prime_100():
    result = prime("100")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "541"


def test_prime_zero():
    result = prime("0")
    assert result.status == ResultStatus.ERROR


def test_prime_negativo():
    result = prime("-1")
    assert result.status == ResultStatus.ERROR


def test_prime_non_intero():
    result = prime("1/2")
    assert result.status == ResultStatus.ERROR


def test_prime_input_vuoto():
    result = prime("")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Test dei passaggi
# ---------------------------------------------------------------------------

def test_prime_1_step():
    """prime(1) produce 1 step."""
    result = prime("1")
    assert len(result.steps) == 1
    assert result.steps[0].rule_name == "definizione"


def test_prime_5_step():
    """prime(5) produce 1 step con l'elenco."""
    result = prime("5")
    assert len(result.steps) == 1
    assert "2, 3, 5, 7, 11" in result.steps[0].description


def test_prime_10_step_finale():
    """prime(10) ha step finale con 29."""
    result = prime("10")
    last = result.steps[-1]
    assert last.after == "29"


def test_prime_100_step_riassunto():
    """prime(100) produce 1 step riassuntivo (n > 20)."""
    result = prime("100")
    assert len(result.steps) == 1
    assert "541" in result.steps[0].description