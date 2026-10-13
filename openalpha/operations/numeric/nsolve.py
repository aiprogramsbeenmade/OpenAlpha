"""
Operazione: risoluzione numerica di equazioni.

Trova una radice **reale** di un'equazione, numericamente. Utile
quando SymPy non riesce a risolvere simbolicamente (es. equazioni
di grado > 4, equazioni trascendenti).

Metodo: ``sympy.nsolve`` (Newton-Raphson con punto iniziale).

Sintassi:
    nsolve(expr, var="x", initial="1")

Restituisce una sola radice. Per trovare più radici, l'utente
chiama l'operazione più volte con punti iniziali diversi.

Casi non gestiti (UNSUPPORTED):
- Equazioni senza radici reali.
- Equazioni che SymPy non riesce a valutare numericamente.
- Funzioni non supportate dal parser.
"""

from __future__ import annotations

import sympy

from openalpha.core.approximation import compute_approximate
from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


def _split_equation(input_expression: str) -> tuple[str, str]:
    """Divide l'input in lhs e rhs (come in ``solve``)."""
    if "=" in input_expression:
        lhs, _, rhs = input_expression.partition("=")
        return lhs.strip(), rhs.strip()
    return input_expression.strip(), "0"


@register("nsolve", "Trova numericamente una radice reale di un'equazione")
def nsolve(
    input_expression: str,
    var: str = "x",
    initial: str = "1",
) -> Result:
    """Trova una radice reale di un'equazione, numericamente.

    Args:
        input_expression: equazione come stringa, con o senza ``=``.
        var: nome della variabile (default ``"x"``).
        initial: punto iniziale per Newton-Raphson (default ``"1"``).

    Returns:
        Un ``Result`` con ``status=APPROXIMATE`` e ``approximate``
        contenente la radice trovata, oppure uno stato di errore.
    """
    try:
        lhs_str, rhs_str = _split_equation(input_expression)

        if not lhs_str:
            raise ParserError("lato sinistro dell'equazione vuoto")
        if not rhs_str:
            raise ParserError("lato destro dell'equazione vuoto")

        lhs = parse_expression(lhs_str)
        rhs = parse_expression(rhs_str)
        expression = lhs - rhs

        variable = sympy.Symbol(var)
        initial_expr = parse_expression(initial)

        result = sympy.nsolve(expression, variable, initial_expr)

        # nsolve restituisce un oggetto Float. Lo convertiamo a stringa.
        approx_str = str(sympy.N(result, 15))

        return Result(
            input_expression=input_expression,
            operation="nsolve",
            status=ResultStatus.APPROXIMATE,
            approximate=approx_str,
            solutions=[f"{var} ≈ {approx_str}"],
            metadata={
                "engine": "sympy",
                "sympy_version": sympy.__version__,
                "variable": var,
                "initial": initial,
                "method": "newton-raphson",
                "explanation_status": "unavailable",
                "explanation_message": (
                    "metodo numerico: il procedimento iterativo non è "
                    "mostrato"
                ),
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="nsolve",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="nsolve",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:
        # nsolve può fallire per convergenza, divisioni per zero, ecc.
        return Result(
            input_expression=input_expression,
            operation="nsolve",
            status=ResultStatus.UNSUPPORTED,
            error=(
                f"impossibile trovare una radice reale con il metodo "
                f"numerico: {exc}"
            ),
        )