"""
Spiegazione passo-passo della funzione φ di Eulero.

Formula: φ(n) = n · Π(1 - 1/p) per ogni primo p che divide n.

Esempi::

    totient(10)  -> "10 = 2 * 5; φ(10) = 10 * (1 - 1/2) * (1 - 1/5) = 4"
    totient(7)   -> "7 è primo; φ(7) = 7 - 1 = 6"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_totient(n: int) -> list[Step]:
    """Restituisce i passi per calcolare φ(n)."""
    if n <= 0:
        return []

    if n == 1:
        return [
            Step(
                before="φ(1)",
                after="1",
                rule_name="definizione",
                description="φ(1) = 1 per definizione.",
            )
        ]

    factors = sympy.factorint(n)
    primi = sorted(factors.keys())

    # Caso speciale: n è primo.
    if len(primi) == 1 and factors[primi[0]] == 1:
        p = primi[0]
        return [
            Step(
                before=f"φ({p})",
                after=str(p - 1),
                rule_name="formula per primi",
                description=(
                    f"{p} è primo, quindi φ({p}) = {p} - 1 = {p - 1}."
                ),
            )
        ]

    # Formula generale.
    result = int(sympy.totient(n))
    fattori_str = " * ".join(
        str(p) if e == 1 else f"{p}^{e}"
        for p, e in sorted(factors.items())
    )
    formula_parte = " * ".join(f"(1 - 1/{p})" for p in primi)

    return [
        Step(
            before=str(n),
            after=fattori_str,
            rule_name="fattorizzazione",
            description=f"Fattorizzo {n}: {n} = {fattori_str}.",
        ),
        Step(
            before=f"φ({n})",
            after=f"{n} * {formula_parte}",
            rule_name="formula di Eulero",
            description=(
                f"Applico φ(n) = n * Π(1 - 1/p) per i primi "
                f"che dividono {n}: {', '.join(str(p) for p in primi)}."
            ),
        ),
        Step(
            before=f"{n} * {formula_parte}",
            after=str(result),
            rule_name="calcolo",
            description=f"Il risultato è φ({n}) = {result}.",
        ),
    ]