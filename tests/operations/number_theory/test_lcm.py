"""Test per l'operazione ``lcm``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.lcm import lcm


def test_lcm_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("lcm").name == "lcm"


def test_lcm_12_18():
    result = lcm("12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "36"


def test_lcm_4_6():
    result = lcm("4", "6")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "12"


def test_lcm_coprimi():
    result = lcm("7", "13")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "91"


def test_lcm_con_negativo():
    result = lcm("-12", "18")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "36"


def test_lcm_zero_e_cinque():
    result = lcm("0", "5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


def test_lcm_zero_zero():
    result = lcm("0", "0")
    assert result.status == ResultStatus.ERROR
    assert "0" in result.error


def test_lcm_non_intero():
    result = lcm("1/2", "3")
    assert result.status == ResultStatus.ERROR


def test_lcm_input_vuoto():
    result = lcm("", "3")
    assert result.status == ResultStatus.ERROR