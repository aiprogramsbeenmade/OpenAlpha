"""
Test per l'operazione ``series``.
"""

from __future__ import annotations

import pytest

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.series import series


# ---------------------------------------------------------------------------
# Casi base
# ---------------------------------------------------------------------------

def test_series_registrata():
    """L'operazione è nel registry."""
    from openalpha.core.registry import get_operation
    spec = get_operation("series")
    assert spec.name == "series"


def test_series_sin_maclaurin():
    """sin(x) -> x - x**3/6 + x**5/120 + O(x**6)."""
    result = series("sin(x)")
    assert result.status == ResultStatus.EXACT
    assert "x**3" in result.exact
    assert "x**5" in result.exact
    assert "O(x**6)" in result.exact


def test_series_exp_maclaurin():
    """exp(x) con order=4 -> 1 + x + x**2/2 + x**3/6 + O(x**4)."""
    result = series("exp(x)", order=4)
    assert result.status == ResultStatus.EXACT
    assert "1" in result.exact
    assert "x**2" in result.exact
    assert "O(x**4)" in result.exact


def test_series_geometric():
    """1/(1-x) con order=5 -> 1 + x + x**2 + x**3 + x**4 + O(x**5)."""
    result = series("1/(1-x)", order=5)
    assert result.status == ResultStatus.EXACT
    assert "x**4" in result.exact
    assert "O(x**5)" in result.exact


def test_series_cos():
    """cos(x) -> 1 - x**2/2 + x**4/24 + O(x**6)."""
    result = series("cos(x)")
    assert result.status == ResultStatus.EXACT
    assert "x**2" in result.exact
    assert "x**4" in result.exact


def test_series_log_around_one():
    """log(x) attorno a 1 -> (x-1) - (x-1)**2/2 + (x-1)**3/3 + O(...)."""
    result = series("log(x)", point="1", order=4)
    assert result.status == ResultStatus.EXACT
    assert "(x - 1)" in result.exact or "x - 1" in result.exact


def test_series_default_order_6():
    """Default order=6."""
    result = series("exp(x)")
    assert result.status == ResultStatus.EXACT
    assert "O(x**6)" in result.exact


def test_series_metadata():
    """I metadati contengono var, point, order."""
    result = series("sin(x)")
    assert result.metadata["var"] == "x"
    assert result.metadata["point"] == "0"
    assert result.metadata["order"] == 6


# ---------------------------------------------------------------------------
# Variabili diverse
# ---------------------------------------------------------------------------

def test_series_var_diversa():
    """Sviluppo in t invece di x."""
    result = series("sin(t)", var="t")
    assert result.status == ResultStatus.EXACT
    assert "t**3" in result.exact


# ---------------------------------------------------------------------------
# Errori
# ---------------------------------------------------------------------------

def test_series_input_vuoto():
    """Input vuoto -> errore."""
    result = series("")
    assert result.status == ResultStatus.ERROR


def test_series_order_zero():
    """Ordine 0 -> errore."""
    result = series("sin(x)", order=0)
    assert result.status == ResultStatus.ERROR


def test_series_order_negativo():
    """Ordine negativo -> errore."""
    result = series("sin(x)", order=-1)
    assert result.status == ResultStatus.ERROR


def test_series_order_non_intero():
    """Ordine non intero -> errore."""
    result = series("sin(x)", order="abc")
    assert result.status == ResultStatus.ERROR


def test_series_sintassi_invalida():
    """Espressione malformata -> errore."""
    result = series("2 +")
    assert result.status == ResultStatus.ERROR


def test_series_funzione_non_supportata():
    """Funzione non supportata -> unsupported."""
    result = series("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED


# ---------------------------------------------------------------------------
# Casi limite
# ---------------------------------------------------------------------------

def test_series_polinomio():
    """Un polinomio è già la sua serie."""
    result = series("x**2 + 3*x + 1")
    assert result.status == ResultStatus.EXACT


def test_series_costante():
    """Costante -> serie banale."""
    result = series("5")
    assert result.status == ResultStatus.EXACT
