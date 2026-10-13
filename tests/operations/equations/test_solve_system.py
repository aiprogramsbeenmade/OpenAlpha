"""
Test dell'operazione "solve_system".
"""

from __future__ import annotations

from openalpha.core.registry import get_operation, list_operations
from openalpha.core.status import ResultStatus

import openalpha.operations  # noqa: F401


def test_solve_system_registrata():
    assert "solve_system" in list_operations()
    spec = get_operation("solve_system")
    assert spec.name == "solve_system"


def test_solve_system_2x2_semplice():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("x + y = 3; x - y = 1")
    assert result.status is ResultStatus.EXACT
    assert set(result.solutions) == {"x = 2", "y = 1"}


def test_solve_system_2x2_coefficienti():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("2*x + y = 5; x - y = 1")
    assert result.status is ResultStatus.EXACT
    assert set(result.solutions) == {"x = 2", "y = 1"}


def test_solve_system_3x3():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system(
        "x + y + z = 6; x - y = 0; z = 2"
    )
    assert result.status is ResultStatus.EXACT
    assert set(result.solutions) == {"x = 2", "y = 2", "z = 2"}


def test_solve_system_una_sola_equazione_errore():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("x + y = 3")
    assert result.status is ResultStatus.ERROR
    assert "almeno 2" in (result.error or "")


def test_solve_system_inconsistente_unsupported():
    from openalpha.operations.equations.solve_system import solve_system

    # x + y = 3; x + y = 4: nessuna soluzione.
    result = solve_system("x + y = 3; x + y = 4")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_system_indeterminato_unsupported():
    from openalpha.operations.equations.solve_system import solve_system

    # x + y = 3; 2*x + 2*y = 6: infinite soluzioni.
    result = solve_system("x + y = 3; 2*x + 2*y = 6")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_system_input_vuoto():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("")
    assert result.status is ResultStatus.ERROR


def test_solve_system_funzione_non_supportata():
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("pippo(x) = 0; x = 1")
    assert result.status is ResultStatus.UNSUPPORTED


def test_solve_system_solutions_ordinate():
    """Le soluzioni sono ordinate alfabeticamente per variabile."""
    from openalpha.operations.equations.solve_system import solve_system

    result = solve_system("y + x = 3; y - x = 1")
    assert result.status is ResultStatus.EXACT
    # Deve essere [x = ..., y = ...] in quest'ordine.
    assert result.solutions[0].startswith("x = ")
    assert result.solutions[1].startswith("y = ")


def test_solve_system_operazione_sul_registro_dal_nome():
    spec = get_operation("solve_system")
    result = spec.function("x + y = 3; x - y = 1")
    assert result.status is ResultStatus.EXACT