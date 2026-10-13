"""
Operazione: risoluzione di equazioni algebriche in una variabile.

Accetta una stringa che può contenere ``=`` per separare lhs e rhs.
Se ``=`` è assente, assume rhs = 0.

Sottoinsieme gestito:

- Equazioni polinomiali in una variabile, grado ≤ 4.
- La variabile incognita è la prima in ordine ``x, y, z, a, b, c, ...``.
- Coefficienti razionali o simbolici semplici.

Casi non gestiti (UNSUPPORTED):

- Equazioni trascendenti (es. ``sin(x) = 0``).
- Equazioni di grado > 4.
- Equazioni con più variabili "libere" senza una scelta chiara.
- Equazioni identiche o senza soluzione: SymPy restituisce ``[]``
  sia per "nessuna soluzione" sia per "identità", e non possiamo
  distinguere senza ambiguità. Meglio dichiarare il limite.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


# Ordine di preferenza per la scelta della variabile incognita.
_VARIABLE_PREFERENCE = ["x", "y", "z", "a", "b", "c", "t", "u", "v", "w"]

# Grado massimo gestito.
_MAX_DEGREE = 4


def _split_equation(input_expression: str) -> tuple[str, str]:
    """Divide l'input in lhs e rhs.

    Se c'è ``=``, divide sulla prima occorrenza. Se non c'è,
    restituisce ``(input, "0")``.
    """
    if "=" in input_expression:
        lhs, _, rhs = input_expression.partition("=")
        return lhs.strip(), rhs.strip()
    return input_expression.strip(), "0"


def _pick_variable(expr: sympy.Expr) -> sympy.Symbol | None:
    """Sceglie la variabile incognita.

    Regola: la prima in ``_VARIABLE_PREFERENCE`` che compare
    nell'espressione. Se nessuna di quelle compare, si prende la
    prima in ordine alfabetico. Se non c'è alcuna variabile,
    restituisce ``None``.
    """
    free = expr.free_symbols
    if not free:
        return None
    names = {s.name for s in free}
    for name in _VARIABLE_PREFERENCE:
        if name in names:
            return sympy.Symbol(name)
    # Fallback: prima in ordine alfabetico.
    return sorted(free, key=lambda s: s.name)[0]


@register("solve", "Risolve un'equazione algebrica in una variabile")
def solve(input_expression: str) -> Result:
    """Risolve un'equazione algebrica.

    Args:
        input_expression: equazione come stringa, con o senza ``=``.
            Es. ``"x**2 - 1 = 0"`` o ``"x**2 - 1"``.

    Returns:
        Un ``Result`` con ``solutions`` popolato, oppure uno degli
        stati di errore.
    """
    try:
        lhs_str, rhs_str = _split_equation(input_expression)

        if not lhs_str:
            raise ParserError("lato sinistro dell'equazione vuoto")
        if not rhs_str:
            raise ParserError("lato destro dell'equazione vuoto")

        lhs = parse_expression(lhs_str)
        rhs = parse_expression(rhs_str)

        equation = sympy.Eq(lhs, rhs)
        variable = _pick_variable(lhs - rhs)

        if variable is None:
            return Result(
                input_expression=input_expression,
                operation="solve",
                status=ResultStatus.UNSUPPORTED,
                error="nessuna variabile incognita nell'equazione",
            )

        # Controlla se è polinomiale e il grado.
        try:
            poly = sympy.Poly(lhs - rhs, variable)
        except sympy.PolynomialError:
            return Result(
                input_expression=input_expression,
                operation="solve",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "equazione non polinomiale: "
                    "il caso non è supportato"
                ),
            )

        if poly.degree() > _MAX_DEGREE:
            return Result(
                input_expression=input_expression,
                operation="solve",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"equazione di grado {poly.degree()}: "
                    f"massimo supportato {_MAX_DEGREE}"
                ),
            )

        # Risolve.
        solutions = sympy.solve(equation, variable)

        if not solutions:
            return Result(
                input_expression=input_expression,
                operation="solve",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "nessuna soluzione trovata o equazione identica: "
                    "SymPy non distingue i due casi"
                ),
            )

        solution_strings = [
            f"{variable} = {sol}" for sol in solutions
        ]

        return Result(
            input_expression=input_expression,
            operation="solve",
            status=ResultStatus.EXACT,
            solutions=solution_strings,
            metadata={
                "engine": "sympy",
                "sympy_version": sympy.__version__,
                "variable": str(variable),
            },
        )

    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="solve",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="solve",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="solve",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante la risoluzione: {exc}",
        )