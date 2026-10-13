"""
Test dell'endpoint /api/execute con operazioni di plot.
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


def test_plot_restituisce_base64(client):
    response = client.post("/api/execute", json={
        "expression": "sin(x)",
        "operation": "plot",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["plot_data"] is not None
    assert len(data["plot_data"]) > 0
    # Base64 di PNG inizia con "iVBOR" (magic bytes).
    assert data["plot_data"].startswith("iVBOR")


def test_plot_non_lascia_file(client, tmp_path, monkeypatch):
    """Il file PNG generato viene cancellato dopo la lettura."""
    import os
    # Cambia la directory corrente in tmp_path per isolare i file.
    monkeypatch.chdir(tmp_path)

    response = client.post("/api/execute", json={
        "expression": "sin(x)",
        "operation": "plot",
    })
    assert response.status_code == 200

    # Nessun file PNG deve rimanere.
    pngs = list(tmp_path.glob("plot*.png"))
    assert len(pngs) == 0


def test_plot3d_restituisce_base64(client):
    response = client.post("/api/execute", json={
        "expression": "x**2 + y**2",
        "operation": "plot3d",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["plot_data"] is not None
    assert data["plot_data"].startswith("iVBOR")


def test_operazione_non_plot_non_ha_plot_data(client):
    response = client.post("/api/execute", json={
        "expression": "x + x",
        "operation": "simplify",
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("plot_data") is None