"""Test per l'operazione ``ceil``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.numeric.ceil import ceil


def test_ceil_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("ceil").name == "ceil"


def test_ceil_2_1():
    result = ceil("2.1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3"


def test_ceil_2_9():
    result = ceil("2.9")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3"


def test_ceil_negativo():
    result = ceil("-2.7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "-2"


def test_ceil_intero():
    result = ceil("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "5"


def test_ceil_zero():
    result = ceil("0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_ceil_con_variabile():
    result = ceil("x")
    assert result.status == ResultStatus.ERROR


def test_ceil_input_vuoto():
    result = ceil("")
    assert result.status == ResultStatus.ERROR