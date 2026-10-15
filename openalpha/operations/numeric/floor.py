"""
Operazione ``floor``: funzione parte intera inferiore.

Restituisce il più grande intero ≤ x.

Esempi::

    floor("2.7")   -> 2
    floor("-2.1")  -> -3
    floor("5")     -> 5
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
    name="floor",
    description="Parte intera inferiore di un numero.",
)
def floor(expression: str) -> Result:
    """Calcola ``floor(expression)``."""
    base = {"input_expression": expression, "operation": "floor"}

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
            error=f"floor richiede un numero, ricevuto: {expr}",
        )

    try:
        result = sympy.floor(expr)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare floor: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )