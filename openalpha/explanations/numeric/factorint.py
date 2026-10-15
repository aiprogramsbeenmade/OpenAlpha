"""
Spiegazione passo-passo della fattorizzazione in primi.

Algoritmo: divisione per tentativi con i primi crescenti.

Esempio per n=24::

    24 -> 12   (divido per 2, 24 / 2 = 12)
    12 -> 6    (divido per 2, 12 / 2 = 6)
    6  -> 3    (divido per 2, 6 / 2 = 3)
    3  -> 1    (divido per 3, 3 / 3 = 1)
    24 -> 2^3 * 3   (fattorizzazione completa)
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_factorint(n: int) -> list[Step]:
    """Restituisce i passi per fattorizzare ``n`` in primi.

    Restituisce una lista vuota se ``n <= 1`` o se ``n`` è primo
    (in questi casi non ci sono passaggi significativi).
    """
    if n <= 1:
        return []

    if sympy.isprime(n):
        return []

    steps: list[Step] = []
    remaining = n
    divisore = 2

    while remaining > 1:
        if remaining % divisore == 0:
            nuovo = remaining // divisore
            steps.append(
                Step(
                    before=str(remaining),
                    after=str(nuovo),
                    rule_name=f"divisione per {divisore}",
                    description=(
                        f"{remaining} è divisibile per {divisore}: "
                        f"{remaining} / {divisore} = {nuovo}"
                    ),
                )
            )
            remaining = nuovo
        else:
            divisore = int(sympy.nextprime(divisore))

    # Step finale: la fattorizzazione completa.
    factors = sympy.factorint(n)
    parti = []
    for primo, esponente in sorted(factors.items()):
        if esponente == 1:
            parti.append(str(primo))
        else:
            parti.append(f"{primo}^{esponente}")
    exact_str = " * ".join(parti)

    steps.append(
        Step(
            before=str(n),
            after=exact_str,
            rule_name="fattorizzazione completa",
            description=f"{n} = {exact_str}",
        )
    )

    return steps