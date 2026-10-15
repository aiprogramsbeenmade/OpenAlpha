"""
Operazione ``mod_inverse``: inverso modulare.

Calcola x tale che ``a * x ≡ 1 (mod m)``, se esiste.

Esempi::

    mod_inverse("3", "7")   -> 5         (3 * 5 = 15 ≡ 1 mod 7)
    mod_inverse("10", "17") -> 12        (10 * 12 = 120 ≡ 1 mod 17)
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.explanations.numeric.mod_inverse import explain_mod_inverse
from openalpha.operations.number_theory.gcd import _parse_interi


@register(
    name="mod_inverse",
    description="Inverso modulare di a modulo m.",
)
def mod_inverse(a: str, m: str) -> Result:
    """Calcola l'inverso di ``a`` modulo ``m``."""
    base = {"input_expression": f"{a}, {m}", "operation": "mod_inverse"}

    valori, errore = _parse_interi(a, m)
    if errore:
        return Result(**base, status=ResultStatus.ERROR, error=errore)

    a_int, m_int = valori[0], valori[1]
    if m_int == 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error="il modulo non può essere 0",
        )

    try:
        result = sympy.mod_inverse(a_int, m_int)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"l'inverso modulare non esiste: {exc}",
            steps=explain_mod_inverse(a_int, m_int),
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
        steps=explain_mod_inverse(a_int, m_int),
    )