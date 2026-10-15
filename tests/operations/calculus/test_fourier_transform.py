"""Test per l'operazione ``fourier_transform``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.fourier_transform import fourier_transform


def test_fourier_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("fourier_transform").name == "fourier_transform"


def test_fourier_gaussiana():
    """F{exp(-x**2)} contiene exp(-pi**2 * k**2)."""
    result = fourier_transform("exp(-x**2)", "x", "k")
    assert result.status == ResultStatus.EXACT
    assert "k" in result.exact


def test_fourier_esponenziale_decrescente():
    """F{exp(-a*abs(x))}: SymPy non lo calcola -> UNSUPPORTED."""
    result = fourier_transform("exp(-a*abs(x))", "x", "k")
    assert result.status == ResultStatus.UNSUPPORTED


def test_fourier_costante():
    """F{1} = DiracDelta(k)."""
    result = fourier_transform("1", "x", "k")
    assert result.status == ResultStatus.EXACT
    assert "DiracDelta" in result.exact


def test_fourier_costante_cinque():
    """F{5} = 5*DiracDelta(k)."""
    result = fourier_transform("5", "x", "k")
    assert result.status == ResultStatus.EXACT
    assert "DiracDelta" in result.exact
    assert "5" in result.exact


def test_fourier_var_non_valida():
    result = fourier_transform("1", x="1abc")
    assert result.status == ResultStatus.ERROR


def test_fourier_input_vuoto():
    result = fourier_transform("")
    assert result.status == ResultStatus.ERROR


def test_fourier_metadata():
    result = fourier_transform("exp(-x**2)", "x", "k")
    assert result.metadata["x"] == "x"
    assert result.metadata["k"] == "k"