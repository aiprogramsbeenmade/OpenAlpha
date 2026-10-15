"""
Spiegazione passo-passo del calcolo dei divisori.

Algoritmo: prova divisori da 1 a √n. Per ogni divisore trovato,
aggiungi sia ``d`` che ``n // d``.

Esempi::

    divisors(12)  -> "1 divide 12; 2 divide 12; 3 divide 12; ..."
    divisors(7)   -> "1 divide 7; nessun altro divisore ≤ √7; 7 è primo"
"""

from __future__ import annotations

import sympy

from openalpha.core.step import Step


def explain_divisors(n: int) -> list[Step]:
    """Restituisce i passi per calcolare i divisori di ``n``.

    Args:
        n: intero positivo.

    Returns:
        Lista di ``Step``. Se ``n <= 0``, lista vuota.
    """
    if n <= 0:
        return []

    steps: list[Step] = []

    # Trova i divisori con sympy (per completezza).
    divs = sympy.divisors(n)

    # Costruisci step "d divide n" per i divisori fino a √n,
    # poi uno step finale con la lista completa.
    radice = sympy.integer_nthroot(n, 2)[0]

    # Mostra solo i divisori <= √n come step "didattici".
    # I divisori > √n sono "coppie" e verrebbero ridondanti.
    divisori_piccoli = [d for d in divs if d <= radice]

    for d in divisori_piccoli:
        coppia = n // d
        if d == coppia:
            steps.append(
                Step(
                    before=f"{d} * {d}",
                    after=str(n),
                    rule_name="quadrato perfetto",
                    description=(
                        f"{d} divide {n}: {d} * {d} = {n}."
                    ),
                )
            )
        else:
            steps.append(
                Step(
                    before=f"{d} * {coppia}",
                    after=str(n),
                    rule_name="coppia di divisori",
                    description=(
                        f"{d} e {coppia} sono divisori: "
                        f"{d} * {coppia} = {n}."
                    ),
                )
            )

    # Step finale: lista completa.
    lista_str = "{" + ", ".join(str(d) for d in divs) + "}"
    steps.append(
        Step(
            before=f"divisors({n})",
            after=lista_str,
            rule_name="elenco completo",
            description=f"I divisori di {n} sono: {lista_str}.",
        )
    )

    return steps