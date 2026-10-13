"""
Test dell'operazione "plot3d".
"""

from __future__ import annotations

import os
import tempfile

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_plot3d_registrata():
    assert "plot3d" in list_operations()
    spec = get_operation("plot3d")
    assert spec.name == "plot3d"


def test_plot3d_paraboloide():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "parab.png")
        result = plot3d("x**2 + y**2", output=output)
        assert result.status is ResultStatus.EXACT
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0


def test_plot3d_sin_cos():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "sincos.png")
        result = plot3d("sin(x)*cos(y)", output=output)
        assert result.status is ResultStatus.EXACT
        assert os.path.exists(output)


def test_plot3d_piano():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "piano.png")
        result = plot3d("x + y", output=output)
        assert result.status is ResultStatus.EXACT


def test_plot3d_una_variabile_unsupported():
    from openalpha.operations.visualization.plot3d import plot3d

    result = plot3d("x**2")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "plot" in (result.error or "").lower()


def test_plot3d_tre_variabili_unsupported():
    from openalpha.operations.visualization.plot3d import plot3d

    result = plot3d("x + y + z")
    assert result.status is ResultStatus.UNSUPPORTED


def test_plot3d_input_vuoto():
    from openalpha.operations.visualization.plot3d import plot3d

    result = plot3d("")
    assert result.status is ResultStatus.ERROR


def test_plot3d_range_invalido():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "invalid.png")
        result = plot3d("x + y", xmin="5", xmax="1", output=output)
        assert result.status is ResultStatus.ERROR
        assert "range" in (result.error or "").lower()


def test_plot3d_metadata_contiene_path():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "x.png")
        result = plot3d("x*y", output=output)
        assert result.metadata.get("plot_path") == output


def test_plot3d_variabili_personalizzate():
    from openalpha.operations.visualization.plot3d import plot3d

    with tempfile.TemporaryDirectory() as tmpdir:
        output = os.path.join(tmpdir, "uv.png")
        result = plot3d("u**2 + v**2", xvar="u", yvar="v", output=output)
        assert result.status is ResultStatus.EXACT
        assert os.path.exists(output)