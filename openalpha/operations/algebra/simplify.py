"""
Operazione: semplificazione di un'espressione algebrica.

Usa ``apply_sympy_operation`` per applicare ``sympy.simplify``.
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.operations._base import apply_sympy_operation


@register("simplify", "Semplifica un'espressione algebrica")
def simplify(input_expression: str) -> Result:
    """Semplifica un'espressione algebrica.

    Args:
        input_expression: espressione come stringa.

    Returns:
        Un ``Result`` con ``status=EXACT`` e ``exact`` contenente la
        forma semplificata, oppure uno degli stati di errore.
    """
    return apply_sympy_operation(
        input_expression,
        "simplify",
        sympy.simplify,
        engine_error_message="Errore interno durante la semplificazione",
    )