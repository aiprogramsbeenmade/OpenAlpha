"""
Operazione ``lcm``: minimo comune multiplo.

Calcola il mcm di due interi positivi.

Esempi::

    lcm("12", "18")   -> 36
    lcm("4", "6")     -> 12
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.explanations.numeric.lcm import explain_lcm
from openalpha.operations.number_theory.gcd import _parse_interi


@register(
    name="lcm",
    description="Minimo comune multiplo di due interi.",
)
def lcm(a: str, b: str) -> Result:
    """Calcola il mcm di ``a`` e ``b``."""
    base = {"input_expression": f"{a}, {b}", "operation": "lcm"}

    valori, errore = _parse_interi(a, b)
    if errore:
        return Result(**base, status=ResultStatus.ERROR, error=errore)

    if valori[0] == 0 and valori[1] == 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error="il mcm di 0 e 0 non è definito",
        )

    try:
        result = sympy.lcm(valori[0], valori[1])
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il mcm: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
        steps=explain_lcm(valori[0], valori[1]),
    )