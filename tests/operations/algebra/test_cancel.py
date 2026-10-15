"""Test per l'operazione ``cancel``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.cancel import cancel


def test_cancel_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("cancel").name == "cancel"


def test_cancel_differenza_di_quadrati():
    """(x**2 - 1)/(x - 1) -> x + 1."""
    result = cancel("(x**2 - 1)/(x - 1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto
    assert result.exact == "x + 1"


def test_cancel_quadrato_perfetto():
    """(x**2 + 2*x + 1)/(x + 1) -> x + 1."""
    result = cancel("(x**2 + 2*x + 1)/(x + 1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto
    assert result.exact == "x + 1"


def test_cancel_gia_ridotta():
    """Una frazione già ridotta resta invariata."""
    result = cancel("(x + 1)/(x - 1)")
    assert result.status == ResultStatus.PARTIAL  # <-- corretto


def test_cancel_input_vuoto():
    result = cancel("")
    assert result.status == ResultStatus.ERROR


def test_cancel_funzione_non_supportata():
    result = cancel("unknownfunc(x)")
    assert result.status == ResultStatus.UNSUPPORTED