"""
Test dell'operazione "factor".
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

# Importiamo il package per attivare la registrazione via decoratore.
import openalpha.operations  # noqa: F401


def _equivalente(ottenuto: str, atteso: str) -> bool:
    """Verifica equivalenza matematica tra due espressioni."""
    a = sympy.sympify(ottenuto)
    b = sympy.sympify(atteso)
    return sympy.simplify(a - b) == 0


def test_factor_registrata():
    assert "factor" in list_operations()
    spec = get_operation("factor")
    assert spec.name == "factor"


def test_factor_quadrato_perfetto():
    from openalpha.operations.algebra.factor import factor

    result = factor("x**2 + 2*x + 1")
    assert result.status is ResultStatus.EXACT
    assert _equivalente(result.exact, "(x + 1)**2")


def test_factor_differenza_di_quadrati():
    from openalpha.operations.algebra.factor import factor

    result = factor("x**2 - 1")
    assert result.status is ResultStatus.EXACT
    assert _equivalente(result.exact, "(x - 1)*(x + 1)")


def test_factor_trinomio():
    from openalpha.operations.algebra.factor import factor

    result = factor("x**2 + 5*x + 6")
    assert result.status is ResultStatus.EXACT
    assert _equivalente(result.exact, "(x + 2)*(x + 3)")


def test_factor_espressione_gia_fattorizzata():
    from openalpha.operations.algebra.factor import factor

    result = factor("x + x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*x"


def test_factor_input_vuoto():
    from openalpha.operations.algebra.factor import factor

    result = factor("")
    assert result.status is ResultStatus.ERROR


def test_factor_sintassi_invalida():
    from openalpha.operations.algebra.factor import factor

    result = factor("2 +")
    assert result.status is ResultStatus.ERROR


def test_factor_funzione_non_supportata():
    from openalpha.operations.algebra.factor import factor

    result = factor("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "pippo" in (result.error or "")


def test_factor_operazione_sul_registro_dal_nome():
    spec = get_operation("factor")
    result = spec.function("x**2 - 1")
    assert result.status is ResultStatus.EXACT

def test_factor_denominatore_restituisce_partial():
    from openalpha.operations.algebra.factor import factor

    result = factor("1/x + 1/x**2")
    assert result.status is ResultStatus.PARTIAL
    assert "x != 0" in result.conditions


def test_factor_polinomio_resta_exact():
    from openalpha.operations.algebra.factor import factor

    result = factor("x**2 - 1")
    assert result.status is ResultStatus.EXACT
    assert result.conditions == []