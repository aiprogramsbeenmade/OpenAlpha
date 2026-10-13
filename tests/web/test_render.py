"""
Test dell'endpoint /api/render.
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


def test_render_polinomio(client):
    response = client.post("/api/render", json={"expr": "x**2 + 2*x + 1"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["latex"] is not None
    assert "x" in data["latex"]


def test_render_frazione(client):
    response = client.post("/api/render", json={"expr": "sin(x)/x"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["latex"] is not None
    assert "frac" in data["latex"]


def test_render_radice(client):
    response = client.post("/api/render", json={"expr": "sqrt(x)"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["latex"] is not None
    assert "sqrt" in data["latex"]


def test_render_costante_pi(client):
    response = client.post("/api/render", json={"expr": "pi"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["latex"] is not None
    assert "pi" in data["latex"]


def test_render_espressione_non_valida(client):
    response = client.post("/api/render", json={"expr": "((("})
    assert response.status_code == 200
    data = response.get_json()
    assert data["latex"] is None
    assert data["raw"] == "((("


def test_render_expr_mancante(client):
    response = client.post("/api/render", json={})
    assert response.status_code == 400


def test_render_json_malformato(client):
    response = client.post(
        "/api/render",
        data="non json",
        content_type="text/plain",
    )
    assert response.status_code == 400