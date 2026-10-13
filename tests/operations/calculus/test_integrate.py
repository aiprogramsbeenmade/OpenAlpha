"""
Test dell'operazione "integrate".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_integrate_registrata():
    assert "integrate" in list_operations()
    spec = get_operation("integrate")
    assert spec.name == "integrate"


def test_integrate_indefinito_x():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "x**2/2 + C"


def test_integrate_indefinito_sin():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("sin(x)")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "-cos(x) + C"


def test_integrate_indefinito_x_quadrato():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("x**2")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "x**3/3 + C"


def test_integrate_indefinito_uno_su_x_partial():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("1/x")
    assert result.status is ResultStatus.PARTIAL
    assert "log(x)" in result.exact
    assert "x != 0" in result.conditions


def test_integrate_indefinito_var_diversa():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("y", var="y")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "y**2/2 + C"


def test_integrate_definito_x():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("x", lower="0", upper="1")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1/2"


def test_integrate_definito_sin():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("sin(x)", lower="0", upper="pi")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2"


def test_integrate_definito_a_infinito():
    from openalpha.operations.calculus.integrate import integrate

    # integrale di e^{-x} da 0 a oo = 1
    result = integrate("exp(-x)", lower="0", upper="oo")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_integrate_solo_lower_errore():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("x", lower="0")
    assert result.status is ResultStatus.ERROR
    assert "entrambi" in (result.error or "")


def test_integrate_solo_upper_errore():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("x", upper="1")
    assert result.status is ResultStatus.ERROR


def test_integrate_input_vuoto():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("")
    assert result.status is ResultStatus.ERROR


def test_integrate_funzione_non_supportata():
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_integrate_funzione_speciale():
    """exp(x**2) ha primitiva non elementare, ma SymPy la calcola
    con la funzione speciale erfi. Il risultato è valido."""
    from openalpha.operations.calculus.integrate import integrate

    result = integrate("exp(x**2)")
    assert result.status is ResultStatus.EXACT
    assert "erfi" in result.exact


def test_integrate_non_calcolabile_unsupported():
    """Un integrale che SymPy NON riesce a calcolare affatto."""
    from openalpha.operations.calculus.integrate import integrate

    # Funzione non riconosciuta dal parser → UNSUPPORTED.
    result = integrate("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_integrate_operazione_sul_registro_dal_nome():
    spec = get_operation("integrate")
    result = spec.function("x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "x**2/2 + C"