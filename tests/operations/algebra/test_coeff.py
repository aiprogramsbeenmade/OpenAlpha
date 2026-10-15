"""Test per l'operazione ``coeff``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.coeff import coeff


def test_coeff_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("coeff").name == "coeff"


def test_coeff_termine_lineare():
    """coeff(x**3 + 2*x + 1, n=1) = 2."""
    result = coeff("x**3 + 2*x + 1", n="1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_coeff_termine_noto():
    """coeff(x**3 + 2*x + 1, n=0) = 1."""
    result = coeff("x**3 + 2*x + 1", n="0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_coeff_termine_assente():
    """coeff(x**3 + 2*x + 1, n=2) = 0."""
    result = coeff("x**3 + 2*x + 1", n="2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_coeff_simbolico():
    """coeff(x**3 + a*x + 1, n=1) = a."""
    result = coeff("x**3 + a*x + 1", n="1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "a"


def test_coeff_var_diversa():
    """coeff(t**2 + 3*t, var='t', n=1) = 3."""
    result = coeff("t**2 + 3*t", var="t", n="1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3"


def test_coeff_var_non_valida():
    result = coeff("x**2", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_coeff_n_non_valido():
    result = coeff("x**2", n="abc")
    assert result.status == ResultStatus.ERROR


def test_coeff_n_negativo():
    result = coeff("x**2", n="-1")
    assert result.status == ResultStatus.ERROR


def test_coeff_input_vuoto():
    result = coeff("")
    assert result.status == ResultStatus.ERROR