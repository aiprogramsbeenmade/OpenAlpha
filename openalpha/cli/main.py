"""
Interfaccia a riga di comando di OpenAlpha.

Comandi supportati::

    python -m openalpha "sin(x)**2 + cos(x)**2"
    python -m openalpha --list
    python -m openalpha --operation simplify "x + x"
    python -m openalpha --help

Exit code:
    0  successo
    1  errore di calcolo (status=ERROR)
    2  errore d'uso (argomenti mancanti, operazione non supportata)
"""

from __future__ import annotations

import argparse
import sys

from openalpha.core.exceptions import OpenAlphaError
from openalpha.core.registry import get_operation, list_operations
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus

# L'import di ``openalpha.operations`` registra le operazioni disponibili.
# Va fatto DOPO gli import del core, ma PRIMA di qualsiasi uso del registro.
import openalpha.operations  # noqa: F401


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openalpha",
        description="Calcolatore matematico simbolico locale.",
        epilog="Esempio: python -m openalpha \"sin(x)**2 + cos(x)**2\"",
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="Espressione matematica da elaborare.",
    )
    parser.add_argument(
        "--operation",
        "-o",
        default="simplify",
        help="Nome dell'operazione da eseguire (default: simplify).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Elenca le operazioni disponibili ed esce.",
    )
    parser.add_argument(
        "--var",
        default="x",
        help="Variabile (per limit, diff). Default: x.",
    )
    parser.add_argument(
        "--point",
        default="0",
        help="Punto (per limit). Default: 0.",
    )
    parser.add_argument(
        "--order",
        default="1",
        help="Ordine della derivata (per diff). Default: 1.",
    )
    parser.add_argument(
        "--from",
        dest="lower",
        default=None,
        help="Estremo inferiore (per integrate).",
    )
    parser.add_argument(
        "--to",
        dest="upper",
        default=None,
        help="Estremo superiore (per integrate).",
    )
    parser.add_argument(
        "--initial",
        default="1",
        help="Punto iniziale (per nsolve). Default: 1.",
    )
    return parser


def _format_result(result: Result) -> str:
    """Formatta un Result per la stampa a terminale."""
    lines = [
        f"input:       {result.input_expression}",
        f"operation:   {result.operation}",
        f"status:      {result.status.value}",
    ]
    if result.exact is not None:
        lines.append(f"exact:       {result.exact}")
    if result.approximate is not None:
        lines.append(f"approximate: {result.approximate}")
    if result.solutions:
        lines.append(f"solutions:   {', '.join(result.solutions)}")
    if result.conditions:
        lines.append(f"conditions:  {', '.join(result.conditions)}")
    if result.error is not None:
        lines.append(f"error:       {result.error}")

    if result.steps:
        lines.append("")
        lines.append("procedimento:")
        from openalpha.explanations.formatter import format_steps
        lines.append(format_steps(result.steps))
    elif result.metadata.get("explanation_message"):
        lines.append("")
        lines.append(f"nota: {result.metadata['explanation_message']}")

    return "\n".join(lines)


def _exit_code_for(result: Result) -> int:
    """Mappa lo stato di un Result a un exit code."""
    if result.status is ResultStatus.ERROR:
        return 1
    if result.status is ResultStatus.UNSUPPORTED:
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point della CLI. Restituisce l'exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list:
        ops = list_operations()
        if not ops:
            print("Nessuna operazione disponibile.")
        else:
            print("Operazioni disponibili:")
            for name in ops:
                spec = get_operation(name)
                print(f"  {name:<12} {spec.description}")
        return 0

    if args.expression is None:
        parser.print_usage(sys.stderr)
        print("openalpha: errore: manca l'espressione da elaborare", file=sys.stderr)
        return 2

    # Recupera l'operazione dal registro.
    try:
        spec = get_operation(args.operation)
    except OpenAlphaError as exc:
        print(f"openalpha: errore: {exc}", file=sys.stderr)
        return 2

    # Dispatch: alcune operazioni accettano parametri extra.
    try:
        if args.operation == "limit":
            result: Result = spec.function(
                args.expression, var=args.var, point=args.point
            )
        elif args.operation == "diff":
            try:
                order = int(args.order)
            except ValueError:
                print(
                    f"openalpha: errore: --order deve essere un intero, "
                    f"ricevuto {args.order!r}",
                    file=sys.stderr,
                )
                return 2
            result = spec.function(args.expression, var=args.var, order=order)
        elif args.operation == "integrate":
            result = spec.function(
                args.expression,
                var=args.var,
                lower=args.lower,
                upper=args.upper,
            )
        elif args.operation == "nsolve":
            result = spec.function(
                args.expression,
                var=args.var,
                initial=args.initial,
            )
        elif args.operation == "nintegrate":
            result = spec.function(
                args.expression,
                var=args.var,
                lower=args.lower,
                upper=args.upper,
            )
        else:
            result = spec.function(args.expression)
    except TypeError as exc:
        print(f"openalpha: errore: {exc}", file=sys.stderr)
        return 2

    print(_format_result(result))
    return _exit_code_for(result)