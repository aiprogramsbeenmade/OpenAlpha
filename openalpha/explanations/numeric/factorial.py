"""
Spiegazione passo-passo del fattoriale.

Formula: n! = n * (n-1) * ... * 1.

Esempi::

    factorial(5)  -> "5! = 5 * 4 * 3 * 2 * 1 = 120"
    factorial(0)  -> "0! = 1 per definizione"
"""

from __future__ import annotations

from openalpha.core.step import Step

# Massimo n per cui elencare tutti i fattori.
_MAX_FATTORI = 10


def explain_factorial(n: int) -> list[Step]:
    """Restituisce i passi per calcolare n!.

    Args:
        n: intero non negativo.

    Returns:
        Lista di ``Step``. Se ``n < 0``, lista vuota.
    """
    if n < 0:
        return []

    if n == 0:
        return [
            Step(
                before="0!",
                after="1",
                rule_name="definizione",
                description="0! = 1 per definizione (prodotto vuoto).",
            )
        ]

    if n == 1:
        return [
            Step(
                before="1!",
                after="1",
                rule_name="definizione",
                description="1! = 1 per definizione.",
            )
        ]

    if n <= _MAX_FATTORI:
        fattori = " * ".join(str(i) for i in range(n, 0, -1))
        risultato = 1
        for i in range(2, n + 1):
            risultato *= i
        return [
            Step(
                before=f"{n}!",
                after=fattori,
                rule_name="definizione",
                description=f"{n}! = {fattori}.",
            ),
            Step(
                before=fattori,
                after=str(risultato),
                rule_name="calcolo",
                description=f"Il prodotto è {risultato}.",
            ),
        ]

    # Troppi fattori: riassumi.
    return [
        Step(
            before=f"{n}!",
            after=f"{n} * {n - 1} * ... * 1",
            rule_name="definizione",
            description=(
                f"{n}! = {n} * {n - 1} * ... * 1. "
                f"Calcolo il prodotto di {n} fattori."
            ),
        )
    ]