"""
Operazione ``critical_points``: punti critici di una funzione scalare.

Trova i punti in cui il gradiente è nullo (tutte le derivate parziali
si annullano).

Esempi::

    critical_points("x**2 + y**2")   -> [(0, 0)]
    critical_points("x*y")           -> [(0, 0)]
    critical_points("x**2")          -> [(0,)]
    critical_points("x**2 + y**2 + z**2") -> [(0, 0, 0)]

Se il sistema ha infinite soluzioni (soluzioni parametriche),
restituisce ``PARTIAL`` con un messaggio.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import (
    OpenAlphaError,
    ParserError,
    UnsupportedOperationError,
)
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


@register(
    name="critical_points",
    description="Punti critici di una funzione scalare.",
)
def critical_points(expression: str, vars: str = "") -> Result:
    """Trova i punti critici di ``expression``.

    Args:
        expression: funzione scalare.
        vars: variabili separate da virgola (es. ``"x,y"``).
            Se vuoto, usa tutte le variabili libere ordinate.

    Returns:
        Un ``Result`` con status ``EXACT`` se le soluzioni sono punti
        finiti, ``PARTIAL`` se parametriche, ``UNSUPPORTED`` se non
        risolvibile, ``ERROR`` per input non valido.
    """
    base = {
        "input_expression": expression,
        "operation": "critical_points",
    }

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    # Determina le variabili.
    if vars.strip():
        nomi = [v.strip() for v in vars.split(",") if v.strip()]
    else:
        nomi = sorted(str(s) for s in expr.free_symbols)

    if not nomi:
        # Funzione costante: nessun punto critico isolato.
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact="[]",
            metadata={"vars": []},
        )

    for nome in nomi:
        if not nome.isidentifier():
            return Result(
                **base,
                status=ResultStatus.ERROR,
                error=f"variabile non valida: {nome!r}",
            )

    simboli = [sympy.Symbol(n) for n in nomi]

    # Gradiente.
    try:
        grad = [sympy.diff(expr, s) for s in simboli]
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il gradiente: {exc}",
        )

    # Sistema: ∂f/∂xi = 0 per ogni i.
    try:
        soluzioni = sympy.solve(grad, simboli, dict=True)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile risolvere il sistema: {exc}",
        )

    if not soluzioni:
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact="[]",
            metadata={"vars": nomi},
        )

    # Verifica se le soluzioni sono punti finiti.
    # Una soluzione è "completa" se contiene un valore per ogni variabile.
    punti = []
    parziale = False
    for sol in soluzioni:
        # sol è un dict {Symbol: valore}.
        if all(s in sol for s in simboli):
            punti.append(tuple(sol[s] for s in simboli))
        else:
            parziale = True
            # Soluzione parziale: prendi quello che c'è.
            punti.append(
                tuple(sol.get(s, s) for s in simboli)
            )

    # Deduplica.
    punti_unici = []
    for p in punti:
        if p not in punti_unici:
            punti_unici.append(p)

    # Formato: "[(0, 0), (1, 2)]".
    def _fmt(punto):
        return "(" + ", ".join(str(c) for c in punto) + ")"

    exact_str = "[" + ", ".join(_fmt(p) for p in punti_unici) + "]"

    if parziale:
        return Result(
            **base,
            status=ResultStatus.PARTIAL,
            exact=exact_str,
            metadata={
                "vars": nomi,
                "message": (
                    "Alcune soluzioni sono parametriche "
                    "(infinite soluzioni)."
                ),
            },
        )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={"vars": nomi},
    )