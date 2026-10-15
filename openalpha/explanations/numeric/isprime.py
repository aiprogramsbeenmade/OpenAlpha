"""
Spiegazione passo-passo del test di primalità.

Algoritmo: prova di divisione per divisori da 2 a √n.

Esempi::

    isprime(7)  -> "7 non è divisibile per 2, 3, 5. Quindi 7 è primo."
    isprime(9)  -> "9 è divisibile per 3: 9 = 3 * 3. Quindi 9 non è primo."
    isprime(1)  -> "1 non è primo per definizione."
    isprime(2)  -> "2 è primo per definizione (unico primo pari)."
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_isprime(n: int) -> list[Step]:
    """Restituisce i passi per verificare se ``n`` è primo.

    Args:
        n: intero da testare.

    Returns:
        Lista di ``Step``. Per la maggior parte dei casi, un solo step
        riassuntivo (l'algoritmo è troppo lungo per mostrare ogni
        divisione).
    """
    if n < 2:
        return [
            Step(
                before=str(n),
                after="non primo",
                rule_name="definizione",
                description=(
                    f"{n} non è primo: i primi sono interi ≥ 2."
                ),
            )
        ]

    if n == 2:
        return [
            Step(
                before=str(n),
                after="primo",
                rule_name="definizione",
                description=(
                    "2 è primo per definizione (unico primo pari)."
                ),
            )
        ]

    if n % 2 == 0:
        return [
            Step(
                before=str(n),
                after="composto",
                rule_name="divisibilità per 2",
                description=(
                    f"{n} è pari e > 2: {n} = 2 * {n // 2}. "
                    f"Quindi {n} non è primo."
                ),
            )
        ]

    # Cerca il più piccolo divisore primo ≤ √n.
    # SymPy fa il lavoro; noi lo usiamo per la spiegazione.
    divisore = None
    # Prova solo i dispari > 2, fino a √n.
    d = 3
    limite = int(sympy.integer_nthroot(n, 2)[0])
    while d <= limite:
        if n % d == 0:
            divisore = d
            break
        d += 2

    if divisore is not None:
        return [
            Step(
                before=str(n),
                after="composto",
                rule_name=f"divisibilità per {divisore}",
                description=(
                    f"{n} è divisibile per {divisore}: "
                    f"{n} = {divisore} * {n // divisore}. "
                    f"Quindi {n} non è primo."
                ),
            )
        ]

    # n è primo: riassunto del test.
    return [
        Step(
            before=str(n),
            after="primo",
            rule_name="test di primalità",
            description=(
                f"{n} non è divisibile per nessun primo ≤ √{n} ≈ {limite}. "
                f"Quindi {n} è primo."
            ),
        )
    ]