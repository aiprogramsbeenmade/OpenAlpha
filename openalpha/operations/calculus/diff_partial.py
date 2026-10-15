"""
Operazione ``diff_partial``: derivata parziale.

Calcola la derivata parziale di un'espressione rispetto a una
variabile, trattando le altre come costanti.

Esempi::

    diff_partial("x**2 + y**2", var="x")  -> 2*x
    diff_partial("x**2 + y**2", var="y")  -> 2*y
    diff_partial("x*y + x + y", var="x")  -> y + 1
    diff_partial("sin(x*y)", var="x")     -> y*cos(x*y)
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
    name="diff_partial",
    description="Derivata parziale rispetto a una variabile.",
)
def diff_partial(
    expression: str,
    var: str = "x",
    order: int = 1,
) -> Result:
    """Calcola la derivata parziale di ``expression`` rispetto a ``var``.

    Args:
        expression: espressione da derivare.
        var: variabile di derivazione (default ``"x"``).
        order: ordine della derivata (default 1).

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo.
    """
    base = {
        "input_expression": expression,
        "operation": "diff_partial",
    }

    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )

    try:
        order_int = int(order)
    except (ValueError, TypeError):
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"ordine non valido: {order!r}",
        )
    if order_int < 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"l'ordine deve essere ≥ 0, ricevuto {order_int}",
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
        result_expr = sympy.diff(expr, var_sym, order_int)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la derivata parziale: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result_expr),
        metadata={"var": var, "order": order_int},
    )