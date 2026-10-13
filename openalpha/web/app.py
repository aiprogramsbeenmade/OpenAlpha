"""
Server Flask per l'interfaccia web locale di OpenAlpha.
"""

from __future__ import annotations

import base64
import os
import webbrowser
import numpy as np
from threading import Timer
from typing import Any

from flask import Flask, jsonify, render_template, request
from sympy import latex
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

from openalpha.core.exceptions import OpenAlphaError
from openalpha.core.registry import get_operation, list_operations
from openalpha.core.result import Result
from openalpha.parser import parse_expression

import openalpha.operations  # noqa: F401


_RENDER_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

# Operazioni che producono un grafico (file PNG).
_PLOT_OPERATIONS = {"plot", "plot3d"}


def _serialize_result(result: Result) -> dict:
    """Serializza un ``Result`` in un dizionario JSON-compatibile."""
    return {
        "operation": result.operation,
        "status": result.status.value,
        "exact": result.exact,
        "approximate": result.approximate,
        "solutions": result.solutions,
        "steps": [
            {
                "before": step.before,
                "after": step.after,
                "rule_name": step.rule_name,
                "description": step.description,
                "conditions": step.conditions,
            }
            for step in result.steps
        ],
        "conditions": result.conditions,
        "error": result.error,
        "metadata": result.metadata,
    }

def _genera_dati_plot3d(
    expression: str,
    xvar: str = "x",
    yvar: str = "y",
    xmin: str = "-5",
    xmax: str = "5",
    ymin: str = "-5",
    ymax: str = "5",
    n_points: int = 50,
) -> dict:
    """Genera i dati per un grafico 3D interattivo (Plotly).

    Restituisce un dizionario con:
        x_values: lista di N valori
        y_values: lista di M valori
        z_matrix: matrice M x N di valori (o None per punti non finiti)
        title: titolo del grafico
    """
    import sympy

    expr = parse_expression(expression)
    x_sym = sympy.Symbol(xvar)
    y_sym = sympy.Symbol(yvar)

    xmin_f = float(parse_expression(xmin))
    xmax_f = float(parse_expression(xmax))
    ymin_f = float(parse_expression(ymin))
    ymax_f = float(parse_expression(ymax))

    if xmin_f >= xmax_f:
        raise ValueError(f"range x non valido: {xmin_f} >= {xmax_f}")
    if ymin_f >= ymax_f:
        raise ValueError(f"range y non valido: {ymin_f} >= {ymax_f}")

    x_vals = np.linspace(xmin_f, xmax_f, n_points)
    y_vals = np.linspace(ymin_f, ymax_f, n_points)
    X, Y = np.meshgrid(x_vals, y_vals)

    f = sympy.lambdify((x_sym, y_sym), expr, modules=["numpy"])
    Z = f(X, Y)
    Z = np.asarray(Z, dtype=float)

    # Sostituisci NaN e Inf con None (Plotly li gestisce come buchi).
    Z_list = [
        [None if (not np.isfinite(z)) else float(z) for z in row]
        for row in Z
    ]

    return {
        "x_values": x_vals.tolist(),
        "y_values": y_vals.tolist(),
        "z_matrix": Z_list,
        "title": f"z = {expr}",
        "xvar": xvar,
        "yvar": yvar,
    }


def _try_latex(expr_str: str) -> str | None:
    """Prova a convertire un'espressione in LaTeX."""
    if not expr_str:
        return None
    try:
        expr = parse_expression(expr_str)
        return latex(expr)
    except Exception:
        pass
    try:
        expr = parse_expr(
            expr_str,
            transformations=_RENDER_TRANSFORMS,
            evaluate=True,
        )
        return latex(expr)
    except Exception:
        return None


def _leggi_plot_base64(path: str) -> str | None:
    """Legge un file PNG e restituisce il contenuto in base64.

    Il file viene **cancellato** dopo la lettura, per non lasciare
    spazzatura sul disco. Se la lettura o la cancellazione falliscono,
    restituisce ``None``.
    """
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode("ascii")
        # Cancella il file per non lasciare spazzatura.
        try:
            os.remove(path)
        except OSError:
            pass
        return encoded
    except OSError:
        return None


def _execute_with_params(
    operation: str,
    expression: str,
    params: dict[str, Any],
) -> Result:
    """Esegue un'operazione con i parametri specificati."""
    spec = get_operation(operation)
    func = spec.function

    if operation == "limit":
        return func(
            expression,
            var=params.get("var", "x"),
            point=params.get("point", "0"),
        )
    if operation == "diff":
        try:
            order = int(params.get("order", 1))
        except (ValueError, TypeError):
            order = params.get("order", 1)
        return func(
            expression,
            var=params.get("var", "x"),
            order=order,
        )
    if operation == "integrate":
        return func(
            expression,
            var=params.get("var", "x"),
            lower=params.get("lower"),
            upper=params.get("upper"),
        )
    if operation == "nsolve":
        return func(
            expression,
            var=params.get("var", "x"),
            initial=params.get("initial", "1"),
        )
    if operation == "nintegrate":
        return func(
            expression,
            var=params.get("var", "x"),
            lower=params.get("lower"),
            upper=params.get("upper"),
        )
    if operation == "plot":
        return func(
            expression,
            var=params.get("var", "x"),
            xmin=params.get("xmin", "-10"),
            xmax=params.get("xmax", "10"),
            output=params.get("output"),
        )
    if operation == "plot3d":
        return func(
            expression,
            xvar=params.get("xvar", "x"),
            yvar=params.get("yvar", "y"),
            xmin=params.get("xmin", "-5"),
            xmax=params.get("xmax", "5"),
            ymin=params.get("ymin", "-5"),
            ymax=params.get("ymax", "5"),
            output=params.get("output"),
        )

    return func(expression)

def _genera_dati_plot2d(
    expression: str,
    var: str = "x",
    xmin: str = "-10",
    xmax: str = "10",
    n_points: int = 500,
) -> dict:
    """Genera i dati per un grafico 2D interattivo (Plotly).

    Restituisce un dizionario con:
        x_values: lista di N valori
        y_values: lista di N valori (o None per punti non finiti)
        title: titolo del grafico
        xvar: nome della variabile
    """
    import sympy

    expr = parse_expression(expression)
    variable = sympy.Symbol(var)

    xmin_f = float(parse_expression(xmin))
    xmax_f = float(parse_expression(xmax))

    if xmin_f >= xmax_f:
        raise ValueError(f"range non valido: {xmin_f} >= {xmax_f}")

    x_vals = np.linspace(xmin_f, xmax_f, n_points)
    f = sympy.lambdify(variable, expr, modules=["numpy"])

    with np.errstate(divide="ignore", invalid="ignore"):
        y_vals = f(x_vals)

    y_vals = np.asarray(y_vals, dtype=float)

    # Sostituisci NaN e Inf con None (Plotly li gestisce come buchi).
    y_list = [
        None if (not np.isfinite(y)) else float(y)
        for y in y_vals
    ]

    return {
        "x_values": x_vals.tolist(),
        "y_values": y_list,
        "title": f"y = {expr}",
        "xvar": var,
    }


def create_app() -> Flask:
    """Crea e configura l'applicazione Flask."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/operations", methods=["GET"])
    def api_operations():
        ops = []
        for name in list_operations():
            spec = get_operation(name)
            ops.append({
                "name": spec.name,
                "description": spec.description,
            })
        return jsonify({"operations": ops})

    @app.route("/api/render", methods=["POST"])
    def api_render():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "richiesta JSON malformata"}), 400

        expr_str = data.get("expr")
        if not expr_str or not isinstance(expr_str, str):
            return jsonify({"error": "campo 'expr' mancante o non valido"}), 400

        latex_str = _try_latex(expr_str)
        if latex_str is None:
            return jsonify({"latex": None, "raw": expr_str})

        return jsonify({"latex": latex_str, "raw": expr_str})

    @app.route("/api/plot2d-data", methods=["POST"])
    def api_plot2d_data():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "richiesta JSON malformata"}), 400

        expression = data.get("expression")
        if not expression or not isinstance(expression, str):
            return jsonify({"error": "campo 'expression' mancante o non valido"}), 400

        try:
            n_points = int(data.get("n_points", 500))
        except (ValueError, TypeError):
            n_points = 500

        try:
            result = _genera_dati_plot2d(
                expression,
                var=data.get("var", "x"),
                xmin=data.get("xmin", "-10"),
                xmax=data.get("xmax", "10"),
                n_points=n_points,
            )
        except OpenAlphaError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:
            return jsonify({"error": f"errore: {exc}"}), 400

        return jsonify(result)

    @app.route("/api/plot3d-data", methods=["POST"])
    def api_plot3d_data():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "richiesta JSON malformata"}), 400

        expression = data.get("expression")
        if not expression or not isinstance(expression, str):
            return jsonify({"error": "campo 'expression' mancante o non valido"}), 400

        try:
            n_points = int(data.get("n_points", 50))
        except (ValueError, TypeError):
            n_points = 50

        try:
            result = _genera_dati_plot3d(
                expression,
                xvar=data.get("xvar", "x"),
                yvar=data.get("yvar", "y"),
                xmin=data.get("xmin", "-5"),
                xmax=data.get("xmax", "5"),
                ymin=data.get("ymin", "-5"),
                ymax=data.get("ymax", "5"),
                n_points=n_points,
            )
        except OpenAlphaError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:
            return jsonify({"error": f"errore: {exc}"}), 400

        return jsonify(result)

    @app.route("/api/execute", methods=["POST"])
    def api_execute():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "richiesta JSON malformata"}), 400

        expression = data.get("expression")
        operation = data.get("operation", "simplify")
        params = data.get("params") or {}

        if not expression or not isinstance(expression, str):
            return jsonify({"error": "campo 'expression' mancante o non valido"}), 400

        if not isinstance(params, dict):
            return jsonify({"error": "campo 'params' deve essere un oggetto"}), 400

        try:
            get_operation(operation)
        except OpenAlphaError as exc:
            return jsonify({"error": str(exc)}), 400

        try:
            result = _execute_with_params(operation, expression, params)
        except Exception as exc:  # pragma: no cover
            return jsonify({"error": f"errore interno: {exc}"}), 500

        serialized = _serialize_result(result)

        # Se è un plot, converti il file in base64 e cancella il file.
        if operation in _PLOT_OPERATIONS and result.exact:
            plot_data = _leggi_plot_base64(result.exact)
            serialized["plot_data"] = plot_data
            # Sostituisci il path con un placeholder per non mostrarlo.
            if plot_data:
                serialized["exact"] = "(grafico generato)"
        else:
            serialized["plot_data"] = None

        # LaTeX per gli altri campi.
        serialized["latex"] = {
            "exact": _try_latex(result.exact) if result.exact else None,
            "solutions": [
                _try_latex(sol.split("=", 1)[1].strip()) if "=" in sol else _try_latex(sol)
                for sol in result.solutions
            ],
            "steps": [
                {
                    "before": _try_latex(step.before),
                    "after": _try_latex(step.after),
                }
                for step in result.steps
            ],
        }

        return jsonify(serialized)

    return app


def _open_browser(url: str) -> None:
    webbrowser.open(url)


def main() -> None:
    app = create_app()
    url = "http://127.0.0.1:5000"
    Timer(1.0, _open_browser, args=[url]).start()
    print(f"OpenAlpha — server locale avviato su {url}")
    print("Premi Ctrl+C per terminare.")
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()