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
    result = gcd("0", "0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_gcd_non_intero():
    result = gcd("1/2", "3")
    assert result.status == ResultStatus.ERROR


def test_gcd_input_vuoto():
    result = gcd("", "3")
    assert result.status == ResultStatus.ERROR


def test_gcd_sintassi_invalida():
    result = gcd("2 +", "3")
    assert result.status == ResultStatus.ERROR