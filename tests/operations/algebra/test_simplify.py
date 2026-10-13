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
    import sympy

    result = simplify("(x + 1)**2")
    assert result.status is ResultStatus.EXACT
    # Verifichiamo equivalenza matematica, non forma specifica.
    assert sympy.simplify(sympy.sympify(result.exact) - sympy.sympify("(x + 1)**2")) == 0


def test_simplify_input_vuoto():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_simplify_input_pericoloso():
    """Input che tenta di eseguire codice: deve essere rifiutato.

    Il parser non riconosce l'apostrofo `'`, quindi l'input viene
    rifiutato come errore di sintassi da `tokenize`. Non arriva
    nemmeno al convertitore.
    """
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("__import__('os').system('echo pwned')")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_simplify_funzione_non_supportata():
    """Funzione sintatticamente valida ma non implementata."""
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "pippo" in (result.error or "")

def test_simplify_sintassi_invalida():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("2 +")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_simplify_input_troppo_lungo():
    from openalpha.operations.algebra.simplify import simplify

    # 2000 caratteri: supera MAX_INPUT_LENGTH = 1000.
    lungo = "x + " * 500 + "x"
    result = simplify(lungo)
    assert result.status is ResultStatus.ERROR
    assert "lungo" in (result.error or "")


def test_simplify_espressione_banale():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("x + x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*x"

def test_simplify_denominatore_restituisce_partial():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("1/x")
    assert result.status is ResultStatus.PARTIAL
    assert "x != 0" in result.conditions


def test_simplify_radice_restituisce_partial():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("sqrt(x)")
    assert result.status is ResultStatus.PARTIAL
    assert "x >= 0" in result.conditions


def test_simplify_log_restituisce_partial():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("log(x)")
    assert result.status is ResultStatus.PARTIAL
    assert "x > 0" in result.conditions


def test_simplify_polinomio_resta_exact():
    from openalpha.operations.algebra.simplify import simplify

    result = simplify("x**2 + 2*x + 1")
    assert result.status is ResultStatus.EXACT
    assert result.conditions == []