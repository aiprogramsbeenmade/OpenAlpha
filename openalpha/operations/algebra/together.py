"""
Operazione ``together``: combinazione su denominatore comune.

Combina una somma di frazioni in un'unica frazione.

Esempi::

    together("1/x + 1/(x+1)")  -> (2*x + 1)/(x*(x + 1))
    together("1/x + 1/y")      -> (x + y)/(x*y)
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.operations._base import apply_sympy_operation


@register(
    name="together",
    description="Combina una somma di frazioni su denominatore comune.",
)
def together(expression: str) -> Result:
    """Combina ``expression`` su denominatore comune."""
    return apply_sympy_operation(expression, "together", sympy.together)