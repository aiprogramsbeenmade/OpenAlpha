"""
Parser a discesa ricorsiva per le espressioni matematiche di OpenAlpha.

Trasforma una lista di token (T2.1) in un AST (``ast_nodes``).
Rispetta precedenze e associatività standard.

Grammatica supportata::

    expression  := term (('+' | '-') term)*
    term        := factor (('*' | '/') factor | implicit factor)*
    factor      := ('-' | '+') factor | power
    power       := atom ('**' | '^') factor
    atom        := NUMBER
                 | NAME
                 | NAME '(' expression ')'
                 | '(' expression ')'

Note:
- La moltiplicazione implicita (``2x``, ``2(x+1)``, ``(x+1)(x-1)``) è
  gestita nella regola ``term``.
- La potenza è associativa a destra: ``2**3**2 == 2**(3**2)``.
- L'unario meno ha precedenza minore della potenza:
  ``-x**2 == -(x**2)``.
"""

from __future__ import annotations

from openalpha.core.exceptions import ParserError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Node,
    Number,
    Symbol,
    UnaryOp,
)
from openalpha.parser.tokenizer import Token, TokenType

# Tipi di token che possono iniziare un "factor", usati per decidere
# se c'è moltiplicazione implicita.
_FACTOR_START = (TokenType.NUMBER, TokenType.NAME, TokenType.LPAREN)


class _Parser:
    """Parser a discesa ricorsiva su una lista di token.

    Stato interno: la lista di token e l'indice corrente. I metodi
    ``_parse_*`` consumano token avanzando l'indice.
    """

    def __init__(self, tokens: list[Token]) -> None:
        if not tokens:
            raise ParserError("lista di token vuota")
        self._tokens = tokens
        self._pos = 0

    # ----- utilità ---------------------------------------------------

    def _peek(self) -> Token:
        """Token corrente, senza consumarlo."""
        return self._tokens[self._pos]

    def _advance(self) -> Token:
        """Consuma e restituisce il token corrente."""
        token = self._tokens[self._pos]
        if token.type is not TokenType.EOF:
            self._pos += 1
        return token

    def _expect(self, token_type: TokenType, value: str | None = None) -> Token:
        """Consuma un token del tipo atteso, o solleva ``ParserError``."""
        token = self._peek()
        if token.type is not token_type:
            raise ParserError(
                f"atteso {token_type.value}, "
                f"trovato {token.type.value} {token.value!r} "
                f"alla posizione {token.position}"
            )
        if value is not None and token.value != value:
            raise ParserError(
                f"atteso {value!r}, "
                f"trovato {token.value!r} alla posizione {token.position}"
            )
        return self._advance()

    # ----- regole della grammatica -----------------------------------

    def parse(self) -> Node:
        """Entry point: parsa l'intera lista di token.

        Dopo aver parsato un'espressione, deve restare solo il token
        EOF. Altrimenti l'input ha token in eccesso (es. ``x)`` o
        ``x y z`` non gestito).
        """
        node = self._parse_expression()
        if self._peek().type is not TokenType.EOF:
            token = self._peek()
            raise ParserError(
                f"token inatteso {token.value!r} alla posizione {token.position}"
            )
        return node

    def _parse_expression(self) -> Node:
        """expression := term (('+' | '-') term)*"""
        left = self._parse_term()
        while (
            self._peek().type is TokenType.OPERATOR
            and self._peek().value in ("+", "-")
        ):
            op = self._advance().value
            right = self._parse_term()
            left = BinaryOp(op, left, right)
        return left

    def _parse_term(self) -> Node:
        """term := factor (('*' | '/') factor | implicit factor)*"""
        left = self._parse_factor()
        while True:
            token = self._peek()

            # Operatore esplicito * o /
            if token.type is TokenType.OPERATOR and token.value in ("*", "/"):
                op = self._advance().value
                right = self._parse_factor()
                left = BinaryOp(op, left, right)
                continue

            # Moltiplicazione implicita: dopo un fattore, se il prossimo
            # token può iniziare un nuovo fattore, moltiplica.
            if token.type in _FACTOR_START:
                right = self._parse_factor()
                left = BinaryOp("*", left, right)
                continue

            break
        return left

    def _parse_factor(self) -> Node:
        """factor := ('-' | '+') factor | power"""
        token = self._peek()
        if token.type is TokenType.OPERATOR and token.value in ("+", "-"):
            op = self._advance().value
            operand = self._parse_factor()
            return UnaryOp(op, operand)
        return self._parse_power()

    def _parse_power(self) -> Node:
        """power := atom ('**' | '^') factor

        Il lato destro è un ``factor``, non un ``power``, per ottenere
        l'associatività a destra: ``2**3**2 == 2**(3**2)``.
        """
        base = self._parse_atom()
        token = self._peek()
        if token.type is TokenType.OPERATOR and token.value in ("**", "^"):
            op = self._advance().value
            exponent = self._parse_factor()
            return BinaryOp(op, base, exponent)
        return base

    def _parse_atom(self) -> Node:
        """atom := NUMBER | NAME | NAME '(' expression ')' | '(' expression ')'"""
        token = self._peek()

        if token.type is TokenType.NUMBER:
            self._advance()
            return Number(token.value)

        if token.type is TokenType.NAME:
            self._advance()
            # Se il prossimo token è '(', è una chiamata di funzione.
            if self._peek().type is TokenType.LPAREN:
                self._advance()  # consuma '('
                argument = self._parse_expression()
                self._expect(TokenType.RPAREN)
                return FunctionCall(token.value, argument)
            return Symbol(token.value)

        if token.type is TokenType.LPAREN:
            self._advance()  # consuma '('
            node = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return node

        raise ParserError(
            f"token inatteso {token.value!r} alla posizione {token.position}"
        )


def parse_tokens(tokens: list[Token]) -> Node:
    """Parsa una lista di token in un AST.

    Args:
        tokens: lista prodotta da ``tokenize``, terminata da EOF.

    Returns:
        Il nodo radice dell'AST.

    Solleva:
        ParserError: se la sequenza di token non è un'espressione valida.
    """
    return _Parser(tokens).parse()