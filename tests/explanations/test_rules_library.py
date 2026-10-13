"""
Test della libreria di regole concrete.
"""

from __future__ import annotations

import pytest
import sympy

from openalpha.explanations.rules import apply_rule
from openalpha.explanations.rules_library import default_rules


def _rule(name: str):
    for r in default_rules():
        if r.name == name:
            return r
    raise ValueError(f"regola non trovata: {name}")


# ---------------------------------------------------------------------------
# square_of_binomial
# ---------------------------------------------------------------------------

def test_square_of_binomial_si_applica():
    rule = _rule("square_of_binomial")
    x, y = sympy.symbols("x y")
    result = apply_rule(rule, (x + y) ** 2)
    assert result is not None
    assert sympy.simplify(result - (x**2 + 2 * x * y + y**2)) == 0


# ---------------------------------------------------------------------------
# difference_of_squares
# ---------------------------------------------------------------------------


def test_difference_of_squares_si_applica():
    rule = _rule("difference_of_squares")
    x, y = sympy.symbols("x y")
    result = apply_rule(rule, x**2 - y**2)
    assert result is not None
    assert sympy.simplify(result - (x - y) * (x + y)) == 0


# ---------------------------------------------------------------------------
# common_factor
# ---------------------------------------------------------------------------

def test_common_factor_si_applica():
    rule = _rule("common_factor")
    x, y, z = sympy.symbols("x y z")
    result = apply_rule(rule, x * y + x * z)
    assert result is not None
    assert sympy.simplify(result - x * (y + z)) == 0


# ---------------------------------------------------------------------------
# cancel_common_factor
# ---------------------------------------------------------------------------

def test_cancel_common_factor_si_applica():
    rule = _rule("cancel_common_factor")
    x, y, z = sympy.symbols("x y z")
    result = apply_rule(rule, (x * y) / (x * z))
    assert result is not None
    assert sympy.simplify(result - y / z) == 0


# ---------------------------------------------------------------------------
# power_of_power
# ---------------------------------------------------------------------------

def test_power_of_power_si_applica():
    rule = _rule("power_of_power")
    x, y, z = sympy.symbols("x y z")
    result = apply_rule(rule, (x**y) ** z)
    # SymPy potrebbe semplificare (x**y)**z in x**(y*z) già in costruzione.
    # Se è già semplificato, il pattern non matcha.
    # Accettiamo entrambi i comportamenti.
    if result is None:
        # Già semplificato da SymPy.
        assert (x**y) ** z == x ** (y * z)
    else:
        assert sympy.simplify(result - x ** (y * z)) == 0


# ---------------------------------------------------------------------------
# default_rules
# ---------------------------------------------------------------------------

def test_default_rules_contiene_cinque_regole():
    rules = default_rules()
    assert len(rules) == 5
    names = {r.name for r in rules}
    assert names == {
        "square_of_binomial",
        "difference_of_squares",
        "common_factor",
        "cancel_common_factor",
        "power_of_power",
    }


def test_default_rules_univoche():
    rules = default_rules()
    names = [r.name for r in rules]
    assert len(names) == len(set(names))


def test_difference_of_squares_rifiuta_caso_degenere():
    """x + 1 non deve matchare difference_of_squares."""
    rule = _rule("difference_of_squares")
    x = sympy.Symbol("x")
    # x + 1 = x - (-1). SymPy potrebbe scomporlo in (sqrt(x))**2 - (I)**2,
    # ma la condition lo rifiuta.
    result = apply_rule(rule, x + 1)
    assert result is None

def test_difference_of_squares_non_si_applica_a_quadrato_perfetto():
    """x**2 + 2*x + 1 NON è una differenza di quadrati."""
    rule = _rule("difference_of_squares")
    x = sympy.Symbol("x")
    result = apply_rule(rule, x**2 + 2 * x + 1)
    assert result is None


def test_difference_of_squares_non_si_applica_a_somma_di_quadrati():
    """x**2 + y**2 NON è una differenza di quadrati."""
    rule = _rule("difference_of_squares")
    x, y = sympy.symbols("x y")
    result = apply_rule(rule, x**2 + y**2)
    assert result is None


def test_difference_of_squares_si_applica_a_quadrati_semplici():
    rule = _rule("difference_of_squares")
    x, y = sympy.symbols("x y")
    result = apply_rule(rule, x**2 - y**2)
    assert result is not None
    assert sympy.simplify(result - (x - y) * (x + y)) == 0


def test_difference_of_squares_con_quadrati_di_binomio():
    rule = _rule("difference_of_squares")
    x = sympy.Symbol("x")
    # (x + 1)**2 - (x - 1)**2
    expr = (x + 1) ** 2 - (x - 1) ** 2
    result = apply_rule(rule, expr)
    assert result is not None
    # Il risultato è ((x+1) - (x-1)) * ((x+1) + (x-1)) = 2 * 2*x = 4*x
    assert sympy.simplify(result - 4 * x) == 0