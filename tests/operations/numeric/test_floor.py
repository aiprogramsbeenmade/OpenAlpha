"""Test per l'operazione ``floor``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.numeric.floor import floor


def test_floor_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("floor").name == "floor"


def test_floor_2_7():
    result = floor("2.7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_floor_2_1():
    result = floor("2.1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_floor_negativo():
    result = floor("-2.1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "-3"


def test_floor_intero():
    result = floor("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_floor_zero():
    result = floor("0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_floor_con_variabile():
    result = floor("x")
    assert result.status == ResultStatus.ERROR


def test_floor_input_vuoto():
    result = floor("")
    assert result.status == ResultStatus.ERROR