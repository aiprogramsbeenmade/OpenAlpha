"""
Test della conversione AST → SymPy.

Verificano: numeri, simboli, costanti, operatori binari, unario,
funzioni ammesse, funzioni non ammesse, annidamento.

Nota: SymPy semplifica automaticamente durante la costruzione
(es. ``x + x`` diventa ``2*x``). Dove serve verificare la struttura,
usiamo ``sympy.srepr`` o confronti per uguaglianza matematica,
non per struttura sintattica.
"""

from __future__ import annotations

import sympy
import pytest

from openalpha.core.exceptions import UnsupportedOperationError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Number,
    Symbol,
    UnaryOp,
)
from openalpha.parser.to_sympy import to_sympy


# ---------------------------------------------------------------------------
# Numeri
# ---------------------------------------------------------------------------

def test_numero_intero():
    result = to_sympy(Number("2"))
    assert result == sympy.Integer(2)
    assert isinstance(result, sympy.Integer)


def test_numero_decimale():
    result = to_sympy(Number("3.14"))
    assert result == sympy.Float(3.14)
    assert isinstance(result, sympy.Float)


def test_numero_notazione_scientifica():
    result = to_sympy(Number("1e-3"))
    assert result == sympy.Float(0.001)


# ---------------------------------------------------------------------------
# Simboli e costanti
# ---------------------------------------------------------------------------

def test_simbolo_libero():
    result = to_sympy(Symbol("x"))
    assert result == sympy.Symbol("x")
    assert isinstance(result, sympy.Symbol)


def test_costante_pi():
    result = to_sympy(Symbol("pi"))
    assert result == sympy.pi


def test_costante_e():
    result = to_sympy(Symbol("e"))
    assert result == sympy.E


def test_costante_E_maiuscola():
    result = to_sympy(Symbol("E"))
    assert result == sympy.E


# ---------------------------------------------------------------------------
# Operatori binari
# ---------------------------------------------------------------------------

def test_somma():
    result = to_sympy(BinaryOp("+", Number("2"), Number("3")))
    assert result == sympy.Integer(5)


def test_sottrazione():
    result = to_sympy(BinaryOp("-", Number("5"), Number("3")))
    assert result == sympy.Integer(2)


def test_moltiplicazione_con_simbolo():
    result = to_sympy(BinaryOp("*", Number("2"), Symbol("x")))
    assert result == 2 * sympy.Symbol("x")


def test_divisione():
    result = to_sympy(BinaryOp("/", Number("6"), Number("3")))
    assert result == sympy.Integer(2)


def test_potenza():
    result = to_sympy(BinaryOp("**", Symbol("x"), Number("2")))
    assert result == sympy.Symbol("x") ** 2


def test_potenza_con_circonflesso_alias():
    result_caret = to_sympy(BinaryOp("^", Symbol("x"), Number("2")))
    result_star = to_sympy(BinaryOp("**", Symbol("x"), Number("2")))
    assert result_caret == result_star


# ---------------------------------------------------------------------------
# Unario
# ---------------------------------------------------------------------------

def test_meno_unario():
    result = to_sympy(UnaryOp("-", Symbol("x")))
    assert result == -sympy.Symbol("x")


def test_piu_unario():
    result = to_sympy(UnaryOp("+", Symbol("x")))
    assert result == sympy.Symbol("x")


# ---------------------------------------------------------------------------
# Funzioni
# ---------------------------------------------------------------------------

def test_funzione_sin():
    result = to_sympy(FunctionCall("sin", Symbol("x")))
    assert result == sympy.sin(sympy.Symbol("x"))


def test_funzione_sqrt():
    result = to_sympy(FunctionCall("sqrt", Symbol("x")))
    assert result == sympy.sqrt(sympy.Symbol("x"))


def test_funzione_abs_alias():
    result_lower = to_sympy(FunctionCall("abs", Symbol("x")))
    result_upper = to_sympy(FunctionCall("Abs", Symbol("x")))
    assert result_lower == result_upper
    assert result_lower == sympy.Abs(sympy.Symbol("x"))


def test_funzione_annidata():
    node = FunctionCall(
        "sin",
        FunctionCall("cos", Symbol("x")),
    )
    result = to_sympy(node)
    x = sympy.Symbol("x")
    assert result == sympy.sin(sympy.cos(x))


def test_funzione_non_supportata():
    with pytest.raises(UnsupportedOperationError, match="pippo"):
        to_sympy(FunctionCall("pippo", Symbol("x")))


# ---------------------------------------------------------------------------
# Espressioni composte
# ---------------------------------------------------------------------------

def test_espressione_composta():
    # 2*x + 1
    node = BinaryOp(
        "+",
        BinaryOp("*", Number("2"), Symbol("x")),
        Number("1"),
    )
    result = to_sympy(node)
    x = sympy.Symbol("x")
    assert result == 2 * x + 1