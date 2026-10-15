"""
Spiegazione passo-passo del coefficiente binomiale C(n, k).

Formula: C(n, k) = n! / (k! * (n-k)!).

Esempi::

    combinations(5, 2)  -> "C(5, 2) = 5! / (2! * 3!) = 120 / 12 = 10"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_combinations(n: int, k: int) -> list[Step]:
    """Restituisce i passi per calcolare C(n, k).

    Args:
        n: intero non negativo.
        k: intero tra 0 e n.

    Returns:
        Lista di ``Step``. Se ``k > n``, lista vuota.
    """
    if k > n or n < 0 or k < 0:
        return []

    if k == 0 or k == n:
        return [
            Step(
                before=f"C({n}, {k})",
                after="1",
                rule_name="definizione",
                description=(
                    f"C({n}, {k}) = 1 per definizione "
                    f"(scelta banale)."
                ),
            )
        ]

    result = int(sympy.binomial(n, k))
    n_fact = int(sympy.factorial(n))
    k_fact = int(sympy.factorial(k))
    nk_fact = int(sympy.factorial(n - k))

    return [
        Step(
            before=f"C({n}, {k})",
            after=f"{n}! / ({k}! * {n - k}!)",
            rule_name="formula",
            description=(
                f"C({n}, {k}) = {n}! / ({k}! * ({n} - {k})!)."
            ),
        ),
        Step(
            before=f"{n}! / ({k}! * {n - k}!)",
            after=f"{n_fact} / ({k_fact} * {nk_fact})",
            rule_name="calcolo dei fattoriali",
            description=(
                f"{n}! = {n_fact}; {k}! = {k_fact}; "
                f"{n - k}! = {nk_fact}."
            ),
        ),
        Step(
            before=f"{n_fact} / ({k_fact} * {nk_fact})",
            after=str(result),
            rule_name="calcolo",
            description=(
                f"{k_fact} * {nk_fact} = {k_fact * nk_fact}; "
                f"{n_fact} / {k_fact * nk_fact} = {result}."
            ),
        ),
    ]