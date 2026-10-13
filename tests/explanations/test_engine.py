"""
Test del motore delle spiegazioni.
"""

from __future__ import annotations

import pytest
import sympy

from openalpha.explanations.engine import explain


def test_nessuna_regola_applicabile():
    """Un'espressione semplice senza regole applicabili."""
    result = explain(sympy.sympify("x + 1"))
    assert result.steps == []
    assert result.complete is False
    assert "nessun procedimento" in result.message


def test_quadrato_del_binomio():
    x, y = sympy.symbols("x y")
    result = explain((x + y) ** 2)
    assert len(result.steps) >= 1
    # Il primo step è il quadrato del binomio.
    assert result.steps[0].rule_name == "square_of_binomial"



def test_differenza_di_quadrati():
    x, y = sympy.symbols("x y")
    result = explain(x**2 - y**2)
    assert len(result.steps) >= 1
    assert result.steps[0].rule_name == "difference_of_squares"


def test_step_sono_verificati():
    """Ogni step prodotto dal motore è verificato."""
    x, y = sympy.symbols("x y")
    result = explain((x + y) ** 2)
    for step in result.steps:
        # before e after non sono identici (verificato da Step).
        assert step.before != step.after
        # rule_name non è vuoto.
        assert step.rule_name


def test_motore_non_loop_infinito():
    """Il motore non entra in loop su espressioni complicate."""
    x, y, z = sympy.symbols("x y z")
    # Espressione con più regole applicabili.
    result = explain((x + y) ** 2 - z**2)
    # Il motore si ferma. Non controlliamo quanti step produce,
    # solo che termini.
    assert isinstance(result.steps, list)