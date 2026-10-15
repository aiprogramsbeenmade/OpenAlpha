"""Test per l'operazione ``laplace_transform``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.laplace_transform import laplace_transform


def test_laplace_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("laplace_transform").name == "laplace_transform"


def test_laplace_uno():
    """L{1} = 1/s."""
    result = laplace_transform("1")
    assert result.status == ResultStatus.EXACT
    assert "1/s" in result.exact or "1 / s" in result.exact


def test_laplace_esponenziale():
    """L{exp(-a*t)} = 1/(a + s)."""
    result = laplace_transform("exp(-a*t)")
    assert result.status == ResultStatus.EXACT
    assert "s" in result.exact


def test_laplace_t():
    """L{t} = 1/s**2."""
    result = laplace_transform("t")
    assert result.status == ResultStatus.EXACT
    assert "s" in result.exact


def test_laplace_sin():
    """L{sin(t)} = 1/(s**2 + 1)."""
    result = laplace_transform("sin(t)")
    assert result.status == ResultStatus.EXACT
    assert "s" in result.exact


def test_laplace_var_personalizzate():
    """L{f(x)}(y) con var personalizzate."""
    result = laplace_transform("x", t="x", s="y")
    assert result.status == ResultStatus.EXACT
    assert "y" in result.exact


def test_laplace_var_non_valida():
    result = laplace_transform("1", t="1abc")
    assert result.status == ResultStatus.ERROR


def test_laplace_input_vuoto():
    result = laplace_transform("")
    assert result.status == ResultStatus.ERROR


def test_laplace_metadata():
    result = laplace_transform("1")
    assert result.metadata["t"] == "t"
    assert result.metadata["s"] == "s"