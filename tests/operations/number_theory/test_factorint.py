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

def test_factorint_24_ha_step():
    """factorint(24) produce passaggi."""
    result = factorint("24")
    assert len(result.steps) > 0


def test_factorint_24_step_divisioni():
    """I primi step sono divisioni per 2."""
    result = factorint("24")
    # 24 = 2^3 * 3: 3 divisioni per 2 + 1 divisione per 3 + finale.
    assert len(result.steps) == 5


def test_factorint_24_step_finale():
    """L'ultimo step è la fattorizzazione completa."""
    result = factorint("24")
    last = result.steps[-1]
    assert last.rule_name == "fattorizzazione completa"
    assert "2^3" in last.after
    assert "3" in last.after


def test_factorint_primo_no_step():
    """Un primo non ha passaggi significativi."""
    result = factorint("7")
    assert result.steps == []


def test_factorint_uno_no_step():
    """1 non ha passaggi."""
    result = factorint("1")
    assert result.steps == []


def test_factorint_100_step():
    """factorint(100): 4 step di divisione + 1 finale."""
    result = factorint("100")
    assert len(result.steps) == 5