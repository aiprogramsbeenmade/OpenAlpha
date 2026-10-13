"""
Test del tokenizer.

Verificano: riconoscimento di numeri, nomi, operatori, parentesi;
gestione di notazione scientifica; rifiuto di caratteri non ammessi;
rifiuto di input vuoto; presenza del token EOF; posizioni corrette.
"""

from __future__ import annotations

import pytest

from openalpha.core.exceptions import ParserError
from openalpha.parser.tokenizer import Token, TokenType, tokenize


def _values(tokens: list[Token]) -> list[str]:
    """Estrae i valori testuali, escludendo EOF."""
    return [t.value for t in tokens if t.type is not TokenType.EOF]


def _types(tokens: list[Token]) -> list[TokenType]:
    """Estrae i tipi, escludendo EOF."""
    return [t.type for t in tokens if t.type is not TokenType.EOF]


# ---------------------------------------------------------------------------
# Riconoscimento base
# ---------------------------------------------------------------------------

def test_numero_semplice():
    tokens = tokenize("2")
    assert _types(tokens) == [TokenType.NUMBER]
    assert _values(tokens) == ["2"]


def test_operatore_semplice():
    tokens = tokenize("+")
    assert _types(tokens) == [TokenType.OPERATOR]
    assert _values(tokens) == ["+"]


def test_espressione_banale():
    tokens = tokenize("2 + 3")
    assert _types(tokens) == [
        TokenType.NUMBER,
        TokenType.OPERATOR,
        TokenType.NUMBER,
    ]
    assert _values(tokens) == ["2", "+", "3"]


def test_parentesi():
    tokens = tokenize("(x)")
    assert _types(tokens) == [
        TokenType.LPAREN,
        TokenType.NAME,
        TokenType.RPAREN,
    ]


def test_funzione():
    tokens = tokenize("sin(x)")
    assert _types(tokens) == [
        TokenType.NAME,
        TokenType.LPAREN,
        TokenType.NAME,
        TokenType.RPAREN,
    ]
    assert _values(tokens) == ["sin", "(", "x", ")"]


# ---------------------------------------------------------------------------
# Numeri
# ---------------------------------------------------------------------------

def test_numero_decimale():
    tokens = tokenize("3.14")
    assert _values(tokens) == ["3.14"]


def test_notazione_scientifica():
    tokens = tokenize("1e-3")
    assert _values(tokens) == ["1e-3"]


def test_notazione_scientifica_maiuscola():
    tokens = tokenize("2.5E+6")
    assert _values(tokens) == ["2.5E+6"]


# ---------------------------------------------------------------------------
# Nomi
# ---------------------------------------------------------------------------

def test_nome_con_cifre():
    tokens = tokenize("x1 + y2")
    assert _values(tokens) == ["x1", "+", "y2"]


def test_nome_lungo():
    tokens = tokenize("alpha + beta")
    assert _values(tokens) == ["alpha", "+", "beta"]


# ---------------------------------------------------------------------------
# Operatori
# ---------------------------------------------------------------------------

def test_potenza_doppio_asterisco():
    tokens = tokenize("x**2")
    assert _values(tokens) == ["x", "**", "2"]


def test_potenza_circonflesso():
    tokens = tokenize("x^2")
    assert _values(tokens) == ["x", "^", "2"]


def test_moltiplicazione_esplicita():
    tokens = tokenize("2 * x")
    assert _values(tokens) == ["2", "*", "x"]


# ---------------------------------------------------------------------------
# Spazi
# ---------------------------------------------------------------------------

def test_spazi_ignorati():
    tokens = tokenize("  2   +   3  ")
    assert _values(tokens) == ["2", "+", "3"]


def test_spazi_non_obbligatori():
    tokens = tokenize("2+3")
    assert _values(tokens) == ["2", "+", "3"]


# ---------------------------------------------------------------------------
# EOF
# ---------------------------------------------------------------------------

def test_eof_presente():
    tokens = tokenize("2")
    assert tokens[-1].type is TokenType.EOF


def test_eof_posizione_fine_input():
    tokens = tokenize("2 + 3")
    assert tokens[-1].position == 5


# ---------------------------------------------------------------------------
# Posizioni
# ---------------------------------------------------------------------------

def test_posizioni_corrette():
    tokens = tokenize("2 + 3")
    assert tokens[0].position == 0  # "2"
    assert tokens[1].position == 2  # "+"
    assert tokens[2].position == 4  # "3"


# ---------------------------------------------------------------------------
# Errori
# ---------------------------------------------------------------------------

def test_input_vuoto_rifiutato():
    with pytest.raises(ParserError, match="vuoto"):
        tokenize("")


def test_input_solo_spazi_rifiutato():
    with pytest.raises(ParserError, match="vuoto"):
        tokenize("   ")


def test_carattere_non_ammesso_rifiutato():
    with pytest.raises(ParserError, match="non ammesso"):
        tokenize("2 @ 3")


def test_carattere_non_ammesso_posizione_riportata():
    with pytest.raises(ParserError, match="posizione 2"):
        tokenize("2 @ 3")