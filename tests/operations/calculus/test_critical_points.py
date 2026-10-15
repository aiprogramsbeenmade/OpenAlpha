"""Test per l'operazione ``critical_points``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.critical_points import critical_points


def test_critical_points_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("critical_points").name == "critical_points"


def test_critical_points_paraboloide():
    """critical_points(x**2 + y**2) -> [(0, 0)]."""
    result = critical_points("x**2 + y**2")
    assert result.status == ResultStatus.EXACT
    assert "(0, 0)" in result.exact


def test_critical_points_sella():
    """critical_points(x**2 - y**2) -> [(0, 0)]."""
    result = critical_points("x**2 - y**2")
    assert result.status == ResultStatus.EXACT
    assert "(0, 0)" in result.exact


def test_critical_points_xy():
    """critical_points(x*y) -> [(0, 0)]."""
    result = critical_points("x*y")
    assert result.status == ResultStatus.EXACT
    assert "(0, 0)" in result.exact


def test_critical_points_una_variabile():
    """critical_points(x**2) -> [(0)]."""
    result = critical_points("x**2")
    assert result.status == ResultStatus.EXACT
    assert "(0)" in result.exact


def test_critical_points_tre_variabili():
    """critical_points(x**2 + y**2 + z**2) -> [(0, 0, 0)]."""
    result = critical_points("x**2 + y**2 + z**2")
    assert result.status == ResultStatus.EXACT
    assert "(0, 0, 0)" in result.exact


def test_critical_points_nessuno():
    """critical_points(exp(x)) -> [] (nessun punto critico)."""
    result = critical_points("exp(x)")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[]"


def test_critical_points_costante():
    """critical_points(5) -> []."""
    result = critical_points("5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "[]"


def test_critical_points_metadata_vars():
    """Il metadata contiene vars."""
    result = critical_points("x**2 + y**2")
    assert result.metadata["vars"] == ["x", "y"]


def test_critical_points_input_vuoto():
    result = critical_points("")
    assert result.status == ResultStatus.ERROR


def test_critical_points_funzione_non_supportata():
    result = critical_points("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED