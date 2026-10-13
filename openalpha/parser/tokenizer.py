"""
Tokenizer per le espressioni matematiche di OpenAlpha.

Trasforma una stringa in una lista di ``Token``. Non interpreta la
struttura dell'espressione: quello è compito del parser (T2.2).

La sintassi supportata è volutamente limitata:

- Numeri: interi, decimali (con punto), notazione scientifica (``1e-3``).
- Nomi: identificatori che iniziano con lettera o underscore, seguiti
  da lettere, cifre o underscore (``x``, ``alpha``, ``x1``).
- Operatori: ``+``, ``-``, ``*``, ``/``, ``**``, ``^``.
- Parentesi: ``(`` e ``)``.

Tutto il resto viene rifiutato con ``ParserError`` e con la posizione
del carattere problematico, per messaggi d'errore utili.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from openalpha.core.exceptions import ParserError


class TokenType(str, Enum):
    """Tipo di un token."""

    NUMBER = "number"
    NAME = "name"
    OPERATOR = "operator"
    LPAREN = "lparen"
    RPAREN = "rparen"
    EOF = "eof"  # sentinella di fine input


@dataclass(frozen=True)
class Token:
    """Token prodotto dal tokenizer.

    Attributi:
        type: tipo del token.
        value: valore testuale del token (es. ``"2"``, ``"sin"``, ``"+"``).
        position: indice del primo carattere del token nella stringa
            originale. Serve per messaggi d'errore posizionati.
    """

    type: TokenType
    value: str
    position: int

    def __str__(self) -> str:
        return f"{self.type.value}({self.value!r})@{self.position}"


# Operatori riconosciuti, in ordine di lunghezza decrescente.
# L'ordine conta: "**" deve essere riconosciuto prima di "*".
_OPERATORS = ("**", "+", "-", "*", "/", "^")

# Caratteri che possono iniziare un nome.
_NAME_START = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")

# Caratteri che possono proseguire un nome.
_NAME_CONT = _NAME_START | set("0123456789")

# Cifre.
_DIGITS = set("0123456789")


def _is_name_start(ch: str) -> bool:
    return ch in _NAME_START


def _is_name_cont(ch: str) -> bool:
    return ch in _NAME_CONT


def _is_digit(ch: str) -> bool:
    return ch in _DIGITS


def _tokenize_number(text: str, start: int) -> tuple[Token, int]:
    """Riconosce un numero a partire da ``start``.

    Restituisce il token e la posizione successiva da esaminare.
    Supporta: interi, decimali (``3.14``), notazione scientifica
    (``1e-3``, ``2.5E+6``).
    """
    i = start
    n = len(text)
    saw_dot = False
    saw_exp = False

    while i < n:
        ch = text[i]
        if _is_digit(ch):
            i += 1
        elif ch == "." and not saw_dot and not saw_exp:
            saw_dot = True
            i += 1
        elif ch in ("e", "E") and not saw_exp:
            # Notazione scientifica: deve essere seguita da cifra,
            # oppure da + o - e poi cifra.
            if i + 1 < n and text[i + 1] in ("+", "-"):
                if i + 2 < n and _is_digit(text[i + 2]):
                    saw_exp = True
                    i += 2
                else:
                    break
            elif i + 1 < n and _is_digit(text[i + 1]):
                saw_exp = True
                i += 1
            else:
                break
        else:
            break

    value = text[start:i]
    return Token(TokenType.NUMBER, value, start), i


def _tokenize_name(text: str, start: int) -> tuple[Token, int]:
    """Riconosce un nome a partire da ``start``."""
    i = start
    n = len(text)
    while i < n and _is_name_cont(text[i]):
        i += 1
    value = text[start:i]
    return Token(TokenType.NAME, value, start), i


def tokenize(input_expression: str) -> list[Token]:
    """Trasforma una stringa in una lista di token.

    Args:
        input_expression: espressione matematica come stringa.

    Returns:
        Lista di ``Token``, terminata sempre da un token ``EOF``.

    Solleva:
        ParserError: se l'input è vuoto o contiene solo spazi, o se
            contiene un carattere non riconosciuto.
    """
    if input_expression is None or not input_expression.strip():
        raise ParserError("input vuoto o composto solo da spazi")

    tokens: list[Token] = []
    i = 0
    n = len(input_expression)

    while i < n:
        ch = input_expression[i]

        # Spazi: saltati, ma registrano separazione (utile al parser
        # per decidere sulla moltiplicazione implicita).
        if ch.isspace():
            i += 1
            continue

        # Parentesi
        if ch == "(":
            tokens.append(Token(TokenType.LPAREN, ch, i))
            i += 1
            continue
        if ch == ")":
            tokens.append(Token(TokenType.RPAREN, ch, i))
            i += 1
            continue

        # Numeri (devono iniziare con una cifra)
        if _is_digit(ch):
            token, i = _tokenize_number(input_expression, i)
            tokens.append(token)
            continue

        # Nomi (devono iniziare con lettera o underscore)
        if _is_name_start(ch):
            token, i = _tokenize_name(input_expression, i)
            tokens.append(token)
            continue

        # Operatori (controlla prima i più lunghi: "**" prima di "*")
        matched_op = None
        for op in _OPERATORS:
            if input_expression.startswith(op, i):
                matched_op = op
                break
        if matched_op is not None:
            tokens.append(Token(TokenType.OPERATOR, matched_op, i))
            i += len(matched_op)
            continue

        # Carattere non riconosciuto
        raise ParserError(
            f"carattere non ammesso: {ch!r} alla posizione {i}"
        )

    tokens.append(Token(TokenType.EOF, "", n))
    return tokens