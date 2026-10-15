"""Test per l'operazione ``permutations``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.permutations import permutations


def test_permutations_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("permutations").name == "permutations"


def test_permutations_5_2():
    """P(5, 2) = 20."""
    result = permutations("5", "2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "20"


def test_permutations_10_3():
    """P(10, 3) = 720."""
    result = permutations("10", "3")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "720"


def test_permutations_5_0():
    """P(5, 0) = 1."""
    result = permutations("5", "0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_permutations_5_5():
    """P(5, 5) = 120."""
    result = permutations("5", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "120"


def test_permutations_k_maggiore_di_n():
    result = permutations("3", "5")
    assert result.status == ResultStatus.ERROR


def test_permutations_non_intero():
    result = permutations("1/2", "2")
    assert result.status == ResultStatus.ERROR


def test_permutations_input_vuoto():
    result = permutations("", "2")
    assert result.status == ResultStatus.ERROR