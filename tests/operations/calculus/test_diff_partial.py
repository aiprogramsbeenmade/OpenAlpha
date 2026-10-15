"""Test per l'operazione ``diff_partial``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.diff_partial import diff_partial


def test_diff_partial_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("diff_partial").name == "diff_partial"


def test_diff_partial_x_su_polinomio():
    """diff_partial(x**2 + y**2, x) = 2*x."""
    result = diff_partial("x**2 + y**2", var="x")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2*x"


def test_diff_partial_y_su_polinomio():
    """diff_partial(x**2 + y**2, y) = 2*y."""
    result = diff_partial("x**2 + y**2", var="y")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2*y"


def test_diff_partial_prodotto():
    """diff_partial(x*y + x + y, x) = y + 1."""
    result = diff_partial("x*y + x + y", var="x")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "y + 1"


def test_diff_partial_sin():
    """diff_partial(sin(x*y), x) = y*cos(x*y)."""
    result = diff_partial("sin(x*y)", var="x")
    assert result.status == ResultStatus.EXACT
    assert "cos" in result.exact


def test_diff_partial_ordine_2():
    """diff_partial(x**3, x, 2) = 6*x."""
    result = diff_partial("x**3", var="x", order=2)
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6*x"


def test_diff_partial_ordine_zero():
    """diff_partial(x**2, x, 0) = x**2."""
    result = diff_partial("x**2", var="x", order=0)
    assert result.status == ResultStatus.EXACT
    assert result.exact == "x**2"


def test_diff_partial_var_non_valida():
    result = diff_partial("x**2", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_diff_partial_input_vuoto():
    result = diff_partial("")
    assert result.status == ResultStatus.ERROR


def test_diff_partial_funzione_non_supportata():
    result = diff_partial("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED