"""
Test dell'operazione "plot".
"""

from __future__ import annotations

import os
import tempfile

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_plot_registrata():
    assert "plot" in list_operations()
    spec = get_operation("plot")
    assert spec.name == "plot"


def test_plot_sin_genera_file():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "sin.png")
        result = plot("sin(x)", output=output)
        assert result.status is ResultStatus.EXACT
        assert result.exact == output
        assert os.path.exists(output)
        # Il file non è vuoto.
        assert os.path.getsize(output) > 0


def test_plot_polinomio():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "quad.png")
        result = plot("x**2", xmin="-5", xmax="5", output=output)
        assert result.status is ResultStatus.EXACT
        assert os.path.exists(output)


def test_plot_asintoto():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "inv.png")
        result = plot("1/x", xmin="-5", xmax="5", output=output)
        assert result.status is ResultStatus.EXACT
        assert os.path.exists(output)


def test_plot_variabile_diversa():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "sin_y.png")
        result = plot("sin(y)", var="y", output=output)
        assert result.status is ResultStatus.EXACT


def test_plot_range_invalido():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "invalid.png")
        result = plot("x", xmin="5", xmax="1", output=output)
        assert result.status is ResultStatus.ERROR
        assert "range" in (result.error or "").lower()


def test_plot_input_vuoto():
    from openalpha.operations.visualization.plot import plot

    result = plot("")
    assert result.status is ResultStatus.ERROR


def test_plot_funzione_non_supportata():
    from openalpha.operations.visualization.plot import plot

    result = plot("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_plot_piu_variabili_unsupported():
    from openalpha.operations.visualization.plot import plot

    result = plot("x + y")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "più variabili" in (result.error or "").lower()


def test_plot_metadata_contiene_path():
    from openalpha.operations.visualization.plot import plot

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "sin.png")
        result = plot("sin(x)", output=output)
        assert result.metadata.get("plot_path") == output