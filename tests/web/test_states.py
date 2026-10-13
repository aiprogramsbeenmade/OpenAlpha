"""
Test degli stati visivi (empty, loading, toast) — presenza nel JS e CSS.
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


def test_css_contiene_spinner(client):
    response = client.get("/static/style.css")
    css = response.data.decode("utf-8")
    assert ".spinner" in css
    assert "@keyframes spin" in css


def test_css_contiene_empty_state(client):
    response = client.get("/static/style.css")
    css = response.data.decode("utf-8")
    assert ".empty-state" in css
    assert ".example-chip" in css


def test_css_contiene_toast(client):
    response = client.get("/static/style.css")
    css = response.data.decode("utf-8")
    assert ".toast" in css
    assert ".toast.visible" in css


def test_css_contiene_fade_in(client):
    response = client.get("/static/style.css")
    css = response.data.decode("utf-8")
    assert "@keyframes fadeIn" in css
    assert ".fade-in" in css


def test_script_contiene_mostra_toast(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "mostraToast" in js


def test_script_contiene_mostra_empty_state(client):
    response = client.get("/static/script.js")
    js = response.data.decode("utf-8")
    assert "mostraEmptyState" in js
    assert "example-chip" in js