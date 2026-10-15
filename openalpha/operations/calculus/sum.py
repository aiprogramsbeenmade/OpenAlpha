"""
Operazione ``sum``: sommatoria.

Calcola Σ_{var=lower}^{upper} expr.

Esempi::

    sum("n", "n", "1", "10")        -> 55
    sum("n**2", "n", "1", "10")     -> 385
    sum("1/n**2", "n", "1", "oo")   -> pi**2/6
    sum("x**n", "n", "0", "oo")     -> 1/(1 - x)
    sum("1/2**n", "n", "0", "oo")   -> 2
"""

from __future__ import annotations

import builtins
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

# Alias per l'infinito (come in limit.py).
_INFINITY_ALIASES = {
    "oo": sympy.oo,
    "inf": sympy.oo,
    "+oo": sympy.oo,
    "+inf": sympy.oo,
    "-oo": -sympy.oo,
    "-inf": -sympy.oo,
}


def _parse_estremo(s: str) -> sympy.Expr:
    """Interpreta un estremo (numero, ``oo``, ecc.)."""
    stripped = s.strip()
    if stripped in _INFINITY_ALIASES:
        return _INFINITY_ALIASES[stripped]
    return parse_expression(stripped)


@register(
    name="sum",
    description="Sommatoria di un'espressione su un intervallo.",
)
def sum(
    expression: str,
    var: str = "n",
    lower: str = "1",
    upper: str = "oo",
) -> Result:
    """Calcola Σ_{var=lower}^{upper} ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "sum",
    }

    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )

    try:
        expr = parse_expression(expression)
        low = _parse_estremo(lower)
        up = _parse_estremo(upper)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    var_sym = sympy.Symbol(var)

    try:
        result_expr = sympy.summation(expr, (var_sym, low, up))
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la sommatoria: {exc}",
        )

    # Se SymPy restituisce un oggetto Sum non valutato, è unsupported.
    if isinstance(result_expr, sympy.Sum):
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=(
                "SymPy non riesce a calcolare questa sommatoria in forma chiusa."
            ),
        )

    # Estrai eventuali condizioni (es. |x| < 1).
    condizioni = []
    for cond in getattr(result_expr, "args", []):
        if isinstance(cond, sympy.core.relational.Relational):
            condizioni.append(str(cond))

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result_expr),
        conditions=condizioni,
        metadata={
            "var": var,
            "lower": lower,
            "upper": upper,
        },
    )