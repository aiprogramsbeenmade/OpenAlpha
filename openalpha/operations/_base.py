"""
Helper interno per la costruzione di operazioni OpenAlpha.

Ogni operazione che applica una funzione SymPy a un'espressione
condivide lo stesso pattern:

1. Interpretare l'input con ``parse_expression``.
2. Raccogliere le condizioni di validità dell'input (dominio).
3. Tentare di spiegare l'input applicando le regole verificate.
4. Applicare la funzione SymPy per il risultato finale.
5. Restituire un ``Result`` con ``status=PARTIAL`` se ci sono
   condizioni, ``EXACT`` altrimenti, e ``steps`` popolati se
   il motore delle spiegazioni ha prodotto passi.
6. Gestire le eccezioni.
"""

from __future__ import annotations

from typing import Any, Callable

import sympy

from openalpha.core.exceptions import (
    ParserError,
    UnsupportedOperationError,
)
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.explanations.domain import collect_conditions
from openalpha.explanations.engine import explain
from openalpha.parser import parse_expression
from openalpha.core.approximation import compute_approximate


def apply_sympy_operation(
    input_expression: str,
    operation_name: str,
    func: Callable[..., sympy.Expr],
    *,
    engine_error_message: str = "Errore interno durante il calcolo",
    **func_kwargs: Any,
) -> Result:
    """Applica una funzione SymPy a un'espressione e restituisce un ``Result``.

    Le condizioni di validità sono raccolte **sull'input parsato**.
    I passi delle spiegazioni sono raccolti **sull'input parsato**,
    prima di applicare ``func``. Motivo: le regole operano
    sull'espressione di partenza, non su come SymPy la riscrive.

    Args:
        input_expression: espressione come stringa.
        operation_name: nome dell'operazione.
        func: funzione SymPy da applicare per il risultato finale.
            Può accettare argomenti extra tramite ``func_kwargs``.
        engine_error_message: messaggio per errori imprevisti.
        **func_kwargs: argomenti extra da passare a ``func``.

    Returns:
        Un ``Result`` con ``exact``, ``steps``, ``conditions`` popolati
        a seconda dei casi.
    """
    try:
        expr = parse_expression(input_expression)
        conditions = collect_conditions(expr)
        explanation = explain(expr)
        result_expr = func(expr, **func_kwargs)
        exact_str = str(result_expr)

        status = ResultStatus.PARTIAL if conditions else ResultStatus.EXACT

        metadata = {
            "engine": "sympy",
            "sympy_version": sympy.__version__,
            "explanation_complete": explanation.complete,
            "explanation_status": explanation.status,
            "explanation_message": explanation.message,
        }

        return Result(
            input_expression=input_expression,
            operation=operation_name,
            status=status,
            exact=exact_str,
            approximate=compute_approximate(exact_str),
            steps=explanation.steps,
            conditions=conditions,
            metadata=metadata,
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation=operation_name,
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation=operation_name,
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation=operation_name,
            status=ResultStatus.ERROR,
            error=f"{engine_error_message}: {exc}",
        )