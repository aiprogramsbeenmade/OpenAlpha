"""
Operazione ``apart``: decomposizione in frazioni parziali.

Scompone una frazione razionale nella somma di frazioni più semplici.
Utile in integrazione e nello studio di funzioni razionali.

Esempi::

    apart("1/(x**2 - 1)")  -> 1/(2*(x - 1)) - 1/(2*(x + 1))
    apart("(x**2 + 1)/x")  -> x + 1/x
    apart("1/(x*(x+1))")   -> 1/x - 1/(x + 1)
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.operations._base import apply_sympy_operation


def _apart(expr: sympy.Expr, var: str) -> sympy.Expr:
    """Wrapper per ``sympy.apart`` con variabile simbolica."""
    return sympy.apart(expr, sympy.Symbol(var))


@register(
    name="apart",
    description="Decompone una frazione razionale in frazioni parziali.",
)
def apart(expression: str, var: str = "x") -> Result:
    """Scompone ``expression`` in frazioni parziali rispetto a ``var``."""
    if not var or not var.isidentifier():
        return Result(
            input_expression=expression,
            operation="apart",
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )
    return apply_sympy_operation(
        expression,
        "apart",
        _apart,
        var=var,
    )