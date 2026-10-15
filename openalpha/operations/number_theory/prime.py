"""
Operazione ``prime``: n-esimo numero primo.

Restituisce l'n-esimo numero primo (1-indexed: prime(1) = 2).

Esempi::

    prime(1)   -> 2
    prime(10)  -> 29
    prime(100) -> 541
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
    name="prime",
    description="Restituisce l'n-esimo numero primo.",
)
def prime(expression: str) -> Result:
    """Restituisce l'n-esimo primo, dove ``expression`` è n."""
    base = {"input_expression": expression, "operation": "prime"}

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
            error=f"l'indice deve essere un intero, ricevuto: {expr}",
        )

    n = int(expr)
    if n < 1:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"l'indice deve essere ≥ 1, ricevuto: {n}",
        )

    try:
        result = sympy.prime(n)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare l'n-esimo primo: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )