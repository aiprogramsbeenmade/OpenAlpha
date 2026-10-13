"""
Test dell'operazione "limit".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_limit_registrata():
    assert "limit" in list_operations()
    spec = get_operation("limit")
    assert spec.name == "limit"


def test_limit_sin_x_su_x():
    from openalpha.operations.calculus.limit import limit

    result = limit("sin(x)/x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_limit_razionale_a_zero():
    from openalpha.operations.calculus.limit import limit

    # lim_{x -> 0} (x**2 - 1)/(x - 1) = (-1)/(-1) = 1
    result = limit("(x**2 - 1)/(x - 1)")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_limit_razionale_a_punto_di_singolarita():
    from openalpha.operations.calculus.limit import limit

    # lim_{x -> 1} (x**2 - 1)/(x - 1) = lim_{x -> 1} (x + 1) = 2
    result = limit("(x**2 - 1)/(x - 1)", point="1")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2"

def test_limit_razionale_a_punto_di_singolarita():
    from openalpha.operations.calculus.limit import limit

    result = limit("(x**2 - 1)/(x - 1)", point="1")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2"


def test_limit_a_infinito():
    from openalpha.operations.calculus.limit import limit

    result = limit("sin(x)/x", point="oo")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "0"


def test_limit_polinomio_a_infinito():
    from openalpha.operations.calculus.limit import limit

    result = limit("x**2", point="oo")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "oo"


def test_limit_a_punto_concreto():
    from openalpha.operations.calculus.limit import limit

    result = limit("sin(x)", point="pi/2")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_limit_variabile_diversa():
    from openalpha.operations.calculus.limit import limit

    # sin(y)/y con y -> 0
    result = limit("sin(y)/y", var="y")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_limit_input_vuoto():
    from openalpha.operations.calculus.limit import limit

    result = limit("")
    assert result.status is ResultStatus.ERROR


def test_limit_funzione_non_supportata():
    from openalpha.operations.calculus.limit import limit

    result = limit("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_limit_inesistente_unsupported():
    """Il limite di 1/x a 0 non esiste (bilaterale)."""
    from openalpha.operations.calculus.limit import limit

    result = limit("1/x", point="0")
    # SymPy restituisce AccumBounds o nan. Il nostro codice lo
    # classifica come UNSUPPORTED.
    assert result.status is ResultStatus.UNSUPPORTED


def test_limit_operazione_sul_registro_dal_nome():
    spec = get_operation("limit")
    result = spec.function("sin(x)/x", var="x", point="0")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"