"""Test per l'operazione ``factorint``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.factorint import factorint


def test_factorint_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("factorint").name == "factorint"


def test_factorint_24():
    """24 = 2^3 * 3."""
    result = factorint("24")
    assert result.status == ResultStatus.EXACT
    assert "2^3" in result.exact
    assert "3" in result.exact


def test_factorint_100():
    """100 = 2^2 * 5^2."""
    result = factorint("100")
    assert result.status == ResultStatus.EXACT
    assert "2^2" in result.exact
    assert "5^2" in result.exact


def test_factorint_primo():
    """7 = 7."""
    result = factorint("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "7"


def test_factorint_uno():
    """1 non ha fattori primi: il risultato è 1 (prodotto vuoto)."""
    result = factorint("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_factorint_zero():
    """0 non è positivo."""
    result = factorint("0")
    assert result.status == ResultStatus.ERROR


def test_factorint_negativo():
    """-5 non è positivo."""
    result = factorint("-5")
    assert result.status == ResultStatus.ERROR


def test_factorint_non_intero():
    """1/2 non è intero."""
    result = factorint("1/2")
    assert result.status == ResultStatus.ERROR


def test_factorint_input_vuoto():
    result = factorint("")
    assert result.status == ResultStatus.ERROR

def test_factorint_metadata_latex():
    """factorint fornisce il LaTeX già pronto."""
    result = factorint("24")
    assert "latex_exact" in result.metadata
    assert "2^{3}" in result.metadata["latex_exact"]
    assert "3" in result.metadata["latex_exact"]