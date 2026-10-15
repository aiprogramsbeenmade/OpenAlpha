"""Test per l'operazione ``isprime``."""

from __future__ import annotations

from openalpha.core.status import ResultStatus
from openalpha.operations.number_theory.isprime import isprime


def test_isprime_registrata():
    from openalpha.core.registry import get_operation
    assert get_operation("isprime").name == "isprime"


def test_isprime_7():
    """7 è primo."""
    result = isprime("7")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_8():
    """8 non è primo."""
    result = isprime("8")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "False"


def test_isprime_97():
    """97 è primo."""
    result = isprime("97")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_1():
    """1 non è primo."""
    result = isprime("1")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "False"


def test_isprime_2():
    """2 è primo."""
    result = isprime("2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "True"


def test_isprime_non_intero():
    """1/2 non è intero."""
    result = isprime("1/2")
    assert result.status == ResultStatus.ERROR


def test_isprime_input_vuoto():
    result = isprime("")
    assert result.status == ResultStatus.ERROR

def test_isprime_7_ha_step():
    """isprime(7) produce un passo."""
    result = isprime("7")
    assert len(result.steps) == 1


def test_isprime_7_step_primo():
    """Il passo di 7 dice che è primo."""
    result = isprime("7")
    step = result.steps[0]
    assert step.before == "7"
    assert step.after == "primo"
    assert "primo" in step.description.lower()


def test_isprime_9_ha_step():
    """isprime(9) produce un passo."""
    result = isprime("9")
    assert len(result.steps) == 1


def test_isprime_9_step_composto():
    """Il passo di 9 dice che è divisibile per 3."""
    result = isprime("9")
    step = result.steps[0]
    assert step.before == "9"
    assert step.after == "composto"
    assert "3" in step.description


def test_isprime_2_step_definizione():
    """2 è primo per definizione."""
    result = isprime("2")
    assert len(result.steps) == 1
    assert result.steps[0].after == "primo"


def test_isprime_1_step_non_primo():
    """1 non è primo."""
    result = isprime("1")
    assert len(result.steps) == 1
    assert result.steps[0].after == "non primo"


def test_isprime_0_step_non_primo():
    """0 non è primo."""
    result = isprime("0")
    assert len(result.steps) == 1
    assert result.steps[0].after == "non primo"


def test_isprime_100_step_composto():
    """100 è pari, quindi composto."""
    result = isprime("100")
    assert len(result.steps) == 1
    assert result.steps[0].after == "composto"
    assert "pari" in result.steps[0].description.lower()


def test_isprime_15_step_composto():
    """15 è divisibile per 3."""
    result = isprime("15")
    assert len(result.steps) == 1
    assert "3" in result.steps[0].description