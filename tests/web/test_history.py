"""
Test della cronologia (presenza di elementi nella pagina e nel JS).
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


def test_pagina_contiene_sidebar_cronologia(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'class="sidebar"' in html
    assert 'id="history-list"' in html


def test_pagina_contiene_bottone_pulisci(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'id="clear-history"' in html
    assert "Pulisci" in html


def test_script_usa_localstorage(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "localStorage" in js
    assert "openalpha_history" in js


def test_script_contiene_render_cronologia(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "renderCronologia" in js
    assert "aggiungiAllaCronologia" in js
    assert "riEsegui" in js


def test_script_limita_cronologia(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "HISTORY_MAX" in js