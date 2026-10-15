"""
Operazione ``laplace_transform``: trasformata di Laplace.

Calcola L{f(t)}(s) = ∫₀^∞ e^(-st) f(t) dt.

Esempi::

    laplace_transform("1")                -> 1/s
    laplace_transform("exp(-a*t)")        -> 1/(a + s)
    laplace_transform("t")                -> 1/s**2
    laplace_transform("sin(t)")           -> 1/(s**2 + 1)
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
    name="laplace_transform",
    description="Trasformata di Laplace di un'espressione.",
)
def laplace_transform(
    expression: str,
    t: str = "t",
    s: str = "s",
) -> Result:
    """Calcola la trasformata di Laplace di ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "laplace_transform",
    }

    if not t or not t.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile t non valida: {t!r}",
        )
    if not s or not s.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile s non valida: {s!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    t_sym = sympy.Symbol(t)
    s_sym = sympy.Symbol(s)

    try:
        risultato = sympy.laplace_transform(expr, t_sym, s_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la trasformata: {exc}",
        )

    # SymPy restituisce una tupla (risultato, convergenza, condizioni).
    # Prendiamo solo il risultato.
    if isinstance(risultato, tuple) and len(risultato) >= 1:
        valore = risultato[0]
        condizioni = []
        if len(risultato) >= 3 and risultato[2] is not True and risultato[2] is not None:
            condizioni.append(str(risultato[2]))
    else:
        valore = risultato
        condizioni = []

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(valore),
        conditions=condizioni,
        metadata={"t": t, "s": s},
    )