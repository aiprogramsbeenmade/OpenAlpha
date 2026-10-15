"""Test per l'operazione ``round``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.numeric.round import round


def test_round_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("round").name == "round"


def test_round_2_4():
    result = round("2.4")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_round_2_6():
    result = round("2.6")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3"


def test_round_2_5():
    """Banker's rounding: 2.5 -> 2."""
    result = round("2.5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_round_3_5():
    """Banker's rounding: 3.5 -> 4."""
    result = round("3.5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "4"


def test_round_2_567_con_2_cifre():
    result = round("2.567", digits=2)
    assert result.status == ResultStatus.EXACT
    assert result.exact.startswith("2.5")


def test_round_intero():
    result = round("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_round_negativo():
    result = round("-2.7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "-3"


def test_round_con_variabile():
    result = round("x")
    assert result.status == ResultStatus.ERROR


def test_round_input_vuoto():
    result = round("")
    assert result.status == ResultStatus.ERROR