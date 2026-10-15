"""
Test per l'operazione ``dsolve``.
"""

from __future__ import annotations

import pytest

from openalpha.core.status import ResultStatus
from openalpha.operations.calculus.dsolve import dsolve


# ---------------------------------------------------------------------------
# Registrazione
# ---------------------------------------------------------------------------

def test_dsolve_registrata():
    """L'operazione è nel registry."""
    from openalpha.core.registry import get_operation
    spec = get_operation("dsolve")
    assert spec.name == "dsolve"


# ---------------------------------------------------------------------------
# ODE del primo ordine
# ---------------------------------------------------------------------------

def test_dsolve_y_prime_uguale_y():
    """y' = y -> y(x) = C1*exp(x)."""
    result = dsolve("y' = y")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact
    assert "C1" in result.exact


def test_dsolve_y_prime_piu_y_uguale_zero():
    """y' + y = 0 -> y(x) = C1*exp(-x)."""
    result = dsolve("y' + y = 0")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact


def test_dsolve_y_prime_uguale_2y():
    """y' = 2y -> y(x) = C1*exp(2*x)."""
    result = dsolve("y' = 2*y")
    assert result.status == ResultStatus.EXACT
    assert "C1" in result.exact


def test_dsolve_leibniz_dy_dx():
    """dy/dx = y -> y(x) = C1*exp(x)."""
    result = dsolve("dy/dx = y")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact


def test_dsolve_funzione_f():
    """f' = f -> f(x) = C1*exp(x)."""
    result = dsolve("f' = f")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact


# ---------------------------------------------------------------------------
# ODE del secondo ordine
# ---------------------------------------------------------------------------

def test_dsolve_y_secondo_piu_y_uguale_zero():
    """y'' + y = 0 -> y(x) = C1*sin(x) + C2*cos(x)."""
    result = dsolve("y'' + y = 0")
    assert result.status == ResultStatus.EXACT
    assert "sin" in result.exact
    assert "cos" in result.exact


def test_dsolve_y_secondo_meno_y_uguale_zero():
    """y'' - y = 0 -> y(x) = C1*exp(x) + C2*exp(-x)."""
    result = dsolve("y'' - y = 0")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact


def test_dsolve_y_secondo_piu_4y_uguale_zero():
    """y'' + 4y = 0 -> y(x) = C1*sin(2*x) + C2*cos(2*x)."""
    result = dsolve("y'' + 4*y = 0")
    assert result.status == ResultStatus.EXACT
    assert "sin" in result.exact
    assert "cos" in result.exact


def test_dsolve_leibniz_secondo_ordine():
    """d2y/dx2 + y = 0 -> y(x) = C1*sin(x) + C2*cos(x)."""
    result = dsolve("d2y/dx2 + y = 0")
    assert result.status == ResultStatus.EXACT
    assert "sin" in result.exact


# ---------------------------------------------------------------------------
# Condizioni iniziali
# ---------------------------------------------------------------------------

def test_dsolve_con_condizione_iniziale_primo_ordine():
    """y' = y, y(0) = 1 -> y(x) = exp(x)."""
    result = dsolve("y' = y, y(0) = 1")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact
    # Non ci sono costanti libere.
    assert "C1" not in result.exact


def test_dsolve_con_due_condizioni_iniziali_secondo_ordine():
    """y'' + y = 0, y(0) = 0, y'(0) = 1 -> y(x) = sin(x)."""
    result = dsolve("y'' + y = 0, y(0) = 0, y'(0) = 1")
    assert result.status == ResultStatus.EXACT
    assert "sin" in result.exact
    assert "C1" not in result.exact
    assert "C2" not in result.exact


def test_dsolve_condizione_iniziale_negativa():
    """y' = -y, y(0) = 5 -> y(x) = 5*exp(-x)."""
    result = dsolve("y' = -y, y(0) = 5")
    assert result.status == ResultStatus.EXACT
    assert "exp" in result.exact


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def test_dsolve_metadata_contiene_var():
    """Il metadata contiene 'var'."""
    result = dsolve("y' = y")
    assert result.metadata["var"] == "x"


def test_dsolve_metadata_contiene_func():
    """Il metadata contiene 'func'."""
    result = dsolve("y' = y")
    assert result.metadata["func"] == "y"


def test_dsolve_metadata_con_f():
    """Il metadata riflette la funzione usata."""
    result = dsolve("f' = f")
    assert result.metadata["func"] == "f"


# ---------------------------------------------------------------------------
# Errori
# ---------------------------------------------------------------------------

def test_dsolve_input_vuoto():
    """Input vuoto -> errore."""
    result = dsolve("")
    assert result.status == ResultStatus.ERROR


def test_dsolve_senza_derivate():
    """Nessuna derivata -> errore."""
    result = dsolve("y = y")
    assert result.status == ResultStatus.ERROR
    assert "derivata" in result.error.lower()


def test_dsolve_senza_uguale():
    """Nessun '=' -> errore."""
    result = dsolve("y'")
    assert result.status == ResultStatus.ERROR
    assert "=" in result.error


def test_dsolve_condizione_senza_uguale():
    """Condizione malformata -> errore."""
    result = dsolve("y' = y, y(0)")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Casi limite
# ---------------------------------------------------------------------------

def test_dsolve_equazione_non_risolvibile():
    """Equazione non lineare difficile -> unsupported (non crash)."""
    result = dsolve("y' = y**2 + x**2")
    # SymPy potrebbe riuscire o no. Accettiamo sia EXACT che UNSUPPORTED,
    # ma non deve crashare.
    assert result.status in (ResultStatus.EXACT, ResultStatus.UNSUPPORTED)


def test_dsolve_steps_vuoti():
    """dsolve non produce passaggi."""
    result = dsolve("y' = y")
    assert result.steps == []


def test_dsolve_conditions_vuote():
    """dsolve non produce condizioni."""
    result = dsolve("y' = y")
    assert result.conditions == []