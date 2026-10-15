"""Test per l'operazione ``inverse_laplace``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.inverse_laplace import inverse_laplace


def test_inverse_laplace_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("inverse_laplace").name == "inverse_laplace"


def test_inverse_laplace_uno_su_s():
    """L⁻¹{1/s} = 1."""
    result = inverse_laplace("1/s")
    assert result.status == ResultStatus.EXACT


def test_inverse_laplace_sin():
    """L⁻¹{1/(s**2 + 1)} = sin(t)."""
    result = inverse_laplace("1/(s**2 + 1)")
    assert result.status == ResultStatus.EXACT
    assert "sin" in result.exact


def test_inverse_laplace_uno_su_s2():
    """L⁻¹{1/s**2} = t."""
    result = inverse_laplace("1/s**2")
    assert result.status == ResultStatus.EXACT


def test_inverse_laplace_var_non_valida():
    result = inverse_laplace("1/s", s="1abc")
    assert result.status == ResultStatus.ERROR


def test_inverse_laplace_input_vuoto():
    result = inverse_laplace("")
    assert result.status == ResultStatus.ERROR


def test_inverse_laplace_metadata():
    result = inverse_laplace("1/s")
    assert result.metadata["s"] == "s"
    assert result.metadata["t"] == "t"