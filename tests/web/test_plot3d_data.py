"""
Test dell'endpoint /api/plot3d-data.
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


def test_plot3d_data_paraboloide(client):
    response = client.post("/api/plot3d-data", json={
        "expression": "x**2 + y**2",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "x_values" in data
    assert "y_values" in data
    assert "z_matrix" in data
    assert len(data["x_values"]) == 50
    assert len(data["y_values"]) == 50
    assert len(data["z_matrix"]) == 50
    assert len(data["z_matrix"][0]) == 50


def test_plot3d_data_range_personalizzato(client):
    response = client.post("/api/plot3d-data", json={
        "expression": "x + y",
        "xmin": "0", "xmax": "1",
        "ymin": "0", "ymax": "1",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["x_values"][0] == 0.0
    assert data["x_values"][-1] == 1.0


def test_plot3d_data_espressione_non_valida(client):
    response = client.post("/api/plot3d-data", json={
        "expression": "((((",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_plot3d_data_range_invalido(client):
    response = client.post("/api/plot3d-data", json={
        "expression": "x + y",
        "xmin": "5", "xmax": "1",
    })
    assert response.status_code == 400


def test_plot3d_data_expression_mancante(client):
    response = client.post("/api/plot3d-data", json={})
    assert response.status_code == 400


def test_plot3d_data_valori_finiti(client):
    """Per un'espressione con singolarità esatta, i valori non finiti
    sono sostituiti con None.

    Usiamo n_points=3 e un range [-1, 1], così la griglia include
    esattamente 0, dove 1/(x*y) ha una singolarità.
    """
    response = client.post("/api/plot3d-data", json={
        "expression": "1/(x*y)",
        "xmin": "-1", "xmax": "1",
        "ymin": "-1", "ymax": "1",
        "n_points": 3,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["x_values"]) == 3
    # Con n_points=3, i punti sono [-1, 0, 1]. La cella (0, 0) è None.
    flat = [v for row in data["z_matrix"] for v in row]
    assert any(v is None for v in flat)