"""
Test del server Flask di OpenAlpha.

Verificano che la pagina principale sia servita correttamente,
che contenga gli elementi attesi, e che gli endpoint di base
rispondano.
"""

from __future__ import annotations

import pytest

from openalpha.web.app import create_app


@pytest.fixture
def client():
    """Client di test per Flask."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_restituisce_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_contiene_titolo(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "OpenAlpha" in html


def test_index_contiene_campo_input(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'id="input-expression"' in html


def test_index_contiene_pulsante_calcola(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'id="calculate-button"' in html
    assert "Calcola" in html


def test_static_css_servito(client):
    response = client.get("/static/style.css")
    assert response.status_code == 200


def test_static_js_servito(client):
    response = client.get("/static/script.js")
    assert response.status_code == 200