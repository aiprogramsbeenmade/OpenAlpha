"""
Approssimazione numerica di un risultato esatto.

Data una stringa che rappresenta un risultato esatto (prodotta da
un'operazione OpenAlpha), calcola l'approssimazione decimale con
15 cifre significative, quando possibile.

Non approssima:
- Espressioni simboliche (con variabili libere).
- Valori non finiti (oo, -oo, zoo, nan).
- Numeri complessi.
- Stringhe non interpretabili.

L'approssimazione è una stringa, non un numero: può essere mostrata
all'utente senza perdita di informazione (es. ``"0.333333333333333"``
invece di ``0.3333333333333333``).

## Perché 15 cifre

È il default di ``sympy.N`` con ``chop=True``. Bilanciamento tra
precisione e leggibilità. Per l'uso tipico (calcoli didattici,
verifiche rapide), 15 cifre sono più che sufficienti.
"""

from __future__ import annotations

import sympy


# Precisione in cifre significative.
_PRECISION = 15


def compute_approximate(exact_str: str) -> str | None:
    """Calcola l'approssimazione numerica di un risultato esatto.

    Args:
        exact_str: stringa che rappresenta un risultato esatto
            (es. ``"1/2"``, ``"sqrt(2)"``, ``"pi"``).

    Returns:
        Una stringa con l'approssimazione decimale, o ``None`` se
        l'approssimazione non è applicabile.
    """
    if not exact_str:
        return None

    try:
        expr = sympy.sympify(exact_str, evaluate=True)
    except (sympy.SympifyError, SyntaxError, TypeError, ValueError):
        return None

    # Rifiuta espressioni con variabili libere.
    if expr.free_symbols:
        return None

    # Rifiuta valori non finiti.
    if expr in (sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
        return None

    # Rifiuta numeri complessi.
    if expr.is_complex and not expr.is_real:
        return None

    # Calcola l'approssimazione.
    try:
        approx = sympy.N(expr, _PRECISION)
    except Exception:
        return None

    # Rifiuta se l'approssimazione è un oggetto non numerico.
    if not approx.is_number:
        return None

    return str(approx)