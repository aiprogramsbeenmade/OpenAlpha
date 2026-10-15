"""
Spiegazione passo-passo del massimo comun divisore (algoritmo di Euclide).

Esempi::

    gcd(12, 18)  -> "18 = 1 * 12 + 6; 12 = 2 * 6 + 0; MCD = 6"
    gcd(100, 75) -> "100 = 1 * 75 + 25; 75 = 3 * 25 + 0; MCD = 25"
    gcd(7, 13)   -> "13 = 1 * 7 + 6; 7 = 1 * 6 + 1; 6 = 6 * 1 + 0; MCD = 1"
"""

from __future__ import annotations

from openalpha.core.step import Step


def explain_gcd(a: int, b: int) -> list[Step]:
    """Restituisce i passi per calcolare il MCD di ``a`` e ``b``.

    Usa l'algoritmo di Euclide: ogni iterazione è uno ``Step``.

    Args:
        a: primo intero (non negativo).
        b: secondo intero (non negativo).

    Returns:
        Lista di ``Step``. Se ``a == 0`` e ``b == 0``, restituisce
        uno step di "MCD non definito". Altrimenti, uno step per
        iterazione di Euclide + uno step finale.
    """
    if a == 0 and b == 0:
        return [
            Step(
                before="gcd(0, 0)",
                after="non definito",
                rule_name="definizione",
                description="Il MCD di 0 e 0 non è definito.",
            )
        ]

    # Euclide: gcd(a, b) = gcd(b, a mod b).
    # Iteriamo finché b != 0.
    steps: list[Step] = []
    m, n = abs(a), abs(b)

    # Caso banale: uno dei due è 0.
    if m == 0 or n == 0:
        result = max(m, n)
        return [
            Step(
                before=f"gcd({m}, {n})",
                after=str(result),
                rule_name="caso banale",
                description=(
                    f"Uno dei due numeri è 0, quindi il MCD è "
                    f"l'altro: gcd({m}, {n}) = {result}."
                ),
            )
        ]

    # Assicura m >= n per evitare un primo step banale.
    if m < n:
        m, n = n, m

    # Euclide.
    while n != 0:
        q = m // n
        r = m % n
        steps.append(
            Step(
                before=f"gcd({m}, {n})",
                after=f"gcd({n}, {r})",
                rule_name="algoritmo di Euclide",
                description=(
                    f"{m} = {q} * {n} + {r}  →  "
                    f"gcd({m}, {n}) = gcd({n}, {r})"
                ),
            )
        )
        m, n = n, r

    steps.append(
        Step(
            before=f"gcd({m}, 0)",
            after=str(m),
            rule_name="caso base",
            description=f"Il MCD è {m}, perché gcd({m}, 0) = {m}.",
        )
    )

    return steps