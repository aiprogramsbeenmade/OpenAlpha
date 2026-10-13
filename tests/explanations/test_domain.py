"""
Test della raccolta delle condizioni di validità.
"""

from __future__ import annotations

import sympy

from openalpha.explanations.domain import collect_conditions


def _cond(s: str) -> list[str]:
    """Utility: parsa una stringa e raccoglie le condizioni."""
    return collect_conditions(sympy.sympify(s))


# ---------------------------------------------------------------------------
# Nessuna condizione
# ---------------------------------------------------------------------------

def test_espressione_senza_condizioni():
    assert _cond("x + 1") == []


def test_polinomio_senza_condizioni():
    assert _cond("x**2 + 2*x + 1") == []


def test_funzione_senza_condizioni():
    assert _cond("sin(x)") == []


def test_costante_senza_condizioni():
    assert _cond("pi") == []


# ---------------------------------------------------------------------------
# Denominatori
# ---------------------------------------------------------------------------

def test_denominatore_semplice():
    assert _cond("1/x") == ["x != 0"]


def test_denominatore_composto():
    conditions = _cond("1/(x + 1)")
    assert conditions == ["x + 1 != 0"]


def test_denominatore_quadrato():
    # 1/x**2 è Pow(x, -2), esponente negativo.
    conditions = _cond("1/x**2")
    assert conditions == ["x != 0"]


def test_divisione_esplicita():
    # a/b è Mul(a, Pow(b, -1)).
    conditions = _cond("a/b")
    assert conditions == ["b != 0"]


# ---------------------------------------------------------------------------
# Radici quadrate
# ---------------------------------------------------------------------------

def test_radice_semplice():
    assert _cond("sqrt(x)") == ["x >= 0"]


def test_radice_composta():
    assert _cond("sqrt(x + 1)") == ["x + 1 >= 0"]


# ---------------------------------------------------------------------------
# Logaritmi
# ---------------------------------------------------------------------------

def test_log_semplice():
    assert _cond("log(x)") == ["x > 0"]


def test_log_composto():
    assert _cond("log(x + 1)") == ["x + 1 > 0"]


# ---------------------------------------------------------------------------
# Combinazioni
# ---------------------------------------------------------------------------

def test_piu_denominatori():
    conditions = _cond("1/x + 1/y")
    assert "x != 0" in conditions
    assert "y != 0" in conditions


def test_denominatore_e_radice():
    conditions = _cond("sqrt(1/x)")
    assert any("x != 0" in c for c in conditions)
    assert any(">= 0" in c for c in conditions)


def test_denominatore_e_log():
    conditions = _cond("log(x) / y")
    assert "y != 0" in conditions
    assert "x > 0" in conditions


# ---------------------------------------------------------------------------
# Niente duplicati
# ---------------------------------------------------------------------------

def test_condizione_non_duplicata():
    # 1/x + 2/x: due denominatori, stessa condizione.
    conditions = _cond("1/x + 2/x")
    assert conditions == ["x != 0"]


def test_condizioni_multiple_non_duplicate():
    conditions = _cond("1/x + 1/y + 1/x")
    assert conditions.count("x != 0") == 1
    assert conditions.count("y != 0") == 1