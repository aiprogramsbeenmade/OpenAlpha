"""
Test del modello standardizzato ``Result``.
"""

from __future__ import annotations

import pytest

from openalpha.core.result import Result
from openalpha.core.status import ResultStatus
from openalpha.core.step import Step


def _step() -> Step:
    """Step di comodo per i test."""
    return Step(
        before="(x + 1)**2",
        after="x**2 + 2*x + 1",
        rule_name="square_of_binomial",
        description="Quadrato del binomio",
    )


# ---------------------------------------------------------------------------
# Costruzioni valide
# ---------------------------------------------------------------------------

def test_exact_valido():
    r = Result(
        input_expression="sin(x)**2 + cos(x)**2",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="1",
    )
    assert r.status is ResultStatus.EXACT
    assert r.exact == "1"
    assert r.approximate is None
    assert r.error is None
    assert r.steps == []


def test_approximate_valido():
    r = Result(
        input_expression="pi",
        operation="evaluate",
        status=ResultStatus.APPROXIMATE,
        approximate=3.14159265,
    )
    assert r.status is ResultStatus.APPROXIMATE
    assert r.exact is None
    assert r.approximate == 3.14159265


def test_partial_con_exact():
    r = Result(
        input_expression="1/x",
        operation="simplify",
        status=ResultStatus.PARTIAL,
        exact="1/x",
        conditions=["x != 0"],
    )
    assert r.status is ResultStatus.PARTIAL
    assert r.exact == "1/x"
    assert r.conditions == ["x != 0"]


def test_partial_con_approximate():
    r = Result(
        input_expression="sqrt(2)",
        operation="evaluate",
        status=ResultStatus.PARTIAL,
        approximate=1.41421356,
        conditions=["approssimazione a 8 cifre"],
    )
    assert r.status is ResultStatus.PARTIAL
    assert r.approximate == 1.41421356


def test_error_valido():
    r = Result(
        input_expression="1/0",
        operation="simplify",
        status=ResultStatus.ERROR,
        error="divisione per zero",
    )
    assert r.status is ResultStatus.ERROR
    assert r.error == "divisione per zero"
    assert r.exact is None
    assert r.approximate is None


def test_unsupported_valido():
    r = Result(
        input_expression="d/dx sin(x)",
        operation="derivative",
        status=ResultStatus.UNSUPPORTED,
    )
    assert r.status is ResultStatus.UNSUPPORTED
    assert r.exact is None
    assert r.approximate is None


def test_unsupported_con_error_ammesso():
    r = Result(
        input_expression="pippo(x)",
        operation="simplify",
        status=ResultStatus.UNSUPPORTED,
        error="funzione non supportata: 'pippo'",
    )
    assert r.status is ResultStatus.UNSUPPORTED
    assert r.error is not None


def test_exact_con_steps():
    r = Result(
        input_expression="(x + 1)**2",
        operation="expand",
        status=ResultStatus.EXACT,
        exact="x**2 + 2*x + 1",
        steps=[_step()],
    )
    assert len(r.steps) == 1
    assert r.steps[0].rule_name == "square_of_binomial"


# ---------------------------------------------------------------------------
# Rifiuti
# ---------------------------------------------------------------------------

def test_input_expression_vuoto_rifiutato_se_non_error():
    with pytest.raises(ValueError, match="input_expression"):
        Result(
            input_expression="",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="1",
        )


def test_input_expression_vuoto_ammesso_se_error():
    r = Result(
        input_expression="",
        operation="simplify",
        status=ResultStatus.ERROR,
        error="input vuoto",
    )
    assert r.input_expression == ""
    assert r.status is ResultStatus.ERROR


def test_operation_vuota_rifiutata():
    with pytest.raises(ValueError, match="operation"):
        Result(
            input_expression="x",
            operation="",
            status=ResultStatus.EXACT,
            exact="x",
        )


def test_error_senza_messaggio_rifiutato():
    with pytest.raises(ValueError, match="ERROR"):
        Result(
            input_expression="1/0",
            operation="simplify",
            status=ResultStatus.ERROR,
        )


def test_error_con_exact_rifiutato():
    with pytest.raises(ValueError, match="ERROR"):
        Result(
            input_expression="1/0",
            operation="simplify",
            status=ResultStatus.ERROR,
            exact="0",
            error="divisione per zero",
        )


def test_error_con_approximate_rifiutato():
    with pytest.raises(ValueError, match="ERROR"):
        Result(
            input_expression="1/0",
            operation="simplify",
            status=ResultStatus.ERROR,
            approximate=0.0,
            error="divisione per zero",
        )


def test_exact_senza_valore_rifiutato():
    with pytest.raises(ValueError, match="EXACT"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
        )


def test_exact_con_error_rifiutato():
    with pytest.raises(ValueError, match="EXACT"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="x",
            error="qualcosa",
        )


def test_approximate_senza_valore_rifiutato():
    with pytest.raises(ValueError, match="APPROXIMATE"):
        Result(
            input_expression="pi",
            operation="evaluate",
            status=ResultStatus.APPROXIMATE,
        )


def test_approximate_con_error_rifiutato():
    with pytest.raises(ValueError, match="APPROXIMATE"):
        Result(
            input_expression="pi",
            operation="evaluate",
            status=ResultStatus.APPROXIMATE,
            approximate=3.14,
            error="qualcosa",
        )


def test_unsupported_con_exact_rifiutato():
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        Result(
            input_expression="d/dx sin(x)",
            operation="derivative",
            status=ResultStatus.UNSUPPORTED,
            exact="cos(x)",
        )


def test_unsupported_con_approximate_rifiutato():
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        Result(
            input_expression="d/dx sin(x)",
            operation="derivative",
            status=ResultStatus.UNSUPPORTED,
            approximate=0.5,
        )


def test_partial_senza_valori_rifiutato():
    with pytest.raises(ValueError, match="PARTIAL"):
        Result(
            input_expression="1/x",
            operation="simplify",
            status=ResultStatus.PARTIAL,
        )


def test_steps_none_rifiutato():
    with pytest.raises(ValueError, match="steps"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="x",
            steps=None,  # type: ignore[arg-type]
        )


def test_conditions_none_rifiutato():
    with pytest.raises(ValueError, match="conditions"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="x",
            conditions=None,  # type: ignore[arg-type]
        )


def test_metadata_none_rifiutato():
    with pytest.raises(ValueError, match="metadata"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="x",
            metadata=None,  # type: ignore[arg-type]
        )


def test_step_non_valido_in_steps_rifiutato():
    with pytest.raises(ValueError, match="steps"):
        Result(
            input_expression="x",
            operation="simplify",
            status=ResultStatus.EXACT,
            exact="x",
            steps=["non uno Step"],  # type: ignore[list-item]
        )


# ---------------------------------------------------------------------------
# is_success
# ---------------------------------------------------------------------------

def test_is_success_true_per_exact():
    r = Result(
        input_expression="x",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="x",
    )
    assert r.is_success() is True


def test_is_success_true_per_approximate():
    r = Result(
        input_expression="pi",
        operation="evaluate",
        status=ResultStatus.APPROXIMATE,
        approximate=3.14,
    )
    assert r.is_success() is True


def test_is_success_true_per_partial():
    r = Result(
        input_expression="1/x",
        operation="simplify",
        status=ResultStatus.PARTIAL,
        exact="1/x",
        conditions=["x != 0"],
    )
    assert r.is_success() is True


def test_is_success_false_per_error():
    r = Result(
        input_expression="1/0",
        operation="simplify",
        status=ResultStatus.ERROR,
        error="divisione per zero",
    )
    assert r.is_success() is False


def test_is_success_false_per_unsupported():
    r = Result(
        input_expression="d/dx sin(x)",
        operation="derivative",
        status=ResultStatus.UNSUPPORTED,
    )
    assert r.is_success() is False


# ---------------------------------------------------------------------------
# Indipendenza dei default mutabili
# ---------------------------------------------------------------------------

def test_steps_indipendenti_tra_istanze():
    r1 = Result(
        input_expression="x",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="x",
    )
    r2 = Result(
        input_expression="y",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="y",
    )
    r1.steps.append(_step())
    assert r2.steps == []


def test_conditions_indipendenti_tra_istanze():
    r1 = Result(
        input_expression="x",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="x",
    )
    r2 = Result(
        input_expression="y",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="y",
    )
    r1.conditions.append("x > 0")
    assert r2.conditions == []


def test_metadata_indipendenti_tra_istanze():
    r1 = Result(
        input_expression="x",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="x",
    )
    r2 = Result(
        input_expression="y",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="y",
    )
    r1.metadata["tempo"] = 0.01
    assert r2.metadata == {}


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------

def test_str_contiene_stato_e_operazione():
    r = Result(
        input_expression="x",
        operation="simplify",
        status=ResultStatus.EXACT,
        exact="x",
    )
    s = str(r)
    assert "exact" in s
    assert "simplify" in s
    assert "exact='x'" in s


def test_str_per_error_mostra_messaggio():
    r = Result(
        input_expression="1/0",
        operation="simplify",
        status=ResultStatus.ERROR,
        error="divisione per zero",
    )
    s = str(r)
    assert "error" in s
    assert "divisione per zero" in s


def test_str_mostra_numero_di_steps():
    r = Result(
        input_expression="(x + 1)**2",
        operation="expand",
        status=ResultStatus.EXACT,
        exact="x**2 + 2*x + 1",
        steps=[_step()],
    )
    assert "steps=1" in str(r)

# ---------------------------------------------------------------------------
# solutions
# ---------------------------------------------------------------------------

def test_exact_con_solutions():
    r = Result(
        input_expression="x**2 = 1",
        operation="solve",
        status=ResultStatus.EXACT,
        solutions=["x = -1", "x = 1"],
    )
    assert r.solutions == ["x = -1", "x = 1"]
    assert r.exact is None


def test_solutions_none_rifiutato():
    with pytest.raises(ValueError, match="solutions"):
        Result(
            input_expression="x",
            operation="solve",
            status=ResultStatus.EXACT,
            solutions=None,  # type: ignore[arg-type]
        )


def test_solutions_con_elemento_non_stringa_rifiutato():
    with pytest.raises(ValueError, match="solutions"):
        Result(
            input_expression="x",
            operation="solve",
            status=ResultStatus.EXACT,
            solutions=[-1, 1],  # type: ignore[list-item]
        )


def test_solutions_con_elemento_vuoto_rifiutato():
    with pytest.raises(ValueError, match="solutions"):
        Result(
            input_expression="x",
            operation="solve",
            status=ResultStatus.EXACT,
            solutions=[""],
        )


def test_unsupported_con_solutions_rifiutato():
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        Result(
            input_expression="x",
            operation="solve",
            status=ResultStatus.UNSUPPORTED,
            solutions=["x = 1"],
        )


def test_solutions_indipendenti_tra_istanze():
    r1 = Result(
        input_expression="x",
        operation="solve",
        status=ResultStatus.EXACT,
        solutions=["x = 1"],
    )
    r2 = Result(
        input_expression="y",
        operation="solve",
        status=ResultStatus.EXACT,
        solutions=["y = 1"],
    )
    r1.solutions.append("x = 2")
    assert r2.solutions == ["y = 1"]