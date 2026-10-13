"""
Test della politica delle spiegazioni.

Verificano che lo stato della spiegazione (`complete`, `partial`,
`unavailable`) sia coerente con il contenuto degli `Step` e con
il messaggio fornito all'utente.
"""

from __future__ import annotations

import sympy

from openalpha.explanations.engine import explain
from openalpha.operations.algebra.simplify import simplify


# ---------------------------------------------------------------------------
# explain() — unavailable
# ---------------------------------------------------------------------------

def test_explain_unavailable_per_espressione_semplice():
    result = explain(sympy.sympify("x + 1"))
    assert result.steps == []
    assert result.complete is False
    assert result.status == "unavailable"
    assert "non disponibile" in result.message


# ---------------------------------------------------------------------------
# explain() — complete
# ---------------------------------------------------------------------------

def test_explain_complete_per_quadrato_del_binomio():
    x, y = sympy.symbols("x y")
    result = explain((x + y) ** 2)
    assert len(result.steps) >= 1
    assert result.complete is True
    assert result.status == "complete"
    assert "completa rispetto" in result.message


def test_explain_complete_per_differenza_di_quadrati():
    x, y = sympy.symbols("x y")
    result = explain(x**2 - y**2)
    assert len(result.steps) >= 1
    assert result.complete is True
    assert result.status == "complete"


# ---------------------------------------------------------------------------
# simplify() — propagazione del metadata
# ---------------------------------------------------------------------------

def test_simplify_metadata_unavailable():
    result = simplify("x + 1")
    assert result.metadata.get("explanation_status") == "unavailable"
    assert result.metadata.get("explanation_complete") is False


def test_simplify_metadata_complete():
    result = simplify("(x + 1)**2")
    assert result.metadata.get("explanation_status") == "complete"
    assert result.metadata.get("explanation_complete") is True


def test_simplify_metadata_contiene_messaggio():
    result = simplify("x + 1")
    assert "explanation_message" in result.metadata
    assert result.metadata["explanation_message"]