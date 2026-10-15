"""Test per l'operazione ``apart``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.apart import apart


def test_apart_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("apart").name == "apart"


def test_apart_frazione_semplice():
    """1/(x**2 - 1) -> 1/(2*(x-1)) - 1/(2*(x+1))."""
    result = apart("1/(x**2 - 1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto
    assert "x - 1" in result.exact or "x-1" in result.exact
    assert len(result.conditions) > 0


def test_apart_polinomio_piu_frazione():
    """(x**2 + 1)/x -> x + 1/x."""
    result = apart("(x**2 + 1)/x")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto


def test_apart_prodotto_di_fattori():
    """1/(x*(x+1)) -> 1/x - 1/(x+1)."""
    result = apart("1/(x*(x+1))")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto
    assert "/x" in result.exact or "1/x" in result.exact


def test_apart_var_non_valida():
    result = apart("1/(x-1)", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_apart_input_vuoto():
    result = apart("")
    assert result.status == ResultStatus.ERROR


def test_apart_sintassi_invalida():
    result = apart("1/(")
    assert result.status == ResultStatus.ERROR


def test_apart_funzione_non_supportata():
    result = apart("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED