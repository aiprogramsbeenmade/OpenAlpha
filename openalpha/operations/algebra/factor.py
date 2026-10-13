"""
Operazione: fattorizzazione di un'espressione algebrica.

Ricompone un'espressione nella forma fattorizzata. Complementare a
``expand``.
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.operations._base import apply_sympy_operation


@register("factor", "Fattorizza un'espressione algebrica")
def factor(input_expression: str) -> Result:
    """Fattorizza un'espressione algebrica.

    Args:
        input_expression: espressione come stringa.

    Returns:
        Un ``Result`` con ``status=EXACT`` e ``exact`` contenente la
        forma fattorizzata, oppure uno degli stati di errore.
    """
    return apply_sympy_operation(
        input_expression,
        "factor",
        sympy.factor,
        engine_error_message="Errore interno durante la fattorizzazione",
    )