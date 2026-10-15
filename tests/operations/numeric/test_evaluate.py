"""
Test per l'operazione ``evaluate``.
"""

from __future__ import annotations

import pytest

from openalpha.core.status import ResultStatus
from openalpha.operations.numeric.evaluate import evaluate


# ---------------------------------------------------------------------------
# Casi esatti
# ---------------------------------------------------------------------------

def test_evaluate_integer_arithmetic():
    """2 + 3 * 4 -> 14 esatto."""
    result = evaluate("2 + 3 * 4")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "14"
    assert result.approximate == "14"
    assert result.error is None


def test_evaluate_sin_pi_half():
    """sin(pi/2) -> 1 esatto."""
    result = evaluate("sin(pi/2)")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_evaluate_power_of_two():
    """2^10 -> 1024 esatto."""
    result = evaluate("2^10")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1024"


def test_evaluate_negative_result():
    """-5 + 3 -> -2 esatto."""
    result = evaluate("-5 + 3")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "-2"


def test_evaluate_rational_that_simplifies_to_integer():
    """4/2 -> 2 esatto."""
    result = evaluate("4/2")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "2"


# ---------------------------------------------------------------------------
# Casi approssimati
# ---------------------------------------------------------------------------

def test_evaluate_sqrt2():
    """sqrt(2) -> approssimato."""
    result = evaluate("sqrt(2)")
    assert result.status == ResultStatus.APPROXIMATE
    assert result.exact == "sqrt(2)"
    assert result.approximate.startswith("1.41421356237")
    assert result.error is None


def test_evaluate_pi():
    """pi -> approssimato."""
    result = evaluate("pi")
    assert result.status == ResultStatus.APPROXIMATE
    assert result.exact == "pi"
    assert result.approximate.startswith("3.14159265358979")


def test_evaluate_one_third():
    """1/3 -> approssimato."""
    result = evaluate("1/3")
    assert result.status == ResultStatus.APPROXIMATE
    assert result.exact == "1/3"
    assert result.approximate.startswith("0.333333333333")


def test_evaluate_e_squared():
    """e^2 -> approssimato."""
    result = evaluate("e^2")
    assert result.status == ResultStatus.APPROXIMATE
    assert result.exact == "exp(2)"
    assert result.approximate.startswith("7.38905609893")


def test_evaluate_sqrt_of_two_over_two():
    """sqrt(2)/2 -> approssimato."""
    result = evaluate("sqrt(2)/2")
    assert result.status == ResultStatus.APPROXIMATE
    assert result.approximate.startswith("0.707106781186")


# ---------------------------------------------------------------------------
# Errori
# ---------------------------------------------------------------------------

def test_evaluate_with_free_variable():
    """x + 1 -> errore."""
    result = evaluate("x + 1")
    assert result.status == ResultStatus.ERROR
    assert "variabili libere" in result.error.lower()
    assert result.exact is None
    assert result.approximate is None


def test_evaluate_with_multiple_free_variables():
    """x + y -> errore con entrambe le variabili nominate."""
    result = evaluate("x + y")
    assert result.status == ResultStatus.ERROR
    assert "x" in result.error
    assert "y" in result.error


def test_evaluate_parser_error():
    """Input malformato -> errore."""
    result = evaluate("2 +")
    assert result.status == ResultStatus.ERROR
    assert result.exact is None


def test_evaluate_empty_input():
    """Input vuoto -> errore."""
    result = evaluate("")
    assert result.status == ResultStatus.ERROR


def test_evaluate_invalid_character():
    """Carattere non ammesso -> errore."""
    result = evaluate("2 $ 3")
    assert result.status == ResultStatus.ERROR


# ---------------------------------------------------------------------------
# Metadati
# ---------------------------------------------------------------------------

def test_evaluate_result_has_operation_name():
    """Il campo operation è 'evaluate'."""
    result = evaluate("2 + 2")
    assert result.operation == "evaluate"
    assert result.input_expression == "2 + 2"


def test_evaluate_no_steps():
    """evaluate non produce passaggi."""
    result = evaluate("sqrt(2)")
    assert result.steps == []


def test_evaluate_no_conditions():
    """evaluate non produce condizioni."""
    result = evaluate("sqrt(2)")
    assert result.conditions == []


# ---------------------------------------------------------------------------
# Casi limite numerici
# ---------------------------------------------------------------------------

def test_evaluate_decimal_input():
    """0.5 + 0.5 -> 1 esatto."""
    result = evaluate("0.5 + 0.5")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1"


def test_evaluate_large_integer():
    """2^50 -> intero esatto."""
    result = evaluate("2^50")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "1125899906842624"


def test_evaluate_scientific_notation():
    """1e-3 -> 0.001 (esatto, Float di SymPy)."""
    result = evaluate("1e-3")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0.001"
    assert result.approximate == "0.001"


def test_evaluate_zero():
    """0 -> 0."""
    result = evaluate("0")
    assert result.status == ResultStatus.EXACT
    assert result.exact == "0"


@pytest.mark.parametrize(
    "expr,expected_status",
    [
        ("2+2", ResultStatus.EXACT),
        ("2+2.5", ResultStatus.EXACT),
        ("sqrt(2)", ResultStatus.APPROXIMATE),
        ("pi", ResultStatus.APPROXIMATE),
        ("sin(1)", ResultStatus.APPROXIMATE),
        ("cos(0)", ResultStatus.EXACT),
    ],
)
def test_evaluate_status_parametrized(expr, expected_status):
    """Verifica lo status su una varietà di input."""
    result = evaluate(expr)
    assert result.status == expected_status