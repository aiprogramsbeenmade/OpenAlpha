"""
Conversione da AST OpenAlpha a oggetti SymPy.

Questo modulo è l'unico punto del progetto in cui l'AST (definito in
``ast_nodes``) incontra SymPy. Tutto il resto del codice — parser,
validatore, operazioni — lavora con l'AST o con il ``Result``, mai
con SymPy direttamente se non attraverso questa conversione.

Responsabilità:
- Tradurre ogni nodo dell'AST in un oggetto SymPy equivalente.
- Rifiutare nomi di funzione non riconosciuti con ``UnsupportedOperationError``.
- Se ``allow_functions=True``, mappare le chiamate di funzione non note
  a ``sympy.Function(name)(arg)`` invece di rifiutarle. Usato da
  ``dsolve`` per le funzioni incognite (es. ``y(x)``).

Non è responsabilità di questo modulo:
- Validare lunghezza o profondità dell'AST (compito del validatore).
- Semplificare o manipolare il risultato (compito delle operazioni).
- Gestire il dominio o le condizioni di validità (compito delle operazioni).
"""

from __future__ import annotations

import sympy

from openalpha.core.exceptions import UnsupportedOperationError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Node,
    Number,
    Symbol,
    UnaryOp,
)

# Mappa: nome funzione nel testo → funzione SymPy corrispondente.
_FUNCTIONS: dict[str, object] = {
    "sin": sympy.sin,
    "cos": sympy.cos,
    "tan": sympy.tan,
    "asin": sympy.asin,
    "acos": sympy.acos,
    "atan": sympy.atan,
    "sinh": sympy.sinh,
    "cosh": sympy.cosh,
    "tanh": sympy.tanh,
    "exp": sympy.exp,
    "log": sympy.log,
    "sqrt": sympy.sqrt,
    "abs": sympy.Abs,
    "Abs": sympy.Abs,
}

# Mappa: nome costante nel testo → costante SymPy.
_CONSTANTS: dict[str, object] = {
    "pi": sympy.pi,
    "e": sympy.E,
    "E": sympy.E,
}

# Cache dei simboli: creare lo stesso Symbol due volte è inutile.
# Non è un problema di correttezza (SymPy li considera uguali), ma
# riduce l'allocazione.
_symbol_cache: dict[str, sympy.Symbol] = {}


def _get_symbol(name: str) -> sympy.Symbol:
    """Restituisce (con cache) un Symbol SymPy per ``name``."""
    sym = _symbol_cache.get(name)
    if sym is None:
        sym = sympy.Symbol(name)
        _symbol_cache[name] = sym
    return sym


def to_sympy(node: Node, allow_functions: bool = False) -> sympy.Expr:
    """Converte un nodo AST in un oggetto SymPy.

    Args:
        node: nodo radice dell'AST.
        allow_functions: se ``True``, le chiamate di funzione non note
            vengono mappate a ``sympy.Function(name)(arg)`` invece di
            sollevare ``UnsupportedOperationError``. Default: ``False``.

    Returns:
        L'oggetto SymPy corrispondente.

    Solleva:
        UnsupportedOperationError: se l'AST contiene una funzione non
            riconosciuta (e ``allow_functions=False``), o un tipo di
            nodo non gestito.
    """
    # Number: interi vs float.
    if isinstance(node, Number):
        try:
            return sympy.Integer(node.value)
        except (ValueError, TypeError):
            try:
                return sympy.Float(node.value)
            except (ValueError, TypeError) as exc:
                raise UnsupportedOperationError(
                    f"numero non interpretabile: {node.value!r}"
                ) from exc

    # Symbol: costante o simbolo libero.
    if isinstance(node, Symbol):
        if node.name in _CONSTANTS:
            return _CONSTANTS[node.name]  # type: ignore[return-value]
        return _get_symbol(node.name)

    # UnaryOp.
    if isinstance(node, UnaryOp):
        operand = to_sympy(node.operand, allow_functions=allow_functions)
        if node.op == "-":
            return -operand
        if node.op == "+":
            return operand
        raise UnsupportedOperationError(
            f"operatore unario non supportato: {node.op!r}"
        )

    # BinaryOp.
    if isinstance(node, BinaryOp):
        left = to_sympy(node.left, allow_functions=allow_functions)
        right = to_sympy(node.right, allow_functions=allow_functions)
        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*":
            return left * right
        if node.op == "/":
            return left / right
        if node.op in ("**", "^"):
            return left ** right
        raise UnsupportedOperationError(
            f"operatore binario non supportato: {node.op!r}"
        )

    # FunctionCall.
    if isinstance(node, FunctionCall):
        func = _FUNCTIONS.get(node.name)
        if func is not None:
            argument = to_sympy(node.argument, allow_functions=allow_functions)
            return func(argument)  # type: ignore[operator]

        if allow_functions:
            # Funzione incognita (es. y(x) in una ODE).
            argument = to_sympy(node.argument, allow_functions=allow_functions)
            return sympy.Function(node.name)(argument)

        raise UnsupportedOperationError(
            f"funzione non supportata: {node.name!r}"
        )

    # Nodo sconosciuto: non dovrebbe accadere se l'AST è ben formato.
    raise UnsupportedOperationError(
        f"tipo di nodo non gestito: {type(node).__name__}"
    )