"""
Test dell'operazione "expand".

Verificano: espansione di prodotti notevoli, differenza di quadrati,
registrazione nel registro, gestione di errori (input vuoto,
sintassi malformata, funzione non supportata).
"""

from __future__ import annotations

import sympy
import pytest

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

# Importiamo il package per attivare la registrazione via decoratore.
import openalpha.operations  # noqa: F401


def test_expand_registrata():
    assert "expand" in list_operations()
    spec = get_operation("expand")
    assert spec.name == "expand"


def test_expand_prodotto_notevole():
    from openalpha.operations.algebra.expand import expand

    result = expand("(x + 1)**2")
    assert result.status is ResultStatus.EXACT
    # Confronto per equivalenza matematica, non per forma.
    atteso = sympy.sympify("x**2 + 2*x + 1")
    ottenuto = sympy.sympify(result.exact)
    assert sympy.simplify(ottenuto - atteso) == 0


def test_expand_differenza_di_quadrati():
    from openalpha.operations.algebra.expand import expand

    result = expand("(x + 1)*(x - 1)")
    assert result.status is ResultStatus.EXACT
    atteso = sympy.sympify("x**2 - 1")
    ottenuto = sympy.sympify(result.exact)
    assert sympy.simplify(ottenuto - atteso) == 0


def test_expand_cubo():
    from openalpha.operations.algebra.expand import expand

    result = expand("(a + b)**3")
    assert result.status is ResultStatus.EXACT
    atteso = sympy.sympify("a**3 + 3*a**2*b + 3*a*b**2 + b**3")
    ottenuto = sympy.sympify(result.exact)
    assert sympy.simplify(ottenuto - atteso) == 0


def test_expand_espressione_gia_semplice():
    from openalpha.operations.algebra.expand import expand

    result = expand("x + x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*x"


def test_expand_input_vuoto():
    from openalpha.operations.algebra.expand import expand

    result = expand("")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_expand_sintassi_invalida():
    from openalpha.operations.algebra.expand import expand

    result = expand("2 +")
    assert result.status is ResultStatus.ERROR
    assert result.error is not None


def test_expand_funzione_non_supportata():
    from openalpha.operations.algebra.expand import expand

    result = expand("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "pippo" in (result.error or "")


def test_expand_operazione_sul_registro_dal_nome():
    """Verifica che l'operazione sia invocabile per nome, come farà la CLI."""
    spec = get_operation("expand")
    result = spec.function("(x + 1)**2")
    assert result.status is ResultStatus.EXACT

def test_expand_denominatore_restituisce_partial():
    from openalpha.operations.algebra.expand import expand

    result = expand("1/(x + 1)")
    assert result.status is ResultStatus.PARTIAL
    assert "x + 1 != 0" in result.conditions


def test_expand_polinomio_resta_exact():
    from openalpha.operations.algebra.expand import expand

    result = expand("(x + 1)**2")
    assert result.status is ResultStatus.EXACT
    assert result.conditions == []