"""
Operazione ``ceil``: funzione parte intera superiore.

Restituisce il più piccolo intero ≥ x.

Esempi::

    ceil("2.1")   -> 3
    ceil("-2.7")  -> -2
    ceil("5")     -> 5
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import (
    OpenAlphaError,
    ParserError,
    UnsupportedOperationError,
)
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


@register(
    name="ceil",
    description="Parte intera superiore di un numero.",
)
def ceil(expression: str) -> Result:
    """Calcola ``ceil(expression)``."""
    base = {"input_expression": expression, "operation": "ceil"}

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    if not expr.is_number or expr.free_symbols:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"ceil richiede un numero, ricevuto: {expr}",
        )

    try:
        result = sympy.ceiling(expr)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare ceil: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )