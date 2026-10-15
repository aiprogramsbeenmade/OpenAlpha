"""
Operazione ``permutations``: permutazioni.

Calcola P(n, k) = n! / (n-k)!, il numero di sequenze ordinate
di k elementi scelti da n.

Esempi::

    permutations("5", "2")   -> 20
    permutations("10", "3")  -> 720
    permutations("5", "0")   -> 1
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.gcd import _parse_interi


@register(
    name="permutations",
    description="Permutazioni P(n, k).",
)
def permutations(n: str, k: str) -> Result:
    """Calcola P(``n``, ``k``)."""
    base = {"input_expression": f"{n}, {k}", "operation": "permutations"}

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
        result = sympy.factorial(n_int) // sympy.factorial(n_int - k_int)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare le permutazioni: {exc}",
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(result),
    )