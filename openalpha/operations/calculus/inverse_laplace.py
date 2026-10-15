"""
Operazione ``inverse_laplace``: trasformata di Laplace inversa.

Calcola L⁻¹{F(s)}(t).

Esempi::

    inverse_laplace("1/s")           -> 1
    inverse_laplace("1/(s**2 + 1)")  -> sin(t)
    inverse_laplace("1/s**2")        -> t
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
    name="inverse_laplace",
    description="Trasformata di Laplace inversa di un'espressione.",
)
def inverse_laplace(
    expression: str,
    s: str = "s",
    t: str = "t",
) -> Result:
    """Calcola la trasformata di Laplace inversa di ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "inverse_laplace",
    }

    if not s or not s.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile s non valida: {s!r}",
        )
    if not t or not t.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile t non valida: {t!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    s_sym = sympy.Symbol(s)
    t_sym = sympy.Symbol(t)

    try:
        valore = sympy.inverse_laplace_transform(expr, s_sym, t_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la trasformata inversa: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(valore),
        metadata={"s": s, "t": t},
    )