"""
Test delle azioni (copia, esportazione) — verifica presenza nel JS e CSS.
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


def test_script_contiene_copia_latex(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "copy-latex" in js
    assert "navigator.clipboard" in js


def test_script_contiene_copia_testo(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "copy-text" in js


def test_script_contiene_export_png(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "export-png" in js
    assert "data:image/png;base64," in js


def test_script_contiene_export_json(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "export-json" in js
    assert "application/json" in js


def test_css_contiene_action_bar(client):
    response = client.get("/static/style.css")
    css = response.data.decode("utf-8")
    assert ".action-bar" in css
    assert ".action-btn" in css