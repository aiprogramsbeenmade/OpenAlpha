"""
Parser di OpenAlpha.

Espone la funzione ``parse_expression``, che è la catena completa
di parsing: tokenize → parse → validate → to_sympy. Ogni operazione
matematica che deve interpretare input utente passa da qui.

Eccezioni sollevate (da catturare nelle operazioni e tradurre in
``Result`` con lo status appropriato):

- ``ParserError`` (incluso ``ValidationError``): l'input non è
  sintatticamente valido o viola le regole di policy.
  → ``Result(status=ERROR)``.
- ``UnsupportedOperationError``: l'input è valido ma usa una funzione
  che OpenAlpha non implementa.
  → ``Result(status=UNSUPPORTED)``.
"""

from __future__ import annotations

import sympy

from openalpha.parser.parser import parse_tokens
from openalpha.parser.to_sympy import to_sympy
from openalpha.parser.tokenizer import tokenize
from openalpha.parser.validator import validate

__all__ = ["parse_expression"]


def parse_expression(input_expression: str) -> sympy.Expr:
    """Interpreta una stringa e restituisce un oggetto SymPy.

    Catena completa: tokenize → parse → validate → to_sympy.

    Args:
        input_expression: espressione matematica come stringa.

    Returns:
        L'oggetto SymPy corrispondente.

    Solleva:
        ParserError: input sintatticamente non valido o troppo grande.
        ValidationError: input che viola le regole di policy.
        UnsupportedOperationError: input valido ma con funzionalità
            non implementate.
    """
    tokens = tokenize(input_expression)
    ast = parse_tokens(tokens)
    validate(ast, input_length=len(input_expression))
    return to_sympy(ast)