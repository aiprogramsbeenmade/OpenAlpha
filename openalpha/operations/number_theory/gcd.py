"""
Operazione ``gcd``: massimo comun divisore.

Calcola il MCD di due o più interi.

Esempi::

    gcd("12", "18")    -> 6
    gcd("100", "75")   -> 25
    gcd("-12", "18")   -> 6
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
from openalpha.explanations.numeric.gcd import explain_gcd
from openalpha.parser import parse_expression


def _parse_interi(*args: str) -> tuple[list[int], str | None]:
    """Parsa una lista di stringhe in interi. Restituisce (interi, errore)."""
    valori = []
    for arg in args:
        try:
            expr = parse_expression(arg)
        except ParserError as exc:
            return [], str(exc)
        except UnsupportedOperationError as exc:
            return [], str(exc)
        except OpenAlphaError as exc:
            return [], str(exc)

        if not expr.is_Integer:
            return [], f"richiede un intero, ricevuto: {expr}"

        valori.append(abs(int(expr)))
    return valori, None


@register(
    name="gcd",
    description="Massimo comun divisore di due o più interi.",
)
def gcd(a: str, b: str) -> Result:
    """Calcola il MCD di ``a`` e ``b``."""
    base = {"input_expression": f"{a}, {b}", "operation": "gcd"}

    valori, errore = _parse_interi(a, b)
    if errore:
        return Result(**base, status=ResultStatus.ERROR, error=errore)

    if valori[0] == 0 and valori[1] == 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error="il MCD di 0 e 0 non è definito",
        )

    try:
        result = sympy.gcd(valori[0], valori[1])
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il MCD: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
        steps=explain_gcd(valori[0], valori[1]),
    )