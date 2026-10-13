"""
Test dell'API di OpenAlpha web.

Verificano che gli endpoint /api/operations e /api/execute
funzionino correttamente.
"""

from __future__ import annotations

import pytest

from openalpha.web.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# /api/operations
# ---------------------------------------------------------------------------

def test_operations_lista(client):
    response = client.get("/api/operations")
    assert response.status_code == 200
    data = response.get_json()
    assert "operations" in data
    names = [op["name"] for op in data["operations"]]
    assert "simplify" in names
    assert "expand" in names
    assert "solve" in names


# ---------------------------------------------------------------------------
# /api/execute — casi validi
# ---------------------------------------------------------------------------

def test_execute_simplify(client):
    response = client.post("/api/execute", json={
        "expression": "sin(x)**2 + cos(x)**2",
        "operation": "simplify",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "simplify"
    assert data["status"] == "exact"
    assert data["exact"] == "1"


def test_execute_expand(client):
    response = client.post("/api/execute", json={
        "expression": "(x + 1)**2",
        "operation": "expand",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "expand"
    assert "x**2" in data["exact"]


def test_execute_solve(client):
    response = client.post("/api/execute", json={
        "expression": "x**2 - 1 = 0",
        "operation": "solve",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "exact"
    assert len(data["solutions"]) == 2


def test_execute_operazione_default(client):
    """Se 'operation' non è specificato, usa 'simplify'."""
    response = client.post("/api/execute", json={
        "expression": "x + x",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "simplify"


def test_execute_con_step(client):
    """Un'operazione con spiegazione produce step nella risposta."""
    response = client.post("/api/execute", json={
        "expression": "(x + 1)**2",
        "operation": "simplify",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["steps"]) >= 1
    assert data["steps"][0]["rule_name"] == "square_of_binomial"


# ---------------------------------------------------------------------------
# /api/execute — casi di errore
# ---------------------------------------------------------------------------

def test_execute_operazione_inesistente(client):
    response = client.post("/api/execute", json={
        "expression": "x + 1",
        "operation": "inesistente",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_execute_expression_mancante(client):
    response = client.post("/api/execute", json={
        "operation": "simplify",
    })
    assert response.status_code == 400


def test_execute_json_malformato(client):
    response = client.post(
        "/api/execute",
        data="non json",
        content_type="text/plain",
    )
    assert response.status_code == 400


def test_execute_expression_vuota(client):
    response = client.post("/api/execute", json={
        "expression": "",
        "operation": "simplify",
    })
    assert response.status_code == 400


def test_execute_errore_di_input_restituisce_200(client):
    """Un input non valido produce un Result con status=error, non un errore HTTP."""
    response = client.post("/api/execute", json={
        "expression": "2 +",
        "operation": "simplify",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "error"
    assert data["error"] is not None