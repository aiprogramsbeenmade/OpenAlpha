"""Test per l'operazione ``sum``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.sum import sum


def test_sum_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("sum").name == "sum"


def test_sum_n_1_10():
    """sum(n, n, 1, 10) = 55."""
    result = sum("n", var="n", lower="1", upper="10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "55"


def test_sum_n2_1_10():
    """sum(n**2, n, 1, 10) = 385."""
    result = sum("n**2", var="n", lower="1", upper="10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "385"


def test_sum_reciproci_quadrati():
    """sum(1/n**2, n, 1, oo) = pi**2/6."""
    result = sum("1/n**2", var="n", lower="1", upper="oo")
    assert result.status == ResultStatus.EXACT
    assert "pi" in result.exact


def test_sum_geometrica():
    """sum(1/2**n, n, 0, oo) = 2."""
    result = sum("1/2**n", var="n", lower="0", upper="oo")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


def test_sum_k_1_5():
    """sum(k, k, 1, 5) = 15 (variabile k)."""
    result = sum("k", var="k", lower="1", upper="5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "15"


def test_sum_metadata():
    """Il metadata contiene var, lower, upper."""
    result = sum("n", var="n", lower="1", upper="10")
    assert result.metadata["var"] == "n"
    assert result.metadata["lower"] == "1"
    assert result.metadata["upper"] == "10"


def test_sum_var_non_valida():
    result = sum("n", var="1abc")
    assert result.status == ResultStatus.ERROR


def test_sum_input_vuoto():
    result = sum("")
    assert result.status == ResultStatus.ERROR


def test_sum_estremo_non_valido():
    result = sum("n", var="n", lower="abc +")
    assert result.status == ResultStatus.ERROR