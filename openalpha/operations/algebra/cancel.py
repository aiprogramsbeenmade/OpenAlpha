"""
Operazione ``cancel``: semplificazione di frazioni razionali.

Riduce una frazione razionale ai minimi termini, cancellando i fattori
comuni tra numeratore e denominatore.

Esempi::

    cancel("(x**2 - 1)/(x - 1)")        -> x + 1
    cancel("(x**2 + 2*x + 1)/(x + 1)")  -> x + 1
"""

from __future__ import annotations

import sympy

from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.operations._base import apply_sympy_operation


@register(
    name="cancel",
    description="Riduce una frazione razionale ai minimi termini.",
)
def cancel(expression: str) -> Result:
    """Riduce ``expression`` ai minimi termini."""
    return apply_sympy_operation(expression, "cancel", sympy.cancel)
