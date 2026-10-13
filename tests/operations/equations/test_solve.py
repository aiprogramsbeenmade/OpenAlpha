"""
Test dell'operazione "solve".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_solve_registrata():
    assert "solve" in list_operations()
    spec = get_operation("solve")
    assert spec.name == "solve"


def test_solve_equazione_quadratica():
    from openalpha.operations.equations.solve import solve

    result = solve("x**2 - 1 = 0")
    assert result.status is ResultStatus.EXACT
    assert len(result.solutions) == 2
    # Le soluzioni sono x = -1 e x = 1, in qualche ordine.
    sols = set(result.solutions)
    assert sols == {"x = -1", "x = 1"}


def test_solve_senza_uguale():
    from openalpha.operations.equations.solve import solve

    result = solve("x**2 - 1")
    assert result.status is ResultStatus.EXACT
    sols = set(result.solutions)
    assert sols == {"x = -1", "x = 1"}


def test_solve_equazione_lineare():
    from openalpha.operations.equations.solve import solve

    result = solve("2*x + 4 = 0")
    assert result.status is ResultStatus.EXACT
    assert result.solutions == ["x = -2"]


def test_solve_x_uguale_1():
    from openalpha.operations.equations.solve import solve

    result = solve("x = 1")
    assert result.status is ResultStatus.EXACT
    assert result.solutions == ["x = 1"]


def test_solve_variabile_preferita_x():
    """x + y = 0: la variabile incognita è x, y è parametro."""
    from openalpha.operations.equations.solve import solve

    result = solve("x + y = 0")
    assert result.status is ResultStatus.EXACT
    assert len(result.solutions) == 1
    assert result.solutions[0].startswith("x = ")


def test_solve_nessuna_soluzione_o_identita_unsupported():
    from openalpha.operations.equations.solve import solve

    # x + 1 = x: nessuna soluzione. SymPy restituisce [].
    result = solve("x + 1 = x")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_equazione_trascendente_unsupported():
    from openalpha.operations.equations.solve import solve

    result = solve("sin(x) = 0")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_grado_troppo_alto_unsupported():
    from openalpha.operations.equations.solve import solve

    result = solve("x**5 - x + 1 = 0")
    assert result.status is ResultStatus.UNSUPPORTED
    assert "grado" in (result.error or "")


def test_solve_funzione_non_supportata():
    from openalpha.operations.equations.solve import solve

    result = solve("pippo(x) = 0")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_input_vuoto():
    from openalpha.operations.equations.solve import solve

    result = solve("")
    assert result.status is ResultStatus.ERROR


def test_solve_lhs_vuoto():
    from openalpha.operations.equations.solve import solve

    result = solve("= 1")
    assert result.status is ResultStatus.ERROR


def test_solve_rhs_vuoto():
    from openalpha.operations.equations.solve import solve

    result = solve("x = ")
    assert result.status is ResultStatus.ERROR


def test_solve_operazione_sul_registro_dal_nome():
    spec = get_operation("solve")
    result = spec.function("x**2 - 1 = 0")
    assert result.status is ResultStatus.EXACT
    assert len(result.solutions) == 2