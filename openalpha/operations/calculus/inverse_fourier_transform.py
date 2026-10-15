"""
Operazione ``inverse_fourier_transform``: trasformata di Fourier inversa.

Calcola F⁻¹{k → x}.

Esempi::

    inverse_fourier_transform("exp(-pi**2*k**2)", "k", "x")
        -> exp(-x**2) / sqrt(pi)
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
    name="inverse_fourier_transform",
    description="Trasformata di Fourier inversa di un'espressione.",
)
def inverse_fourier_transform(
    expression: str,
    k: str = "k",
    x: str = "x",
) -> Result:
    """Calcola la trasformata di Fourier inversa di ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "inverse_fourier_transform",
    }

    if not k or not k.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile k non valida: {k!r}",
        )
    if not x or not x.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile x non valida: {x!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    k_sym = sympy.Symbol(k)
    x_sym = sympy.Symbol(x)

    try:
        valore = sympy.inverse_fourier_transform(expr, k_sym, x_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la trasformata inversa: {exc}",
        )

    # Se SymPy restituisce un oggetto InverseFourierTransform non valutato.
    if isinstance(valore, sympy.InverseFourierTransform):
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=(
                "SymPy non riesce a calcolare questa trasformata "
                "inversa in forma chiusa."
            ),
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(valore),
        metadata={"k": k, "x": x},
    )