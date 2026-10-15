"""
Operazione ``divisors``: divisori di un intero.

Restituisce la lista di tutti i divisori positivi di un intero.

Esempi::

    divisors(12)  -> [1, 2, 3, 4, 6, 12]
    divisors(7)   -> [1, 7]
    divisors(1)   -> [1]
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
from openalpha.explanations.numeric.divisors import explain_divisors
from openalpha.parser import parse_expression


@register(
    name="divisors",
    description="Restituisce i divisori positivi di un intero.",
)
def divisors(expression: str) -> Result:
    """Restituisce i divisori di ``expression``."""
    base = {"input_expression": expression, "operation": "divisors"}

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
            error=f"il calcolo dei divisori richiede un intero, ricevuto: {expr}",
        )

    n = int(expr)
    if n <= 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"il calcolo dei divisori richiede un intero positivo, ricevuto: {n}",
        )

    try:
        divs = sympy.divisors(n)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare i divisori: {exc}",
        )

    exact_str = "[" + ", ".join(str(d) for d in divs) + "]"
    latex_str = "\\{" + ", ".join(str(d) for d in divs) + "\\}"

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        steps=explain_divisors(n),
        metadata={
            "divisors": [int(d) for d in divs],
            "latex_exact": latex_str,
        },
    )