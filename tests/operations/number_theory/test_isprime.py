"""Test per l'operazione ``isprime``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.isprime import isprime


def test_isprime_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("isprime").name == "isprime"


def test_isprime_7():
    """7 è primo."""
    result = isprime("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_8():
    """8 non è primo."""
    result = isprime("8")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "False"


def test_isprime_97():
    """97 è primo."""
    result = isprime("97")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_1():
    """1 non è primo."""
    result = isprime("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "False"


def test_isprime_2():
    """2 è primo."""
    result = isprime("2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_non_intero():
    """1/2 non è intero."""
    result = isprime("1/2")
    assert result.status == ResultStatus.ERROR


def test_isprime_input_vuoto():
    result = isprime("")
    assert result.status == ResultStatus.ERROR