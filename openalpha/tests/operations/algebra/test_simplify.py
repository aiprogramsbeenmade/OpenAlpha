"""
Test dell'operazione "simplify".

Verificano: semplificazione di identità trigonometriche, espansione
di prodotti notevoli, gestione di input vuoto, input pericoloso, e
presenza dell'operazione nel registro.
"""

from __future__ import annotations

import pytest

from openalpha.core.registry import clear_registry, get_operation, list_operations
from openalpha.core.status import ResultStatus

# Importiamo il package per attivare la registrazione via decoratore.
import openalpha.operations  # noqa: F401


def test_simplify_registrata():
    assert "simplify" in list_operations()
    spec = get_operation("simplify")
    assert spec.name == "simplify"


def test_simplify_identita_trigonometrica():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("sin(x)**2 + cos(x)**2")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_simplify_prodotto_notevole():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("(x + 1)**2")
    assert result.status is ResultStatus.EXACT
    # SymPy può restituire "x**2 + 2*x + 1" o una forma equivalente.
    # Normalizziamo per il confronto.
    import sympy

    assert sympy.simplify(result.exact) == sympy.sympify("x**2 + 2*x + 1")


def test_simplify_input_vuoto():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_simplify_input_pericoloso():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("__import__('os').system('echo pwned')")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_simplify_espressione_banale():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("x + x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*x"