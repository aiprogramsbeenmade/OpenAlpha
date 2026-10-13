"""
Test del parser.

Verificano: precedenze, associatività, moltiplicazione implicita,
unario, parentesi, chiamate di funzione, errori di sintassi.
"""

from __future__ import annotations

import pytest

from openalpha.core.exceptions import ParserError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Number,
    Symbol,
    UnaryOp,
)
from openalpha.parser.parser import parse_tokens
from openalpha.parser.tokenizer import tokenize


def _parse(s: str):
    return parse_tokens(tokenize(s))


# ---------------------------------------------------------------------------
# Atomi
# ---------------------------------------------------------------------------

def test_numero():
    assert _parse("2") == Number("2")


def test_simbolo():
    assert _parse("x") == Symbol("x")


def test_parentesi_ridondanti():
    assert _parse("(x)") == Symbol("x")


# ---------------------------------------------------------------------------
# Operatori binari
# ---------------------------------------------------------------------------

def test_somma():
    assert _parse("2 + 3") == BinaryOp("+", Number("2"), Number("3"))


def test_sottrazione():
    assert _parse("5 - 3") == BinaryOp("-", Number("5"), Number("3"))


def test_moltiplicazione():
    assert _parse("2 * 3") == BinaryOp("*", Number("2"), Number("3"))


def test_divisione():
    assert _parse("6 / 2") == BinaryOp("/", Number("6"), Number("2"))


# ---------------------------------------------------------------------------
# Precedenze
# ---------------------------------------------------------------------------

def test_precedenza_moltiplicazione_su_somma():
    # 2 + 3 * 4 == 2 + (3 * 4)
    assert _parse("2 + 3 * 4") == BinaryOp(
        "+",
        Number("2"),
        BinaryOp("*", Number("3"), Number("4")),
    )


def test_precedenza_somma_a_sinistra():
    # 2 * 3 + 4 == (2 * 3) + 4
    assert _parse("2 * 3 + 4") == BinaryOp(
        "+",
        BinaryOp("*", Number("2"), Number("3")),
        Number("4"),
    )


def test_parentesi_forzano_precedenza():
    # (2 + 3) * 4
    assert _parse("(2 + 3) * 4") == BinaryOp(
        "*",
        BinaryOp("+", Number("2"), Number("3")),
        Number("4"),
    )


# ---------------------------------------------------------------------------
# Associatività
# ---------------------------------------------------------------------------

def test_somma_associativa_a_sinistra():
    # 1 + 2 + 3 == (1 + 2) + 3
    assert _parse("1 + 2 + 3") == BinaryOp(
        "+",
        BinaryOp("+", Number("1"), Number("2")),
        Number("3"),
    )


def test_potenza_associativa_a_destra():
    # 2 ** 3 ** 2 == 2 ** (3 ** 2)
    assert _parse("2 ** 3 ** 2") == BinaryOp(
        "**",
        Number("2"),
        BinaryOp("**", Number("3"), Number("2")),
    )


def test_potenza_con_circonflesso():
    assert _parse("x ^ 2") == BinaryOp("^", Symbol("x"), Number("2"))


# ---------------------------------------------------------------------------
# Unario
# ---------------------------------------------------------------------------

def test_meno_unario():
    assert _parse("-x") == UnaryOp("-", Symbol("x"))


def test_piu_unario():
    assert _parse("+x") == UnaryOp("+", Symbol("x"))


def test_meno_unario_doppio():
    assert _parse("--x") == UnaryOp("-", UnaryOp("-", Symbol("x")))


def test_meno_unario_ha_precedenza_minore_della_potenza():
    # -x**2 == -(x**2)
    assert _parse("-x**2") == UnaryOp(
        "-",
        BinaryOp("**", Symbol("x"), Number("2")),
    )


# ---------------------------------------------------------------------------
# Moltiplicazione implicita
# ---------------------------------------------------------------------------

def test_moltiplicazione_implicita_numero_simbolo():
    assert _parse("2x") == BinaryOp("*", Number("2"), Symbol("x"))


def test_moltiplicazione_implicita_numero_parentesi():
    assert _parse("2(x+1)") == BinaryOp(
        "*",
        Number("2"),
        BinaryOp("+", Symbol("x"), Number("1")),
    )


def test_moltiplicazione_implicita_parentesi_parentesi():
    assert _parse("(x+1)(x-1)") == BinaryOp(
        "*",
        BinaryOp("+", Symbol("x"), Number("1")),
        BinaryOp("-", Symbol("x"), Number("1")),
    )


def test_moltiplicazione_implicita_numero_numero():
    assert _parse("2 3") == BinaryOp("*", Number("2"), Number("3"))


# ---------------------------------------------------------------------------
# Funzioni
# ---------------------------------------------------------------------------

def test_chiamata_funzione():
    assert _parse("sin(x)") == FunctionCall("sin", Symbol("x"))


def test_funzione_con_espressione():
    assert _parse("sin(x + 1)") == FunctionCall(
        "sin",
        BinaryOp("+", Symbol("x"), Number("1")),
    )


def test_funzione_annidata():
    assert _parse("sin(cos(x))") == FunctionCall(
        "sin",
        FunctionCall("cos", Symbol("x")),
    )


def test_funzione_nome_non_controllato_dal_parser():
    # Il parser accetta qualsiasi nome; il validatore (T2.4) filtrerà.
    assert _parse("pippo(x)") == FunctionCall("pippo", Symbol("x"))


# ---------------------------------------------------------------------------
# Errori di sintassi
# ---------------------------------------------------------------------------

def test_espressione_incompleta():
    with pytest.raises(ParserError):
        _parse("2 +")


def test_parentesi_non_chiusa():
    with pytest.raises(ParserError):
        _parse("(x")


def test_parentesi_non_aperta():
    with pytest.raises(ParserError):
        _parse("x)")


def test_operatore_senza_operandi():
    with pytest.raises(ParserError):
        _parse("*")


def test_token_in_eccesso():
    # Parentesi chiusa senza apertura: errore reale.
    with pytest.raises(ParserError):
        _parse("2 )")