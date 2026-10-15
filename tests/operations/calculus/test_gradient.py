"""Test per l'operazione ``gradient``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.gradient import gradient


def test_gradient_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("gradient").name == "gradient"


def test_gradient_auto_vars():
    """gradient(x**2 + y**2) -> [2*x, 2*y]."""
    result = gradient("x**2 + y**2")
    assert result.status == ResultStatus.EXACT
    assert "2*x" in result.exact
    assert "2*y" in result.exact


def test_gradient_vars_esplicite():
    """gradient(x**2 + y**2, 'x,y') -> [2*x, 2*y]."""
    result = gradient("x**2 + y**2", "x,y")
    assert result.status == ResultStatus.EXACT
    assert "2*x" in result.exact
    assert "2*y" in result.exact


def test_gradient_ordine_vars():
    """gradient(x**2 + y**2, 'y,x') -> [2*y, 2*x]."""
    result = gradient("x**2 + y**2", "y,x")
    assert result.status == ResultStatus.EXACT
    pos_y = result.exact.find("2*y")
    pos_x = result.exact.find("2*x")
    assert pos_y < pos_x


def test_gradient_tre_variabili():
    """gradient(x*y*z) -> [y*z, x*z, x*y]."""
    result = gradient("x*y*z")
    assert result.status == ResultStatus.EXACT
    assert "y*z" in result.exact
    assert "x*z" in result.exact
    assert "x*y" in result.exact


def test_gradient_costante():
    """gradient(5) -> []."""
    result = gradient("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[]"


def test_gradient_metadata_vars():
    """Il metadata contiene vars."""
    result = gradient("x**2 + y**2")
    assert result.metadata["vars"] == ["x", "y"]


def test_gradient_vars_non_valida():
    result = gradient("x**2", "1abc")
    assert result.status == ResultStatus.ERROR


def test_gradient_input_vuoto():
    result = gradient("")
    assert result.status == ResultStatus.ERROR


def test_gradient_funzione_non_supportata():
    result = gradient("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED