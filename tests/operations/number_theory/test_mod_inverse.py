"""Test per l'operazione ``mod_inverse``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.mod_inverse import mod_inverse


def test_mod_inverse_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("mod_inverse").name == "mod_inverse"


def test_mod_inverse_3_7():
    """3 * 5 = 15 ≡ 1 (mod 7)."""
    result = mod_inverse("3", "7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_mod_inverse_10_17():
    """10 * 12 = 120 ≡ 1 (mod 17)."""
    result = mod_inverse("10", "17")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_mod_inverse_non_esiste():
    """gcd(2, 4) = 2, quindi 2 non ha inverso mod 4."""
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