"""
Spiegazione passo-passo dell'inverso modulare.

Algoritmo: Euclide esteso. Trova x tale che a * x ≡ 1 (mod m).

Esempi::

    mod_inverse(3, 7)    -> "3 * 5 = 15 ≡ 1 (mod 7); quindi 5"
    mod_inverse(10, 17)  -> "10 * 12 = 120 ≡ 1 (mod 17); quindi 12"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_mod_inverse(a: int, m: int) -> list[Step]:
    """Restituisce i passi per calcolare l'inverso di ``a`` mod ``m``.

    Args:
        a: intero.
        m: modulo positivo.

    Returns:
        Lista di ``Step``. Se l'inverso non esiste, restituisce
        uno step di errore. Se ``m <= 0``, lista vuota.
    """
    if m <= 0:
        return []

    if m == 1:
        return [
            Step(
                before=f"mod_inverse({a}, 1)",
                after="0",
                rule_name="caso banale",
                description=(
                    "Modulo 1, ogni intero è congruo a 0, "
                    "quindi l'inverso è 0."
                ),
            )
        ]

    g = int(sympy.gcd(a, m))
    if g != 1:
        return [
            Step(
                before=f"mod_inverse({a}, {m})",
                after="non esiste",
                rule_name="condizione di esistenza",
                description=(
                    f"gcd({a}, {m}) = {g} ≠ 1. L'inverso esiste solo "
                    f"se a e m sono coprimi. Quindi l'inverso non esiste."
                ),
            )
        ]

    # Algoritmo di Euclide esteso.
    # Troviamo x, y tali che a*x + m*y = 1.
    old_r, r = a, m
    old_s, s = 1, 0
    old_t, t = 0, 1

    steps: list[Step] = []

    # Euclide esteso.
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    # old_r è il gcd, old_s è il coefficiente di a.
    x = old_s % m

    # Step finale.
    prodotto = a * x
    steps.append(
        Step(
            before=f"{a} * {x}",
            after=str(prodotto),
            rule_name="verifica",
            description=(
                f"{a} * {x} = {prodotto}. "
                f"{prodotto} mod {m} = {prodotto % m}."
            ),
        )
    )
    steps.append(
        Step(
            before=f"mod_inverse({a}, {m})",
            after=str(x),
            rule_name="risultato",
            description=(
                f"L'inverso di {a} modulo {m} è {x}, "
                f"perché {a} * {x} ≡ 1 (mod {m})."
            ),
        )
    )

    return steps