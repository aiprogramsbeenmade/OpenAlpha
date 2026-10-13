"""
Operazione: espansione di un'espressione algebrica.

Sviluppa prodotti e potenze nella forma estesa. Complementare a
``simplify``.
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.operations._base import apply_sympy_operation


@register("expand", "Sviluppa prodotti e potenze di un'espressione algebrica")
def expand(input_expression: str) -> Result:
    """Espande un'espressione algebrica.

    Args:
        input_expression: espressione come stringa.

    Returns:
        Un ``Result`` con ``status=EXACT`` e ``exact`` contenente la
        forma espansa, oppure uno degli stati di errore.
    """
    return apply_sympy_operation(
        input_expression,
        "expand",
        sympy.expand,
        engine_error_message="Errore interno durante l'espansione",
    )