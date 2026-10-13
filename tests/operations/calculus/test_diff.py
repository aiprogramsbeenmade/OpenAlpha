"""
Test dell'operazione "diff".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_diff_registrata():
    assert "diff" in list_operations()
    spec = get_operation("diff")
    assert spec.name == "diff"


def test_diff_sin_x():
    from openalpha.operations.calculus.diff import diff

    result = diff("sin(x)")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "cos(x)"


def test_diff_polinomio():
    from openalpha.operations.calculus.diff import diff

    result = diff("x**2")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*x"


def test_diff_derivata_seconda():
    from openalpha.operations.calculus.diff import diff

    result = diff("x**2", order=2)
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2"


def test_diff_derivata_quarta_di_sin():
    from openalpha.operations.calculus.diff import diff

    result = diff("sin(x)", order=4)
    assert result.status is ResultStatus.EXACT
    assert result.exact == "sin(x)"


def test_diff_polinomio_esteso():
    from openalpha.operations.calculus.diff import diff

    result = diff("x**3 + 2*x")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "3*x**2 + 2"


def test_diff_variabile_diversa():
    from openalpha.operations.calculus.diff import diff

    result = diff("y**2", var="y")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "2*y"


def test_diff_costante_rispetto_a_variabile():
    from openalpha.operations.calculus.diff import diff

    result = diff("x + y", var="y")
    assert result.status is ResultStatus.EXACT
    assert result.exact == "1"


def test_diff_input_vuoto():
    from openalpha.operations.calculus.diff import diff

    result = diff("")
    assert result.status is ResultStatus.ERROR


def test_diff_funzione_non_supportata():
    from openalpha.operations.calculus.diff import diff

    result = diff("pippo(x)")
    assert result.status is ResultStatus.UNSUPPORTED


def test_diff_order_zero():
    from openalpha.operations.calculus.diff import diff

    result = diff("x", order=0)
    assert result.status is ResultStatus.ERROR
    assert "order" in (result.error or "")


def test_diff_order_negativo():
    from openalpha.operations.calculus.diff import diff

    result = diff("x", order=-1)
    assert result.status is ResultStatus.ERROR


def test_diff_order_non_intero():
    from openalpha.operations.calculus.diff import diff

    result = diff("x", order=1.5)  # type: ignore[arg-type]
    assert result.status is ResultStatus.ERROR


def test_diff_operazione_sul_registro_dal_nome():
    spec = get_operation("diff")
    result = spec.function("sin(x)", var="x", order=1)
    assert result.status is ResultStatus.EXACT
    assert result.exact == "cos(x)"