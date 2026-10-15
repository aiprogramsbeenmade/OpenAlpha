"""
Operazione ``collect``: raccolta per variabile.

Raccoglie i termini di un'espressione in potenze della variabile data.
Utile per vedere un polinomio in forma standard.

Esempi::

    collect("x**2 + 2*x + 1 + 3*x**3")  -> 3*x**3 + x**2 + 2*x + 1
    collect("x*y + x*z + x", var="x")   -> x*(y + z + 1)
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.operations._base import apply_sympy_operation


def _collect(expr: sympy.Expr, var: str) -> sympy.Expr:
    """Wrapper per ``sympy.collect`` con variabile simbolica."""
    return sympy.collect(expr, sympy.Symbol(var))


@register(
    name="collect",
    description="Raccoglie i termini in potenze della variabile data.",
)
def collect(expression: str, var: str = "x") -> Result:
    """Raccoglie ``expression`` rispetto a ``var``."""
    if not var or not var.isidentifier():
        return Result(
            input_expression=expression,
            operation="collect",
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )
    return apply_sympy_operation(
        expression,
        "collect",
        _collect,
        var=var,
    )