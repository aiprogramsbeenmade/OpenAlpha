"""
Operazione ``coeff``: coefficiente di un polinomio.

Restituisce il coefficiente del termine di grado ``n``.

Esempi::

    coeff("x**3 + 2*x + 1", n="1")   -> 2
    coeff("x**3 + 2*x + 1", n="0")   -> 1
    coeff("x**3 + 2*x + 1", n="2")   -> 0
    coeff("x**3 + a*x + 1", n="1")   -> a
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
    name="coeff",
    description="Coefficiente del termine di grado n di un polinomio.",
)
def coeff(
    expression: str,
    var: str = "x",
    n: str = "0",
) -> Result:
    """Restituisce il coefficiente di ``var**n`` in ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "coeff",
    }

    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )

    try:
        n_int = int(n)
    except (ValueError, TypeError):
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"grado non valido: {n!r}",
        )
    if n_int < 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"il grado deve essere ≥ 0, ricevuto {n_int}",
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
        result = expr.coeff(var_sym, n_int)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il coefficiente: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
        metadata={"var": var, "n": n_int},
    )