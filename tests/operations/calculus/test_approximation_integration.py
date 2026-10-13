"""
Test dell'integrazione dell'approssimazione nelle operazioni.
"""

from __future__ import annotations

from openalpha.operations.algebra.simplify import simplify
from openalpha.operations.calculus.diff import diff
from openalpha.operations.calculus.integrate import integrate
from openalpha.operations.calculus.limit import limit

import openalpha.operations  # noqa: F401


def test_simplify_sqrt_due_approssimato():
    result = simplify("sqrt(2)")
    assert result.exact == "sqrt(2)"
    assert result.approximate is not None
    assert result.approximate.startswith("1.41421")


def test_simplify_espressione_simbolica_senza_approssimazione():
    result = simplify("x + 1")
    assert result.exact == "x + 1"
    assert result.approximate is None


def test_limit_approssimato():
    result = limit("sin(x)/x")
    assert result.exact == "1"
    assert result.approximate is not None


def test_diff_simbolica_senza_approssimazione():
    result = diff("sin(x)")
    assert result.exact == "cos(x)"
    assert result.approximate is None


def test_integrate_definito_approssimato():
    result = integrate("exp(-x**2)", lower="0", upper="oo")
    # Il risultato è sqrt(pi)/2, approssimabile.
    assert result.approximate is not None