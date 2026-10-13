"""
Test dell'endpoint /api/execute con parametri extra.
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
# Operazioni senza parametri (firma standard)
# ---------------------------------------------------------------------------

def test_execute_simplify_senza_params(client):
    response = client.post("/api/execute", json={
        "expression": "x + x",
        "operation": "simplify",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "2*x"


def test_execute_solve_senza_params(client):
    response = client.post("/api/execute", json={
        "expression": "x**2 - 1 = 0",
        "operation": "solve",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["solutions"]) == 2


# ---------------------------------------------------------------------------
# Operazioni con parametri
# ---------------------------------------------------------------------------

def test_execute_diff_con_var(client):
    response = client.post("/api/execute", json={
        "expression": "y**2",
        "operation": "diff",
        "params": {"var": "y"},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "2*y"


def test_execute_diff_con_order(client):
    response = client.post("/api/execute", json={
        "expression": "x**3",
        "operation": "diff",
        "params": {"order": 2},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "6*x"


def test_execute_limit_con_point(client):
    response = client.post("/api/execute", json={
        "expression": "sin(x)/x",
        "operation": "limit",
        "params": {"point": "0"},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "1"


def test_execute_limit_a_infinito(client):
    response = client.post("/api/execute", json={
        "expression": "sin(x)/x",
        "operation": "limit",
        "params": {"point": "oo"},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "0"


def test_execute_integrate_indefinito(client):
    response = client.post("/api/execute", json={
        "expression": "x",
        "operation": "integrate",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "x**2/2" in data["exact"]


def test_execute_integrate_definito(client):
    response = client.post("/api/execute", json={
        "expression": "x",
        "operation": "integrate",
        "params": {"lower": "0", "upper": "1"},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "1/2"


def test_execute_nsolve_con_initial(client):
    response = client.post("/api/execute", json={
        "expression": "x**2 - 2",
        "operation": "nsolve",
        "params": {"initial": "-1"},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["approximate"].startswith("-1.41421")


# ---------------------------------------------------------------------------
# Validazione dei parametri
# ---------------------------------------------------------------------------

def test_execute_params_non_dict(client):
    response = client.post("/api/execute", json={
        "expression": "x + x",
        "operation": "simplify",
        "params": "non un dict",
    })
    assert response.status_code == 400
    assert "params" in response.get_json()["error"]


def test_execute_params_vuoto(client):
    response = client.post("/api/execute", json={
        "expression": "x + x",
        "operation": "simplify",
        "params": {},
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["exact"] == "2*x"