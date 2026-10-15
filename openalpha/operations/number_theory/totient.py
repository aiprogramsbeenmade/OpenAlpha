"""
Operazione ``totient``: funzione φ di Eulero.

Calcola il numero di interi positivi minori o uguali a n che sono
coprimi con n.

Esempi::

    totient(10)  -> 4       (1, 3, 7, 9 sono coprimi con 10)
    totient(7)   -> 6
    totient(1)   -> 1
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
    name="totient",
    description="Calcola la funzione φ di Eulero.",
)
def totient(expression: str) -> Result:
    """Calcola φ(``expression``)."""
    base = {"input_expression": expression, "operation": "totient"}

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    if not expr.is_Integer:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"φ di Eulero richiede un intero, ricevuto: {expr}",
        )

    n = int(expr)
    if n <= 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"φ di Eulero richiede un intero positivo, ricevuto: {n}",
        )

    try:
        result = sympy.totient(n)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare φ: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )