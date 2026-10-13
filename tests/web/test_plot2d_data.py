"""
Test dell'endpoint /api/plot2d-data.
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


def test_plot2d_data_sin(client):
    response = client.post("/api/plot2d-data", json={
        "expression": "sin(x)",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "x_values" in data
    assert "y_values" in data
    assert len(data["x_values"]) == 500
    assert len(data["y_values"]) == 500


def test_plot2d_data_range_personalizzato(client):
    response = client.post("/api/plot2d-data", json={
        "expression": "x**2",
        "xmin": "0", "xmax": "5",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["x_values"][0] == 0.0
    assert data["x_values"][-1] == 5.0


def test_plot2d_data_n_points(client):
    response = client.post("/api/plot2d-data", json={
        "expression": "sin(x)",
        "n_points": 10,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["x_values"]) == 10


def test_plot2d_data_range_invalido(client):
    response = client.post("/api/plot2d-data", json={
        "expression": "sin(x)",
        "xmin": "5", "xmax": "1",
    })
    assert response.status_code == 400


def test_plot2d_data_espressione_non_valida(client):
    response = client.post("/api/plot2d-data", json={
        "expression": "(((",
    })
    assert response.status_code == 400


def test_plot2d_data_valori_finiti(client):
    """Per 1/x, il valore in x=0 è None."""
    response = client.post("/api/plot2d-data", json={
        "expression": "1/x",
        "xmin": "-1", "xmax": "1",
        "n_points": 3,
    })
    assert response.status_code == 200
    data = response.get_json()
    # Con n_points=3, x = [-1, 0, 1]. y_values[1] è None.
    assert data["y_values"][1] is None