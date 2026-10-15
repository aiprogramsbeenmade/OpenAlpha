"""Test per l'operazione ``product``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.product import product


def test_product_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("product").name == "product"


def test_product_fattoriale():
    """product(n, n, 1, 5) = 120."""
    result = product("n", var="n", lower="1", upper="5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "120"


def test_product_10_fattoriale():
    """product(n, n, 1, 10) = 3628800."""
    result = product("n", var="n", lower="1", upper="10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "3628800"


def test_product_telescopica():
    """product((n+1)/n, n, 1, 5) = 6."""
    result = product("(n+1)/n", var="n", lower="1", upper="5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "6"


def test_product_k():
    """product(k, k, 1, 4) = 24."""
    result = product("k", var="k", lower="1", upper="4")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "24"


def test_product_metadata():
    """Il metadata contiene var, lower, upper."""
    result = product("n", var="n", lower="1", upper="5")
    assert result.metadata["var"] == "n"
    assert result.metadata["lower"] == "1"
    assert result.metadata["upper"] == "5"


def test_product_var_non_valida():
    result = product("n", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_product_input_vuoto():
    result = product("")
    assert result.status == ResultStatus.ERROR