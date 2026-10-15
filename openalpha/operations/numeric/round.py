"""
Operazione ``round``: arrotondamento al più vicino.

Arrotonda un numero al più vicino intero (o a ``digits`` cifre decimali).
Usa il banking rounding di Python (round half to even).

Esempi::

    round("2.4")       -> 2
    round("2.5")       -> 2       (banker's rounding)
    round("2.6")       -> 3
    round("2.567", 2)  -> 2.57
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import (
    OpenAlphaError,
    ParserError,
    UnsupportedOperationError,
)
import builtins
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


@register(
    name="round",
    description="Arrotonda un numero al più vicino intero o a N cifre.",
)
def round(expression: str, digits: int = 0) -> Result:
    """Arrotonda ``expression`` a ``digits`` cifre decimali."""
    base = {"input_expression": expression, "operation": "round"}

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    if not expr.is_number or expr.free_symbols:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"l'arrotondamento richiede un numero, ricevuto: {expr}",
        )

    try:
        float_val = float(expr)
        result = builtins.round(float_val, int(digits))
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile arrotondare: {exc}",
        )

    # Se digits=0, restituisci un intero; altrimenti un float.
    if int(digits) == 0:
        exact_str = str(int(result))
    else:
        exact_str = str(result)

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
    )