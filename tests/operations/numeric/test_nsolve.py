"""
Test dell'operazione "nsolve".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_nsolve_registrata():
    assert "nsolve" in list_operations()
    spec = get_operation("nsolve")
    assert spec.name == "nsolve"


def test_nsolve_polinomio_grado_5_con_initial_negativo():
    """x**5 - x + 1 converge da -1, non da 1.

    Documenta un limite del metodo di Newton-Raphson: il punto
    iniziale conta.
    """
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**5 - x + 1", initial="-1")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("-1.167")


def test_nsolve_polinomio_grado_5_default_non_converge():
    """Con initial=1, x**5 - x + 1 non converge. Il nostro codice
    restituisce UNSUPPORTED con un messaggio chiaro."""
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**5 - x + 1")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "another starting point" in (result.error or "").lower() or \
           "radice" in (result.error or "").lower()


def test_nsolve_radice_quadrata_di_2():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 - 2")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("1.41421")


def test_nsolve_punto_iniziale_negativo():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 - 2", initial="-1")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None
    assert result.approximate.startswith("-1.41421")


def test_nsolve_con_uguale():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 = 2")
    assert result.status is ResultStatus.APPROXIMATE
    assert result.approximate is not None


def test_nsolve_senza_radici_reali():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 + 1")
    assert result.status is ResultStatus.UNSUPPORTED


def test_nsolve_input_vuoto():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("")
    assert result.status is ResultStatus.ERROR


def test_nsolve_funzione_non_supportata():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_nsolve_solutions_popolato():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 - 2")
    assert len(result.solutions) == 1
    assert result.solutions[0].startswith("x ≈ ")


def test_nsolve_steps_vuoti():
    from openalpha.operations.numeric.nsolve import nsolve

    result = nsolve("x**2 - 2")
    assert result.steps == []
    assert result.metadata.get("explanation_status") == "unavailable"