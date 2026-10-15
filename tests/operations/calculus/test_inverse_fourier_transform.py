"""Test per l'operazione ``inverse_fourier_transform``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.inverse_fourier_transform import (
    inverse_fourier_transform,
)


def test_inverse_fourier_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("inverse_fourier_transform").name == "inverse_fourier_transform"


def test_inverse_fourier_gaussiana():
    """F⁻¹{exp(-pi**2*k**2)} = exp(-x**2)/sqrt(pi)."""
    result = inverse_fourier_transform("exp(-pi**2*k**2)", "k", "x")
    assert result.status == ResultStatus.EXACT
    assert "x" in result.exact


def test_inverse_fourier_var_non_valida():
    result = inverse_fourier_transform("1", k="1abc")
    assert result.status == ResultStatus.ERROR


def test_inverse_fourier_input_vuoto():
    result = inverse_fourier_transform("")
    assert result.status == ResultStatus.ERROR


def test_inverse_fourier_metadata():
    result = inverse_fourier_transform("exp(-k**2)", "k", "x")
    assert result.metadata["k"] == "k"
    assert result.metadata["x"] == "x"