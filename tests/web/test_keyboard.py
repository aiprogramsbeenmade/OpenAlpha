"""
Test della tastiera matematica (verifica HTML).
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


def test_pagina_contiene_tastiera(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'class="keyboard"' in html


def test_pagina_contiene_schede(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    for tab in ["basic", "calculus", "algebra", "trig", "plot"]:
        assert f'data-tab="{tab}"' in html


def test_pagina_contiene_pulsanti_basic(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'data-insert="**2"' in html
    assert 'data-insert="sqrt()"' in html
    assert 'data-insert="pi"' in html


def test_pagina_contiene_pulsanti_calculus(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'data-insert="integrate(, x)"' in html
    assert 'data-insert="diff(, x)"' in html
    assert 'data-insert="limit(, x, 0)"' in html


def test_pagina_contiene_pulsanti_trig(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'data-insert="sin()"' in html
    assert 'data-insert="cos()"' in html
    assert 'data-insert="tan()"' in html


def test_pagina_contiene_pulsanti_plot(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'data-insert="plot()"' in html
    assert 'data-insert="plot3d()"' in html


def test_script_contiene_analizza_input(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "analizzaInput" in js


def test_script_contiene_setup_tastiera(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "setupTastiera" in js


def test_script_contiene_inserisci_frammento(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "inserisciFrammento" in js