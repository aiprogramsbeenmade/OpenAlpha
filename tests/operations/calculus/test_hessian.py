"""Test per l'operazione ``hessian``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.hessian import hessian


def test_hessian_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("hessian").name == "hessian"


def test_hessian_x2_y2():
    """hessian(x**2 + y**2) -> [[2, 0], [0, 2]]."""
    result = hessian("x**2 + y**2")
    assert result.status == ResultStatus.EXACT
    assert "[[2, 0], [0, 2]]" in result.exact or "[[2, 0], [0, 2]]" == result.exact


def test_hessian_xy():
    """hessian(x*y) -> [[0, 1], [1, 0]]."""
    result = hessian("x*y")
    assert result.status == ResultStatus.EXACT
    assert "[[0, 1], [1, 0]]" in result.exact or "[[0, 1], [1, 0]]" == result.exact


def test_hessian_cubi():
    """hessian(x**3 + y**3) -> [[6*x, 0], [0, 6*y]]."""
    result = hessian("x**3 + y**3")
    assert result.status == ResultStatus.EXACT
    assert "6*x" in result.exact
    assert "6*y" in result.exact


def test_hessian_metadata_vars():
    """Il metadata contiene vars."""
    result = hessian("x**2 + y**2")
    assert result.metadata["vars"] == ["x", "y"]


def test_hessian_costante():
    """hessian(5) -> []."""
    result = hessian("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[]"


def test_hessian_input_vuoto():
    result = hessian("")
    assert result.status == ResultStatus.ERROR


def test_hessian_funzione_non_supportata():
    result = hessian("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED