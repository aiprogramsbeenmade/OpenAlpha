"""
Test dell'operazione "nintegrate".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_nintegrate_registrata():
    assert "nintegrate" in list_operations()
    spec = get_operation("nintegrate")
    assert spec.name == "nintegrate"


def test_nintegrate_gaussiana():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("exp(-x**2)", lower="0", upper="1")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("0.7468")


def test_nintegrate_sin():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("sin(x)", lower="0", upper="pi")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("2.0")


def test_nintegrate_uno_su_x():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("1/x", lower="1", upper="2")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("0.693")


def test_nintegrate_a_infinito():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("exp(-x**2)", lower="0", upper="oo")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    # sqrt(pi)/2 ≈ 0.8862
    assert result.approximate.startswith("0.886")


def test_nintegrate_manca_upper():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("x", lower="0")
    assert result.status is ResultStatus.ERROR


def test_nintegrate_manca_lower():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("x", upper="1")
    assert result.status is ResultStatus.ERROR


def test_nintegrate_input_vuoto():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("", lower="0", upper="1")
    assert result.status is ResultStatus.ERROR


def test_nintegrate_funzione_non_supportata():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("pippo(x)", lower="0", upper="1")
    assert result.status is ResultStatus.UNSUPPORTED


def test_nintegrate_steps_vuoti():
    from openalpha.operations.numeric.nintegrate import nintegrate

    result = nintegrate("x", lower="0", upper="1")
    assert result.steps == []
    assert result.metadata.get("explanation_status") == "unavailable"