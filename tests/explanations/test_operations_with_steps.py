"""
Test dell'integrazione tra operazioni e motore delle spiegazioni.
"""

from __future__ import annotations

import pytest

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.simplify import simplify

import openalpha.operations  # noqa: F401


def test_simplify_con_quadrato_del_binomio_produce_step():
    result = simplify("(x + 1)**2")
    # L'input (x + 1)**2 ha una regola applicabile.
    assert len(result.steps) >= 1
    assert result.steps[0].rule_name == "square_of_binomial"


def test_simplify_senza_regole_step_vuoti():
    result = simplify("x + 1")
    assert result.steps == []
    assert result.metadata.get("explanation_complete") is False


def test_simplify_metadata_contiene_messaggio():
    result = simplify("x + 1")
    assert "explanation_message" in result.metadata
    assert result.metadata["explanation_message"]



def test_simplify_differenza_di_quadrati_produce_step():
    result = simplify("x**2 - 1")
    assert len(result.steps) >= 1
    assert result.steps[0].rule_name == "difference_of_squares"