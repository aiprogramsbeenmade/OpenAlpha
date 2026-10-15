"""
Spiegazione passo-passo delle permutazioni P(n, k).

Formula: P(n, k) = n! / (n-k)!.

Esempi::

    permutations(5, 2)  -> "P(5, 2) = 5! / 3! = 120 / 6 = 20"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_permutations(n: int, k: int) -> list[Step]:
    """Restituisce i passi per calcolare P(n, k).

    Args:
        n: intero non negativo.
        k: intero tra 0 e n.

    Returns:
        Lista di ``Step``. Se ``k > n``, lista vuota.
    """
    if k > n or n < 0 or k < 0:
        return []

    if k == 0:
        return [
            Step(
                before=f"P({n}, {k})",
                after="1",
                rule_name="definizione",
                description=f"P({n}, 0) = 1 per definizione.",
            )
        ]

    result = int(sympy.factorial(n)) // int(sympy.factorial(n - k))
    n_fact = int(sympy.factorial(n))
    nk_fact = int(sympy.factorial(n - k))

    return [
        Step(
            before=f"P({n}, {k})",
            after=f"{n}! / {n - k}!",
            rule_name="formula",
            description=f"P({n}, {k}) = {n}! / ({n} - {k})!.",
        ),
        Step(
            before=f"{n}! / {n - k}!",
            after=f"{n_fact} / {nk_fact}",
            rule_name="calcolo dei fattoriali",
            description=(
                f"{n}! = {n_fact}; {n - k}! = {nk_fact}."
            ),
        ),
        Step(
            before=f"{n_fact} / {nk_fact}",
            after=str(result),
            rule_name="calcolo",
            description=f"{n_fact} / {nk_fact} = {result}.",
        ),
    ]