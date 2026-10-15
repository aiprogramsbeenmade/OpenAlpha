"""
Operazione ``gradient``: gradiente di una funzione scalare.

Calcola il vettore delle derivate parziali rispetto a un insieme
di variabili. Se ``vars`` non è specificato, usa tutte le variabili
libere in ordine alfabetico.

Esempi::

    gradient("x**2 + y**2")        -> [2*x, 2*y]
    gradient("x*y*z")              -> [y*z, x*z, x*y]
    gradient("x**2 + y**2", "y,x") -> [2*y, 2*x]
    gradient("5")                  -> []
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
    name="gradient",
    description="Gradiente di una funzione scalare.",
)
def gradient(expression: str, vars: str = "") -> Result:
    """Calcola il gradiente di ``expression``.

    Args:
        expression: funzione scalare.
        vars: variabili separate da virgola (es. ``"x,y"``).
            Se vuoto, usa tutte le variabili libere ordinate.

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo.
    """
    base = {
        "input_expression": expression,
        "operation": "gradient",
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
        # Funzione costante: gradiente nullo.
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact="[]",
            metadata={
                "vars": [],
                "latex_exact": "\\mathbf{0}",
            },
        )

    # Valida i nomi.
    for nome in nomi:
        if not nome.isidentifier():
            return Result(
                **base,
                status=ResultStatus.ERROR,
                error=f"variabile non valida: {nome!r}",
            )

    simboli = [sympy.Symbol(n) for n in nomi]

    try:
        derivate = [sympy.diff(expr, s) for s in simboli]
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare il gradiente: {exc}",
        )

    # Formato lista: "[2*x, 2*y]".
    exact_str = "[" + ", ".join(str(d) for d in derivate) + "]"

    # LaTeX: pmatrix (vettore colonna).
    latex_str = (
        "\\begin{pmatrix}"
        + " \\\\ ".join(sympy.latex(d) for d in derivate)
        + "\\end{pmatrix}"
    )

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={
            "vars": nomi,
            "latex_exact": latex_str,
        },
    )