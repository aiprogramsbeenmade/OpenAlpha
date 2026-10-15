"""Test per l'operazione ``roots``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.roots import roots


def test_roots_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("roots").name == "roots"


def test_roots_quadratica_semplice():
    """x**2 - 1 = (x-1)(x+1) -> radici -1, 1."""
    result = roots("x**2 - 1")
    assert result.status == ResultStatus.EXACT
    assert "-1" in result.exact
    assert "1" in result.exact


def test_roots_quadrato_perfetto():
    """x**2 - 2x + 1 = (x-1)^2 -> radice 1 con molteplicità 2."""
    result = roots("x**2 - 2*x + 1")
    assert result.status == ResultStatus.EXACT
    assert "1: 2" in result.exact


def test_roots_cubica():
    """x**3 - x = x(x-1)(x+1) -> radici -1, 0, 1."""
    result = roots("x**3 - x")
    assert result.status == ResultStatus.EXACT
    assert "-1" in result.exact
    assert "0" in result.exact
    assert "1" in result.exact


def test_roots_complesse():
    """x**2 + 1 -> radici -I, I."""
    result = roots("x**2 + 1")
    assert result.status == ResultStatus.EXACT
    # sympy stampa I come "I"
    assert "I" in result.exact


def test_roots_irrazionali():
    """x**2 - 2 -> radici -sqrt(2), sqrt(2)."""
    result = roots("x**2 - 2")
    assert result.status == ResultStatus.EXACT
    assert "sqrt(2)" in result.exact


def test_roots_lineare():
    """2*x + 4 -> radice -2."""
    result = roots("2*x + 4")
    assert result.status == ResultStatus.EXACT
    assert "-2" in result.exact


def test_roots_costante_non_zero():
    """5 = 0 non ha radici."""
    result = roots("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "{}"


def test_roots_var_diversa():
    """x**2 - 1 in t: t**2 - 1."""
    result = roots("t**2 - 1", var="t")
    assert result.status == ResultStatus.EXACT


def test_roots_var_non_valida():
    result = roots("x**2 - 1", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_roots_non_polinomio():
    """sin(x) non è un polinomio."""
    result = roots("sin(x)")
    assert result.status == ResultStatus.UNSUPPORTED


def test_roots_frazione():
    """1/x non è un polinomio."""
    result = roots("1/x")
    assert result.status == ResultStatus.UNSUPPORTED


def test_roots_input_vuoto():
    result = roots("")
    assert result.status == ResultStatus.ERROR


def test_roots_sintassi_invalida():
    result = roots("2 +")
    assert result.status == ResultStatus.ERROR


def test_roots_metadata():
    """Il metadata contiene roots e var."""
    result = roots("x**2 - 1")
    assert "roots" in result.metadata
    assert result.metadata["var"] == "x"