"""
Operazione ``evaluate``: calcolo numerico diretto di un'espressione.

Prende un'espressione senza variabili libere e ne calcola il valore
numerico. Il risultato può essere:

- ``EXACT``: l'espressione è già un valore numerico esatto
  (es. ``2 + 3 * 4`` → ``14``). Il campo ``approximate`` contiene
  comunque la rappresentazione decimale.
- ``APPROXIMATE``: l'espressione è simbolica ma il valore numerico è
  calcolabile (es. ``sqrt(2)`` → ``1.414...``). Il campo ``exact``
  contiene la forma simbolica, ``approximate`` il decimale.

Esempi::

    evaluate("2 + 3 * 4")   -> EXACT, exact="14"
    evaluate("sin(pi/2)")   -> EXACT, exact="1"
    evaluate("sqrt(2)")     -> APPROXIMATE, exact="sqrt(2)",
                               approximate="1.4142135623731"
    evaluate("1/3")         -> APPROXIMATE, exact="1/3",
                               approximate="0.333333333333333"

L'operazione rifiuta espressioni con variabili libere: ``evaluate(x+1)``
restituisce ``ERROR``. Il caso d'uso è "calcola questo numero", non
"semplifica questa espressione".
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

# Numero di cifre significative per l'approssimazione.
_DIGITS = 15


def _clean_decimal(s: str) -> str:
    """Rimuove gli zeri finali da una stringa decimale.

    Esempi::

        "1.00000000000000"  -> "1"
        "1.50000000000000"  -> "1.5"
        "1.41421356237310"  -> "1.4142135623731"
        "14.0000000000000"  -> "14"
        "3.14159265358979"  -> "3.14159265358979"

    Non tocca stringhe in notazione scientifica (es. ``1e-20``) né
    stringhe senza punto decimale.
    """
    if "." not in s or "e" in s.lower():
        return s
    s = s.rstrip("0").rstrip(".")
    return s


@register(
    name="evaluate",
    description="Calcola il valore numerico di un'espressione.",
)
def evaluate(expression: str) -> Result:
    """Calcola il valore numerico di ``expression``.

    Args:
        expression: espressione matematica senza variabili libere.

    Returns:
        Un ``Result`` con status ``EXACT`` o ``APPROXIMATE``, oppure
        ``ERROR`` / ``UNSUPPORTED`` in caso di problemi.

    Note:
        L'operazione non gestisce espressioni con variabili libere
        (es. ``x + 1``): restituisce ``ERROR``.
    """
    base = {
        "input_expression": expression,
        "operation": "evaluate",
    }

    # 1. Parse dell'input.
    try:
        expr = parse_expression(expression)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    # 2. Variabili libere?
    free = expr.free_symbols
    if free:
        names = ", ".join(sorted(str(s) for s in free))
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=(
                f"l'espressione contiene variabili libere: {names}. "
                f"Usa un'espressione numerica."
            ),
        )

    # 3. Approssimazione numerica.
    try:
        approx = sympy.N(expr, _DIGITS)
    except Exception as exc:  # pragma: no cover — difensivo
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"impossibile calcolare il valore numerico: {exc}",
        )

    # 4. Determina lo status: è esatto se il valore è un intero,
    #    un razionale con denominatore che ha solo fattori 2 e 5
    #    (decimale finito), o un Float.
    exact_str = _clean_decimal(str(expr))
    approx_str = _clean_decimal(str(approx))

    is_exact = False
    if expr.is_Integer or expr.is_Float:
        is_exact = True
    elif expr.is_Rational:
        # Razionale: esatto solo se il denominatore ha solo fattori 2 e 5.
        den = expr.q
        while den % 2 == 0:
            den //= 2
        while den % 5 == 0:
            den //= 5
        is_exact = (den == 1)

    if is_exact:
        return Result(
            **base,
            status=ResultStatus.EXACT,
            exact=exact_str,
            approximate=approx_str,
        )

    return Result(
        **base,
        status=ResultStatus.APPROXIMATE,
        exact=exact_str,
        approximate=approx_str,
    )