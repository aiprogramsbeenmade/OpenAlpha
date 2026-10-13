"""
Operazione: integrale indefinito o definito.

Due modalità:

1. **Indefinito**: ``integrate(expr)`` → ``sympy.integrate(expr, var)``.
   Aggiunge ``+ C`` al risultato.

2. **Definito**: ``integrate(expr, lower=..., upper=...)`` →
   ``sympy.integrate(expr, (var, lower, upper))``. Nessuna costante.

Casi non gestiti (UNSUPPORTED):
- Integrali che SymPy non riesce a calcolare.
- Integrali definiti con risultato ``nan``, ``zoo``, ``oo``, ``-oo``.

Casi di errore (ERROR):
- ``lower`` specificato senza ``upper``, o viceversa.
- Input non valido.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.explanations.domain import collect_conditions
from openalpha.parser import parse_expression
from openalpha.core.approximation import compute_approximate


# Valori speciali per i limiti di integrazione.
_BOUND_ALIASES = {
    "oo": sympy.oo,
    "inf": sympy.oo,
    "+oo": sympy.oo,
    "-oo": -sympy.oo,
    "-inf": -sympy.oo,
}


def _parse_bound(bound: str) -> sympy.Expr:
    """Interpreta un estremo di integrazione."""
    if bound in _BOUND_ALIASES:
        return _BOUND_ALIASES[bound]
    return parse_expression(bound)


@register("integrate", "Calcola l'integrale indefinito o definito di un'espressione")
def integrate(
    input_expression: str,
    var: str = "x",
    lower: str | None = None,
    upper: str | None = None,
) -> Result:
    """Calcola un integrale.

    Args:
        input_expression: espressione come stringa.
        var: nome della variabile di integrazione (default ``"x"``).
        lower: estremo inferiore (per integrale definito). ``None``
            per integrale indefinito.
        upper: estremo superiore (per integrale definito).

    Returns:
        Un ``Result`` con ``exact`` contenente il risultato.
    """
    # Validazione: lower e upper vanno specificati insieme o nessuno.
    if (lower is None) != (upper is None):
        return Result(
            input_expression=input_expression,
            operation="integrate",
            status=ResultStatus.ERROR,
            error=(
                "specificare entrambi 'lower' e 'upper', oppure nessuno "
                "dei due"
            ),
        )

    is_definite = lower is not None and upper is not None

    try:
        expr = parse_expression(input_expression)
        variable = sympy.Symbol(var)

        if is_definite:
            lower_expr = _parse_bound(lower)
            upper_expr = _parse_bound(upper)
            result = sympy.integrate(expr, (variable, lower_expr, upper_expr))

            # Rifiuta risultati non rappresentabili.
            if result is sympy.nan or result in (sympy.zoo, sympy.oo, -sympy.oo):
                return Result(
                    input_expression=input_expression,
                    operation="integrate",
                    status=ResultStatus.UNSUPPORTED,
                    error=(
                        f"integrale definito non calcolabile o divergente "
                        f"(risultato: {result})"
                    ),
                )

            exact_str = str(result)
            return Result(
                input_expression=input_expression,
                operation="integrate",
                status=ResultStatus.EXACT,
                exact=exact_str,
                approximate=compute_approximate(exact_str),
                metadata={
                    "engine": "sympy",
                    "sympy_version": sympy.__version__,
                    "variable": var,
                    "lower": lower,
                    "upper": upper,
                },
            )
        else:
            # Integrale indefinito.
            result = sympy.integrate(expr, variable)

            # Rifiuta risultati non calcolabili.
            if result.has(sympy.Integral):
                return Result(
                    input_expression=input_expression,
                    operation="integrate",
                    status=ResultStatus.UNSUPPORTED,
                    error=(
                        "integrale non calcolabile in forma chiusa: "
                        "SymPy ha restituito l'integrale non risolto"
                    ),
                )

            # Aggiungi + C (o solo C se il risultato è 0).
            if result == 0:
                exact = "C"
            else:
                exact = f"{result} + C"

            conditions = collect_conditions(expr)
            status = ResultStatus.PARTIAL if conditions else ResultStatus.EXACT

            return Result(
                input_expression=input_expression,
                operation="integrate",
                status=status,
                exact=exact,
                conditions=conditions,
                approximate=compute_approximate(str(result)),
                metadata={
                    "engine": "sympy",
                    "sympy_version": sympy.__version__,
                    "variable": var,
                },
            )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="integrate",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="integrate",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="integrate",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante il calcolo dell'integrale: {exc}",
        )