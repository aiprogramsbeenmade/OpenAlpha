"""
Raccolta delle condizioni di validità di un'espressione.

Analizza un'espressione SymPy e restituisce le condizioni necessarie
perché sia ben definita. Copre tre casi:

1. **Denominatori**: ``1/f`` richiede ``f != 0``.
2. **Radici quadrate**: ``sqrt(f)`` richiede ``f >= 0``.
3. **Logaritmi**: ``log(f)`` richiede ``f > 0``.

Le condizioni sono restituite come stringhe leggibili, senza tentare
di semplificarle. ``x + 1 != 0`` resta ``x + 1 != 0``: non lo
trasformiamo in ``x != -1``. Quest'ultima sarebbe più "risolta", ma
anche più costosa da calcolare e potenzialmente imprecisa. Meglio
la forma onesta.

Cosa NON gestiamo (per ora):

- Dominio di ``tan``, ``asin``, ``acos``.
- Parametri con segno (``sqrt(a)`` con ``a`` simbolo).
- Unificazione di condizioni ridondanti.
- Verifica di soddisfacibilità.

Queste limitazioni sono esplicite: se una condizione non viene
raccolta, il ``Result`` non la dichiara. Meglio nessuna condizione
che una condizione sbagliata.
"""

from __future__ import annotations

import sympy


def collect_conditions(expr: sympy.Expr) -> list[str]:
    """Raccoglie le condizioni di validità di un'espressione.

    Args:
        expr: espressione SymPy da analizzare.

    Returns:
        Lista di stringhe, una per condizione, in ordine stabile.
        Lista vuota se l'espressione non ha condizioni note.
    """
    conditions: list[str] = []
    seen: set[str] = set()

    def _add(condition_str: str) -> None:
        if condition_str not in seen:
            seen.add(condition_str)
            conditions.append(condition_str)

    # Denominatori: ogni Pow con esponente negativo.
    for power in expr.atoms(sympy.Pow):
        base, exp = power.args
        # Denominatore: esponente negativo.
        if exp.is_negative:
            cond = f"{base} != 0"
            _add(cond)

    # Radici quadrate: Pow con esponente 1/2.
    for power in expr.atoms(sympy.Pow):
        base, exp = power.args
        if exp == sympy.Rational(1, 2):
            cond = f"{base} >= 0"
            _add(cond)

    # Logaritmi.
    for log_expr in expr.atoms(sympy.log):
        arg = log_expr.args[0]
        cond = f"{arg} > 0"
        _add(cond)

    return conditions