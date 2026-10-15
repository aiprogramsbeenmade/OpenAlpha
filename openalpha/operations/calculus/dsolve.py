"""
Operazione ``dsolve``: risoluzione di equazioni differenziali ordinarie.

Supporta ODE del primo e secondo ordine, con o senza condizioni
iniziali. La sintassi di input è "naturale" (Livello 1 + elementi del
Livello 2).

Derivate supportate::

    y'      -> y'(x)
    y''     -> y''(x)
    y'''    -> y'''(x)
    dy/dx   -> y'(x)
    d2y/dx2 -> y''(x)
    d^2y/dx^2 -> y''(x)

Funzione incognita: rilevata automaticamente tra f, y, u, v, g, h, z, w.

Variabile indipendente: rilevata dal contesto (dy/dx -> x).
Default: ``x``.

Condizioni iniziali: inline, dopo una virgola, forma ``y(0) = 1``.
Separatore: ``","``.

Esempi::

    dsolve("y' = y")                  -> y(x) = C1*exp(x)
    dsolve("y'' + y = 0")             -> y(x) = C1*sin(x) + C2*cos(x)
    dsolve("y' = y, y(0) = 1")        -> y(x) = exp(x)
    dsolve("dy/dx + y = sin(x)")      -> ...
"""

from __future__ import annotations

import re

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

# Nomi di funzione incognita riconosciuti automaticamente.
_FUNC_NAMES = ("f", "y", "u", "v", "g", "h", "z", "w")

# Pattern per riconoscere le derivate con apici: y', y'', y'''.
_APICI_RE = re.compile(r"\b([a-zA-Z])\s*('+)")

# Pattern per riconoscere le derivate Leibniz: dy/dx, d2y/dx2, d^2y/dx^2.
_LEIBNIZ_RE = re.compile(
    r"d\^?(\d*)\s*([a-zA-Z])\s*/\s*d([a-zA-Z])\^?(\d*)"
)


def _normalizza(expr: str) -> str:
    """Normalizza spazi e caratteri unicode."""
    s = expr.strip()
    s = s.replace("\u00A0", " ")
    s = s.replace("−", "-")
    s = s.replace("×", "*")
    s = s.replace("÷", "/")
    s = s.replace("’", "'")  # apostrofo tipografico
    return s


def _split_top_level(s: str, sep: str) -> list[str]:
    """Splitta ``s`` sul separatore ``sep`` ignorando le parentesi.

    Esempio::

        _split_top_level("y(0) = 1, y'(0) = 0", ",") -> ["y(0) = 1", " y'(0) = 0"]
    """
    parts = []
    depth = 0
    current = []
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return parts


def _rileva_funzione_e_var(expr: str) -> tuple[str, str, int]:
    """Rileva la funzione incognita, la variabile indipendente e l'ordine massimo.

    Returns:
        (nome_funzione, nome_variabile, ordine_massimo)

    Raises:
        ValueError: se non viene trovata alcuna derivata.
    """
    # Prova Leibniz prima (più specifico).
    m = _LEIBNIZ_RE.search(expr)
    if m:
        ordine_str, func_name, var_name, _ = m.groups()
        ordine = int(ordine_str) if ordine_str else 1
        return func_name, var_name, ordine

    # Prova apici.
    matches = _APICI_RE.findall(expr)
    if matches:
        # Prendi il primo match (di solito è la funzione principale).
        func_name, apici = matches[0]
        # Cerca l'ordine massimo tra tutti i match della stessa funzione.
        ordine = max(len(a) for f, a in matches if f == func_name)
        return func_name, "x", ordine

    raise ValueError("nessuna derivata trovata nell'equazione")


def _sostituisci_derivate(expr: str, func: str, var: str) -> str:
    """Sostituisce le derivate con placeholder.

    Esempio (func='y', var='x')::

        "y'' + y = 0"  ->  "__D2__ + y = 0"
        "dy/dx + y"    ->  "__D1__ + y"
    """
    s = expr

    # Leibniz: dy/dx, d2y/dx2, d^2y/dx^2
    def repl_leibniz(match):
        ordine_str, fname, vname, _ = match.groups()
        if fname != func or vname != var:
            return match.group(0)
        ordine = int(ordine_str) if ordine_str else 1
        return f"__D{ordine}__"

    s = _LEIBNIZ_RE.sub(repl_leibniz, s)

    # Apici: y', y'', y'''
    def repl_apici(match):
        fname, apici = match.groups()
        if fname != func:
            return match.group(0)
        return f"__D{len(apici)}__"

    s = _APICI_RE.sub(repl_apici, s)

    return s


def _sostituisci_funzione(expr: str, func: str, var: str) -> str:
    """Sostituisce le occorrenze di ``func`` (non derivate) con ``func(var)``.

    Esempio (func='y', var='x')::

        "__D2__ + y = 0"  ->  "__D2__ + y(x) = 0"
    """
    # Regex per parola intera.
    pattern = re.compile(rf"\b{re.escape(func)}\b")
    return pattern.sub(f"{func}({var})", expr)


def _parse_lato(lato: str, func: str, var: str) -> sympy.Expr:
    """Parsa un lato dell'equazione (LHS o RHS).

    Sostituisce le derivate con placeholder, sostituisce la funzione
    con ``func(var)``, parsa con ``parse_expression(..., allow_functions=True)``,
    poi sostituisce i placeholder con le derivate SymPy.
    """
    s = lato.strip()
    s = _sostituisci_derivate(s, func, var)
    s = _sostituisci_funzione(s, func, var)

    expr = parse_expression(s, allow_functions=True)

    # Sostituisci i placeholder con le derivate.
    func_sym = sympy.Function(func)
    var_sym = sympy.Symbol(var)

    for i in range(1, 10):
        placeholder = sympy.Symbol(f"__D{i}__")
        if placeholder in expr.free_symbols:
            deriv = sympy.Derivative(func_sym(var_sym), var_sym, i)
            expr = expr.subs(placeholder, deriv)

    return expr


def _parse_condizione(
    cond: str, func: str, var: str
) -> tuple[sympy.Expr, sympy.Expr]:
    """Parsa una condizione iniziale ``y(0) = 1`` in ``(y(0), 1)``.

    Restituisce la coppia (lhs, rhs) come oggetti SymPy.
    """
    if "=" not in cond:
        raise ValueError(f"condizione senza '=': {cond!r}")

    lhs_str, rhs_str = cond.split("=", 1)
    lhs_str = lhs_str.strip()
    rhs_str = rhs_str.strip()

    # Estrai il punto di valutazione da "y(0)" o "y'(0)".
    # Regex: nome_funzione [apici] ( punto )
    m = re.match(
        rf"^\s*{re.escape(func)}\s*('{{0,3}})\s*\(\s*(.+?)\s*\)\s*$",
        lhs_str,
    )
    if not m:
        raise ValueError(f"condizione non valida: {lhs_str!r}")

    apici, punto_str = m.groups()
    ordine = len(apici)
    punto = parse_expression(punto_str)

    func_sym = sympy.Function(func)
    var_sym = sympy.Symbol(var)

    if ordine == 0:
        lhs = func_sym(var_sym).subs(var_sym, punto)
    else:
        lhs = sympy.Derivative(func_sym(var_sym), var_sym, ordine).subs(
            var_sym, punto
        )

    rhs = parse_expression(rhs_str, allow_functions=True)
    return lhs, rhs


@register(
    name="dsolve",
    description="Risolve un'equazione differenziale ordinaria.",
)
def dsolve(expression: str) -> Result:
    """Risolve l'equazione differenziale ``expression``.

    Args:
        expression: ODE in sintassi naturale. Es. ``"y' = y"``,
            ``"y'' + y = 0"``, ``"y' = y, y(0) = 1"``.

    Returns:
        Un ``Result`` con status ``EXACT`` in caso di successo,
        ``ERROR`` o ``UNSUPPORTED`` in caso di problemi.
    """
    base = {
        "input_expression": expression,
        "operation": "dsolve",
    }

    if not expression or not expression.strip():
        return Result(**base, status=ResultStatus.ERROR, error="input vuoto")

    # 1. Normalizza.
    s = _normalizza(expression)

    # 2. Splitta ODE e condizioni sulla prima virgola top-level.
    parti = _split_top_level(s, ",")
    ode_str = parti[0].strip()
    condizioni_str = [p.strip() for p in parti[1:] if p.strip()]

    # 3. Rileva funzione e variabile.
    try:
        func_name, var_name, _ordine = _rileva_funzione_e_var(ode_str)
    except ValueError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))

    # 4. Split su '='.
    if "=" not in ode_str:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error="l'equazione differenziale deve contenere '='",
        )
    lhs_str, rhs_str = ode_str.split("=", 1)

    # 5. Parsa LHS e RHS.
    try:
        lhs = _parse_lato(lhs_str, func_name, var_name)
        rhs = _parse_lato(rhs_str, func_name, var_name)
    except ParserError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except UnsupportedOperationError as exc:
        return Result(**base, status=ResultStatus.UNSUPPORTED, error=str(exc))
    except OpenAlphaError as exc:
        return Result(**base, status=ResultStatus.ERROR, error=str(exc))
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.ERROR,
            error=f"impossibile interpretare l'equazione: {exc}",
        )

    eq = sympy.Eq(lhs, rhs)
    func_expr = sympy.Function(func_name)(sympy.Symbol(var_name))

    # 6. Parsa le condizioni iniziali.
    ics_dict: dict = {}
    for cond_str in condizioni_str:
        try:
            cond_lhs, cond_rhs = _parse_condizione(
                cond_str, func_name, var_name
            )
            ics_dict[cond_lhs] = cond_rhs
        except (ParserError, UnsupportedOperationError, OpenAlphaError) as exc:
            return Result(**base, status=ResultStatus.ERROR, error=str(exc))
        except Exception as exc:
            return Result(
                **base,
                status=ResultStatus.ERROR,
                error=f"condizione iniziale non valida: {exc}",
            )

    # 7. Chiama sympy.dsolve.
    try:
        if ics_dict:
            solution = sympy.dsolve(eq, func_expr, ics=ics_dict)
        else:
            solution = sympy.dsolve(eq, func_expr)
    except Exception as exc:
        return Result(
            **base,
            status=ResultStatus.UNSUPPORTED,
            error=f"impossibile risolvere l'equazione: {exc}",
        )

    # 8. Costruisci il risultato.
    return Result(
        **base,
        status=ResultStatus.EXACT,
        exact=str(solution),
        metadata={
            "var": var_name,
            "func": func_name,
            "ics": {str(k): str(v) for k, v in ics_dict.items()},
        },
    )