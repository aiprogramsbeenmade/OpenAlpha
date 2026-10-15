"""
Operazione ``series``: sviluppo in serie di Taylor (o Laurent).

Sviluppa un'espressione in serie attorno a un punto, fino a un ordine
dato. Usa ``sympy.series``, che gestisce serie di Taylor, Laurent e
sviluppi con termine ``O(...)``.

Esempi::

    series("sin(x)")                    -> x - x**3/6 + x**5/120 + O(x**6)
    series("exp(x)", order=4)           -> 1 + x + x**2/2 + x**3/6 + O(x**4)
    series("1/(1-x)", order=5)          -> 1 + x + x**2 + x**3 + x**4 + O(x**5)
    series("log(x)", point="1", order=4) -> (x-1) - (x-1)**2/2 + (x-1)**3/3 + O((x-1)**4)

Il risultato è ``EXACT`` quando SymPy calcola la serie con successo.
Il termine ``O(...)`` è incluso nel risultato.
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

# Ordine di default (SymPy usa O(x**n), quindi n=6 dà termini fino a x**5).
_DEFAULT_ORDER = 6


@register(
    name="series",
    description="Sviluppa un'espressione in serie attorno a un punto.",
)
def series(
    expression: str,
    var: str = "x",
    point: str = "0",
    order: int = _DEFAULT_ORDER,
) -> Result:
    """Sviluppa ``expression`` in serie attorno a ``point``.

    Args:
        expression: espressione da sviluppare.
        var: variabile dello sviluppo (default ``"x"``).
        point: punto di sviluppo (default ``"0"``, serie di Maclaurin).
        order: ordine di troncamento (default 6). SymPy usa ``O(x**order)``.

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo,
        ``ERROR`` o ``UNSUPPORTED`` in caso di problemi.
    """
    base = {
        "input_expression": expression,
        "operation": "series",
    }

    # Validazione di order.
    try:
        order_int = int(order)
    except (ValueError, TypeError):
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"ordine non valido: {order!r}",
        )
    if order_int < 1:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"l'ordine deve essere un intero positivo, ricevuto {order_int}",
        )

    # Parse dell'espressione e del punto.
    try:
        expr = parse_expression(expression)
        point_expr = parse_expression(point)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    # La variabile deve essere un simbolo valido.
    if not var or not var.isidentifier():
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"variabile non valida: {var!r}",
        )
    var_sym = sympy.Symbol(var)

    # Sviluppo in serie.
    try:
        result_expr = sympy.series(
            expr, var_sym, point_expr, order_int
        )
    except Exception as exc:
        # SymPy può sollevare PoleError, ValueError, NotImplementedError.
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile sviluppare in serie: {exc}",
        )

    # Rimuovi il termine O(...) per il campo "exact"? No: lo teniamo.
    # Ma il confronto con 0 va fatto sul risultato senza O.
    exact_str = str(result_expr)

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={
            "var": var,
            "point": point,
            "order": order_int,
        },
    )