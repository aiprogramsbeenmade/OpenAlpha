"""
Operazione ``factorial``: fattoriale.

Calcola ``n! = n * (n-1) * ... * 1``.

Esempi::

    factorial("5")   -> 120
    factorial("0")   -> 1
    factorial("20")  -> 2432902008176640000
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
from openalpha.explanations.numeric.factorial import explain_factorial
from openalpha.parser import parse_expression


@register(
    name="factorial",
    description="Fattoriale di un intero non negativo.",
)
def factorial(expression: str) -> Result:
    """Calcola ``expression!``."""
    base = {"input_expression": expression, "operation": "factorial"}

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
            error=f"il fattoriale richiede un intero, ricevuto: {expr}",
        )

    n = int(expr)
    if n < 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"il fattoriale richiede n ≥ 0, ricevuto: {n}",
        )

    try:
        result = sympy.factorial(n)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il fattoriale: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
        steps=explain_factorial(n),
    )