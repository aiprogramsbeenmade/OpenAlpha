"""
Operazione: calcolo di un limite.

Calcola il limite di un'espressione per una variabile che tende a
un punto. Il punto può essere un numero, ``oo`` o ``-oo``.

Sintassi:
    limit(expr, var="x", point="0")

Il limite è **bilaterale**. I limiti laterali non sono supportati.

Casi non gestiti (UNSUPPORTED):
- Limiti che SymPy non riesce a risolvere.
- Limiti il cui risultato è ``AccumBounds`` o ``nan`` (indeterminati
  in modo non rappresentabile).
- Limiti con parametri liberi oltre alla variabile.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression
from openalpha.core.approximation import compute_approximate


# Valori speciali per il punto.
_POINT_ALIASES = {
    "oo": sympy.oo,
    "inf": sympy.oo,
    "+oo": sympy.oo,
    "-oo": -sympy.oo,
    "-inf": -sympy.oo,
}


def _parse_point(point: str) -> sympy.Expr:
    """Interpreta il punto come espressione SymPy.

    Riconosce gli alias per l'infinito (``oo``, ``-oo``, ``inf``).
    Per il resto, usa il parser normale.
    """
    if point in _POINT_ALIASES:
        return _POINT_ALIASES[point]
    return parse_expression(point)


@register("limit", "Calcola il limite di un'espressione per una variabile")
def limit(
    input_expression: str,
    var: str = "x",
    point: str = "0",
) -> Result:
    """Calcola il limite di un'espressione.

    Args:
        input_expression: espressione come stringa.
        var: nome della variabile (default ``"x"``).
        point: punto a cui tende la variabile (default ``"0"``).
            Accetta ``oo``, ``-oo``, ``inf`` come alias.

    Returns:
        Un ``Result`` con ``exact`` contenente il valore del limite,
        oppure uno degli stati di errore.
    """
    try:
        expr = parse_expression(input_expression)
        variable = sympy.Symbol(var)
        point_expr = _parse_point(point)

        # Calcola il limite bilaterale verificando i limiti laterali.
        result_right = sympy.limit(expr, variable, point_expr, dir="+")
        result_left = sympy.limit(expr, variable, point_expr, dir="-")

        if result_right != result_left:
            return Result(
                input_expression=input_expression,
                operation="limit",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"il limite bilaterale non esiste: "
                    f"limite da destra = {result_right}, "
                    f"limite da sinistra = {result_left}"
                ),
            )

        result = result_right

        # Rifiuta risultati non rappresentabili.
        if result is sympy.nan or isinstance(result, sympy.AccumBounds):
            return Result(
                input_expression=input_expression,
                operation="limit",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"il limite non esiste o è indeterminato in modo "
                    f"non rappresentabile (risultato: {result})"
                ),
            )

        return Result(
            input_expression=input_expression,
            operation="limit",
            status=ResultStatus.EXACT,
            exact=str(result),
            approximate=compute_approximate(str(result)),
            metadata={
                "engine": "sympy",
                "sympy_version": sympy.__version__,
                "variable": var,
                "point": point,
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="limit",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="limit",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="limit",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante il calcolo del limite: {exc}",
        )