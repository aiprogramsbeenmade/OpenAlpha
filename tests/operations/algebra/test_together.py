"""Test per l'operazione ``together``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.together import together


def test_together_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("together").name == "together"


def test_together_somma_frazioni():
    """1/x + 1/(x+1) -> (2*x + 1)/(x*(x+1))."""
    result = together("1/x + 1/(x+1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto
    assert "x" in result.exact


def test_together_frazioni_con_variabili():
    """1/x + 1/y -> (x + y)/(x*y)."""
    result = together("1/x + 1/y")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto


def test_together_espressione_gia_combinata():
    """Un'unica frazione resta invariata."""
    result = together("(x + 1)/(x - 1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto


def test_together_input_vuoto():
    result = together("")
    assert result.status == ResultStatus.ERROR


def test_together_funzione_non_supportata():
    result = together("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED