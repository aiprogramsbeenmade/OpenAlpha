"""
Operazione ``fourier_transform``: trasformata di Fourier.

Calcola F(k) = ∫_{-∞}^∞ f(x) e^(-2πi k x) dx (convenzione SymPy).

Esempi::

    fourier_transform("exp(-x**2)", "x", "k")
        -> sqrt(pi) * exp(-pi**2 * k**2)
    fourier_transform("1", "x", "k")
        -> DiracDelta(k)
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
    name="fourier_transform",
    description="Trasformata di Fourier di un'espressione.",
)
def fourier_transform(
    expression: str,
    x: str = "x",
    k: str = "k",
) -> Result:
    """Calcola la trasformata di Fourier di ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "fourier_transform",
    }

    if not x or not x.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile x non valida: {x!r}",
        )
    if not k or not k.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile k non valida: {k!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    x_sym = sympy.Symbol(x)
    k_sym = sympy.Symbol(k)

    # Caso speciale: funzioni costanti.
    # F{c} = c * DiracDelta(k) (nel senso delle distribuzioni).
    # SymPy non lo calcola automaticamente, quindi lo gestiamo noi.
    if expr.is_constant():
        valore = expr * sympy.DiracDelta(k_sym)
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact=str(valore),
            metadata={"x": x, "k": k},
        )

    try:
        valore = sympy.fourier_transform(expr, x_sym, k_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la trasformata: {exc}",
        )

    # Se SymPy restituisce un oggetto FourierTransform non valutato,
    # la trasformata non è calcolabile in forma chiusa.
    if isinstance(valore, sympy.FourierTransform):
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=(
                "SymPy non riesce a calcolare questa trasformata "
                "in forma chiusa."
            ),
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(valore),
        metadata={"x": x, "k": k},
    )