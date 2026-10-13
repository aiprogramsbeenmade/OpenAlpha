"""
Operazione: grafico 2D di una funzione.

Genera un grafico di una funzione a una variabile, salvandolo come
file PNG. Il path del file è restituito nel ``Result``.

Sintassi:
    plot(expr, var="x", xmin="-10", xmax="10", output=None)

Il grafico è generato con Matplotlib in modalità ``Agg`` (nessuna
finestra), salvato su file, e il path è restituito. L'utente apre
il file con il visualizzatore di sistema.

Casi non gestiti (UNSUPPORTED):
- Funzioni che Matplotlib non riesce a plottare.
- Espressioni con più di una variabile libera (plot 3D: T4.7).

Casi di errore (ERROR):
- Input non valido.
- Range di plot non valido (xmin >= xmax).
"""

from __future__ import annotations

import os
import time

# Backend Agg: nessuna finestra, salva su file.
# Va impostato PRIMA di importare pyplot.
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import sympy

from openalpha.core.exceptions import ParserError, UnsupportedOperationError
from openalpha.core.registry import register
from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.parser import parse_expression


# Numero di punti per il grafico.
_N_POINTS = 500


def _default_output_path() -> str:
    """Genera un path di default per il file PNG."""
    timestamp = int(time.time())
    return os.path.abspath(f"plot_{timestamp}.png")


@register("plot", "Genera un grafico 2D di una funzione")
def plot(
    input_expression: str,
    var: str = "x",
    xmin: str = "-10",
    xmax: str = "10",
    output: str | None = None,
) -> Result:
    """Genera un grafico 2D di una funzione e lo salva su file.

    Args:
        input_expression: espressione come stringa.
        var: nome della variabile (default ``"x"``).
        xmin: estremo inferiore del range (default ``"-10"``).
        xmax: estremo superiore del range (default ``"10"``).
        output: path del file PNG (default: generato automaticamente).

    Returns:
        Un ``Result`` con ``exact`` contenente il path del file.
    """
    try:
        expr = parse_expression(input_expression)
        variable = sympy.Symbol(var)

        # Rifiuta espressioni con più di una variabile libera.
        free = expr.free_symbols
        if variable not in free and free:
            return Result(
                input_expression=input_expression,
                operation="plot",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"l'espressione non contiene la variabile {var!r}: "
                    f"variabili trovate: {sorted(s.name for s in free)}"
                ),
            )
        if len(free) > 1:
            return Result(
                input_expression=input_expression,
                operation="plot",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"l'espressione contiene più variabili: "
                    f"{sorted(s.name for s in free)}. "
                    "Solo plot 2D con una variabile sono supportati."
                ),
            )

        # Interpreta gli estremi.
        xmin_expr = parse_expression(xmin)
        xmax_expr = parse_expression(xmax)
        xmin_f = float(xmin_expr)
        xmax_f = float(xmax_expr)

        if xmin_f >= xmax_f:
            return Result(
                input_expression=input_expression,
                operation="plot",
                status=ResultStatus.ERROR,
                error=(
                    f"range non valido: xmin={xmin_f} >= xmax={xmax_f}"
                ),
            )

        # Genera i punti.
        x_values = np.linspace(xmin_f, xmax_f, _N_POINTS)

        # Converte l'espressione in una funzione numerica.
        f = sympy.lambdify(variable, expr, modules=["numpy"])

        try:
            y_values = f(x_values)
        except Exception as exc:
            return Result(
                input_expression=input_expression,
                operation="plot",
                status=ResultStatus.UNSUPPORTED,
                error=f"impossibile valutare la funzione sui punti: {exc}",
            )

        # Disegna.
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_values, y_values, label=str(expr))
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel(var)
        ax.set_ylabel(f"f({var})")
        ax.set_title(f"y = {expr}")
        ax.legend()

        # Salva.
        output_path = output if output else _default_output_path()
        fig.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close(fig)

        return Result(
            input_expression=input_expression,
            operation="plot",
            status=ResultStatus.EXACT,
            exact=output_path,
            metadata={
                "engine": "matplotlib",
                "matplotlib_version": matplotlib.__version__,
                "variable": var,
                "xmin": xmin,
                "xmax": xmax,
                "plot_path": output_path,
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="plot",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="plot",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="plot",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante la generazione del grafico: {exc}",
        )