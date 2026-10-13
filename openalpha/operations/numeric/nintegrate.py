"""
Operazione: integrazione numerica di un integrale definito.

Calcola numericamente il valore di un integrale definito. Utile
quando SymPy non riesce a calcolarlo simbolicamente (es.
``exp(-x**2)`` senza limiti infiniti).

Metodo: ``sympy.mpmath.quad`` (quadratura adattiva).

Sintassi:
    nintegrate(expr, var="x", lower, upper)

Casi non gestiti (UNSUPPORTED):
- Integrali che la quadratura non riesce a calcolare.
- Funzioni non supportate dal parser.
"""

from __future__ import annotations

import sympy
import mpmath

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


# Alias per gli estremi infiniti.
_BOUND_ALIASES = {
    "oo": sympy.oo,
    "inf": sympy.oo,
    "+oo": sympy.oo,
    "-oo": -sympy.oo,
    "-inf": -sympy.oo,
}


def _parse_bound(bound: str) -> sympy.Expr:
    if bound in _BOUND_ALIASES:
        return _BOUND_ALIASES[bound]
    return parse_expression(bound)


@register("nintegrate", "Calcola numericamente un integrale definito")
def nintegrate(
    input_expression: str,
    var: str = "x",
    lower: str | None = None,
    upper: str | None = None,
) -> Result:
    """Calcola numericamente un integrale definito.

    Args:
        input_expression: espressione come stringa.
        var: nome della variabile di integrazione (default ``"x"``).
        lower: estremo inferiore.
        upper: estremo superiore.

    Returns:
        Un ``Result`` con ``status=APPROXIMATE`` e ``approximate``
        contenente il valore, oppure uno stato di errore.
    """
    if lower is None or upper is None:
        return Result(
            input_expression=input_expression,
            operation="nintegrate",
            status=ResultStatus.ERROR,
            error="specificare 'lower' e 'upper' per l'integrale numerico",
        )

    try:
        expr = parse_expression(input_expression)
        variable = sympy.Symbol(var)
        lower_expr = _parse_bound(lower)
        upper_expr = _parse_bound(upper)

        # Converte l'espressione in una funzione lambda numerica.
        f = sympy.lambdify(variable, expr, modules=["mpmath"])

        # mpmath gestisce gli infiniti come mpmath.inf.
        lower_num = (
            -mpmath.inf if lower_expr == -sympy.oo
            else mpmath.inf if lower_expr == sympy.oo
            else float(lower_expr)
        )
        upper_num = (
            -mpmath.inf if upper_expr == -sympy.oo
            else mpmath.inf if upper_expr == sympy.oo
            else float(upper_expr)
        )

        result = mpmath.quad(f, [lower_num, upper_num])

        approx_str = mpmath.nstr(result, 15)

        return Result(
            input_expression=input_expression,
            operation="nintegrate",
            status=ResultStatus.APPROXIMATE,
            approximate=approx_str,
            metadata={
                "engine": "sympy.mpmath",
                "sympy_version": sympy.__version__,
                "variable": var,
                "lower": lower,
                "upper": upper,
                "method": "quadratura adattiva",
                "explanation_status": "unavailable",
                "explanation_message": (
                    "metodo numerico: il procedimento di quadratura non "
                    "è mostrato"
                ),
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="nintegrate",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="nintegrate",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:
        return Result(
            input_expression=input_expression,
            operation="nintegrate",
            status=ResultStatus.UNSUPPORTED,
            error=(
                f"impossibile calcolare l'integrale numericamente: {exc}"
            ),
        )