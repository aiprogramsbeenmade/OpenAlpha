"""
Operazione ``product``: produttoria.

Calcola Π_{var=lower}^{upper} expr.

Esempi::

    product("n", "n", "1", "5")     -> 120
    product("n", "n", "1", "10")    -> 3628800
    product("(n+1)/n", "n", "1", "5") -> 6
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
    name="product",
    description="Produttoria di un'espressione su un intervallo.",
)
def product(
    expression: str,
    var: str = "n",
    lower: str = "1",
    upper: str = "oo",
) -> Result:
    """Calcola Π_{var=lower}^{upper} ``expression``."""
    base = {
        "input_expression": expression,
        "operation": "product",
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
        result_expr = sympy.product(expr, (var_sym, low, up))
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare la produttoria: {exc}",
        )

    if isinstance(result_expr, sympy.Product):
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=(
                "SymPy non riesce a calcolare questa produttoria in forma chiusa."
            ),
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result_expr),
        metadata={
            "var": var,
            "lower": lower,
            "upper": upper,
        },
    )