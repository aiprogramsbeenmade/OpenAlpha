"""
Operazione: derivata di un'espressione.

Calcola la derivata (prima, seconda, ...) di un'espressione rispetto
a una variabile.

Sintassi:
    diff(expr, var="x", order=1)

Casi non gestiti (UNSUPPORTED):
- Derivate di funzioni non note.
- Derivate parziali multiple.

Casi di errore (ERROR):
- ``order`` non intero o minore di 1.
- Input non valido.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression
from openalpha.core.approximation import compute_approximate


@register("diff", "Calcola la derivata di un'espressione rispetto a una variabile")
def diff(
    input_expression: str,
    var: str = "x",
    order: int = 1,
) -> Result:
    """Calcola la derivata di un'espressione.

    Args:
        input_expression: espressione come stringa.
        var: nome della variabile (default ``"x"``).
        order: ordine della derivata (default ``1``). Deve essere un
            intero positivo.

    Returns:
        Un ``Result`` con ``exact`` contenente la derivata, oppure
        uno degli stati di errore.
    """
    # Validazione di order PRIMA del parsing: è un errore d'uso.
    if not isinstance(order, int) or isinstance(order, bool):
        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.ERROR,
            error=f"'order' deve essere un intero, ricevuto {type(order).__name__}",
        )
    if order < 1:
        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.ERROR,
            error=f"'order' deve essere >= 1, ricevuto {order}",
        )

    try:
        expr = parse_expression(input_expression)
        variable = sympy.Symbol(var)

        result = sympy.diff(expr, variable, order)

        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.EXACT,
            exact=str(result),
            approximate=compute_approximate(str(result)),
            metadata={
                "engine": "sympy",
                "sympy_version": sympy.__version__,
                "variable": var,
                "order": order,
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="diff",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante il calcolo della derivata: {exc}",
        )