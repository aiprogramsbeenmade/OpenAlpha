"""
Spiegazione passo-passo del minimo comune multiplo.

Formula: lcm(a, b) = (a * b) / gcd(a, b).

Esempi::

    lcm(12, 18)  -> "gcd(12, 18) = 6; 12 * 18 = 216; 216 / 6 = 36"
    lcm(4, 6)    -> "gcd(4, 6) = 2; 4 * 6 = 24; 24 / 2 = 12"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_lcm(a: int, b: int) -> list[Step]:
    """Restituisce i passi per calcolare il mcm di ``a`` e ``b``.

    Usa la formula ``lcm(a, b) = (a * b) / gcd(a, b)``.

    Args:
        a: primo intero (non negativo).
        b: secondo intero (non negativo).

    Returns:
        Lista di ``Step``. Se ``a == 0`` e ``b == 0``, restituisce
        uno step di "mcm non definito". Se uno dei due è 0, restituisce
        uno step "mcm = 0".
    """
    if a == 0 and b == 0:
        return [
            Step(
                before="lcm(0, 0)",
                after="non definito",
                rule_name="definizione",
                description="Il mcm di 0 e 0 non è definito.",
            )
        ]

    m, n = abs(a), abs(b)

    if m == 0 or n == 0:
        return [
            Step(
                before=f"lcm({m}, {n})",
                after="0",
                rule_name="caso banale",
                description=(
                    f"Uno dei due numeri è 0, quindi il mcm è 0: "
                    f"lcm({m}, {n}) = 0."
                ),
            )
        ]

    g = int(sympy.gcd(m, n))
    prodotto = m * n
    risultato = prodotto // g

    return [
        Step(
            before=f"lcm({m}, {n})",
            after=f"({m} * {n}) / gcd({m}, {n})",
            rule_name="formula",
            description=(
                f"lcm({m}, {n}) = ({m} * {n}) / gcd({m}, {n})."
            ),
        ),
        Step(
            before=f"gcd({m}, {n})",
            after=str(g),
            rule_name="calcolo del MCD",
            description=f"Il MCD di {m} e {n} è {g}.",
        ),
        Step(
            before=f"({m} * {n}) / {g}",
            after=str(risultato),
            rule_name="divisione",
            description=(
                f"{m} * {n} = {prodotto}; {prodotto} / {g} = {risultato}."
            ),
        ),
    ]