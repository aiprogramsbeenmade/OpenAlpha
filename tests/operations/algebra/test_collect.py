"""Test per l'operazione ``collect``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.collect import collect


def test_collect_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("collect").name == "collect"


def test_collect_polinomio():
    """x**2 + 2*x + 1 + 3*x**3 -> 3*x**3 + x**2 + 2*x + 1."""
    result = collect("x**2 + 2*x + 1 + 3*x**3")
    assert result.status == ResultStatus.EXACT


def test_collect_con_fattor_comune():
    """x*y + x*z + x -> x*(y + z + 1)."""
    result = collect("x*y + x*z + x", var="x")
    assert result.status == ResultStatus.EXACT
    assert "x*" in result.exact


def test_collect_var_default():
    """Senza var, default 'x'."""
    result = collect("x**2 + x")
    assert result.status == ResultStatus.EXACT


def test_collect_var_non_valida():
    result = collect("x**2", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_collect_input_vuoto():
    result = collect("")
    assert result.status == ResultStatus.ERROR


def test_collect_funzione_non_supportata():
    result = collect("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED