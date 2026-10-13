"""
Operazione: risoluzione di sistemi di equazioni lineari.

Accetta più equazioni separate da ``;``. Risolve il sistema se è
lineare, quadrato, e ha soluzione unica.

Sintassi:
    solve_system("x + y = 3; x - y = 1")

Restituisce una lista di soluzioni, una per variabile:
    solutions=["x = 2", "y = 1"]

Casi non gestiti (UNSUPPORTED):
- Sistemi con meno di 2 equazioni.
- Sistemi non lineari.
- Sistemi inconsistenti (nessuna soluzione).
- Sistemi indeterminati (infinite soluzioni).

Casi di errore (ERROR):
- Input non valido.
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


def _split_equations(input_expression: str) -> list[str]:
    """Divide l'input in equazioni separate da ``;``."""
    parts = [p.strip() for p in input_expression.split(";")]
    return [p for p in parts if p]


def _parse_equation(eq_str: str) -> sympy.Expr:
    """Interpreta ``lhs = rhs`` come ``lhs - rhs`` (espressione = 0)."""
    if "=" in eq_str:
        lhs_str, _, rhs_str = eq_str.partition("=")
        lhs_str = lhs_str.strip()
        rhs_str = rhs_str.strip()
        if not lhs_str or not rhs_str:
            raise ParserError(f"equazione malformata: {eq_str!r}")
        lhs = parse_expression(lhs_str)
        rhs = parse_expression(rhs_str)
        return lhs - rhs
    else:
        return parse_expression(eq_str)


@register("solve_system", "Risolve un sistema di equazioni lineari")
def solve_system(input_expression: str) -> Result:
    """Risolve un sistema di equazioni lineari.

    Args:
        input_expression: equazioni separate da ``;``.

    Returns:
        Un ``Result`` con ``solutions`` popolato, oppure uno stato
        di errore.
    """
    try:
        eq_strings = _split_equations(input_expression)

        if len(eq_strings) < 2:
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.ERROR,
                error=(
                    "un sistema richiede almeno 2 equazioni separate "
                    "da ';'"
                ),
            )

        equations = [_parse_equation(eq) for eq in eq_strings]

        # Trova le variabili.
        all_symbols: set[sympy.Symbol] = set()
        for eq in equations:
            all_symbols |= eq.free_symbols

        if not all_symbols:
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.ERROR,
                error="nessuna variabile nelle equazioni",
            )

        variables = sorted(all_symbols, key=lambda s: s.name)

        # Prova a risolvere come sistema lineare.
        try:
            solution = sympy.linsolve(equations, variables)
        except Exception as exc:
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.UNSUPPORTED,
                error=f"impossibile risolvere il sistema: {exc}",
            )

        # `linsolve` restituisce un `FiniteSet` di tuple.
        # - Vuoto: nessuna soluzione.
        # - Con una tupla: soluzione unica (o parametrizzata).
        # - Con un insieme con parametri: infinite soluzioni.

        if not solution:
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.UNSUPPORTED,
                error="il sistema non ha soluzioni",
            )

        # Prende la prima (e unica) tupla.
        try:
            solutions_tuple = next(iter(solution))
        except StopIteration:
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.UNSUPPORTED,
                error="il sistema non ha soluzioni",
            )

        # Verifica che sia una tupla di valori (non parametrizzata).
        # Verifica che sia una tupla (Python o SymPy) di valori.
        # SymPy usa `sympy.core.containers.Tuple`, che non è una
        # sottoclasse di `tuple`, ma si comporta come tale.
        if not isinstance(solutions_tuple, (tuple, sympy.Tuple)):
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "il sistema non ha una soluzione unica "
                    "(forse indeterminato)"
                ),
            )

        # Converte a tuple Python per uniformità.
        solutions_tuple = tuple(solutions_tuple)

        # Verifica che il numero di valori corrisponda al numero di variabili.
        if len(solutions_tuple) != len(variables):
            return Result(
                input_expression=input_expression,
                operation="solve_system",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "il sistema non ha una soluzione unica"
                ),
            )

        # Verifica che non ci siano parametri liberi.
        for val in solutions_tuple:
            if not val.is_number:
                return Result(
                    input_expression=input_expression,
                    operation="solve_system",
                    status=ResultStatus.UNSUPPORTED,
                    error=(
                        "il sistema ha infinite soluzioni o soluzioni "
                        "parametriche: non supportato"
                    ),
                )

        # Costruisce le soluzioni.
        solution_strings = [
            f"{var} = {val}" for var, val in zip(variables, solutions_tuple)
        ]

        return Result(
            input_expression=input_expression,
            operation="solve_system",
            status=ResultStatus.EXACT,
            solutions=solution_strings,
            metadata={
                "engine": "sympy",
                "sympy_version": sympy.__version__,
                "variables": [s.name for s in variables],
            },
        )

    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="solve_system",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="solve_system",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="solve_system",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante la risoluzione del sistema: {exc}",
        )