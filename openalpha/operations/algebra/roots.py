"""
Operazione ``roots``: radici di un polinomio.

Trova le radici (reali e complesse) di un polinomio e ne riporta la
molteplicità.

Esempi::

    roots("x**2 - 1")           -> {-1: 1, 1: 1}
    roots("x**2 - 2*x + 1")     -> {1: 2}
    roots("x**3 - x")           -> {-1: 1, 0: 1, 1: 1}
    roots("x**2 + 1")           -> {-I: 1, I: 1}
    roots("x**2 - 1", var="x")  -> {-1: 1, 1: 1}

Input non polinomiale (es. ``sin(x)``) restituisce ``UNSUPPORTED``.
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
    name="roots",
    description="Trova le radici di un polinomio con le loro molteplicità.",
)
def roots(expression: str, var: str = "x") -> Result:
    """Trova le radici di ``expression`` rispetto a ``var``.

    Args:
        expression: polinomio in una variabile.
        var: variabile del polinomio (default ``"x"``).

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo,
        ``UNSUPPORTED`` se l'input non è un polinomio, ``ERROR`` per
        problemi di parsing o di input.
    """
    base = {"input_expression": expression, "operation": "roots"}

    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    var_sym = sympy.Symbol(var)

    # Verifica che sia un polinomio in var.
    try:
        if not expr.is_polynomial(var_sym):
            return Result(
                **base,
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"l'espressione non è un polinomio in {var!r}: "
                    f"{expr}"
                ),
            )
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile verificare il polinomio: {exc}",
        )

    # Calcola le radici.
    try:
        roots_dict = sympy.roots(expr, var_sym)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile calcolare le radici: {exc}",
        )

    # Costruisci la stringa esatta: "{-1: 1, 1: 1}" con ordine stabile.
    # SymPy restituisce un dict, ordiniamo per stringa della radice.
    if not roots_dict:
        exact_str = "{}"
        latex_str = "\\{\\}"
    else:
        coppie = sorted(
            roots_dict.items(),
            key=lambda kv: str(kv[0]),
        )
        parti = [f"{r}: {m}" for r, m in coppie]
        parti_latex = [f"{sympy.latex(r)}: {m}" for r, m in coppie]
        exact_str = "{" + ", ".join(parti) + "}"
        latex_str = "\\{" + ", ".join(parti_latex) + "\\}"

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={
            "roots": {str(r): int(m) for r, m in roots_dict.items()},
            "var": var,
            # Il risultato è un dict formattato, non un'espressione
            # matematica. Forniamo il LaTeX già pronto.
            "latex_exact": latex_str,
        },
    )