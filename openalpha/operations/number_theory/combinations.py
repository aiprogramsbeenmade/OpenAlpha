"""
Operazione ``combinations``: coefficiente binomiale.

Calcola C(n, k) = n! / (k! * (n-k)!), il numero di sottoinsiemi
di k elementi scelti da n.

Esempi::

    combinations("5", "2")   -> 10
    combinations("10", "3")  -> 120
    combinations("5", "0")   -> 1
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.gcd import _parse_interi


@register(
    name="combinations",
    description="Coefficiente binomiale C(n, k).",
)
def combinations(n: str, k: str) -> Result:
    """Calcola C(``n``, ``k``)."""
    base = {"input_expression": f"{n}, {k}", "operation": "combinations"}

    valori, errore = _parse_interi(n, k)
    if errore:
        return Result(**base, status=ResultStatus.ERROR, error=errore)

    n_int, k_int = valori[0], valori[1]
    if k_int > n_int:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"k ({k_int}) non può essere maggiore di n ({n_int})",
        )

    try:
        result = sympy.binomial(n_int, k_int)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il coefficiente binomiale: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )