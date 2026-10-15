"""
Spiegazione passo-passo dell'n-esimo numero primo.

Algoritmo: genera i primi in sequenza fino al risultato.

Esempi::

    prime(1)   -> "2 è il 1° primo"
    prime(5)   -> "2, 3, 5, 7, 11; l'11 è il 5° primo"
    prime(10)  -> "2, 3, 5, 7, 11, 13, 17, 19, 23, 29"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step

# Massimo numero di primi da elencare nella spiegazione.
# Oltre questa soglia, riassumiamo.
_MAX_ELENCO = 20


def explain_prime(n: int) -> list[Step]:
    """Restituisce i passi per calcolare l'n-esimo primo.

    Args:
        n: indice del primo (1-indexed).

    Returns:
        Lista di ``Step``. Se ``n < 1``, lista vuota.
    """
    if n < 1:
        return []

    result = int(sympy.prime(n))

    if n == 1:
        return [
            Step(
                before="prime(1)",
                after="2",
                rule_name="definizione",
                description="Il 1° numero primo è 2.",
            )
        ]

    # Genera i primi da 1 a n.
    primi = [int(sympy.prime(i)) for i in range(1, n + 1)]

    if n <= _MAX_ELENCO:
        elenco_str = ", ".join(str(p) for p in primi)
        return [
            Step(
                before=f"prime({n})",
                after=str(result),
                rule_name="sequenza dei primi",
                description=(
                    f"I primi {n} numeri primi sono: {elenco_str}. "
                    f"Il {n}° è {result}."
                ),
            )
        ]

    # Troppi per elencarli: riassumi.
    primi_inizio = ", ".join(str(p) for p in primi[:5])
    primi_fine = ", ".join(str(p) for p in primi[-3:])
    return [
        Step(
            before=f"prime({n})",
            after=str(result),
            rule_name="sequenza dei primi",
            description=(
                f"Genero i primi {n} numeri primi: {primi_inizio}, ..., "
                f"{primi_fine}. Il {n}° è {result}."
            ),
        )
    ]