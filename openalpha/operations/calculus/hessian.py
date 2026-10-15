"""
Operazione ``hessian``: matrice hessiana di una funzione scalare.

Calcola la matrice delle derivate parziali seconde rispetto a un
insieme di variabili. Se ``vars`` non è specificato, usa tutte le
variabili libere in ordine alfabetico.

Esempi::

    hessian("x**2 + y**2")   -> [[2, 0], [0, 2]]
    hessian("x*y")           -> [[0, 1], [1, 0]]
    hessian("x**3 + y**3")   -> [[6*x, 0], [0, 6*y]]
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
    name="hessian",
    description="Matrice hessiana di una funzione scalare.",
)
def hessian(expression: str, vars: str = "") -> Result:
    """Calcola la matrice hessiana di ``expression``.

    Args:
        expression: funzione scalare.
        vars: variabili separate da virgola (es. ``"x,y"``).
            Se vuoto, usa tutte le variabili libere ordinate.

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo.
    """
    base = {
        "input_expression": expression,
        "operation": "hessian",
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
        # Funzione costante: hessiana vuota.
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact="[]",
            metadata={
                "vars": [],
                "latex_exact": "\\mathbf{0}",
            },
        )

    for nome in nomi:
        if not nome.isidentifier():
            return Result(
                **base,
                status=ResultStatus.ERROR,
                error=f"variabile non valida: {nome!r}",
            )

    simboli = [sympy.Symbol(n) for n in nomi]

    try:
        # Matrice hessiana: H[i][j] = ∂²f / ∂x_i ∂x_j.
        matrice = [
            [sympy.diff(expr, s_i, s_j) for s_j in simboli]
            for s_i in simboli
        ]
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare l'hessiana: {exc}",
        )

    # Formato lista di liste: "[[2, 0], [0, 2]]".
    righe_str = [
        "[" + ", ".join(str(cell) for cell in riga) + "]"
        for riga in matrice
    ]
    exact_str = "[" + ", ".join(righe_str) + "]"

    # LaTeX: pmatrix con righe separate da \\ e colonne da &.
    righe_latex = [
        " & ".join(sympy.latex(cell) for cell in riga)
        for riga in matrice
    ]
    latex_str = (
        "\\begin{pmatrix}"
        + " \\\\ ".join(righe_latex)
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