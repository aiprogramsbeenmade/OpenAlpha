"""
Operazione ``isprime``: test di primalità.

Verifica se un intero positivo è primo.

Esempi::

    isprime(7)   -> True
    isprime(8)   -> False
    isprime(97)  -> True
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
from openalpha.explanations.numeric.isprime import explain_isprime


@register(
    name="isprime",
    description="Verifica se un intero è primo.",
)
def isprime(expression: str) -> Result:
    """Verifica se ``expression`` è primo."""
    base = {"input_expression": expression, "operation": "isprime"}

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
            error=f"il test di primalità richiede un intero, ricevuto: {expr}",
        )

    try:
        result = sympy.isprime(int(expr))
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile eseguire il test: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact="True" if result else "False",
        steps=explain_isprime(int(expr)),
        metadata={
            "latex_exact": "\\text{Vero}" if result else "\\text{Falso}",
        },
    )