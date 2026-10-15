"""
Operazione ``degree``: grado di un polinomio.

Calcola il grado di un polinomio rispetto a una variabile.

Esempi::

    degree("x**3 + x + 1")               -> 3
    degree("x**2*y + x*y**2", var="x")   -> 2
    degree("x**2*y + x*y**2", var="y")   -> 2
    degree("5")                          -> 0
    degree("0")                          -> -oo
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
    name="degree",
    description="Grado di un polinomio rispetto a una variabile.",
)
def degree(expression: str, var: str = "x") -> Result:
    """Calcola il grado di ``expression`` rispetto a ``var``."""
    base = {
        "input_expression": expression,
        "operation": "degree",
    }

    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    var_sym = sympy.Symbol(var)

    try:
        result = sympy.degree(expr, var_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il grado: {exc}",
        )

    exact_str = str(result)
    latex_str = "-\\infty" if exact_str == "-oo" else exact_str

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={
            "var": var,
            "latex_exact": latex_str,
        },
    )