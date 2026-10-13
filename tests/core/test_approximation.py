"""
Test dell'helper di approssimazione.
"""

from __future__ import annotations

from openalpha.core.approximation import compute_approximate


def test_intero():
    assert compute_approximate("2") == "2.00000000000000"


def test_razionale():
    assert compute_approximate("1/2") == "0.500000000000000"


def test_terzo():
    result = compute_approximate("1/3")
    assert result is not None
    assert result.startswith("0.333333333333333")


def test_sqrt_due():
    result = compute_approximate("sqrt(2)")
    assert result is not None
    assert result.startswith("1.41421356237310")


def test_e():
    result = compute_approximate("E")
    assert result is not None
    assert result.startswith("2.71828182845905")


def test_pi():
    result = compute_approximate("pi")
    assert result is not None
    assert result.startswith("3.14159265358979")


def test_espressione_simbolica_restituisce_none():
    assert compute_approximate("x") is None
    assert compute_approximate("x + 1") is None
    assert compute_approximate("cos(x)") is None


def test_oo_restituisce_none():
    assert compute_approximate("oo") is None
    assert compute_approximate("-oo") is None


def test_nan_restituisce_none():
    assert compute_approximate("nan") is None


def test_stringa_non_interpretabile_restituisce_none():
    assert compute_approximate("pippo!!!") is None


def test_stringa_vuota_restituisce_none():
    assert compute_approximate("") is None