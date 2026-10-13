"""
Operazione: grafico 3D di una funzione a due variabili.

Genera una superficie 3D di una funzione ``f(x, y)``, salvandola
come file PNG. Il path del file è restituito nel ``Result``.

Sintassi:
    plot3d(expr, xvar="x", yvar="y",
           xmin="-5", xmax="5", ymin="-5", ymax="5", output=None)

Il grafico è generato con Matplotlib in modalità ``Agg`` (nessuna
finestra), salvato su file, e il path è restituito.

Casi non gestiti (UNSUPPORTED):
- Espressioni con meno di due variabili (usare ``plot`` per il 2D).
- Espressioni con più di due variabili.
- Funzioni non supportate.

Casi di errore (ERROR):
- Input non valido.
- Range di plot non valido (xmin >= xmax, o ymin >= ymax).
"""

from __future__ import annotations

import os
import time

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


# Numero di punti per lato della griglia.
_N_POINTS = 50


def _default_output_path() -> str:
    """Genera un path di default per il file PNG."""
    timestamp = int(time.time())
    return os.path.abspath(f"plot3d_{timestamp}.png")


@register("plot3d", "Genera un grafico 3D di una funzione a due variabili")
def plot3d(
    input_expression: str,
    xvar: str = "x",
    yvar: str = "y",
    xmin: str = "-5",
    xmax: str = "5",
    ymin: str = "-5",
    ymax: str = "5",
    output: str | None = None,
) -> Result:
    """Genera un grafico 3D di una funzione a due variabili.

    Args:
        input_expression: espressione come stringa.
        xvar: nome della prima variabile (default ``"x"``).
        yvar: nome della seconda variabile (default ``"y"``).
        xmin: estremo inferiore di x (default ``"-5"``).
        xmax: estremo superiore di x (default ``"5"``).
        ymin: estremo inferiore di y (default ``"-5"``).
        ymax: estremo superiore di y (default ``"5"``).
        output: path del file PNG (default: generato automaticamente).

    Returns:
        Un ``Result`` con ``exact`` contenente il path del file.
    """
    try:
        expr = parse_expression(input_expression)
        x_sym = sympy.Symbol(xvar)
        y_sym = sympy.Symbol(yvar)

        free = expr.free_symbols

        # Controlli sulle variabili.
        if len(free) == 0:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "l'espressione non contiene variabili: "
                    "non è una funzione"
                ),
            )
        if len(free) == 1:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    "l'espressione contiene una sola variabile: "
                    "usa 'plot' per il grafico 2D"
                ),
            )
        if len(free) > 2:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.UNSUPPORTED,
                error=(
                    f"l'espressione contiene più di due variabili: "
                    f"{sorted(s.name for s in free)}. "
                    "Solo plot 3D con due variabili sono supportati."
                ),
            )

        # Interpreta i range.
        xmin_f = float(parse_expression(xmin))
        xmax_f = float(parse_expression(xmax))
        ymin_f = float(parse_expression(ymin))
        ymax_f = float(parse_expression(ymax))

        if xmin_f >= xmax_f:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.ERROR,
                error=f"range x non valido: {xmin_f} >= {xmax_f}",
            )
        if ymin_f >= ymax_f:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.ERROR,
                error=f"range y non valido: {ymin_f} >= {ymax_f}",
            )

        # Griglia.
        x_vals = np.linspace(xmin_f, xmax_f, _N_POINTS)
        y_vals = np.linspace(ymin_f, ymax_f, _N_POINTS)
        X, Y = np.meshgrid(x_vals, y_vals)

        # Funzione numerica.
        f = sympy.lambdify((x_sym, y_sym), expr, modules=["numpy"])

        try:
            Z = f(X, Y)
        except Exception as exc:
            return Result(
                input_expression=input_expression,
                operation="plot3d",
                status=ResultStatus.UNSUPPORTED,
                error=f"impossibile valutare la funzione sulla griglia: {exc}",
            )

        # Disegna la superficie.
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9)
        ax.set_xlabel(xvar)
        ax.set_ylabel(yvar)
        ax.set_zlabel(f"f({xvar}, {yvar})")
        ax.set_title(f"z = {expr}")

        # Salva.
        output_path = output if output else _default_output_path()
        fig.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close(fig)

        return Result(
            input_expression=input_expression,
            operation="plot3d",
            status=ResultStatus.EXACT,
            exact=output_path,
            metadata={
                "engine": "matplotlib",
                "matplotlib_version": matplotlib.__version__,
                "xvar": xvar,
                "yvar": yvar,
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
                "plot_path": output_path,
            },
        )
    except UnsupportedOperationError as exc:
        return Result(
            input_expression=input_expression,
            operation="plot3d",
            status=ResultStatus.UNSUPPORTED,
            error=str(exc),
        )
    except ParserError as exc:
        return Result(
            input_expression=input_expression,
            operation="plot3d",
            status=ResultStatus.ERROR,
            error=f"Input non valido: {exc}",
        )
    except Exception as exc:  # pragma: no cover — rete di sicurezza
        return Result(
            input_expression=input_expression,
            operation="plot3d",
            status=ResultStatus.ERROR,
            error=f"Errore interno durante la generazione del grafico 3D: {exc}",
        )