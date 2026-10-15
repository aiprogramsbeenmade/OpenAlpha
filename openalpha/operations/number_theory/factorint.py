"""
Operazione ``factorint``: fattorizzazione in numeri primi.

Scompone un intero positivo nel prodotto di potenze di primi.

Esempi::

    factorint(24)   -> {2: 3, 3: 1}       (24 = 2**3 * 3)
    factorint(100)  -> {2: 2, 5: 2}       (100 = 2**2 * 5**2)
    factorint(7)    -> {7: 1}
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
    name="factorint",
    description="Fattorizza un intero in numeri primi.",
)
def factorint(expression: str) -> Result:
    """Fattorizza ``expression`` in numeri primi."""
    base = {"input_expression": expression, "operation": "factorint"}

    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    if not expr.is_Integer:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"fattorizzazione richiede un intero, ricevuto: {expr}",
        )

    n = int(expr)
    if n <= 0:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"fattorizzazione richiede un intero positivo, ricevuto: {n}",
        )

    try:
        factors = sympy.factorint(n)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile fattorizzare: {exc}",
        )

    # Formato leggibile: "2^3 * 3" invece di "{2: 3, 3: 1}"
    parti = []
    parti_latex = []
    for primo, esponente in sorted(factors.items()):
        if esponente == 1:
            parti.append(str(primo))
            parti_latex.append(str(primo))
        else:
            parti.append(f"{primo}^{esponente}")
            parti_latex.append(f"{primo}^{{{esponente}}}")

    if not parti:
        # 1 non ha fattori primi: la sua fattorizzazione è il
        # prodotto vuoto, che per convenzione è 1.
        exact_str = "1"
        latex_str = "1"
    else:
        exact_str = " * ".join(parti)
        latex_str = " \\cdot ".join(parti_latex)

    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=exact_str,
        metadata={
            "factors": {str(k): v for k, v in factors.items()},
            # Il risultato è una stringa formattata ("2^3 * 3"),
            # non un'espressione matematica. SymPy la valuterebbe
            # (2^3 * 3 = 24). Forniamo il LaTeX già pronto, così
            # il frontend lo renderizza senza rivalutarlo.
            "latex_exact": latex_str,
        },
    )