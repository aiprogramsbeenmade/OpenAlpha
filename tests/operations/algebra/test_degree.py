"""Test per l'operazione ``degree``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.degree import degree


def test_degree_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("degree").name == "degree"


def test_degree_polinomio_semplice():
    """degree(x**3 + x + 1) = 3."""
    result = degree("x**3 + x + 1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3"


def test_degree_in_x():
    """degree(x**2*y + x*y**2, 'x') = 2."""
    result = degree("x**2*y + x*y**2", var="x")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_degree_in_y():
    """degree(x**2*y + x*y**2, 'y') = 2."""
    result = degree("x**2*y + x*y**2", var="y")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_degree_costante():
    """degree(5) = 0."""
    result = degree("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_degree_zero():
    """degree(0) = -oo."""
    result = degree("0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "-oo"


def test_degree_var_non_valida():
    result = degree("x**2", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_degree_input_vuoto():
    result = degree("")
    assert result.status == ResultStatus.ERROR